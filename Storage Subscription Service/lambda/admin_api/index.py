import boto3
import json
import jwt
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('StorageUsers')
files_table = dynamodb.Table('StorageFiles')

JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
ADMIN_EMAILS = os.environ.get('ADMIN_EMAILS', 'admin@yourdomain.com').split(',')

def lambda_handler(event, context):
    # Handle OPTIONS for CORS preflight
    if event.get('httpMethod') == 'OPTIONS' or event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return response(200, {})
    
    try:
        token = event.get('headers', {}).get('Authorization', '').replace('Bearer ', '')
        if not token:
            return response(401, {'error': 'No token provided'})
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            email = payload['email']
            
            if email not in ADMIN_EMAILS:
                return response(403, {'error': 'Admin access required'})
        except:
            return response(401, {'error': 'Invalid token'})
        
        method = event['httpMethod']
        path = event.get('path', '')
        
        if 'users' in path:
            if method == 'GET':
                return get_all_users()
            elif method == 'DELETE':
                return delete_user(event)
            elif method == 'PUT':
                return update_user(event)
        elif 'stats' in path:
            return get_statistics()
        else:
            return response(400, {'error': 'Invalid endpoint'})
    except Exception as e:
        return response(500, {'error': str(e)})

def get_all_users():
    result = users_table.scan()
    users = []
    
    for item in result['Items']:
        users.append({
            'email': item['email'],
            'userId': item['userId'],
            'name': item['name'],
            'subscriptionTier': item['subscriptionTier'],
            'storageUsed': int(item['storageUsed']),
            'storageQuota': int(item['storageQuota']),
            'subscriptionStatus': item.get('subscriptionStatus', 'active'),
            'createdAt': item.get('createdAt', '')
        })
    
    return response(200, {'users': users, 'count': len(users)})

def delete_user(event):
    params = event.get('queryStringParameters') or {}
    email = params.get('email')
    
    if not email:
        return response(400, {'error': 'email parameter required'})
    
    # Delete user
    users_table.delete_item(Key={'email': email})
    
    return response(200, {'message': 'User deleted successfully'})

def update_user(event):
    body = json.loads(event['body'])
    email = body.get('email')
    updates = body.get('updates', {})
    
    if not email:
        return response(400, {'error': 'email required'})
    
    # Build update expression
    update_expr = 'SET '
    expr_values = {}
    
    for key, value in updates.items():
        if key in ['subscriptionTier', 'storageQuota', 'subscriptionStatus']:
            update_expr += f"{key} = :{key}, "
            if key == 'storageQuota':
                expr_values[f':{key}'] = Decimal(str(value))
            else:
                expr_values[f':{key}'] = value
    
    update_expr = update_expr.rstrip(', ')
    
    users_table.update_item(
        Key={'email': email},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_values
    )
    
    return response(200, {'message': 'User updated successfully'})

def get_statistics():
    users_result = users_table.scan()
    files_result = files_table.scan()
    
    total_users = len(users_result['Items'])
    total_storage_used = sum(int(u['storageUsed']) for u in users_result['Items'])
    total_files = len(files_result['Items'])
    
    tier_counts = {'free': 0, 'basic': 0, 'pro': 0, 'business': 0}
    for user in users_result['Items']:
        tier = user['subscriptionTier']
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
    
    return response(200, {
        'totalUsers': total_users,
        'totalStorageUsed': total_storage_used,
        'totalStorageUsedGB': round(total_storage_used / 1073741824, 2),
        'totalFiles': total_files,
        'tierDistribution': tier_counts,
        'revenue': (tier_counts['basic'] * 5) + (tier_counts['pro'] * 15) + (tier_counts['business'] * 50)
    })

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        'body': json.dumps(body)
    }
