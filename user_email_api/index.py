import json
import boto3
import os
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
subscribers_table = dynamodb.Table('user-email-subscribers')
campaigns_table = dynamodb.Table('user-email-campaigns')
events_table = dynamodb.Table('user-email-events')
users_table = dynamodb.Table('users')

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

def extract_user_id(event):
    auth_header = event.get('headers', {}).get('Authorization') or event.get('headers', {}).get('authorization')
    if not auth_header:
        return None
    
    import jwt
    token = auth_header.replace('Bearer ', '')
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get('user_id')
    except:
        return None

def check_subscriber_quota(user_id):
    response = users_table.get_item(Key={'user_id': user_id})
    user = response.get('Item', {})
    
    limit = int(user.get('email_subscriber_limit', 0))
    count = int(user.get('email_subscribers_count', 0))
    
    if count >= limit:
        return False, f"Subscriber limit reached ({count}/{limit})"
    return True, "Quota available"

def check_send_quota(user_id, recipient_count):
    response = users_table.get_item(Key={'user_id': user_id})
    user = response.get('Item', {})
    
    limit = int(user.get('email_monthly_limit', 0))
    sent = int(user.get('email_sent_this_month', 0))
    
    if sent + recipient_count > limit:
        return False, f"Monthly email limit reached ({sent + recipient_count}/{limit})"
    return True, "Quota available"

def add_subscriber(user_id, data):
    allowed, message = check_subscriber_quota(user_id)
    if not allowed:
        return cors_response(403, {'error': message, 'upgrade_url': '/pricing'})
    
    subscriber_email = data.get('email')
    if not subscriber_email:
        return cors_response(400, {'error': 'Email required'})
    
    item = {
        'user_id': user_id,
        'subscriber_email': subscriber_email,
        'first_name': data.get('first_name', ''),
        'last_name': data.get('last_name', ''),
        'phone': data.get('phone', ''),
        'status': 'active',
        'subscribed_at': datetime.now().isoformat(),
        'source': data.get('source', 'manual'),
        'tags': data.get('tags', [])
    }
    
    subscribers_table.put_item(Item=item)
    
    users_table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET email_subscribers_count = email_subscribers_count + :inc',
        ExpressionAttributeValues={':inc': 1}
    )
    
    return cors_response(200, {'message': 'Subscriber added', 'subscriber': item})

def list_subscribers(user_id, params):
    status = params.get('status', 'active')
    
    response = subscribers_table.query(
        IndexName='status-index',
        KeyConditionExpression='user_id = :uid AND #status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':uid': user_id, ':status': status}
    )
    
    return cors_response(200, {'subscribers': response['Items']})

def delete_subscriber(user_id, data):
    subscriber_email = data.get('email')
    
    subscribers_table.delete_item(
        Key={'user_id': user_id, 'subscriber_email': subscriber_email}
    )
    
    users_table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET email_subscribers_count = email_subscribers_count - :dec',
        ExpressionAttributeValues={':dec': 1}
    )
    
    return cors_response(200, {'message': 'Subscriber deleted'})

def create_campaign(user_id, data):
    campaign_id = str(uuid.uuid4())
    
    item = {
        'user_id': user_id,
        'campaign_id': campaign_id,
        'title': data.get('title', ''),
        'subject': data.get('subject', ''),
        'content': data.get('content', ''),
        'template_id': data.get('template_id', ''),
        'status': 'draft',
        'created_at': datetime.now().isoformat(),
        'recipient_count': 0,
        'open_count': 0,
        'click_count': 0
    }
    
    campaigns_table.put_item(Item=item)
    
    return cors_response(200, {'message': 'Campaign created', 'campaign_id': campaign_id})

def list_campaigns(user_id):
    response = campaigns_table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': user_id}
    )
    
    return cors_response(200, {'campaigns': response['Items']})

def send_campaign(user_id, data):
    campaign_id = data.get('campaign_id')
    
    response = campaigns_table.get_item(Key={'user_id': user_id, 'campaign_id': campaign_id})
    campaign = response.get('Item')
    
    if not campaign:
        return cors_response(404, {'error': 'Campaign not found'})
    
    if campaign['user_id'] != user_id:
        return cors_response(403, {'error': 'Not your campaign'})
    
    subs_response = subscribers_table.query(
        IndexName='status-index',
        KeyConditionExpression='user_id = :uid AND #status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':uid': user_id, ':status': 'active'}
    )
    
    recipient_count = len(subs_response['Items'])
    
    allowed, message = check_send_quota(user_id, recipient_count)
    if not allowed:
        return cors_response(403, {'error': message, 'upgrade_url': '/pricing'})
    
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/371751795928/email-sending-queue'
    
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps({
            'user_id': user_id,
            'campaign_id': campaign_id,
            'recipients': [s['subscriber_email'] for s in subs_response['Items']]
        })
    )
    
    campaigns_table.update_item(
        Key={'user_id': user_id, 'campaign_id': campaign_id},
        UpdateExpression='SET #status = :status, recipient_count = :count',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'sending', ':count': recipient_count}
    )
    
    return cors_response(200, {'message': 'Campaign queued for sending', 'recipient_count': recipient_count})

def lambda_handler(event, context):
    if event.get('httpMethod') == 'OPTIONS':
        return cors_response(200, {})
    
    user_id = extract_user_id(event)
    if not user_id:
        return cors_response(401, {'error': 'Unauthorized'})
    
    params = event.get('queryStringParameters') or {}
    action = params.get('action')
    
    try:
        body = json.loads(event.get('body', '{}'))
    except:
        body = {}
    
    if action == 'add_subscriber':
        return add_subscriber(user_id, body)
    elif action == 'list_subscribers':
        return list_subscribers(user_id, params)
    elif action == 'delete_subscriber':
        return delete_subscriber(user_id, body)
    elif action == 'create_campaign':
        return create_campaign(user_id, body)
    elif action == 'list_campaigns':
        return list_campaigns(user_id)
    elif action == 'send_campaign':
        return send_campaign(user_id, body)
    else:
        return cors_response(400, {'error': 'Invalid action'})
