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
reviews_table = dynamodb.Table('Reviews')
products_table = dynamodb.Table('Products')
JWT_SECRET = os.environ.get('JWT_SECRET', '')

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
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
        return None, {'statusCode': 401, 'headers': HEADERS, 'body': json.dumps({'error': 'Authentication required. Please log in.'})}
    return user, None

def lambda_handler(event, context):
    try:
        if event.get('httpMethod') == 'OPTIONS':
            return {'statusCode': 200, 'headers': HEADERS, 'body': ''}

        action = (event.get('queryStringParameters') or {}).get('action')

        if action == 'list':
            return list_reviews(event)
        elif action == 'create':
            return create_review(event)
        elif action == 'vote':
            return vote_review(event)
        else:
            return {'statusCode': 400, 'headers': HEADERS, 'body': json.dumps({'error': 'Invalid action'})}
    except Exception as e:
        return {'statusCode': 500, 'headers': HEADERS, 'body': json.dumps({'error': str(e)})}

def list_reviews(event):
    params = event.get('queryStringParameters') or {}
    product_id = params.get('product_id')

    response = reviews_table.query(
        IndexName='product_id-created_at-index',
        KeyConditionExpression='product_id = :pid',
        ExpressionAttributeValues={':pid': product_id, ':approved': 'approved'},
        FilterExpression='#status = :approved',
        ExpressionAttributeNames={'#status': 'status'}
    )

    return {'statusCode': 200, 'headers': HEADERS, 'body': json.dumps({'reviews': decimal_to_float(response.get('Items', [])), 'count': response.get('Count', 0)})}

def create_review(event):
    user, err = require_auth(event)
    if err: return err

    body = json.loads(event.get('body', '{}'))
    review_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    review = {
        'review_id': review_id,
        'product_id': body['product_id'],
        'user_id': user['email'],
        'user_name': f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or user['email'],
        'rating': body['rating'],
        'title': body['title'],
        'review_text': body['review_text'],
        'helpful_votes': 0,
        'unhelpful_votes': 0,
        'verified_purchase': body.get('verified_purchase', False),
        'status': 'approved',
        'created_at': timestamp
    }

    reviews_table.put_item(Item=review)
    update_product_rating(body['product_id'])

    return {'statusCode': 200, 'headers': HEADERS, 'body': json.dumps({'review_id': review_id, 'status': 'created'})}

def vote_review(event):
    user, err = require_auth(event)
    if err: return err

    body = json.loads(event.get('body', '{}'))
    field = 'helpful_votes' if body['vote_type'] == 'helpful' else 'unhelpful_votes'

    reviews_table.update_item(
        Key={'review_id': body['review_id']},
        UpdateExpression=f'SET {field} = {field} + :inc',
        ExpressionAttributeValues={':inc': 1}
    )

    return {'statusCode': 200, 'headers': HEADERS, 'body': json.dumps({'status': 'voted'})}

def update_product_rating(product_id):
    response = reviews_table.query(
        IndexName='product_id-created_at-index',
        KeyConditionExpression='product_id = :pid',
        ExpressionAttributeValues={':pid': product_id, ':approved': 'approved'},
        FilterExpression='#status = :approved',
        ExpressionAttributeNames={'#status': 'status'}
    )

    reviews = response.get('Items', [])
    if reviews:
        avg_rating = sum(r['rating'] for r in reviews) / len(reviews)
        products_table.update_item(
            Key={'product_id': product_id},
            UpdateExpression='SET average_rating = :rating, review_count = :count',
            ExpressionAttributeValues={
                ':rating': Decimal(str(round(avg_rating, 1))),
                ':count': len(reviews)
            }
        )
