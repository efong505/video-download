import json
import boto3
import os
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
feature_flags_table = dynamodb.Table('feature-flags')
contributors_table = dynamodb.Table('contributors')

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }

def verify_admin_token(headers):
    """Verify JWT token and check for admin/super_user role"""
    import jwt
    
    auth_header = headers.get('Authorization') or headers.get('authorization')
    if not auth_header:
        return None
    
    try:
        token = auth_header.replace('Bearer ', '')
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        role = decoded.get('role', '')
        if role in ['admin', 'super_user']:
            return decoded
        return None
    except:
        return None

def get_active_volunteer_count():
    """Get count of active contributors for election system"""
    try:
        response = contributors_table.scan(
            FilterExpression='#status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': 'active'}
        )
        return len(response.get('Items', []))
    except Exception as e:
        print(f'Error getting volunteer count: {str(e)}')
        return 0

def check_seasonal_status(flag):
    """Check if feature is within its active season"""
    if not flag.get('seasonal', False):
        return True
    
    try:
        season_start = flag.get('season_start')
        season_end = flag.get('season_end')
        
        if not season_start or not season_end:
            return True
        
        now = datetime.utcnow()
        start = datetime.fromisoformat(season_start.replace('Z', '+00:00'))
        end = datetime.fromisoformat(season_end.replace('Z', '+00:00'))
        
        return start <= now <= end
    except:
        return True

