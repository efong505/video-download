import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb')
events_table = dynamodb.Table('events')

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    # Handle both API Gateway v1 and v2 formats
    http_method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method')
    
    if http_method == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        # Check query parameters first (for both GET and POST)
        params = event.get('queryStringParameters') or {}
        action = params.get('action')
        
        # If no action in query params and it's POST, check body
        if not action and http_method == 'POST':
            body = json.loads(event.get('body', '{}'))
            action = body.get('action', 'list')
            print(f'POST body action: {action}, body keys: {list(body.keys())}')
        
        # Default to list if still no action
        if not action:
            action = 'list'
        
        print(f'Final action: {action}, method: {http_method}')
        
        if action == 'create':
            return create_event(event, headers)
        elif action == 'list':
            return list_events(event, headers)
        elif action == 'get':
            return get_event(event, headers)
        elif action == 'update':
            return update_event(event, headers)
        elif action == 'delete':
            return delete_event(event, headers)
        elif action == 'register':
            return register_attendee(event, headers)
        else:
            return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Invalid action'})}
    
    except Exception as e:
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': str(e)})}

def create_event(event, headers):
    body = json.loads(event['body'])
    
    event_item = {
        'event_id': str(uuid.uuid4()),
        'title': body['title'],
        'description': body['description'],
        'event_type': body.get('event_type', 'general'),
        'category': body.get('category', 'general'),
        'event_date': body['event_date'],
        'event_time': body.get('event_time', ''),
        'location': body.get('location', ''),
        'address': body.get('address', ''),
        'state': body.get('state', ''),
        'registration_required': body.get('registration_required', False),
        'registration_url': body.get('registration_url', ''),
        'max_attendees': body.get('max_attendees', 0),
        'attendee_count': 0,
        'contact_email': body.get('contact_email', ''),
        'contact_phone': body.get('contact_phone', ''),
        'image_url': body.get('image_url', ''),
        'status': 'active',
        'created_by': body.get('created_by', ''),
        'created_at': datetime.utcnow().isoformat()
    }
    
    events_table.put_item(Item=event_item)
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Event created', 'event_id': event_item['event_id']})}

def list_events(event, headers):
    params = event.get('queryStringParameters') or {}
    response = events_table.scan()
    events = response.get('Items', [])
    
    if params.get('category'):
        events = [e for e in events if e.get('category') == params['category']]
    if params.get('state'):
        events = [e for e in events if e.get('state') == params['state']]
    if params.get('status'):
        events = [e for e in events if e.get('status') == params['status']]
    
    events.sort(key=lambda x: x.get('event_date', ''))
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'events': events}, cls=DecimalEncoder)}

def get_event(event, headers):
    params = event.get('queryStringParameters') or {}
    event_id = params.get('event_id')
    
    if not event_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'event_id required'})}
    
    response = events_table.get_item(Key={'event_id': event_id})
    event_item = response.get('Item')
    
    if not event_item:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Event not found'})}
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'event': event_item}, cls=DecimalEncoder)}

def update_event(event, headers):
    body = json.loads(event['body'])
    event_id = body['event_id']
    
    update_expr = 'SET '
    expr_values = {}
    expr_names = {}
    updates = []
    
    fields = ['title', 'description', 'event_type', 'category', 'event_date', 'event_time', 'location', 
              'address', 'state', 'registration_required', 'registration_url', 'max_attendees',
              'contact_email', 'contact_phone', 'image_url', 'status', 'organizer']
    
    for field in fields:
        if field in body:
            updates.append(f'#{field} = :{field}')
            expr_values[f':{field}'] = body[field]
            expr_names[f'#{field}'] = field
    
    if not updates:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'No fields to update'})}
    
    update_expr += ', '.join(updates)
    
    events_table.update_item(
        Key={'event_id': event_id},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_names,
        ExpressionAttributeValues=expr_values
    )
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Event updated'})}

def delete_event(event, headers):
    params = event.get('queryStringParameters') or {}
    event_id = params.get('event_id')
    
    if not event_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'event_id required'})}
    
    events_table.delete_item(Key={'event_id': event_id})
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Event deleted'})}

def register_attendee(event, headers):
    body = json.loads(event['body'])
    event_id = body['event_id']
    
    events_table.update_item(
        Key={'event_id': event_id},
        UpdateExpression='SET attendee_count = if_not_exists(attendee_count, :zero) + :inc',
        ExpressionAttributeValues={':inc': 1, ':zero': 0}
    )
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Registration recorded'})}
