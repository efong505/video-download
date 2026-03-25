"""
Business Directory API Lambda Function
Christian business listings with categories, search, and user submissions
"""

import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('business-directory')

VALID_CATEGORIES = [
    'Financial Services', 'Web & Technology', 'Health & Wellness', 'Food & Beverage',
    'Education & Training', 'Media & Marketing', 'Construction & Trades',
    'Legal Services', 'Real Estate', 'Retail & Shopping', 'Ministry & Nonprofit',
    'Art & Creative', 'Consulting', 'Christian Schools', 'Christian School Resources', 'Other'
]

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        'body': json.dumps(body, default=decimal_default)
    }

def extract_user(event):
    auth_header = event.get('headers', {}).get('Authorization') or event.get('headers', {}).get('authorization')
    if not auth_header:
        return None, None
    import jwt
    token = auth_header.replace('Bearer ', '')
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get('user_id'), payload.get('role', 'user')
    except:
        return None, None

def list_businesses(params):
    category = params.get('category')
    search = params.get('search', '').lower()
    try:
        if category:
            response = table.query(
                IndexName='category-index',
                KeyConditionExpression='category = :cat',
                FilterExpression='#s = :approved',
                ExpressionAttributeNames={'#s': 'status'},
                ExpressionAttributeValues={':cat': category, ':approved': 'approved'}
            )
        else:
            response = table.scan(
                FilterExpression='#s = :approved',
                ExpressionAttributeNames={'#s': 'status'},
                ExpressionAttributeValues={':approved': 'approved'}
            )

        businesses = response.get('Items', [])

        if search:
            businesses = [b for b in businesses if
                search in b.get('name', '').lower() or
                search in b.get('description', '').lower() or
                search in b.get('city', '').lower() or
                search in b.get('state', '').lower()]

        businesses.sort(key=lambda x: x.get('name', ''))
        return cors_response(200, {'businesses': businesses, 'total': len(businesses)})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def submit_business(user_id, data):
    name = data.get('name', '').strip()
    category = data.get('category', '').strip()
    website = data.get('website', '').strip()
    description = data.get('description', '').strip()

    if not name or not category:
        return cors_response(400, {'error': 'Name and category are required'})

    business_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    item = {
        'business_id': business_id,
        'name': name,
        'category': category,
        'website': website,
        'description': description,
        'city': data.get('city', '').strip(),
        'state': data.get('state', '').strip(),
        'phone': data.get('phone', '').strip(),
        'email': data.get('email', '').strip(),
        'submitted_by': user_id,
        'created_at': now,
        'status': 'approved',  # Auto-approve for now; change to 'pending' for moderation
        'featured': False
    }

    table.put_item(Item=item)
    return cors_response(200, {'message': 'Business submitted', 'business': item})

def get_categories(params):
    return cors_response(200, {'categories': VALID_CATEGORIES})

def get_business(params):
    business_id = params.get('business_id')
    if not business_id:
        return cors_response(400, {'error': 'business_id required'})
    try:
        item = table.get_item(Key={'business_id': business_id}).get('Item')
        if not item:
            return cors_response(404, {'error': 'Business not found'})
        return cors_response(200, {'business': item})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def delete_business(user_id, role, data):
    business_id = data.get('business_id')
    if not business_id:
        return cors_response(400, {'error': 'business_id required'})
    try:
        item = table.get_item(Key={'business_id': business_id}).get('Item')
        if not item:
            return cors_response(404, {'error': 'Business not found'})
        if item['submitted_by'] != user_id and role not in ('admin', 'super_user'):
            return cors_response(403, {'error': 'Not authorized'})
        table.delete_item(Key={'business_id': business_id})
        return cors_response(200, {'message': 'Business deleted'})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def lambda_handler(event, context):
    if event.get('httpMethod') == 'OPTIONS':
        return cors_response(200, {})

    params = event.get('queryStringParameters') or {}
    action = params.get('action')

    # Public actions
    if action == 'list':
        return list_businesses(params)
    if action == 'categories':
        return get_categories(params)
    if action == 'get':
        return get_business(params)

    # Auth-required actions
    user_id, role = extract_user(event)
    if not user_id:
        return cors_response(401, {'error': 'Login required'})

    try:
        body = json.loads(event.get('body', '{}'))
    except:
        body = {}

    if action == 'submit':
        return submit_business(user_id, body)
    elif action == 'delete':
        return delete_business(user_id, role, body)
    else:
        return cors_response(400, {'error': f'Invalid action: {action}'})
