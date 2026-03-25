import json
import boto3
import uuid
import os
import time
from datetime import datetime, timedelta
from decimal import Decimal
from collections import Counter

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name='us-east-1')

queue_table = dynamodb.Table('MarketingQueue')
cart_table = dynamodb.Table('Cart')
views_table = dynamodb.Table('ProductViews')
prefs_table = dynamodb.Table('EmailPreferences')
watchlist_table = dynamodb.Table('WatchList')
products_table = dynamodb.Table('Products')

FROM_EMAIL = 'contact@christianconservativestoday.com'
SITE_URL = 'https://christianconservativestoday.com'

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,OPTIONS'
}

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def respond(status, body):
    return {'statusCode': status, 'headers': HEADERS, 'body': json.dumps(body, default=decimal_default)}


def lambda_handler(event, context):
    # CloudWatch scheduled event — run all scans
    if event.get('source') == 'aws.events' or event.get('detail-type') == 'Scheduled Event':
        return run_all_scans()

    # API Gateway request
    if event.get('httpMethod') == 'OPTIONS':
        return respond(200, {})

    action = (event.get('queryStringParameters') or {}).get('action', '')
    method = event.get('httpMethod', 'GET')

    try:
        if action == 'preferences-get' and method == 'GET':
            return get_preferences(event)
        elif action == 'preferences-update' and method == 'POST':
            return update_preferences(event)
        elif action == 'unsubscribe' and method == 'GET':
            return unsubscribe(event)
        elif action == 'run-scans' and method == 'POST':
            return run_all_scans()
        elif action == 'stats' and method == 'GET':
            return get_stats()
        else:
            return respond(400, {'error': f'Invalid action: {action}'})
    except Exception as e:
        print(f"Error: {e}")
        return respond(500, {'error': str(e)})


# ==================== SCAN JOBS ====================

def run_all_scans():
    results = {
        'abandoned_carts': scan_abandoned_carts(),
        'browse_abandonment': scan_browse_abandonment(),
        'price_drops': scan_price_drops(),
        'emails_sent': send_queued_emails()
    }
    print(f"Scan results: {json.dumps(results)}")
    return respond(200, results) if isinstance(results, dict) else results


def scan_abandoned_carts():
    """Find carts with items that haven't been touched in 24-72 hours."""
    now = datetime.utcnow()
    cutoff_start = (now - timedelta(hours=72)).isoformat() + 'Z'
    cutoff_end = (now - timedelta(hours=24)).isoformat() + 'Z'

    try:
        resp = cart_table.scan(
            FilterExpression='updated_at BETWEEN :start AND :end',
            ExpressionAttributeValues={':start': cutoff_start, ':end': cutoff_end}
        )
    except Exception as e:
        print(f"Cart scan error: {e}")
        return {'queued': 0, 'error': str(e)}

    queued = 0
    for cart in resp.get('Items', []):
        items = cart.get('items', [])
        if not items:
            continue

        user_id = cart['user_id']
        prefs = _get_prefs(user_id)
        if not prefs or not prefs.get('email') or prefs.get('unsubscribed'):
            continue
        if not prefs.get('abandoned_cart_emails', True):
            continue
        if _recently_emailed(prefs['email'], 'abandoned_cart', days=7):
            continue

        cart_total = sum(float(i.get('price', 0)) * int(i.get('quantity', 1)) for i in items)

        _queue_email(
            user_id=user_id,
            email=prefs['email'],
            trigger_type='abandoned_cart',
            subject='You left items in your cart!',
            template='abandoned_cart',
            trigger_data={'cart_items': items, 'cart_total': cart_total},
            discount_code='CART10',
            discount_amount=10
        )
        queued += 1

    return {'queued': queued}