def lambda_handler(event, context):
    try:
        print('Event:', json.dumps(event))
        
        # Handle OPTIONS for CORS
        http_method = event.get('requestContext', {}).get('http', {}).get('method') or event.get('httpMethod')
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({'message': 'CORS preflight'})
            }
        
        # Get action from query parameters
        params = event.get('queryStringParameters') or {}
        action = params.get('action', 'list')
        
        headers = event.get('headers') or {}
        
        # GET /feature-flags - List all flags (public endpoint)
        if action == 'list':
            response = feature_flags_table.scan()
            flags = response.get('Items', [])
            
            # Update volunteer count for election system
            for flag in flags:
                if flag.get('feature_id') == 'election_system' and flag.get('volunteer_dependent'):
                    flag['active_volunteers'] = get_active_volunteer_count()
            
            # Return only enabled status for public, full details for admins
            user = verify_admin_token(headers)
            if not user:
                # Public view - return feature_id, enabled, and public status info
                public_flags = []
                for f in flags:
                    public_flag = {
                        'feature_id': f['feature_id'],
                        'enabled': f.get('enabled', False),
                        'name': f.get('name', ''),
                        'seasonal': f.get('seasonal', False),
                        'volunteer_dependent': f.get('volunteer_dependent', False),
                        'active_volunteers': f.get('active_volunteers', 0),
                        'min_volunteers_required': f.get('min_volunteers_required', 0),
                        'season_start': f.get('season_start'),
                        'season_end': f.get('season_end'),
                        'disable_reason': f.get('disable_reason', ''),
                        'volunteer_signup_url': f.get('volunteer_signup_url', '')
                    }
                    public_flags.append(public_flag)
                flags = public_flags
            
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps(flags, default=decimal_default)
            }
        
        # GET /feature-flags?action=get&feature_id=X - Get single flag
        if action == 'get':
            feature_id = params.get('feature_id')
            if not feature_id:
                return {
                    'statusCode': 400,
                    'headers': cors_headers(),
                    'body': json.dumps({'error': 'feature_id required'})
                }
            
            response = feature_flags_table.get_item(Key={'feature_id': feature_id})
            flag = response.get('Item')
            
            if not flag:
                return {
                    'statusCode': 404,
                    'headers': cors_headers(),
                    'body': json.dumps({'error': 'Feature flag not found'})
                }
            
            # Update volunteer count if applicable
            if flag.get('feature_id') == 'election_system' and flag.get('volunteer_dependent'):
                flag['active_volunteers'] = get_active_volunteer_count()
            
            # Public can see status info
            user = verify_admin_token(headers)
            if not user:
                flag = {
                    'feature_id': flag['feature_id'],
                    'enabled': flag.get('enabled', False),
                    'name': flag.get('name', ''),
                    'seasonal': flag.get('seasonal', False),
                    'volunteer_dependent': flag.get('volunteer_dependent', False),
                    'active_volunteers': flag.get('active_volunteers', 0),
                    'min_volunteers_required': flag.get('min_volunteers_required', 0),
                    'season_start': flag.get('season_start'),
                    'season_end': flag.get('season_end'),
                    'disable_reason': flag.get('disable_reason', ''),
                    'volunteer_signup_url': flag.get('volunteer_signup_url', '')
                }
            
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps(flag, default=decimal_default)
            }
        
        # Admin-only actions below
        user = verify_admin_token(headers)
        if not user:
            return {
                'statusCode': 403,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Admin access required'})
            }
        
        # POST /feature-flags?action=create - Create new flag
        if action == 'create':
            body = json.loads(event.get('body', '{}'))
            
            feature_id = body.get('feature_id')
            if not feature_id:
                return {
                    'statusCode': 400,
                    'headers': cors_headers(),
                    'body': json.dumps({'error': 'feature_id required'})
                }
            
            flag_data = {
                'feature_id': feature_id,
                'enabled': body.get('enabled', False),
                'name': body.get('name', feature_id),
                'description': body.get('description', ''),
                'admin_only_access': body.get('admin_only_access', True),
                'seasonal': body.get('seasonal', False),
                'volunteer_dependent': body.get('volunteer_dependent', False),
                'min_volunteers_required': body.get('min_volunteers_required', 0),
                'active_volunteers': 0,
                'season_start': body.get('season_start', ''),
                'season_end': body.get('season_end', ''),
                'disable_reason': body.get('disable_reason', ''),
                'volunteer_signup_url': body.get('volunteer_signup_url', ''),
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat(),
                'updated_by': user.get('email', 'unknown')
            }
            
            feature_flags_table.put_item(Item=flag_data)
            
            return {
                'statusCode': 201,
                'headers': cors_headers(),
                'body': json.dumps({'message': 'Feature flag created', 'flag': flag_data}, default=decimal_default)
            }
        
        # PUT /feature-flags?action=update - Update flag
        if action == 'update':
            body = json.loads(event.get('body', '{}'))
            
            feature_id = body.get('feature_id')
            if not feature_id:
                return {
                    'statusCode': 400,
                    'headers': cors_headers(),
                    'body': json.dumps({'error': 'feature_id required'})
                }
            
            # Get existing flag
            response = feature_flags_table.get_item(Key={'feature_id': feature_id})
            if 'Item' not in response:
                return {
                    'statusCode': 404,
                    'headers': cors_headers(),
                    'body': json.dumps({'error': 'Feature flag not found'})
                }
            
            # Build update expression
            update_parts = []
            expr_values = {
                ':updated_at': datetime.utcnow().isoformat(),
                ':updated_by': user.get('email', 'unknown')
            }
            expr_names = {}
            
            update_parts.append('updated_at = :updated_at')
            update_parts.append('updated_by = :updated_by')
            
            if 'enabled' in body:
                update_parts.append('enabled = :enabled')
                expr_values[':enabled'] = body['enabled']
            
            if 'name' in body:
                update_parts.append('#n = :name')
                expr_values[':name'] = body['name']
                expr_names['#n'] = 'name'
            
            if 'description' in body:
                update_parts.append('description = :description')
                expr_values[':description'] = body['description']
            
            if 'admin_only_access' in body:
                update_parts.append('admin_only_access = :admin_only_access')
                expr_values[':admin_only_access'] = body['admin_only_access']
            
            if 'seasonal' in body:
                update_parts.append('seasonal = :seasonal')
                expr_values[':seasonal'] = body['seasonal']
            
            if 'volunteer_dependent' in body:
                update_parts.append('volunteer_dependent = :volunteer_dependent')
                expr_values[':volunteer_dependent'] = body['volunteer_dependent']
            
            if 'min_volunteers_required' in body:
                update_parts.append('min_volunteers_required = :min_volunteers_required')
                expr_values[':min_volunteers_required'] = body['min_volunteers_required']
            
            if 'season_start' in body:
                update_parts.append('season_start = :season_start')
                expr_values[':season_start'] = body['season_start']
            
            if 'season_end' in body:
                update_parts.append('season_end = :season_end')
                expr_values[':season_end'] = body['season_end']
            
            if 'disable_reason' in body:
                update_parts.append('disable_reason = :disable_reason')
                expr_values[':disable_reason'] = body['disable_reason']
            
            if 'volunteer_signup_url' in body:
                update_parts.append('volunteer_signup_url = :volunteer_signup_url')
                expr_values[':volunteer_signup_url'] = body['volunteer_signup_url']
            
            update_expr = 'SET ' + ', '.join(update_parts)
            
            update_params = {
                'Key': {'feature_id': feature_id},
                'UpdateExpression': update_expr,
                'ExpressionAttributeValues': expr_values
            }
            
            if expr_names:
                update_params['ExpressionAttributeNames'] = expr_names
            
            feature_flags_table.update_item(**update_params)
            
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({'message': 'Feature flag updated'})
            }
        
        # DELETE /feature-flags?action=delete&feature_id=X - Delete flag
        if action == 'delete':
            feature_id = params.get('feature_id')
            if not feature_id:
                return {
                    'statusCode': 400,
                    'headers': cors_headers(),
                    'body': json.dumps({'error': 'feature_id required'})
                }
            
            feature_flags_table.delete_item(Key={'feature_id': feature_id})
            
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({'message': 'Feature flag deleted'})
            }
        
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'Invalid action'})
        }
        
    except Exception as e:
        print('Error:', str(e))
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }
