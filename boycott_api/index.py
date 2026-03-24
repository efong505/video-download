"""
Boycott Tracker API Lambda Function
Track companies with boycott status, reasons, user reports, and alternatives
"""

import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('boycott-tracker')

VALID_STATUSES = ['active', 'resolved', 'watching']

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

def list_boycotts(params):
    status_filter = params.get('status', 'active')
    try:
        if status_filter == 'all':
            response = table.scan()
        else:
            response = table.query(
                IndexName='status-index',
                KeyConditionExpression='#s = :status',
                ExpressionAttributeNames={'#s': 'status'},
                ExpressionAttributeValues={':status': status_filter}
            )
        items = response.get('Items', [])
        items.sort(key=lambda x: x.get('boycott_votes', 0), reverse=True)
        return cors_response(200, {'boycotts': items, 'total': len(items)})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def report_company(user_id, data):
    company_name = data.get('company_name', '').strip()
    reason = data.get('reason', '').strip()
    if not company_name or not reason:
        return cors_response(400, {'error': 'Company name and reason are required'})

    boycott_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    item = {
        'boycott_id': boycott_id,
        'company_name': company_name,
        'reason': reason,
        'category': data.get('category', 'General'),
        'alternatives': data.get('alternatives', ''),
        'source_url': data.get('source_url', ''),
        'reported_by': user_id,
        'created_at': now,
        'status': 'active',
        'boycott_votes': 1,
        'voted_by': [user_id]
    }

    table.put_item(Item=item)
    return cors_response(200, {'message': 'Company reported', 'boycott': item})

def vote_boycott(user_id, data):
    boycott_id = data.get('boycott_id')
    if not boycott_id:
        return cors_response(400, {'error': 'boycott_id required'})

    try:
        item = table.get_item(Key={'boycott_id': boycott_id}).get('Item')
        if not item:
            return cors_response(404, {'error': 'Not found'})

        voted_by = item.get('voted_by', [])
        if user_id in voted_by:
            voted_by.remove(user_id)
            table.update_item(
                Key={'boycott_id': boycott_id},
                UpdateExpression='SET boycott_votes = boycott_votes - :one, voted_by = :vb',
                ExpressionAttributeValues={':one': 1, ':vb': voted_by}
            )
            return cors_response(200, {'message': 'Vote removed', 'votes': item['boycott_votes'] - 1})
        else:
            voted_by.append(user_id)
            table.update_item(
                Key={'boycott_id': boycott_id},
                UpdateExpression='SET boycott_votes = boycott_votes + :one, voted_by = :vb',
                ExpressionAttributeValues={':one': 1, ':vb': voted_by}
            )
            return cors_response(200, {'message': 'Voted', 'votes': item['boycott_votes'] + 1})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def add_alternative(user_id, data):
    boycott_id = data.get('boycott_id')
    alternative = data.get('alternative', '').strip()
    if not boycott_id or not alternative:
        return cors_response(400, {'error': 'boycott_id and alternative required'})

    try:
        item = table.get_item(Key={'boycott_id': boycott_id}).get('Item')
        if not item:
            return cors_response(404, {'error': 'Not found'})

        existing = item.get('alternatives', '')
        updated = (existing + '\n' + alternative).strip() if existing else alternative
        table.update_item(
            Key={'boycott_id': boycott_id},
            UpdateExpression='SET alternatives = :alt',
            ExpressionAttributeValues={':alt': updated}
        )
        return cors_response(200, {'message': 'Alternative added'})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def lambda_handler(event, context):
    if event.get('httpMethod') == 'OPTIONS':
        return cors_response(200, {})

    params = event.get('queryStringParameters') or {}
    action = params.get('action')

    if action == 'list':
        return list_boycotts(params)

    user_id, role = extract_user(event)
    if not user_id:
        return cors_response(401, {'error': 'Login required'})

    try:
        body = json.loads(event.get('body', '{}'))
    except:
        body = {}

    if action == 'report':
        return report_company(user_id, body)
    elif action == 'vote':
        return vote_boycott(user_id, body)
    elif action == 'add_alternative':
        return add_alternative(user_id, body)
    else:
        return cors_response(400, {'error': f'Invalid action: {action}'})