def scan_browse_abandonment():
    """Find users who viewed products 3+ times but never added to cart."""
    cutoff = (datetime.utcnow() - timedelta(hours=48)).isoformat() + 'Z'

    try:
        resp = views_table.scan(
            FilterExpression='added_to_cart = :f AND #ts < :cutoff',
            ExpressionAttributeNames={'#ts': 'timestamp'},
            ExpressionAttributeValues={':f': False, ':cutoff': cutoff},
            ProjectionExpression='user_id,product_id,product_name,product_price,product_category'
        )
    except Exception as e:
        print(f"Browse scan error: {e}")
        return {'queued': 0, 'error': str(e)}

    # Group views by user → product
    user_products = {}
    for v in resp.get('Items', []):
        uid = v.get('user_id', '')
        pid = v['product_id']
        key = f"{uid}|{pid}"
        if key not in user_products:
            user_products[key] = {'user_id': uid, 'count': 0, **v}
        user_products[key]['count'] += 1

    # Filter to 3+ views
    queued = 0
    seen_users = set()
    for item in sorted(user_products.values(), key=lambda x: x['count'], reverse=True):
        if item['count'] < 3:
            continue
        uid = item['user_id']
        if uid in seen_users or uid.startswith('anon_'):
            continue
        seen_users.add(uid)

        prefs = _get_prefs(uid)
        if not prefs or not prefs.get('email') or prefs.get('unsubscribed'):
            continue
        if not prefs.get('browse_abandonment_emails', True):
            continue
        if _recently_emailed(prefs['email'], 'browse_abandonment', days=7):
            continue

        _queue_email(
            user_id=uid,
            email=prefs['email'],
            trigger_type='browse_abandonment',
            subject=f"Still interested in {item.get('product_name', 'this product')}?",
            template='browse_abandonment',
            trigger_data={'product_name': item.get('product_name'), 'product_id': item['product_id'], 'view_count': item['count']},
            discount_code='BROWSE5',
            discount_amount=5
        )
        queued += 1

    return {'queued': queued}


def scan_price_drops():
    """Check watchlist items for price drops below target."""
    try:
        resp = watchlist_table.scan()
    except Exception as e:
        print(f"Watchlist scan error: {e}")
        return {'queued': 0, 'error': str(e)}

    queued = 0
    for item in resp.get('Items', []):
        if not item.get('notify_on_price_drop') or item.get('notified_price_drop'):
            continue

        # Get current price
        try:
            prod = products_table.get_item(Key={'product_id': item['product_id']})
            product = prod.get('Item')
            if not product:
                continue
        except Exception:
            continue

        current_price = float(product.get('price', 0))
        target_price = float(item.get('target_price', 0))

        if current_price >= target_price:
            continue

        uid = item['user_id']
        prefs = _get_prefs(uid)
        if not prefs or not prefs.get('email') or prefs.get('unsubscribed'):
            continue
        if not prefs.get('price_drop_alerts', True):
            continue

        old_price = float(item.get('current_price', 0))
        _queue_email(
            user_id=uid,
            email=prefs['email'],
            trigger_type='price_drop',
            subject=f"Price Drop Alert: {product.get('name', 'Product')}",
            template='price_drop',
            trigger_data={
                'product_name': product.get('name'),
                'product_id': item['product_id'],
                'old_price': old_price,
                'new_price': current_price,
                'savings': round(old_price - current_price, 2)
            }
        )

        # Mark notified
        watchlist_table.update_item(
            Key={'user_id': uid, 'product_id': item['product_id']},
            UpdateExpression='SET notified_price_drop = :t, current_price = :p',
            ExpressionAttributeValues={':t': True, ':p': Decimal(str(current_price))}
        )
        queued += 1

    return {'queued': queued}


# ==================== EMAIL SENDING ====================

def send_queued_emails():
    """Send all pending emails in MarketingQueue."""
    now = datetime.utcnow().isoformat() + 'Z'

    resp = queue_table.query(
        IndexName='sent-scheduled_send_time-index',
        KeyConditionExpression='sent = :f AND scheduled_send_time <= :now',
        ExpressionAttributeValues={':f': 'false', ':now': now},
        Limit=50
    )

    sent = 0
    failed = 0
    for item in resp.get('Items', []):
        try:
            html = _render_email(item['email_template'], item.get('trigger_data', {}), item)
            ses.send_email(
                Source=FROM_EMAIL,
                Destination={'ToAddresses': [item['user_email']]},
                Message={
                    'Subject': {'Data': item['email_subject']},
                    'Body': {'Html': {'Data': html}}
                }
            )
            queue_table.update_item(
                Key={'queue_id': item['queue_id']},
                UpdateExpression='SET sent = :t, sent_at = :now',
                ExpressionAttributeValues={':t': 'true', ':now': now}
            )
            sent += 1
        except Exception as e:
            print(f"Email send error for {item.get('user_email')}: {e}")
            failed += 1

    return {'sent': sent, 'failed': failed}


