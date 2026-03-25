import json
import boto3
import uuid
import hashlib
import hmac
import base64
import os
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table('Orders')
products_table = dynamodb.Table('Products')
sns = boto3.client('sns')
ses = boto3.client('ses', region_name='us-east-1')

JWT_SECRET = os.environ.get('JWT_SECRET', '')
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:371751795928:platform-critical-alerts'

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
}

def decimal_to_float(obj):
    if isinstance(obj, list):
        return [decimal_to_float(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj

def verify_jwt(event):
    auth = (event.get('headers') or {}).get('Authorization') or (event.get('headers') or {}).get('authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth.split(' ')[1]
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        msg = f"{parts[0]}.{parts[1]}"
        sig = base64.urlsafe_b64encode(hmac.new(JWT_SECRET.encode(), msg.encode(), hashlib.sha256).digest()).decode().rstrip('=')
        if sig != parts[2]:
            return None
        pad = parts[1] + '=' * (4 - len(parts[1]) % 4)
        payload = json.loads(base64.urlsafe_b64decode(pad))
        if payload.get('exp', 0) < datetime.utcnow().timestamp():
            return None
        return payload
    except Exception:
        return None

def require_auth(event):
    user = verify_jwt(event)
    if not user:
        return None, {'statusCode': 401, 'headers': HEADERS, 'body': json.dumps({'error': 'Authentication required'})}
    return user, None

def require_admin(event):
    user = verify_jwt(event)
    if not user:
        return None, {'statusCode': 401, 'headers': HEADERS, 'body': json.dumps({'error': 'Authentication required'})}
    if user.get('role') not in ('admin', 'super_user'):
        return None, {'statusCode': 403, 'headers': HEADERS, 'body': json.dumps({'error': 'Admin access required'})}
    return user, None

def lambda_handler(event, context):
    try:
        method = event.get('httpMethod', '')
        if method == 'OPTIONS':
            return {'statusCode': 200, 'headers': HEADERS, 'body': ''}

        params = event.get('queryStringParameters') or {}
        action = params.get('action', 'create')

        if method == 'POST':
            body = json.loads(event.get('body', '{}'))
            action = body.get('action', action)

        if action == 'create':
            return create_order(event)
        elif action == 'get':
            return get_order(event, params)
        elif action == 'list':
            return list_orders(event, params)
        elif action == 'update_status':
            return update_order_status(event)
        elif action == 'cancel':
            return cancel_order(event)
        else:
            return {'statusCode': 400, 'headers': HEADERS, 'body': json.dumps({'error': 'Invalid action'})}

    except Exception as e:
        print(f'Lambda handler error: {str(e)}')
        import traceback
        traceback.print_exc()
        return {'statusCode': 500, 'headers': HEADERS, 'body': json.dumps({'error': str(e)})}

def create_order(event):
    try:
        # Optional auth — logged-in users get their email as user_id, guests get 'guest'
        user = verify_jwt(event)
        user_id = user['email'] if user else 'guest'

        body = json.loads(event.get('body', '{}'))
        order_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        # Validate stock
        for item in body['items']:
            response = products_table.get_item(Key={'product_id': item['product_id']})
            if 'Item' not in response:
                return {'statusCode': 400, 'headers': HEADERS, 'body': json.dumps({'error': f'Product not found: {item["product_id"]}'})}
            product = response['Item']
            if product['stock'] < item['quantity']:
                return {'statusCode': 400, 'headers': HEADERS, 'body': json.dumps({'error': f'Insufficient stock for {product["name"]}'})}

        items = [{
            'product_id': item['product_id'],
            'name': item['name'],
            'price': Decimal(str(item['price'])),
            'quantity': item['quantity']
        } for item in body['items']]

        order = {
            'order_id': order_id,
            'user_id': user_id,
            'user_email': body.get('user_email', user['email'] if user else ''),
            'user_name': body.get('user_name', f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() if user else ''),
            'user_phone': body.get('user_phone', ''),
            'items': items,
            'subtotal': Decimal(str(body['subtotal'])),
            'tax': Decimal(str(body['tax'])),
            'total': Decimal(str(body['total'])),
            'status': body.get('initial_status', 'pending'),
            'order_status': body.get('initial_status', 'pending'),
            'order_date': timestamp,
            'payment_status': body.get('payment_status', 'pending'),
            'payment_method': body.get('payment_method', 'pending'),
            'paypal_order_id': body.get('paypal_order_id', ''),
            'shipping_address': body.get('shipping_address', {}),
            'created_at': timestamp,
            'updated_at': timestamp
        }

        orders_table.put_item(Item=order)

        # Send customer confirmation email
        try:
            customer_email = order['user_email']
            customer_name = order['user_name'] or 'Customer'
            items_list = '\n'.join([f"  - {item['name']} (Qty: {item['quantity']}) - ${float(item['price']):.2f}" for item in body['items']])

            ses.send_email(
                Source='Christian Conservatives Today <contact@christianconservativestoday.com>',
                Destination={'ToAddresses': [customer_email]},
                Message={
                    'Subject': {'Data': f'Order Confirmation #{order_id[:8]} - Christian Conservatives Today'},
                    'Body': {
                        'Text': {'Data': f"""Thank you for your order, {customer_name}!

Your order has been received and is being processed.

Order ID: {order_id}
Date: {timestamp}

Items:
{items_list}

Subtotal: ${float(order['subtotal']):.2f}
Tax: ${float(order['tax']):.2f}
Total: ${float(order['total']):.2f}

Payment: {order['payment_method']}
Status: {order['status']}

We'll send you another email when your order ships.

Christian Conservatives Today
https://christianconservativestoday.com"""}
                    }
                }
            )
        except Exception as e:
            print(f'Customer email error: {e}')

        # Send SNS notification
        try:
            items_summary = '\n'.join([f"  - {item['name']} x{item['quantity']} @ ${float(item['price']):.2f}" for item in body['items']])
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=f'New Order #{order_id[:8]} - ${float(order["total"]):.2f}',
                Message=f"""NEW ORDER RECEIVED

Order ID: {order_id}
Customer: {order['user_name']}
Email: {order['user_email']}
Payment: {order['payment_method']}

Items:
{items_summary}

Total: ${float(order['total']):.2f}
Date: {timestamp}"""
            )
        except Exception as e:
            print(f'SNS error: {e}')

        # Update stock
        for item in body['items']:
            products_table.update_item(
                Key={'product_id': item['product_id']},
                UpdateExpression='SET stock = stock - :qty',
                ExpressionAttributeValues={':qty': item['quantity']}
            )

        return {'statusCode': 200, 'headers': HEADERS, 'body': json.dumps({'order_id': order_id, 'status': 'created'})}

    except Exception as e:
        print(f'Error in create_order: {e}')
        import traceback
        traceback.print_exc()
        return {'statusCode': 500, 'headers': HEADERS, 'body': json.dumps({'error': str(e)})}

def get_order(event, params):
    user, err = require_auth(event)
    if err: return err

    order_id = params.get('order_id')
    response = orders_table.get_item(Key={'order_id': order_id})
    order = response.get('Item')

    if not order:
        return {'statusCode': 404, 'headers': HEADERS, 'body': json.dumps({'error': 'Order not found'})}

    # Users can only see their own orders, admins can see all
    if user.get('role') not in ('admin', 'super_user') and order['user_id'] != user['email']:
        return {'statusCode': 403, 'headers': HEADERS, 'body': json.dumps({'error': 'Access denied'})}

    return {'statusCode': 200, 'headers': HEADERS, 'body': json.dumps({'order': decimal_to_float(order)})}

def list_orders(event, params):
    user, err = require_auth(event)
    if err: return err

    status_filter = params.get('status')

    # Admins can list all orders or filter by status
    if user.get('role') in ('admin', 'super_user'):
        if status_filter:
            response = orders_table.query(
                IndexName='order_status-order_date-index',
                KeyConditionExpression='#status = :status',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':status': status_filter}
            )
        else:
            user_id = params.get('user_id')
            if user_id:
                response = orders_table.query(
                    IndexName='user_id-order_date-index',
                    KeyConditionExpression='user_id = :uid',
                    ExpressionAttributeValues={':uid': user_id}
                )
            else:
                response = orders_table.scan()
    else:
        # Regular users only see their own orders
        response = orders_table.query(
            IndexName='user_id-order_date-index',
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': user['email']}
        )

    orders = decimal_to_float(response.get('Items', []))
    return {'statusCode': 200, 'headers': HEADERS, 'body': json.dumps({'orders': orders, 'count': len(orders)})}

def update_order_status(event):
    user, err = require_admin(event)
    if err: return err

    body = json.loads(event.get('body', '{}'))
    orders_table.update_item(
        Key={'order_id': body['order_id']},
        UpdateExpression='SET #status = :status, order_status = :status, updated_at = :updated',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': body['status'], ':updated': datetime.utcnow().isoformat()}
    )
    return {'statusCode': 200, 'headers': HEADERS, 'body': json.dumps({'status': 'updated'})}

def cancel_order(event):
    user, err = require_auth(event)
    if err: return err

    body = json.loads(event.get('body', '{}'))
    order_id = body.get('order_id')
    if not order_id:
        return {'statusCode': 400, 'headers': HEADERS, 'body': json.dumps({'error': 'order_id required'})}

    response = orders_table.get_item(Key={'order_id': order_id})
    order = response.get('Item')
    if not order:
        return {'statusCode': 404, 'headers': HEADERS, 'body': json.dumps({'error': 'Order not found'})}

    # Owner or admin can cancel
    if user.get('role') not in ('admin', 'super_user') and order['user_id'] != user['email']:
        return {'statusCode': 403, 'headers': HEADERS, 'body': json.dumps({'error': 'Access denied'})}

    if order['status'] not in ['pending', 'processing']:
        return {'statusCode': 400, 'headers': HEADERS, 'body': json.dumps({'error': f'Cannot cancel order with status: {order["status"]}'})}

    orders_table.update_item(
        Key={'order_id': order_id},
        UpdateExpression='SET #status = :status, order_status = :status, updated_at = :updated',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'cancelled', ':updated': datetime.utcnow().isoformat()}
    )

    # Restore stock
    for item in order['items']:
        products_table.update_item(
            Key={'product_id': item['product_id']},
            UpdateExpression='SET stock = stock + :qty',
            ExpressionAttributeValues={':qty': int(item['quantity'])}
        )

    # Send cancellation email
    try:
        ses.send_email(
            Source='Christian Conservatives Today <contact@christianconservativestoday.com>',
            Destination={'ToAddresses': [order.get('user_email', user['email'])]},
            Message={
                'Subject': {'Data': f'Order Cancelled #{order_id[:8]}'},
                'Body': {'Text': {'Data': f"Your order #{order_id[:8]} has been cancelled.\n\nIf you were charged, a refund will be processed within 5-7 business days.\n\nChristian Conservatives Today"}}
            }
        )
    except Exception as e:
        print(f'Cancellation email error: {e}')

    return {'statusCode': 200, 'headers': HEADERS, 'body': json.dumps({'success': True, 'message': 'Order cancelled'})}
