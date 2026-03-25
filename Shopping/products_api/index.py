import json
import boto3
import hashlib
import hmac
import base64
import os
from decimal import Decimal
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
products_table = dynamodb.Table('Products')
JWT_SECRET = os.environ.get('JWT_SECRET', '')

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

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

def require_admin(event):
    user = verify_jwt(event)
    if not user:
        return None, {'statusCode': 401, 'headers': HEADERS, 'body': json.dumps({'error': 'Authentication required'})}
    if user.get('role') not in ('admin', 'super_user'):
        return None, {'statusCode': 403, 'headers': HEADERS, 'body': json.dumps({'error': 'Admin access required'})}
    return user, None

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
}

def lambda_handler(event, context):
    try:
        if event.get('httpMethod') == 'OPTIONS':
            return {'statusCode': 200, 'headers': HEADERS, 'body': ''}

        action = (event.get('queryStringParameters') or {}).get('action', 'list')

        # Public endpoints
        if action in ('list', 'get', 'search'):
            if action == 'list': return list_products(event, HEADERS)
            if action == 'get': return get_product(event, HEADERS)
            return search_products(event, HEADERS)

        # Admin-only endpoints
        if action in ('create', 'update', 'delete'):
            user, err = require_admin(event)
            if err: return err
            if action == 'create': return create_product(event, HEADERS)
            if action == 'update': return update_product(event, HEADERS)
            return delete_product(event, HEADERS)

        return {'statusCode': 400, 'headers': HEADERS, 'body': json.dumps({'error': 'Invalid action'})}

    except Exception as e:
        return {'statusCode': 500, 'headers': HEADERS, 'body': json.dumps({'error': str(e)})}

def list_products(event, headers):
    params = event.get('queryStringParameters') or {}
    category = params.get('category')
    limit = int(params.get('limit', 50))
    
    if category:
        response = products_table.query(
            IndexName='category-index',
            KeyConditionExpression='category = :cat',
            ExpressionAttributeValues={':cat': category},
            Limit=limit
        )
    else:
        response = products_table.scan(Limit=limit)
    
    items = response.get('Items', [])
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({'products': items, 'count': len(items)}, default=decimal_default)
    }

def get_product(event, headers):
    params = event.get('queryStringParameters') or {}
    product_id = params.get('product_id')
    
    if not product_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'product_id required'})}
    
    response = products_table.get_item(Key={'product_id': product_id})
    
    if 'Item' not in response:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Product not found'})}
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'product': response['Item']}, default=decimal_default)}

def search_products(event, headers):
    params = event.get('queryStringParameters') or {}
    query = params.get('q', '').lower()
    
    if not query:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Search query required'})}
    
    response = products_table.scan()
    items = [i for i in response.get('Items', []) if query in i.get('name', '').lower()]
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'products': items, 'count': len(items)}, default=decimal_default)}

def create_product(event, headers):
    import uuid
    from datetime import datetime
    
    body = json.loads(event.get('body', '{}'))
    product_id = str(uuid.uuid4())
    
    product = {
        'product_id': product_id,
        'name': body['name'],
        'description': body['description'],
        'price': Decimal(str(body['price'])),
        'stock': body['stock'],
        'category': body['category'],
        'image_url': body['image_url'],
        'featured': body.get('featured', '0'),
        'average_rating': Decimal('0'),
        'review_count': 0,
        'created_at': datetime.utcnow().isoformat()
    }
    
    products_table.put_item(Item=product)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'product_id': product_id})}

def update_product(event, headers):
    body = json.loads(event.get('body', '{}'))
    product_id = body['product_id']
    
    products_table.update_item(
        Key={'product_id': product_id},
        UpdateExpression='SET #name = :name, description = :desc, price = :price, stock = :stock, category = :cat, image_url = :img, featured = :feat',
        ExpressionAttributeNames={'#name': 'name'},
        ExpressionAttributeValues={
            ':name': body['name'],
            ':desc': body['description'],
            ':price': Decimal(str(body['price'])),
            ':stock': body['stock'],
            ':cat': body['category'],
            ':img': body['image_url'],
            ':feat': body.get('featured', '0')
        }
    )
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'status': 'updated'})}

def delete_product(event, headers):
    body = json.loads(event.get('body', '{}'))
    product_id = body['product_id']
    
    products_table.delete_item(Key={'product_id': product_id})
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'status': 'deleted'})}
