"""
7 Mountains API Lambda Function
Handles pledges, badges, contributions, and leaderboards
"""

import json
import boto3
import os
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
pledges_table = dynamodb.Table('mountain-pledges')
badges_table = dynamodb.Table('mountain-badges')
contributions_table = dynamodb.Table('mountain-contributions')
users_table = dynamodb.Table('users')

VALID_MOUNTAINS = ['family', 'religion', 'education', 'media', 'art', 'economics', 'government']
VALID_BADGE_TYPES = ['pledge', 'contributor', 'warrior', 'champion']
VALID_CONTENT_TYPES = ['video', 'article', 'prayer', 'event']

def decimal_default(obj):
    """JSON serializer for Decimal objects"""
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def cors_response(status_code, body):
    """Return response with CORS headers"""
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
    """Extract user_id from JWT token"""
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

def validate_mountain(mountain):
    """Validate mountain name"""
    return mountain.lower() in VALID_MOUNTAINS

def create_pledge(user_id, data):
    """Record a user's pledge to a mountain"""
    mountain = data.get('mountain', '').lower()
    
    if not validate_mountain(mountain):
        return cors_response(400, {'error': f'Invalid mountain. Must be one of: {", ".join(VALID_MOUNTAINS)}'})
    
    # Check if pledge already exists
    try:
        existing = pledges_table.get_item(Key={'user_id': user_id, 'mountain': mountain})
        if 'Item' in existing:
            return cors_response(409, {'error': 'Pledge already exists for this mountain', 'pledge': existing['Item']})
    except:
        pass
    
    # Create pledge
    pledge = {
        'user_id': user_id,
        'mountain': mountain,
        'pledge_date': datetime.now().isoformat(),
        'active': True
    }
    
    pledges_table.put_item(Item=pledge)
    
    # Auto-award "pledge" badge
    badge_id = str(uuid.uuid4())
    badge = {
        'badge_id': badge_id,
        'user_id': user_id,
        'mountain': mountain,
        'badge_type': 'pledge',
        'earned_date': datetime.now().isoformat()
    }
    badges_table.put_item(Item=badge)
    
    return cors_response(200, {
        'message': f'Pledge recorded for {mountain} mountain',
        'pledge': pledge,
        'badge_awarded': badge
    })

def get_user_pledges(user_id):
    """Get all pledges for a user"""
    try:
        response = pledges_table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': user_id}
        )
        return cors_response(200, {'pledges': response['Items']})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def award_badge(user_id, data):
    """Award a badge to a user"""
    mountain = data.get('mountain', '').lower()
    badge_type = data.get('badge_type', '').lower()
    
    if not validate_mountain(mountain):
        return cors_response(400, {'error': f'Invalid mountain. Must be one of: {", ".join(VALID_MOUNTAINS)}'})
    
    if badge_type not in VALID_BADGE_TYPES:
        return cors_response(400, {'error': f'Invalid badge type. Must be one of: {", ".join(VALID_BADGE_TYPES)}'})
    
    badge_id = str(uuid.uuid4())
    badge = {
        'badge_id': badge_id,
        'user_id': user_id,
        'mountain': mountain,
        'badge_type': badge_type,
        'earned_date': datetime.now().isoformat()
    }
    
    badges_table.put_item(Item=badge)
    
    return cors_response(200, {
        'message': f'{badge_type.capitalize()} badge awarded for {mountain} mountain',
        'badge': badge
    })

