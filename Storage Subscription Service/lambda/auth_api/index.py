import boto3
import json
import jwt
import hashlib
import os
from datetime import datetime, timedelta
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('StorageUsers')
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')

def lambda_handler(event, context):
    # Handle OPTIONS for CORS preflight
    if event.get('httpMethod') == 'OPTIONS' or event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return response(200, {})
    
    try:
        body = json.loads(event.get('body', '{}'))
        action = body.get('action')
        
        if action == 'register':
            return register_user(body)
        elif action == 'login':
            return login_user(body)
        elif action == 'verify':
            return verify_token(event)
        else:
            return response(400, {'error': 'Invalid action'})
    except Exception as e:
        return response(500, {'error': str(e)})

def register_user(body):
    email = body.get('email', '').lower().strip()
    password = body.get('password', '')
    name = body.get('name', '')
    
    if not email or not password or not name:
        return response(400, {'error': 'Email, password, and name are required'})
    
    # Check if user exists
    try:
        existing = users_table.get_item(Key={'email': email})
        if 'Item' in existing:
            return response(400, {'error': 'Email already registered'})
    except:
        pass
    
    # Create user
    user_id = hashlib.sha256(email.encode()).hexdigest()[:16]
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    users_table.put_item(Item={
        'email': email,
        'userId': user_id,
        'name': name,
        'passwordHash': password_hash,
        'subscriptionTier': 'free',
        'storageQuota': Decimal('1073741824'),  # 1GB
        'storageUsed': Decimal('0'),
        'subscriptionStatus': 'active',
        'createdAt': datetime.utcnow().isoformat(),
        'stripeCustomerId': '',
        'stripeSubscriptionId': ''
    })
    
    token = jwt.encode({
        'userId': user_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=30)
    }, JWT_SECRET, algorithm='HS256')
    
    return response(200, {
        'token': token,
        'userId': user_id,
        'email': email,
        'name': name,
        'subscriptionTier': 'free'
    })

def login_user(body):
    email = body.get('email', '').lower().strip()
    password = body.get('password', '')
    
    if not email or not password:
        return response(400, {'error': 'Email and password are required'})
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        result = users_table.get_item(Key={'email': email})
        if 'Item' not in result:
            return response(401, {'error': 'Invalid credentials'})
        
        user = result['Item']
        if user['passwordHash'] != password_hash:
            return response(401, {'error': 'Invalid credentials'})
        
        token = jwt.encode({
            'userId': user['userId'],
            'email': user['email'],
            'exp': datetime.utcnow() + timedelta(days=30)
        }, JWT_SECRET, algorithm='HS256')
        
        return response(200, {
            'token': token,
            'userId': user['userId'],
            'email': user['email'],
            'name': user['name'],
            'subscriptionTier': user['subscriptionTier'],
            'storageQuota': int(user['storageQuota']),
            'storageUsed': int(user['storageUsed'])
        })
    except Exception as e:
        return response(500, {'error': str(e)})

def verify_token(event):
    token = event.get('headers', {}).get('Authorization', '').replace('Bearer ', '')
    
    if not token:
        return response(401, {'error': 'No token provided'})
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return response(200, {'valid': True, 'userId': payload['userId']})
    except jwt.ExpiredSignatureError:
        return response(401, {'error': 'Token expired'})
    except:
        return response(401, {'error': 'Invalid token'})

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
