import json
import boto3
import uuid
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
prayer_table = dynamodb.Table('prayer-requests')
lambda_client = boto3.client('lambda')

# Toggle moderation: set to 'true' to require approval, 'false' for auto-approve
REQUIRE_MODERATION = os.environ.get('REQUIRE_MODERATION', 'false').lower() == 'true'

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        if event.get('httpMethod') == 'GET':
            action = event.get('queryStringParameters', {}).get('action', 'list')
        else:
            body = json.loads(event.get('body', '{}'))
            action = body.get('action', 'list')
        
        if action == 'create':
            return create_prayer(event, headers)
        elif action == 'list':
            return list_prayers(event, headers)
        elif action == 'pray':
            return increment_prayer_count(event, headers)
        elif action == 'update':
            return update_prayer(event, headers)
        elif action == 'delete':
            return delete_prayer(event, headers)
        elif action == 'get_config':
            return get_config(headers)
        elif action == 'set_config':
            return set_config(event, headers)
        else:
            return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Invalid action'})}
    
    except Exception as e:
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': str(e)})}

def create_prayer(event, headers):
    body = json.loads(event['body'])
    
    prayer_item = {
        'request_id': str(uuid.uuid4()),
        'title': body['title'],
        'description': body['description'],
        'category': body.get('category', 'personal'),
        'state': body.get('state', ''),
        'submitted_by': body['submitted_by'],
        'submitted_by_name': body.get('submitted_by_name', 'Anonymous'),
        'status': 'pending' if REQUIRE_MODERATION else 'active',
        'privacy': body.get('privacy', 'public'),
        'prayer_count': 0,
        'created_at': datetime.utcnow().isoformat()
    }
    
    prayer_table.put_item(Item=prayer_item)
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Prayer request created', 'request_id': prayer_item['request_id']})}

def list_prayers(event, headers):
    params = event.get('queryStringParameters', {})
    response = prayer_table.scan()
    prayers = response.get('Items', [])
    
    if params.get('category'):
        prayers = [p for p in prayers if p.get('category') == params['category']]
    if params.get('state'):
        prayers = [p for p in prayers if p.get('state') == params['state']]
    if params.get('status'):
        prayers = [p for p in prayers if p.get('status') == params['status']]
    
    privacy = params.get('privacy', 'public')
    prayers = [p for p in prayers if p.get('privacy') == privacy]
    
    for prayer in prayers:
        if 'prayer_count' in prayer:
            prayer['prayer_count'] = int(prayer['prayer_count'])
    
    prayers.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'prayers': prayers})}

def increment_prayer_count(event, headers):
    body = json.loads(event['body'])
    request_id = body['request_id']
    
    prayer_table.update_item(
        Key={'request_id': request_id},
        UpdateExpression='SET prayer_count = if_not_exists(prayer_count, :zero) + :inc',
        ExpressionAttributeValues={':inc': 1, ':zero': 0}
    )
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Prayer count incremented'})}

def update_prayer(event, headers):
    body = json.loads(event['body'])
    request_id = body['request_id']
    
    update_expr = 'SET '
    expr_values = {}
    expr_names = {}
    updates = []
    
    status_changed_to_answered = False
    if 'status' in body:
        updates.append('#status = :status')
        expr_values[':status'] = body['status']
        expr_names['#status'] = 'status'
        if body['status'] == 'answered':
            status_changed_to_answered = True
    if 'testimony' in body:
        updates.append('testimony = :testimony')
        expr_values[':testimony'] = body['testimony']
    
    update_expr += ', '.join(updates)
    
    prayer_table.update_item(
        Key={'request_id': request_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_values,
        ExpressionAttributeNames=expr_names if expr_names else None
    )
    
    # Send notification if prayer was marked as answered
    if status_changed_to_answered:
        try:
            prayer_response = prayer_table.get_item(Key={'request_id': request_id})
            prayer = prayer_response.get('Item', {})
            if prayer.get('submitted_by'):
                lambda_client.invoke(
                    FunctionName='notifications_api',
                    InvocationType='Event',
                    Payload=json.dumps({
                        'body': json.dumps({
                            'action': 'send_notification',
                            'type': 'prayer_update',
                            'recipient_email': prayer['submitted_by'],
                            'subject': 'Prayer Request Answered!',
                            'message': f'Great news! Your prayer request "{prayer.get("title", "")}" has been marked as answered.',
                            'link': 'https://christianconservativestoday.com/prayer-wall.html'
                        })
                    })
                )
        except Exception as e:
            print(f'Notification error: {e}')
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Prayer request updated'})}

def delete_prayer(event, headers):
    params = event.get('queryStringParameters', {})
    request_id = params.get('request_id')
    
    prayer_table.delete_item(Key={'request_id': request_id})
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Prayer request deleted'})}

def get_config(headers):
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'require_moderation': REQUIRE_MODERATION})}

def set_config(event, headers):
    body = json.loads(event['body'])
    require_moderation = body.get('require_moderation', False)
    
    lambda_client = boto3.client('lambda')
    lambda_client.update_function_configuration(
        FunctionName='prayer_api',
        Environment={'Variables': {'REQUIRE_MODERATION': 'true' if require_moderation else 'false'}}
    )
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Configuration updated', 'require_moderation': require_moderation})}
