import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal
import base64

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name='us-east-1')
contributors_table = dynamodb.Table('contributors')
candidates_table = dynamodb.Table('candidates')
election_events_table = dynamodb.Table('election-events')
users_table = dynamodb.Table('users')
races_table = dynamodb.Table('races')
summaries_table = dynamodb.Table('state-summaries')
pending_changes_table = dynamodb.Table('pending-changes')

def lambda_handler(event, context):
    headers = cors_headers()
    
    try:
        method = event.get('httpMethod', 'GET')
        if method == 'OPTIONS':
            return {'statusCode': 200, 'headers': headers, 'body': ''}
        
        query_params = event.get('queryStringParameters') or {}
        action = query_params.get('action', 'list')
        resource = query_params.get('resource', 'contributors')
        
        if resource == 'users':
            return list_users(event, headers)
        elif resource == 'pending-changes':
            if method == 'POST': return submit_change(event, headers)
            elif method == 'PUT': return review_change(event, headers)
            else: return list_pending_changes(event, headers)
        
        if resource == 'races':
            if method == 'POST': return create_race(event, headers)
            elif method == 'PUT': return update_race(event, headers)
            elif method == 'DELETE': return delete_race(event, headers)
            elif action == 'get': return get_race(event, headers)
            else: return list_races(event, headers)
        elif resource == 'contributors':
            if method == 'POST': return create_contributor(event, headers)
            elif method == 'PUT': return update_contributor(event, headers)
            elif method == 'DELETE': return delete_contributor(event, headers)
            elif action == 'get': return get_contributor(event, headers)
            else: return list_contributors(event, headers)
        elif resource == 'candidates':
            if method == 'POST': return create_candidate(event, headers)
            elif method == 'PUT': return update_candidate(event, headers)
            elif method == 'DELETE': return delete_candidate(event, headers)
            elif action == 'get': return get_candidate(event, headers)
            else: return list_candidates(event, headers)
        elif resource == 'events':
            if method == 'POST': return create_event(event, headers)
            elif method == 'PUT': return update_event(event, headers)
            elif method == 'DELETE': return delete_event(event, headers)
            else: return list_events(event, headers)
        elif resource == 'summaries':
            if method == 'POST': return create_summary(event, headers)
            elif method == 'PUT': return update_summary(event, headers)
            elif method == 'DELETE': return delete_summary(event, headers)
            elif action == 'get': return get_summary(event, headers)
            else: return list_summaries(event, headers)
        else:
            return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Resource not found'})}
            
    except Exception as e:
        import traceback
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': str(e), 'trace': traceback.format_exc()})}

def verify_token(event):
    try:
        headers = event.get('headers', {})
        auth_header = headers.get('Authorization') or headers.get('authorization', '')
        if not auth_header.startswith('Bearer '):
            print(f"No Bearer token found")
            return None
        token = auth_header.split(' ')[1]
        parts = token.split('.')
        if len(parts) != 3:
            print(f"Invalid token format: {len(parts)} parts")
            return None
        payload_data = parts[1]
        payload_data += '=' * (4 - len(payload_data) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_data))
        print(f"Decoded payload: {payload}")
        exp = payload.get('exp', 0)
        if exp < datetime.utcnow().timestamp():
            print(f"Token expired: {exp} < {datetime.utcnow().timestamp()}")
            return None
        print(f"Token valid. Role: {payload.get('role')}")
        return payload
    except Exception as e:
        print(f"Token verification error: {e}")
        import traceback
        print(traceback.format_exc())
        return None

def verify_admin_token(event):
    user_info = verify_token(event)
    if user_info and user_info.get('role') in ['admin', 'super_user']: return user_info
    return None

def verify_editor_token(event):
    user_info = verify_token(event)
    if user_info and user_info.get('role') in ['admin', 'super_user', 'editor']: return user_info
    return None

def is_editor_for_state(user_email, state):
    response = contributors_table.scan(
        FilterExpression='user_email = :email AND #state = :state AND #status = :status',
        ExpressionAttributeNames={'#state': 'state', '#status': 'status'},
        ExpressionAttributeValues={':email': user_email, ':state': state, ':status': 'active'}
    )
    return len(response.get('Items', [])) > 0

def has_bypass_approval(user_email):
    response = contributors_table.scan(
        FilterExpression='user_email = :email AND #status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':email': user_email, ':status': 'active'}
    )
    if response.get('Items'):
        return response['Items'][0].get('bypass_approval', False)
    return False