def get_user_badges(user_id):
    """Get all badges for a user"""
    try:
        response = badges_table.query(
            IndexName='user-index',
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': user_id}
        )
        return cors_response(200, {'badges': response['Items']})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def track_contribution(user_id, data):
    """Track a user's contribution to a mountain"""
    mountain = data.get('mountain', '').lower()
    content_type = data.get('content_type', '').lower()
    content_id = data.get('content_id')
    
    if not validate_mountain(mountain):
        return cors_response(400, {'error': f'Invalid mountain. Must be one of: {", ".join(VALID_MOUNTAINS)}'})
    
    if content_type not in VALID_CONTENT_TYPES:
        return cors_response(400, {'error': f'Invalid content type. Must be one of: {", ".join(VALID_CONTENT_TYPES)}'})
    
    if not content_id:
        return cors_response(400, {'error': 'content_id is required'})
    
    contribution_id = str(uuid.uuid4())
    contribution = {
        'contribution_id': contribution_id,
        'user_id': user_id,
        'mountain': mountain,
        'content_type': content_type,
        'content_id': content_id,
        'contribution_date': datetime.now().isoformat()
    }
    
    contributions_table.put_item(Item=contribution)
    
    # Check if user should be awarded a badge
    # Get user's contribution count for this mountain
    response = contributions_table.query(
        IndexName='user-index',
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': user_id}
    )
    
    mountain_contributions = [c for c in response['Items'] if c['mountain'] == mountain]
    count = len(mountain_contributions)
    
    # Award badges based on contribution count
    badge_awarded = None
    if count == 5:
        badge_id = str(uuid.uuid4())
        badge = {
            'badge_id': badge_id,
            'user_id': user_id,
            'mountain': mountain,
            'badge_type': 'contributor',
            'earned_date': datetime.now().isoformat()
        }
        badges_table.put_item(Item=badge)
        badge_awarded = badge
    elif count == 25:
        badge_id = str(uuid.uuid4())
        badge = {
            'badge_id': badge_id,
            'user_id': user_id,
            'mountain': mountain,
            'badge_type': 'warrior',
            'earned_date': datetime.now().isoformat()
        }
        badges_table.put_item(Item=badge)
        badge_awarded = badge
    elif count == 100:
        badge_id = str(uuid.uuid4())
        badge = {
            'badge_id': badge_id,
            'user_id': user_id,
            'mountain': mountain,
            'badge_type': 'champion',
            'earned_date': datetime.now().isoformat()
        }
        badges_table.put_item(Item=badge)
        badge_awarded = badge
    
    response_data = {
        'message': f'Contribution tracked for {mountain} mountain',
        'contribution': contribution,
        'total_contributions': count
    }
    
    if badge_awarded:
        response_data['badge_awarded'] = badge_awarded
    
    return cors_response(200, response_data)

def get_leaderboard(mountain):
    """Get top contributors for a mountain"""
    mountain = mountain.lower()
    
    if not validate_mountain(mountain):
        return cors_response(400, {'error': f'Invalid mountain. Must be one of: {", ".join(VALID_MOUNTAINS)}'})
    
    try:
        response = contributions_table.query(
            IndexName='mountain-index',
            KeyConditionExpression='mountain = :mountain',
            ExpressionAttributeValues={':mountain': mountain}
        )
        
        contributions = response['Items']
        
        user_counts = {}
        for contrib in contributions:
            user_id = contrib['user_id']
            user_counts[user_id] = user_counts.get(user_id, 0) + 1
        
        leaderboard = []
        for user_id, count in user_counts.items():
            try:
                user_response = users_table.get_item(Key={'user_id': user_id})
                user = user_response.get('Item', {})
                
                leaderboard.append({
                    'user_id': user_id,
                    'name': f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or user.get('email', 'Unknown'),
                    'email': user.get('email', ''),
                    'contribution_count': count
                })
            except:
                leaderboard.append({
                    'user_id': user_id,
                    'name': 'Unknown User',
                    'contribution_count': count
                })
        
        leaderboard.sort(key=lambda x: x['contribution_count'], reverse=True)
        
        return cors_response(200, {
            'mountain': mountain,
            'leaderboard': leaderboard[:50]
        })
    
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def lambda_handler(event, context):
    """Main Lambda handler"""
    if event.get('httpMethod') == 'OPTIONS':
        return cors_response(200, {})
    
    user_id = extract_user_id(event)
    if not user_id:
        return cors_response(401, {'error': 'Unauthorized - valid token required'})
    
    params = event.get('queryStringParameters') or {}
    action = params.get('action')
    
    try:
        body = json.loads(event.get('body', '{}'))
    except:
        body = {}
    
    if action == 'create_pledge':
        return create_pledge(user_id, body)
    elif action == 'get_pledges':
        return get_user_pledges(user_id)
    elif action == 'award_badge':
        return award_badge(user_id, body)
    elif action == 'get_badges':
        return get_user_badges(user_id)
    elif action == 'track_contribution':
        return track_contribution(user_id, body)
    elif action == 'get_leaderboard':
        mountain = params.get('mountain', '')
        return get_leaderboard(mountain)
    else:
        return cors_response(400, {'error': f'Invalid action: {action}'})
