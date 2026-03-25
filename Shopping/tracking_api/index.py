import json
import boto3
import uuid
import time
from datetime import datetime, timedelta
from decimal import Decimal
from collections import Counter

dynamodb = boto3.resource('dynamodb')
views_table = dynamodb.Table('ProductViews')
watchlist_table = dynamodb.Table('WatchList')
products_table = dynamodb.Table('Products')

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS'
}

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def respond(status, body):
    return {'statusCode': status, 'headers': HEADERS, 'body': json.dumps(body, default=decimal_default)}

def lambda_handler(event, context):
    if event.get('httpMethod') == 'OPTIONS':
        return respond(200, {})

    action = (event.get('queryStringParameters') or {}).get('action', '')
    method = event.get('httpMethod', 'GET')

    try:
        if action == 'track-view' and method == 'POST':
            return track_view(event)
        elif action == 'track-cart-add' and method == 'POST':
            return track_cart_add(event)
        elif action == 'recommendations' and method == 'GET':
            return get_recommendations(event)
        elif action == 'watchlist-add' and method == 'POST':
            return watchlist_add(event)
        elif action == 'watchlist-remove' and method == 'DELETE':
            return watchlist_remove(event)
        elif action == 'watchlist' and method == 'GET':
            return get_watchlist(event)
        elif action == 'popular' and method == 'GET':
            return get_popular_products(event)
        else:
            return respond(400, {'error': f'Invalid action: {action}'})
    except Exception as e:
        print(f"Error: {e}")
        return respond(500, {'error': str(e)})


def _get_user_id(event):
    """Extract user_id from query params or body. Falls back to session_id."""
    params = event.get('queryStringParameters') or {}
    if params.get('user_id'):
        return params['user_id'], None
    body = json.loads(event.get('body', '{}')) if event.get('body') else {}
    user_id = body.get('user_id')
    session_id = body.get('session_id') or params.get('session_id') or f"anon_{uuid.uuid4().hex[:12]}"
    return user_id, session_id


def track_view(event):
    body = json.loads(event.get('body', '{}'))
    user_id, session_id = _get_user_id(event)
    now = datetime.utcnow().isoformat() + 'Z'
    # TTL: 90 days from now
    expires_at = int(time.time()) + (90 * 24 * 3600)

    view_id = f"view_{uuid.uuid4().hex[:16]}"

    item = {
        'view_id': view_id,
        'timestamp': now,
        'user_id': user_id or session_id,
        'session_id': session_id or 'none',
        'product_id': body['product_id'],
        'product_name': body.get('product_name', ''),
        'product_price': Decimal(str(body.get('product_price', 0))),
        'product_category': body.get('product_category', ''),
        'added_to_cart': False,
        'purchased': False,
        'referrer': body.get('referrer', ''),
        'device_type': body.get('device_type', 'unknown'),
        'created_at': now,
        'expires_at': expires_at
    }

    views_table.put_item(Item=item)
    return respond(200, {'success': True, 'view_id': view_id})


def track_cart_add(event):
    body = json.loads(event.get('body', '{}'))
    user_id, session_id = _get_user_id(event)
    uid = user_id or session_id
    product_id = body['product_id']

    # Find the most recent view of this product by this user and mark it
    resp = views_table.query(
        IndexName='user_id-timestamp-index',
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': uid},
        ScanIndexForward=False,
        Limit=20
    )

    updated = False
    for item in resp.get('Items', []):
        if item['product_id'] == product_id and not item.get('added_to_cart'):
            views_table.update_item(
                Key={'view_id': item['view_id'], 'timestamp': item['timestamp']},
                UpdateExpression='SET added_to_cart = :t',
                ExpressionAttributeValues={':t': True}
            )
            updated = True
            break

    return respond(200, {'success': True, 'updated': updated})