def create_contributor(event, headers):
    user_info = verify_admin_token(event)
    if not user_info:
        print(f"Admin verification failed. Headers: {event.get('headers', {})}")
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required. Your session may have expired - please log out and log back in.'})}
    
    print(f"Creating contributor. User: {user_info.get('email')}, Role: {user_info.get('role')}")
    body = json.loads(event['body'])
    contributor_id = str(uuid.uuid4())
    user_email = body['user_email']
    
    contributor = {
        'contributor_id': contributor_id,
        'user_email': user_email,
        'first_name': body.get('first_name', ''),
        'last_name': body.get('last_name', ''),
        'phone_number': body.get('phone_number', ''),
        'state': body['state'],
        'status': body.get('status', 'active'),
        'bio': body.get('bio', ''),
        'verified': body.get('verified', False),
        'bypass_approval': body.get('bypass_approval', False),
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    contributors_table.put_item(Item=contributor)
    
    # Auto-assign editor role
    try:
        response = users_table.scan(
            FilterExpression='email = :email',
            ExpressionAttributeValues={':email': user_email}
        )
        if response['Items']:
            user_id = response['Items'][0]['user_id']
            users_table.update_item(
                Key={'user_id': user_id},
                UpdateExpression='SET #role = :role',
                ExpressionAttributeNames={'#role': 'role'},
                ExpressionAttributeValues={':role': 'editor'}
            )
    except: pass
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Contributor created and editor role assigned', 'contributor_id': contributor_id})}

def list_contributors(event, headers):
    params = event.get('queryStringParameters') or {}
    state = params.get('state')
    
    if state:
        response = contributors_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': state})
    else:
        response = contributors_table.scan()
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps(convert_decimals(response.get('Items', [])))}

def create_candidate(event, headers):
    user_info = verify_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Authentication required'})}
    
    body = json.loads(event['body'])
    
    # Editors submit for approval (unless bypass_approval is enabled), admins create directly
    if user_info.get('role') == 'editor':
        if not is_editor_for_state(user_info['email'], body['state']):
            return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Not authorized for this state'})}
        if not has_bypass_approval(user_info['email']):
            return submit_change(event, headers, change_type='create_candidate', data=body)
    
    if user_info.get('role') not in ['admin', 'super_user']:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required'})}
    
    candidate_id = str(uuid.uuid4())
    candidate = {
        'candidate_id': candidate_id,
        'name': body['name'],
        'state': body['state'],
        'office': body['office'],
        'party': body.get('party', 'Republican'),
        'bio': body.get('bio', ''),
        'website': body.get('website', ''),
        'photo_url': body.get('photo_url', ''),
        'status': body.get('status', 'active'),
        'race_id': body.get('race_id', ''),
        'positions': body.get('positions', {}),
        'endorsements': body.get('endorsements', []),
        'voting_record_url': body.get('voting_record_url', ''),
        'faith_statement': body.get('faith_statement', ''),
        'created_by': user_info['email'],
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    candidates_table.put_item(Item=candidate)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Candidate created', 'candidate_id': candidate_id})}

def list_candidates(event, headers):
    params = event.get('queryStringParameters') or {}
    state = params.get('state')
    
    if state:
        response = candidates_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': state})
    else:
        response = candidates_table.scan()
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps(convert_decimals(response.get('Items', [])))}

def create_event(event, headers):
    user_info = verify_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Authentication required'})}
    
    body = json.loads(event['body'])
    event_id = str(uuid.uuid4())
    
    election_event = {
        'event_id': event_id,
        'title': body['title'],
        'state': body.get('state', 'National'),
        'event_date': body['event_date'],
        'event_type': body.get('event_type', 'primary'),
        'description': body.get('description', ''),
        'created_by': user_info['email'],
        'created_at': datetime.utcnow().isoformat()
    }
    
    election_events_table.put_item(Item=election_event)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Event created', 'event_id': event_id})}

def list_events(event, headers):
    params = event.get('queryStringParameters') or {}
    state = params.get('state')
    
    if state:
        response = election_events_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': state})
    else:
        response = election_events_table.scan()
    
    items = response.get('Items', [])
    items.sort(key=lambda x: x.get('event_date', ''))
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps(convert_decimals(items))}

def get_contributor(event, headers):
    params = event.get('queryStringParameters') or {}
    contributor_id = params.get('contributor_id')
    if not contributor_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'contributor_id required'})}
    response = contributors_table.get_item(Key={'contributor_id': contributor_id})
    if 'Item' not in response:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Not found'})}
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps(convert_decimals(response['Item']))}

