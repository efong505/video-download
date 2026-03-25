"""
Fact-Check API Lambda Function
Submit claims, assign verdicts, vote on accuracy, search by category
"""

import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('fact-checks')

VALID_VERDICTS = ['true', 'false', 'misleading', 'unverified', 'partly-true']

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

def list_facts(params):
    try:
        response = table.scan()
        items = response.get('Items', [])

        verdict = params.get('verdict')
        if verdict and verdict != 'all':
            items = [i for i in items if i.get('verdict') == verdict]

        category = params.get('category')
        if category:
            items = [i for i in items if category.lower() in i.get('category', '').lower()]

        search = params.get('search')
        if search:
            s = search.lower()
            items = [i for i in items if s in i.get('claim', '').lower() or s in i.get('source', '').lower() or s in i.get('explanation', '').lower()]

        items.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return cors_response(200, {'facts': items, 'total': len(items)})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def submit_fact(user_id, data):
    claim = data.get('claim', '').strip()
    verdict = data.get('verdict', '').strip().lower()
    if not claim or verdict not in VALID_VERDICTS:
        return cors_response(400, {'error': 'Claim and valid verdict required (true/false/misleading/unverified/partly-true)'})

    fact_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    item = {
        'id': fact_id,
        'claim': claim,
        'verdict': verdict,
        'source': data.get('source', '').strip(),
        'source_url': data.get('source_url', '').strip(),
        'explanation': data.get('explanation', '').strip(),
        'category': data.get('category', 'General'),
        'submitted_by': user_id,
        'created_at': now,
        'agree_votes': 0,
        'disagree_votes': 0,
        'voted_by': {}
    }

    table.put_item(Item=item)
    return cors_response(200, {'message': 'Fact-check submitted', 'fact': item})

def vote_fact(user_id, data):
    fact_id = data.get('fact_id')
    vote_type = data.get('vote_type')
    if not fact_id or vote_type not in ['agree', 'disagree']:
        return cors_response(400, {'error': 'fact_id and vote_type (agree/disagree) required'})

    try:
        item = table.get_item(Key={'id': fact_id}).get('Item')
        if not item:
            return cors_response(404, {'error': 'Not found'})

        voted_by = item.get('voted_by', {})
        prev_vote = voted_by.get(user_id)

        agree = item.get('agree_votes', 0)
        disagree = item.get('disagree_votes', 0)

        # Remove previous vote if exists
        if prev_vote == 'agree':
            agree -= 1
        elif prev_vote == 'disagree':
            disagree -= 1

        # Toggle off if same vote, otherwise apply new vote
        if prev_vote == vote_type:
            del voted_by[user_id]
        else:
            voted_by[user_id] = vote_type
            if vote_type == 'agree':
                agree += 1
            else:
                disagree += 1

        table.update_item(
            Key={'id': fact_id},
            UpdateExpression='SET agree_votes = :a, disagree_votes = :d, voted_by = :vb',
            ExpressionAttributeValues={':a': agree, ':d': disagree, ':vb': voted_by}
        )
        return cors_response(200, {'agree': agree, 'disagree': disagree})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def delete_fact(user_id, role, data):
    fact_id = data.get('fact_id')
    if not fact_id:
        return cors_response(400, {'error': 'fact_id required'})
    try:
        item = table.get_item(Key={'id': fact_id}).get('Item')
        if not item:
            return cors_response(404, {'error': 'Not found'})
        if item.get('submitted_by') != user_id and role != 'admin':
            return cors_response(403, {'error': 'Not authorized'})
        table.delete_item(Key={'id': fact_id})
        return cors_response(200, {'message': 'Deleted'})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def lambda_handler(event, context):
    if event.get('httpMethod') == 'OPTIONS':
        return cors_response(200, {})

    params = event.get('queryStringParameters') or {}
    action = params.get('action')

    if action == 'list':
        return list_facts(params)

    user_id, role = extract_user(event)
    if not user_id:
        return cors_response(401, {'error': 'Login required'})

    try:
        body = json.loads(event.get('body', '{}'))
    except:
        body = {}

    if action == 'submit':
        return submit_fact(user_id, body)
    elif action == 'vote':
        return vote_fact(user_id, body)
    elif action == 'delete':
        return delete_fact(user_id, role, body)
    else:
        return cors_response(400, {'error': f'Invalid action: {action}'})