def get_recommendations(event):
    params = event.get('queryStringParameters') or {}
    user_id = params.get('user_id') or params.get('session_id')
    if not user_id:
        return respond(400, {'error': 'user_id or session_id required'})

    # Get user's recent views
    resp = views_table.query(
        IndexName='user_id-timestamp-index',
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': user_id},
        ScanIndexForward=False,
        Limit=50
    )
    views = resp.get('Items', [])

    if not views:
        # No history — return featured products
        prod_resp = products_table.scan(Limit=6)
        return respond(200, {'recommendations': prod_resp.get('Items', []), 'source': 'featured'})

    # Find top category from views
    categories = [v.get('product_category', '') for v in views if v.get('product_category')]
    viewed_product_ids = {v['product_id'] for v in views}

    if not categories:
        prod_resp = products_table.scan(Limit=6)
        return respond(200, {'recommendations': prod_resp.get('Items', []), 'source': 'featured'})

    top_category = Counter(categories).most_common(1)[0][0]

    # Get products in that category, excluding already-viewed
    prod_resp = products_table.query(
        IndexName='category-created_at-index',
        KeyConditionExpression='category = :cat',
        ExpressionAttributeValues={':cat': top_category},
        Limit=20
    )

    recs = [p for p in prod_resp.get('Items', []) if p['product_id'] not in viewed_product_ids][:6]

    # If not enough, pad with other products
    if len(recs) < 6:
        all_resp = products_table.scan(Limit=20)
        for p in all_resp.get('Items', []):
            if p['product_id'] not in viewed_product_ids and p not in recs:
                recs.append(p)
            if len(recs) >= 6:
                break

    return respond(200, {'recommendations': recs, 'source': 'personalized', 'based_on': top_category})


def watchlist_add(event):
    body = json.loads(event.get('body', '{}'))
    user_id = body.get('user_id')
    if not user_id:
        return respond(400, {'error': 'user_id required'})

    now = datetime.utcnow().isoformat() + 'Z'

    item = {
        'user_id': user_id,
        'product_id': body['product_id'],
        'product_name': body.get('product_name', ''),
        'current_price': Decimal(str(body.get('current_price', 0))),
        'target_price': Decimal(str(body.get('target_price', 0))),
        'notify_on_price_drop': body.get('notify_on_price_drop', True),
        'notify_on_restock': body.get('notify_on_restock', True),
        'notified_price_drop': False,
        'notified_restock': False,
        'created_at': now
    }

    watchlist_table.put_item(Item=item)
    return respond(200, {'success': True})


def watchlist_remove(event):
    params = event.get('queryStringParameters') or {}
    user_id = params.get('user_id')
    product_id = params.get('product_id')
    if not user_id or not product_id:
        return respond(400, {'error': 'user_id and product_id required'})

    watchlist_table.delete_item(Key={'user_id': user_id, 'product_id': product_id})
    return respond(200, {'success': True})


def get_watchlist(event):
    params = event.get('queryStringParameters') or {}
    user_id = params.get('user_id')
    if not user_id:
        return respond(400, {'error': 'user_id required'})

    resp = watchlist_table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': user_id}
    )

    return respond(200, {'watchlist': resp.get('Items', []), 'count': resp.get('Count', 0)})


def get_popular_products(event):
    """Get most-viewed products in the last 7 days."""
    cutoff = (datetime.utcnow() - timedelta(days=7)).isoformat() + 'Z'

    # Scan recent views and count by product_id
    resp = views_table.scan(
        FilterExpression='#ts > :cutoff',
        ExpressionAttributeNames={'#ts': 'timestamp'},
        ExpressionAttributeValues={':cutoff': cutoff},
        ProjectionExpression='product_id,product_name'
    )

    product_counts = Counter()
    product_names = {}
    for item in resp.get('Items', []):
        pid = item['product_id']
        product_counts[pid] += 1
        product_names[pid] = item.get('product_name', '')

    popular = [
        {'product_id': pid, 'product_name': product_names[pid], 'view_count': count}
        for pid, count in product_counts.most_common(10)
    ]

    return respond(200, {'popular': popular})