def update_contributor(event, headers):
    user_info = verify_admin_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required'})}
    body = json.loads(event['body'])
    contributor_id = body.get('contributor_id')
    if not contributor_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'contributor_id required'})}
    update_expr = 'SET updated_at = :updated'
    expr_values = {':updated': datetime.utcnow().isoformat()}
    for field in ['status', 'bio', 'verified', 'first_name', 'last_name', 'phone_number', 'bypass_approval']:
        if field in body:
            update_expr += f', {field} = :{field}'
            expr_values[f':{field}'] = body[field]
    contributors_table.update_item(Key={'contributor_id': contributor_id}, UpdateExpression=update_expr, ExpressionAttributeValues=expr_values)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Updated'})}

def delete_contributor(event, headers):
    user_info = verify_admin_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required'})}
    params = event.get('queryStringParameters') or {}
    contributor_id = params.get('contributor_id')
    if not contributor_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'contributor_id required'})}
    contributors_table.delete_item(Key={'contributor_id': contributor_id})
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Deleted'})}

def get_candidate(event, headers):
    params = event.get('queryStringParameters') or {}
    candidate_id = params.get('candidate_id')
    if not candidate_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'candidate_id required'})}
    response = candidates_table.get_item(Key={'candidate_id': candidate_id})
    if 'Item' not in response:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Not found'})}
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps(convert_decimals(response['Item']))}

def update_candidate(event, headers):
    user_info = verify_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Authentication required'})}
    body = json.loads(event['body'])
    candidate_id = body.get('candidate_id')
    if not candidate_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'candidate_id required'})}
    
    # Get candidate to check state
    candidate = candidates_table.get_item(Key={'candidate_id': candidate_id}).get('Item')
    if not candidate:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Candidate not found'})}
    
    # Editors submit for approval, admins update directly
    if user_info.get('role') == 'editor':
        if not is_editor_for_state(user_info['email'], candidate['state']):
            return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Not authorized for this state'})}
        return submit_change(event, headers, change_type='update_candidate', data=body)
    
    if user_info.get('role') not in ['admin', 'super_user']:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required'})}
    
    update_expr = 'SET updated_at = :updated'
    expr_values = {':updated': datetime.utcnow().isoformat()}
    expr_names = {}
    for field in ['name', 'bio', 'website', 'photo_url', 'status', 'office', 'party', 'state', 'race_id', 'positions', 'endorsements', 'voting_record_url', 'faith_statement']:
        if field in body:
            value = body[field]
            if value == '' and field == 'race_id':
                value = None
            expr_names[f'#{field}'] = field
            update_expr += f', #{field} = :{field}'
            expr_values[f':{field}'] = value
    candidates_table.update_item(Key={'candidate_id': candidate_id}, UpdateExpression=update_expr, ExpressionAttributeNames=expr_names, ExpressionAttributeValues=expr_values)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Updated'})}

def delete_candidate(event, headers):
    user_info = verify_admin_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required'})}
    params = event.get('queryStringParameters') or {}
    candidate_id = params.get('candidate_id')
    if not candidate_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'candidate_id required'})}
    candidates_table.delete_item(Key={'candidate_id': candidate_id})
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Deleted'})}

def update_event(event, headers):
    user_info = verify_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Authentication required'})}
    body = json.loads(event['body'])
    event_id = body.get('event_id')
    if not event_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'event_id required'})}
    update_expr = 'SET updated_at = :updated'
    expr_values = {':updated': datetime.utcnow().isoformat()}
    for field in ['title', 'event_date', 'event_type', 'description']:
        if field in body:
            update_expr += f', {field} = :{field}'
            expr_values[f':{field}'] = body[field]
    election_events_table.update_item(Key={'event_id': event_id}, UpdateExpression=update_expr, ExpressionAttributeValues=expr_values)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Updated'})}

def delete_event(event, headers):
    user_info = verify_admin_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required'})}
    params = event.get('queryStringParameters') or {}
    event_id = params.get('event_id')
    if not event_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'event_id required'})}
    election_events_table.delete_item(Key={'event_id': event_id})
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Deleted'})}

def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj

def create_race(event, headers):
    user_info = verify_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Authentication required'})}
    
    body = json.loads(event['body'])
    
    # Editors submit for approval, admins create directly
    if user_info.get('role') == 'editor':
        if not is_editor_for_state(user_info['email'], body['state']):
            return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Not authorized for this state'})}
        return submit_change(event, headers, change_type='create_race', data=body)
    
    if user_info.get('role') not in ['admin', 'super_user']:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required'})}
    
    race_id = str(uuid.uuid4())
    race = {
        'race_id': race_id,
        'state': body['state'],
        'office': body['office'],
        'election_date': body['election_date'],
        'race_type': body.get('race_type', 'general'),
        'description': body.get('description', ''),
        'created_by': user_info['email'],
        'created_at': datetime.utcnow().isoformat()
    }
    
    races_table.put_item(Item=race)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Race created', 'race_id': race_id})}

