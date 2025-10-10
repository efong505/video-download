import json
import boto3
import hashlib
import jwt
import uuid
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('users')

JWT_SECRET = 'your-jwt-secret-key'  # In production, use AWS Secrets Manager

def lambda_handler(event, context):
    try:
        method = event.get('httpMethod', 'POST')
        query_params = event.get('queryStringParameters') or {}
        action = query_params.get('action')
        
        if method == 'POST' and action == 'register':
            return register_user(event)
        elif method == 'POST' and action == 'login':
            return login_user(event)
        elif method == 'GET' and action == 'verify':
            return verify_token(event)
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

def register_user(event):
    body = json.loads(event['body'])
    email = body['email'].lower()
    password = body['password']
    role = body.get('role', 'user')
    
    # Check if user exists
    try:
        response = users_table.query(
            IndexName='email-index',
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        if response['Items']:
            return {
                'statusCode': 400,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'User already exists'})
            }
    except Exception:
        pass
    
    # Create user
    user_id = str(uuid.uuid4())
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    users_table.put_item(
        Item={
            'user_id': user_id,
            'email': email,
            'password_hash': password_hash,
            'role': role,
            'created_at': datetime.utcnow().isoformat(),
            'active': True
        }
    )
    
    return {
        'statusCode': 201,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'User registered successfully',
            'user_id': user_id
        })
    }

def login_user(event):
    body = json.loads(event['body'])
    email = body['email'].lower()
    password = body['password']
    
    # Find user by email
    response = users_table.query(
        IndexName='email-index',
        KeyConditionExpression='email = :email',
        ExpressionAttributeValues={':email': email}
    )
    
    if not response['Items']:
        return {
            'statusCode': 401,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'Invalid credentials'})
        }
    
    user = response['Items'][0]
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if user['password_hash'] != password_hash or not user.get('active', True):
        return {
            'statusCode': 401,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'Invalid credentials'})
        }
    
    # Generate JWT token
    token = jwt.encode({
        'user_id': user['user_id'],
        'email': user['email'],
        'role': user['role'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, JWT_SECRET, algorithm='HS256')
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'Login successful',
            'token': token,
            'user': {
                'user_id': user['user_id'],
                'email': user['email'],
                'role': user['role']
            }
        })
    }

def verify_token(event):
    auth_header = event.get('headers', {}).get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return {
            'statusCode': 401,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'Missing or invalid token'})
        }
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({
                'valid': True,
                'user': {
                    'user_id': payload['user_id'],
                    'email': payload['email'],
                    'role': payload['role']
                }
            })
        }
    except jwt.ExpiredSignatureError:
        return {
            'statusCode': 401,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'Token expired'})
        }
    except jwt.InvalidTokenError:
        return {
            'statusCode': 401,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'Invalid token'})
        }

def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    }