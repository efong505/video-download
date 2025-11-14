import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table('Orders')
products_table = dynamodb.Table('Products')

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
        params = event.get('queryStringParameters') or {}
        action = params.get('action', 'create')
        
        if action == 'create':
            return create_order(event)
        elif action == 'get':
            return get_order(params)
        elif action == 'list':
            return list_orders(params)
        else:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Invalid action'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

def create_order(event):
    try:
        print('Event:', json.dumps(event))
        body = json.loads(event.get('body', '{}'))
        print('Body:', body)
        
        order_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Validate stock
        for item in body['items']:
            product = products_table.get_item(Key={'product_id': item['product_id']})['Item']
            if product['stock'] < item['quantity']:
                return {
                    'statusCode': 400,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'error': f'Insufficient stock for {product["name"]}'})
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
            'user_id': body.get('user_id', 'guest'),
            'items': items,
            'subtotal': Decimal(str(body['subtotal'])),
            'tax': Decimal(str(body['tax'])),
            'total': Decimal(str(body['total'])),
            'status': 'pending',
            'shipping_address': body.get('shipping_address', {}),
            'payment_method': body.get('payment_method', 'pending'),
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        orders_table.put_item(Item=order)
        
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
    user_id = params.get('user_id', 'guest')
    response = orders_table.query(
        IndexName='user_id-index',
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': user_id}
    )
    
    orders = decimal_to_float(response.get('Items', []))
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'orders': orders, 'count': len(orders)})
    }