# ==================== PREFERENCES ====================

def get_preferences(event):
    params = event.get('queryStringParameters') or {}
    user_id = params.get('user_id')
    if not user_id:
        return respond(400, {'error': 'user_id required'})

    resp = prefs_table.get_item(Key={'user_id': user_id})
    item = resp.get('Item')
    if not item:
        return respond(200, {'preferences': _default_prefs(user_id), 'exists': False})
    return respond(200, {'preferences': item, 'exists': True})


def update_preferences(event):
    body = json.loads(event.get('body', '{}'))
    user_id = body.get('user_id')
    if not user_id:
        return respond(400, {'error': 'user_id required'})

    now = datetime.utcnow().isoformat() + 'Z'
    token = body.get('unsubscribe_token', uuid.uuid4().hex[:16])

    item = {
        'user_id': user_id,
        'email': body.get('email', ''),
        'marketing_emails': body.get('marketing_emails', True),
        'abandoned_cart_emails': body.get('abandoned_cart_emails', True),
        'browse_abandonment_emails': body.get('browse_abandonment_emails', True),
        'price_drop_alerts': body.get('price_drop_alerts', True),
        'back_in_stock_alerts': body.get('back_in_stock_alerts', True),
        'product_recommendations': body.get('product_recommendations', True),
        'newsletter': body.get('newsletter', True),
        'unsubscribed': body.get('unsubscribed', False),
        'unsubscribe_token': token,
        'updated_at': now
    }

    # Preserve created_at if exists
    existing = prefs_table.get_item(Key={'user_id': user_id}).get('Item')
    item['created_at'] = existing['created_at'] if existing else now

    prefs_table.put_item(Item=item)
    return respond(200, {'success': True})


def unsubscribe(event):
    params = event.get('queryStringParameters') or {}
    token = params.get('token')
    if not token:
        return respond(400, {'error': 'token required'})

    # Scan for matching token
    resp = prefs_table.scan(
        FilterExpression='unsubscribe_token = :t',
        ExpressionAttributeValues={':t': token},
        Limit=1
    )

    items = resp.get('Items', [])
    if not items:
        return respond(404, {'error': 'Invalid unsubscribe token'})

    user_id = items[0]['user_id']
    prefs_table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET unsubscribed = :t, unsubscribed_at = :now',
        ExpressionAttributeValues={':t': True, ':now': datetime.utcnow().isoformat() + 'Z'}
    )

    return respond(200, {'success': True, 'message': 'You have been unsubscribed from all marketing emails.'})


def get_stats():
    """Get marketing email stats."""
    resp = queue_table.scan(
        ProjectionExpression='trigger_type,sent,opened,clicked,converted'
    )

    stats = {'total': 0, 'sent': 0, 'opened': 0, 'clicked': 0, 'converted': 0, 'by_type': {}}
    for item in resp.get('Items', []):
        stats['total'] += 1
        tt = item.get('trigger_type', 'unknown')
        if tt not in stats['by_type']:
            stats['by_type'][tt] = {'total': 0, 'sent': 0, 'opened': 0, 'clicked': 0, 'converted': 0}
        stats['by_type'][tt]['total'] += 1
        if item.get('sent') == 'true':
            stats['sent'] += 1
            stats['by_type'][tt]['sent'] += 1
        if item.get('opened'):
            stats['opened'] += 1
            stats['by_type'][tt]['opened'] += 1
        if item.get('clicked'):
            stats['clicked'] += 1
            stats['by_type'][tt]['clicked'] += 1
        if item.get('converted'):
            stats['converted'] += 1
            stats['by_type'][tt]['converted'] += 1

    return respond(200, stats)


# ==================== HELPERS ====================

def _get_prefs(user_id):
    try:
        resp = prefs_table.get_item(Key={'user_id': user_id})
        return resp.get('Item')
    except Exception:
        return None

def _default_prefs(user_id):
    return {
        'user_id': user_id, 'email': '', 'marketing_emails': True,
        'abandoned_cart_emails': True, 'browse_abandonment_emails': True,
        'price_drop_alerts': True, 'back_in_stock_alerts': True,
        'product_recommendations': True, 'newsletter': True,
        'unsubscribed': False
    }

def _recently_emailed(email, trigger_type, days=7):
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat() + 'Z'
    try:
        resp = queue_table.query(
            IndexName='user_email-trigger_type-index',
            KeyConditionExpression='user_email = :e AND trigger_type = :t',
            FilterExpression='created_at > :c',
            ExpressionAttributeValues={':e': email, ':t': trigger_type, ':c': cutoff},
            Limit=1
        )
        return resp.get('Count', 0) > 0
    except Exception:
        return False

def _queue_email(user_id, email, trigger_type, subject, template, trigger_data, discount_code=None, discount_amount=None):
    now = datetime.utcnow().isoformat() + 'Z'
    expires_at = int(time.time()) + (30 * 24 * 3600)

    item = {
        'queue_id': f"mq_{uuid.uuid4().hex[:16]}",
        'user_id': user_id,
        'user_email': email,
        'trigger_type': trigger_type,
        'trigger_data': trigger_data,
        'email_subject': subject,
        'email_template': template,
        'scheduled_send_time': now,
        'sent': 'false',
        'opened': False,
        'clicked': False,
        'converted': False,
        'created_at': now,
        'expires_at': expires_at
    }
    if discount_code:
        item['discount_code'] = discount_code
        item['discount_amount'] = discount_amount

    queue_table.put_item(Item=item)


