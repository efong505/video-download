import json
import boto3
import jwt
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
users_table = dynamodb.Table('users')
metadata_table = dynamodb.Table('video-metadata')

JWT_SECRET = 'your-jwt-secret-key'

def lambda_handler(event, context):
    try:
        method = event.get('httpMethod', 'GET')
        
        # Handle OPTIONS request first, before token verification
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': ''
            }
        
        # Verify admin token for non-OPTIONS requests
        auth_result = verify_admin_token(event)
        if auth_result['statusCode'] != 200:
            return auth_result
        
        query_params = event.get('queryStringParameters') or {}
        action = query_params.get('action')
        if method == 'GET' and action == 'users':
            return get_all_users(event)
        elif method == 'GET' and action == 'videos':
            return get_all_videos(event)
        elif method == 'PUT' and action == 'user_role':
            return update_user_role(event)
        elif method == 'DELETE' and action == 'user':
            return delete_user(event)
        elif method == 'DELETE' and action == 'video':
            return delete_video(event)
        else:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Endpoint not found'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def verify_admin_token(event):
    auth_header = event.get('headers', {}).get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return {
            'statusCode': 401,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'Missing token'})
        }
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        if payload.get('role') != 'admin':
            return {
                'statusCode': 403,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Admin access required'})
            }
        return {'statusCode': 200, 'user': payload}
    except jwt.InvalidTokenError:
        return {
            'statusCode': 401,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'Invalid token'})
        }

def get_all_users(event):
    response = users_table.scan()
    users = []
    
    for item in response['Items']:
        users.append({
            'user_id': item['user_id'],
            'email': item['email'],
            'role': item['role'],
            'created_at': item['created_at'],
            'active': item.get('active', True)
        })
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'users': users,
            'count': len(users)
        })
    }

def get_all_videos(event):
    # Get videos from S3
    s3_response = s3_client.list_objects_v2(
        Bucket='my-video-downloads-bucket',
        Prefix='videos/'
    )
    
    videos = []
    if 'Contents' in s3_response:
        for obj in s3_response['Contents']:
            if obj['Key'] != 'videos/':
                filename = obj['Key'].replace('videos/', '')
                
                # Get metadata if available
                try:
                    metadata_response = metadata_table.get_item(
                        Key={'video_id': filename}
                    )
                    metadata = metadata_response.get('Item', {})
                except:
                    metadata = {}
                
                videos.append({
                    'filename': filename,
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat(),
                    'tags': metadata.get('tags', []),
                    'title': metadata.get('title', filename.replace('.mp4', ''))
                })
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'videos': videos,
            'count': len(videos)
        })
    }

def update_user_role(event):
    body = json.loads(event['body'])
    user_id = body['user_id']
    new_role = body['role']
    
    users_table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET #role = :role, updated_at = :updated',
        ExpressionAttributeNames={'#role': 'role'},
        ExpressionAttributeValues={
            ':role': new_role,
            ':updated': datetime.utcnow().isoformat()
        }
    )
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'User role updated',
            'user_id': user_id,
            'role': new_role
        })
    }

def delete_user(event):
    query_params = event.get('queryStringParameters') or {}
    user_id = query_params.get('user_id')
    
    if not user_id:
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'user_id required'})
        }
    
    users_table.delete_item(Key={'user_id': user_id})
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'User deleted',
            'user_id': user_id
        })
    }

def delete_video(event):
    query_params = event.get('queryStringParameters') or {}
    filename = query_params.get('filename')
    
    if not filename:
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'filename required'})
        }
    
    # Delete from S3
    s3_client.delete_object(
        Bucket='my-video-downloads-bucket',
        Key=f'videos/{filename}'
    )
    
    # Delete thumbnails
    try:
        base_name = filename.rsplit('.', 1)[0]
        for i in range(1, 4):
            s3_client.delete_object(
                Bucket='my-video-downloads-bucket',
                Key=f'thumbnails/{base_name}_thumb_{i}.jpg'
            )
    except:
        pass
    
    # Delete metadata
    try:
        metadata_table.delete_item(Key={'video_id': filename})
    except:
        pass
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'Video deleted',
            'filename': filename
        })
    }

def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Max-Age': '86400'
    }