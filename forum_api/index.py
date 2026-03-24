"""
Forum/Discussion API Lambda Function
Handles threaded discussions by mountain category
"""

import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('forum-posts')
users_table = dynamodb.Table('users')

VALID_MOUNTAINS = ['family', 'religion', 'education', 'media', 'art', 'economics', 'government', 'general']

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

def extract_user(event):
    auth_header = event.get('headers', {}).get('Authorization') or event.get('headers', {}).get('authorization')
    if not auth_header:
        return None, None
    import jwt
    token = auth_header.replace('Bearer ', '')
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id = payload.get('user_id')
        # Get user display name
        try:
            user = users_table.get_item(Key={'user_id': user_id}).get('Item', {})
            name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or user.get('email', 'Anonymous')
        except:
            name = 'Anonymous'
        return user_id, name
    except:
        return None, None

def create_post(user_id, user_name, data):
    mountain = data.get('mountain', 'general').lower()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    parent_id = data.get('parent_id')  # None for top-level, set for replies

    if mountain not in VALID_MOUNTAINS:
        return cors_response(400, {'error': 'Invalid mountain category'})
    if not content:
        return cors_response(400, {'error': 'Content is required'})
    if not parent_id and not title:
        return cors_response(400, {'error': 'Title is required for new posts'})

    post_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    item = {
        'post_id': post_id,
        'mountain': mountain,
        'user_id': user_id,
        'user_name': user_name,
        'content': content,
        'created_at': now,
        'updated_at': now,
        'upvotes': 0,
        'upvoted_by': [],
        'reply_count': 0,
        'status': 'active'
    }

    if parent_id:
        item['parent_id'] = parent_id
        item['title'] = ''
        # Increment reply_count on parent
        try:
            table.update_item(
                Key={'post_id': parent_id},
                UpdateExpression='SET reply_count = if_not_exists(reply_count, :zero) + :one',
                ExpressionAttributeValues={':zero': 0, ':one': 1}
            )
        except:
            pass
    else:
        item['parent_id'] = 'NONE'
        item['title'] = title

    table.put_item(Item=item)
    return cors_response(200, {'message': 'Post created', 'post': item})

def list_posts(params):
    mountain = params.get('mountain', 'all').lower()
    page_size = int(params.get('limit', '20'))

    try:
        if mountain == 'all':
            # Scan for top-level posts only
            response = table.scan(
                FilterExpression='parent_id = :none AND #s = :active',
                ExpressionAttributeNames={'#s': 'status'},
                ExpressionAttributeValues={':none': 'NONE', ':active': 'active'}
            )
        else:
            response = table.query(
                IndexName='mountain-index',
                KeyConditionExpression='mountain = :m',
                FilterExpression='parent_id = :none AND #s = :active',
                ExpressionAttributeNames={'#s': 'status'},
                ExpressionAttributeValues={':m': mountain, ':none': 'NONE', ':active': 'active'}
            )

        posts = response.get('Items', [])
        posts.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return cors_response(200, {'posts': posts[:page_size], 'total': len(posts)})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def get_post(params):
    post_id = params.get('post_id')
    if not post_id:
        return cors_response(400, {'error': 'post_id required'})

    try:
        post = table.get_item(Key={'post_id': post_id}).get('Item')
        if not post:
            return cors_response(404, {'error': 'Post not found'})

        # Get replies
        response = table.scan(
            FilterExpression='parent_id = :pid AND #s = :active',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':pid': post_id, ':active': 'active'}
        )
        replies = response.get('Items', [])
        replies.sort(key=lambda x: x.get('created_at', ''))

        return cors_response(200, {'post': post, 'replies': replies})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def upvote_post(user_id, data):
    post_id = data.get('post_id')
    if not post_id:
        return cors_response(400, {'error': 'post_id required'})

    try:
        post = table.get_item(Key={'post_id': post_id}).get('Item')
        if not post:
            return cors_response(404, {'error': 'Post not found'})

        upvoted_by = post.get('upvoted_by', [])
        if user_id in upvoted_by:
            # Remove upvote
            upvoted_by.remove(user_id)
            table.update_item(
                Key={'post_id': post_id},
                UpdateExpression='SET upvotes = upvotes - :one, upvoted_by = :ub',
                ExpressionAttributeValues={':one': 1, ':ub': upvoted_by}
            )
            return cors_response(200, {'message': 'Upvote removed', 'upvotes': post['upvotes'] - 1})
        else:
            upvoted_by.append(user_id)
            table.update_item(
                Key={'post_id': post_id},
                UpdateExpression='SET upvotes = upvotes + :one, upvoted_by = :ub',
                ExpressionAttributeValues={':one': 1, ':ub': upvoted_by}
            )
            return cors_response(200, {'message': 'Upvoted', 'upvotes': post['upvotes'] + 1})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def delete_post(user_id, data):
    post_id = data.get('post_id')
    if not post_id:
        return cors_response(400, {'error': 'post_id required'})

    try:
        post = table.get_item(Key={'post_id': post_id}).get('Item')
        if not post:
            return cors_response(404, {'error': 'Post not found'})
        if post['user_id'] != user_id:
            return cors_response(403, {'error': 'Can only delete your own posts'})

        table.update_item(
            Key={'post_id': post_id},
            UpdateExpression='SET #s = :deleted',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':deleted': 'deleted'}
        )
        return cors_response(200, {'message': 'Post deleted'})
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def lambda_handler(event, context):
    if event.get('httpMethod') == 'OPTIONS':
        return cors_response(200, {})

    params = event.get('queryStringParameters') or {}
    action = params.get('action')

    # Public actions (no auth needed)
    if action == 'list':
        return list_posts(params)
    if action == 'get':
        return get_post(params)

    # Auth-required actions
    user_id, user_name = extract_user(event)
    if not user_id:
        return cors_response(401, {'error': 'Login required'})

    try:
        body = json.loads(event.get('body', '{}'))
    except:
        body = {}

    if action == 'create':
        return create_post(user_id, user_name, body)
    elif action == 'upvote':
        return upvote_post(user_id, body)
    elif action == 'delete':
        return delete_post(user_id, body)
    else:
        return cors_response(400, {'error': f'Invalid action: {action}'})