def list_races(event, headers):
    params = event.get('queryStringParameters') or {}
    state = params.get('state')
    
    if state:
        response = races_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': state})
    else:
        response = races_table.scan()
    
    items = response.get('Items', [])
    items.sort(key=lambda x: x.get('election_date', ''))
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps(convert_decimals(items))}

def get_race(event, headers):
    params = event.get('queryStringParameters') or {}
    race_id = params.get('race_id')
    if not race_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'race_id required'})}
    response = races_table.get_item(Key={'race_id': race_id})
    if 'Item' not in response:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Not found'})}
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps(convert_decimals(response['Item']))}

def update_race(event, headers):
    user_info = verify_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Authentication required'})}
    body = json.loads(event['body'])
    race_id = body.get('race_id')
    if not race_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'race_id required'})}
    
    # Get race to check state
    race = races_table.get_item(Key={'race_id': race_id}).get('Item')
    if not race:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Race not found'})}
    
    # Editors submit for approval, admins update directly
    if user_info.get('role') == 'editor':
        if not is_editor_for_state(user_info['email'], race['state']):
            return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Not authorized for this state'})}
        return submit_change(event, headers, change_type='update_race', data=body)
    
    if user_info.get('role') not in ['admin', 'super_user']:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required'})}
    
    update_expr = 'SET updated_at = :updated'
    expr_values = {':updated': datetime.utcnow().isoformat()}
    for field in ['office', 'election_date', 'race_type', 'description']:
        if field in body:
            update_expr += f', {field} = :{field}'
            expr_values[f':{field}'] = body[field]
    races_table.update_item(Key={'race_id': race_id}, UpdateExpression=update_expr, ExpressionAttributeValues=expr_values)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Updated'})}

def delete_race(event, headers):
    user_info = verify_admin_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required'})}
    params = event.get('queryStringParameters') or {}
    race_id = params.get('race_id')
    if not race_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'race_id required'})}
    races_table.delete_item(Key={'race_id': race_id})
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Deleted'})}

def create_summary(event, headers):
    user_info = verify_admin_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required'})}
    body = json.loads(event['body'])
    summary = {
        'state': body['state'],
        'title': body.get('title', f"{body['state']} Election Guide"),
        'content': body.get('content', ''),
        'election_year': body.get('election_year', '2026'),
        'last_updated': datetime.utcnow().isoformat(),
        'updated_by': user_info['email']
    }
    summaries_table.put_item(Item=summary)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Summary created'})}

def get_summary(event, headers):
    params = event.get('queryStringParameters') or {}
    state = params.get('state')
    if not state:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'state required'})}
    response = summaries_table.get_item(Key={'state': state})
    if 'Item' not in response:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Not found'})}
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps(convert_decimals(response['Item']))}

def list_summaries(event, headers):
    response = summaries_table.scan()
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps(convert_decimals(response.get('Items', [])))}

def update_summary(event, headers):
    user_info = verify_admin_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required'})}
    body = json.loads(event['body'])
    state = body.get('state')
    if not state:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'state required'})}
    update_expr = 'SET last_updated = :updated, updated_by = :by'
    expr_values = {':updated': datetime.utcnow().isoformat(), ':by': user_info['email']}
    for field in ['title', 'content', 'election_year']:
        if field in body:
            update_expr += f', {field} = :{field}'
            expr_values[f':{field}'] = body[field]
    summaries_table.update_item(Key={'state': state}, UpdateExpression=update_expr, ExpressionAttributeValues=expr_values)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Updated'})}

def delete_summary(event, headers):
    user_info = verify_admin_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required'})}
    params = event.get('queryStringParameters') or {}
    state = params.get('state')
    if not state:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'state required'})}
    summaries_table.delete_item(Key={'state': state})
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Deleted'})}

def submit_change(event, headers, change_type=None, data=None):
    user_info = verify_editor_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Editor access required'})}
    
    if not change_type:
        body = json.loads(event['body'])
        change_type = body['change_type']
        data = body['data']
    
    change_id = str(uuid.uuid4())
    change = {
        'change_id': change_id,
        'change_type': change_type,
        'data': data,
        'submitted_by': user_info['email'],
        'submitted_at': datetime.utcnow().isoformat(),
        'status': 'pending',
        'state': data.get('state', '')
    }
    
    pending_changes_table.put_item(Item=change)
    notify_admins_of_pending_change(change)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Change submitted for review', 'change_id': change_id})}

