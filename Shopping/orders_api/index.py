import json
import boto3
import uuid
import os
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table('Orders')
products_table = dynamodb.Table('Products')
sns = boto3.client('sns')
ses = boto3.client('ses', region_name='us-east-1')

JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-here')
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:371751795928:platform-critical-alerts'

try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    print('PyJWT not available, JWT validation disabled')

def decimal_to_float(obj):
    if isinstance(obj, list):
        return [decimal_to_float(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj

def lambda_handler(event, context):
    try:
        method = event.get('httpMethod', '')
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
                },
                'body': ''
            }
        
        params = event.get('queryStringParameters') or {}
        action = params.get('action', 'create')
        
        # Handle POST body actions
        if method == 'POST':
            body = json.loads(event.get('body', '{}'))
            action = body.get('action', action)
        
        if action == 'create':
            return create_order(event)
        elif action == 'get':
            return get_order(params)
        elif action == 'list':
            return list_orders(params)
        elif action == 'update_status':
            return update_order_status(event)
        elif action == 'cancel':
            return cancel_order(event)
        else:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Invalid action'})
            }
            
    except Exception as e:
        print(f'Lambda handler error: {str(e)}')
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

def create_order(event):
    try:
        print('Event:', json.dumps(event))
        
        # Extract and validate JWT token
        headers = event.get('headers', {})
        auth_header = headers.get('Authorization') or headers.get('authorization', '')
        token = auth_header.replace('Bearer ', '')
        
        user_id = 'guest'  # Default
        
        if token and JWT_AVAILABLE:
            try:
                user = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
                user_id = user['email']
            except Exception as jwt_error:
                print(f'JWT decode error: {jwt_error}')
                # Continue with guest if token invalid
        
        body = json.loads(event.get('body', '{}'))
        print('Body:', body)
        
        order_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Validate stock
        for item in body['items']:
            try:
                response = products_table.get_item(Key={'product_id': item['product_id']})
                if 'Item' not in response:
                    return {
                        'statusCode': 400,
                        'headers': {'Access-Control-Allow-Origin': '*'},
                        'body': json.dumps({'error': f'Product not found: {item["product_id"]}'})
                    }
                product = response['Item']
                if product['stock'] < item['quantity']:
                    return {
                        'statusCode': 400,
                        'headers': {'Access-Control-Allow-Origin': '*'},
                        'body': json.dumps({'error': f'Insufficient stock for {product["name"]}'})
                    }
            except Exception as product_error:
                print(f'Product validation error: {product_error}')
                return {
                    'statusCode': 400,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'error': f'Error validating product: {str(product_error)}'})
                }
        
        # Convert items to Decimal
        items = [{
            'product_id': item['product_id'],
            'name': item['name'],
            'price': Decimal(str(item['price'])),
            'quantity': item['quantity']
        } for item in body['items']]
        
        # Create order
        order = {
            'order_id': order_id,
            'user_id': user_id,
            'user_email': body.get('user_email', user_id),
            'user_name': body.get('user_name', ''),
            'user_phone': body.get('user_phone', ''),
            'items': items,
            'subtotal': Decimal(str(body['subtotal'])),
            'tax': Decimal(str(body['tax'])),
            'total': Decimal(str(body['total'])),
            'status': 'pending',
            'order_status': 'pending',
            'order_date': timestamp,
            'payment_status': 'pending',
            'shipping_address': body.get('shipping_address', {}),
            'payment_method': body.get('payment_method', 'pending'),
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        orders_table.put_item(Item=order)
        
        # Send customer confirmation email
        try:
            customer_email = order.get('user_email', user_id)
            customer_name = order.get('user_name', 'Customer')
            
            items_list = '\n'.join([f"  • {item['name']} (Qty: {item['quantity']}) - ${float(item['price']):.2f}" for item in body['items']])
            
            ses.send_email(
                Source='Christian Conservatives Today <contact@christianconservativestoday.com>',
                Destination={'ToAddresses': [customer_email]},
                Message={
                    'Subject': {'Data': f'Order Confirmation #{order_id[:8]} - Christian Conservatives Today'},
                    'Body': {
                        'Text': {'Data': f"""Thank you for your order, {customer_name}!

Your order has been received and is being processed.

Order Details:
Order ID: {order_id}
Order Date: {timestamp}

Items Ordered:
{items_list}

Order Summary:
Subtotal: ${float(order['subtotal']):.2f}
Tax: ${float(order['tax']):.2f}
Total: ${float(order['total']):.2f}

Shipping Address:
{order.get('shipping_address', 'N/A')}

Payment Method: {order['payment_method']}
Order Status: {order['status']}

We'll send you another email when your order ships.

Thank you for shopping with us!

Christian Conservatives Today
https://christianconservativestoday.com

Questions? Reply to this email or contact us at contact@christianconservativestoday.com"""}
                    }
                }
            )
        except Exception as email_error:
            print(f'Customer email error: {email_error}')
        
        # Send SNS notification
        try:
            items_summary = '\n'.join([f"  - {item['name']} x{item['quantity']} @ ${float(item['price']):.2f}" for item in body['items']])
            
            message = f"""NEW ORDER RECEIVED

Order ID: {order_id}
Customer: {order.get('user_name', 'N/A')}
Email: {order.get('user_email', user_id)}
Phone: {order.get('user_phone', 'N/A')}

Items:
{items_summary}

Subtotal: ${float(order['subtotal']):.2f}
Tax: ${float(order['tax']):.2f}
Total: ${float(order['total']):.2f}

Shipping Address:
{order.get('shipping_address', 'N/A')}

Payment: {order['payment_method']}
Status: {order['status']}
Date: {timestamp}
"""
            
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=f'New Order #{order_id[:8]} - ${float(order["total"]):.2f}',
                Message=message
            )
        except Exception as sns_error:
            print(f'SNS notification error: {sns_error}')
            # Don't fail the order if SNS fails
        
        # Update stock
        for item in body['items']:
            products_table.update_item(
                Key={'product_id': item['product_id']},
                UpdateExpression='SET stock = stock - :qty',
                ExpressionAttributeValues={':qty': item['quantity']}
            )
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'order_id': order_id, 'status': 'created'})
        }
    except Exception as e:
        print('Error in create_order:', str(e))
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