def _render_email(template, data, queue_item):
    """Render HTML email from template name and data."""
    unsubscribe_url = f"{SITE_URL}/Shopping/preferences.html?action=unsubscribe&user_id={queue_item.get('user_id', '')}"
    prefs_url = f"{SITE_URL}/Shopping/preferences.html?user_id={queue_item.get('user_id', '')}"
    cart_url = f"{SITE_URL}/Shopping/cart.html"
    shop_url = f"{SITE_URL}/Shopping/shop.html"

    discount_code = queue_item.get('discount_code', '')
    discount_amount = queue_item.get('discount_amount', '')

    if template == 'abandoned_cart':
        items_html = ''
        for item in data.get('cart_items', []):
            items_html += f"""
            <tr>
                <td style="padding:10px;border-bottom:1px solid #eee">{item.get('name', 'Product')}</td>
                <td style="padding:10px;border-bottom:1px solid #eee;text-align:center">{item.get('quantity', 1)}</td>
                <td style="padding:10px;border-bottom:1px solid #eee;text-align:right">${item.get('price', 0):.2f}</td>
            </tr>"""
        total = data.get('cart_total', 0)

        return f"""<!DOCTYPE html><html><body style="font-family:Arial,sans-serif;margin:0;padding:0;background:#f4f4f4">
        <div style="max-width:600px;margin:20px auto;background:white;border-radius:8px;overflow:hidden">
            <div style="background:#003366;color:white;padding:30px;text-align:center">
                <h1 style="margin:0">You Left Items in Your Cart!</h1>
            </div>
            <div style="padding:30px">
                <p>Hi there,</p>
                <p>You left some great items in your cart. Don't miss out!</p>
                <table style="width:100%;border-collapse:collapse;margin:20px 0">
                    <tr style="background:#f8f9fa"><th style="padding:10px;text-align:left">Item</th><th style="padding:10px">Qty</th><th style="padding:10px;text-align:right">Price</th></tr>
                    {items_html}
                    <tr><td colspan="2" style="padding:10px;text-align:right;font-weight:bold">Total:</td><td style="padding:10px;text-align:right;font-weight:bold">${total:.2f}</td></tr>
                </table>
                <p>Complete your purchase now and get <strong>{discount_amount}% OFF</strong> with code: <strong>{discount_code}</strong></p>
                <div style="text-align:center;margin:30px 0">
                    <a href="{cart_url}" style="background:#28a745;color:white;padding:15px 40px;text-decoration:none;border-radius:5px;font-size:18px">Complete Purchase</a>
                </div>
                <p>Blessings,<br>Christian Conservatives Today</p>
            </div>
            <div style="background:#f8f9fa;padding:20px;text-align:center;font-size:12px;color:#666">
                <a href="{unsubscribe_url}">Unsubscribe</a> | <a href="{prefs_url}">Email Preferences</a>
            </div>
        </div></body></html>"""

    elif template == 'browse_abandonment':
        pname = data.get('product_name', 'a product')
        views = data.get('view_count', 0)
        pid = data.get('product_id', '')

        return f"""<!DOCTYPE html><html><body style="font-family:Arial,sans-serif;margin:0;padding:0;background:#f4f4f4">
        <div style="max-width:600px;margin:20px auto;background:white;border-radius:8px;overflow:hidden">
            <div style="background:#003366;color:white;padding:30px;text-align:center">
                <h1 style="margin:0">Still Interested?</h1>
            </div>
            <div style="padding:30px">
                <p>Hi there,</p>
                <p>We noticed you've been checking out <strong>{pname}</strong> ({views} times!). It's still available.</p>
                <p>Use code <strong>{discount_code}</strong> for <strong>{discount_amount}% OFF</strong> your purchase!</p>
                <div style="text-align:center;margin:30px 0">
                    <a href="{SITE_URL}/Shopping/product.html?id={pid}" style="background:#667eea;color:white;padding:15px 40px;text-decoration:none;border-radius:5px;font-size:18px">View Product</a>
                </div>
                <p>Blessings,<br>Christian Conservatives Today</p>
            </div>
            <div style="background:#f8f9fa;padding:20px;text-align:center;font-size:12px;color:#666">
                <a href="{unsubscribe_url}">Unsubscribe</a> | <a href="{prefs_url}">Email Preferences</a>
            </div>
        </div></body></html>"""

    elif template == 'price_drop':
        pname = data.get('product_name', 'Product')
        old = data.get('old_price', 0)
        new = data.get('new_price', 0)
        savings = data.get('savings', 0)
        pid = data.get('product_id', '')

        return f"""<!DOCTYPE html><html><body style="font-family:Arial,sans-serif;margin:0;padding:0;background:#f4f4f4">
        <div style="max-width:600px;margin:20px auto;background:white;border-radius:8px;overflow:hidden">
            <div style="background:#28a745;color:white;padding:30px;text-align:center">
                <h1 style="margin:0">Price Drop Alert!</h1>
            </div>
            <div style="padding:30px">
                <p>Great news!</p>
                <p><strong>{pname}</strong> just dropped in price:</p>
                <div style="text-align:center;margin:20px 0;padding:20px;background:#f8f9fa;border-radius:8px">
                    <span style="text-decoration:line-through;color:#999;font-size:24px">${old:.2f}</span>
                    <span style="color:#28a745;font-size:32px;font-weight:bold;margin-left:15px">${new:.2f}</span>
                    <p style="color:#28a745;font-weight:bold">You save ${savings:.2f}!</p>
                </div>
                <div style="text-align:center;margin:30px 0">
                    <a href="{SITE_URL}/Shopping/product.html?id={pid}" style="background:#28a745;color:white;padding:15px 40px;text-decoration:none;border-radius:5px;font-size:18px">Buy Now</a>
                </div>
                <p>Blessings,<br>Christian Conservatives Today</p>
            </div>
            <div style="background:#f8f9fa;padding:20px;text-align:center;font-size:12px;color:#666">
                <a href="{unsubscribe_url}">Unsubscribe</a> | <a href="{prefs_url}">Email Preferences</a>
            </div>
        </div></body></html>"""

    # Fallback
    return f"""<html><body><p>You have a notification from Christian Conservatives Today.</p>
    <p><a href="{shop_url}">Visit our shop</a></p>
    <p><a href="{unsubscribe_url}">Unsubscribe</a></p></body></html>"""