def list_pending_changes(event, headers):
    user_info = verify_admin_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required'})}
    
    response = pending_changes_table.scan(FilterExpression='#status = :status', ExpressionAttributeNames={'#status': 'status'}, ExpressionAttributeValues={':status': 'pending'})
    items = response.get('Items', [])
    items.sort(key=lambda x: x.get('submitted_at', ''), reverse=True)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps(convert_decimals(items))}

def review_change(event, headers):
    user_info = verify_admin_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Admin access required'})}
    
    body = json.loads(event['body'])
    change_id = body['change_id']
    action = body['action']  # 'approve' or 'deny'
    
    change = pending_changes_table.get_item(Key={'change_id': change_id}).get('Item')
    if not change:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Change not found'})}
    
    if action == 'approve':
        apply_change(change, user_info)
        status = 'approved'
    else:
        status = 'denied'
    
    pending_changes_table.update_item(
        Key={'change_id': change_id},
        UpdateExpression='SET #status = :status, reviewed_by = :by, reviewed_at = :time',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': status, ':by': user_info['email'], ':time': datetime.utcnow().isoformat()}
    )
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': f'Change {status}'})}

def apply_change(change, admin_info):
    change_type = change['change_type']
    data = change['data']
    
    if change_type == 'create_candidate':
        candidate_id = str(uuid.uuid4())
        data['candidate_id'] = candidate_id
        data['created_by'] = change['submitted_by']
        data['approved_by'] = admin_info['email']
        data['created_at'] = datetime.utcnow().isoformat()
        data['updated_at'] = datetime.utcnow().isoformat()
        candidates_table.put_item(Item=data)
    elif change_type == 'update_candidate':
        candidate_id = data['candidate_id']
        update_expr = 'SET updated_at = :updated, approved_by = :by'
        expr_values = {':updated': datetime.utcnow().isoformat(), ':by': admin_info['email']}
        expr_names = {}
        for field in ['name', 'bio', 'website', 'photo_url', 'status', 'office', 'party', 'state', 'race_id', 'positions', 'endorsements', 'voting_record_url', 'faith_statement']:
            if field in data:
                expr_names[f'#{field}'] = field
                update_expr += f', #{field} = :{field}'
                expr_values[f':{field}'] = data[field]
        candidates_table.update_item(Key={'candidate_id': candidate_id}, UpdateExpression=update_expr, ExpressionAttributeNames=expr_names, ExpressionAttributeValues=expr_values)
    elif change_type == 'create_race':
        race_id = str(uuid.uuid4())
        data['race_id'] = race_id
        data['created_by'] = change['submitted_by']
        data['approved_by'] = admin_info['email']
        data['created_at'] = datetime.utcnow().isoformat()
        races_table.put_item(Item=data)
    elif change_type == 'update_race':
        race_id = data['race_id']
        update_expr = 'SET updated_at = :updated, approved_by = :by'
        expr_values = {':updated': datetime.utcnow().isoformat(), ':by': admin_info['email']}
        for field in ['office', 'election_date', 'race_type', 'description']:
            if field in data:
                update_expr += f', {field} = :{field}'
                expr_values[f':{field}'] = data[field]
        races_table.update_item(Key={'race_id': race_id}, UpdateExpression=update_expr, ExpressionAttributeValues=expr_values)

def notify_admins_of_pending_change(change):
    try:
        response = users_table.scan(FilterExpression='#role IN (:admin, :super)', ExpressionAttributeNames={'#role': 'role'}, ExpressionAttributeValues={':admin': 'admin', ':super': 'super_user'})
        admins = response.get('Items', [])
        
        for admin in admins:
            ses.send_email(
                Source='contact@ekewaka.com',
                Destination={'ToAddresses': [admin['email']]},
                Message={
                    'Subject': {'Data': f'New {change["change_type"]} Pending Review'},
                    'Body': {'Text': {'Data': f'A new change has been submitted by {change["submitted_by"]} for state {change["state"]}. Please review in the admin dashboard.'}}
                }
            )
    except: pass

def list_users(event, headers):
    user_info = verify_editor_token(event)
    if not user_info:
        return {'statusCode': 403, 'headers': headers, 'body': json.dumps({'error': 'Editor/Admin access required'})}
    
    response = users_table.scan()
    users = response.get('Items', [])
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps(convert_decimals(users))}

def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