def get_order(params):
    order_id = params.get('order_id')
    response = orders_table.get_item(Key={'order_id': order_id})
    order = decimal_to_float(response.get('Item', {}))
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'order': order})
    }

def list_orders(params):
    # Note: In production, validate JWT and extract user_id from token
    # For now, accepting user_id from params for backward compatibility
    user_id = params.get('user_id', 'guest')
    status_filter = params.get('status')
    
    if status_filter:
        # Filter by status
        response = orders_table.query(
            IndexName='order_status-order_date-index',
            KeyConditionExpression='#status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': status_filter}
        )
    else:
        # Get all orders for user
        response = orders_table.query(
            IndexName='user_id-order_date-index',
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': user_id}
        )
    
    orders = decimal_to_float(response.get('Items', []))
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'orders': orders, 'count': len(orders)})
    }

def update_order_status(event):
    body = json.loads(event.get('body', '{}'))
    order_id = body['order_id']
    new_status = body['status']
    
    orders_table.update_item(
        Key={'order_id': order_id},
        UpdateExpression='SET #status = :status, order_status = :status, updated_at = :updated',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={
            ':status': new_status,
            ':updated': datetime.utcnow().isoformat()
        }
    )
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'status': 'updated'})
    }


def cancel_order(event):
    try:
        body = json.loads(event.get('body', '{}'))
        order_id = body.get('order_id')
        user_id = body.get('user_id')
        
        if not order_id:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'order_id required'})
            }
        
        # Get order
        response = orders_table.get_item(Key={'order_id': order_id})
        order = response.get('Item')
        
        if not order:
            return {
                'statusCode': 404,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Order not found'})
            }
        
        # Verify user owns the order
        if order['user_id'] != user_id:
            return {
                'statusCode': 403,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Unauthorized'})
            }
        
        # Check if order can be cancelled
        if order['status'] not in ['pending', 'processing']:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': f'Cannot cancel order with status: {order["status"]}'})
            }
        
        # Update order status to cancelled
        orders_table.update_item(
            Key={'order_id': order_id},
            UpdateExpression='SET #status = :status, order_status = :status, updated_at = :updated',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'cancelled',
                ':updated': datetime.utcnow().isoformat()
            }
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
            customer_email = order.get('user_email', user_id)
            customer_name = order.get('user_name', 'Customer')
            
            ses.send_email(
                Source='Christian Conservatives Today <contact@christianconservativestoday.com>',
                Destination={'ToAddresses': [customer_email]},
                Message={
                    'Subject': {'Data': f'Order Cancelled #{order_id[:8]} - Christian Conservatives Today'},
                    'Body': {
                        'Text': {'Data': f"""Dear {customer_name},

Your order #{order_id[:8]} has been cancelled as requested.

Order Total: ${float(order['total']):.2f}

If you were charged, a refund will be processed within 5-7 business days.

If you have any questions, please contact us at contact@christianconservativestoday.com

Thank you,
Christian Conservatives Today
https://christianconservativestoday.com"""}
                    }
                }
            )
        except Exception as email_error:
            print(f'Cancellation email error: {email_error}')
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'success': True, 'message': 'Order cancelled successfully'})
        }
        
    except Exception as e:
        print(f'Error cancelling order: {str(e)}')
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
