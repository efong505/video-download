import json
import boto3
from datetime import datetime
import uuid
import base64
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
comments_table = dynamodb.Table('comments')
users_table = dynamodb.Table('users')
articles_table = dynamodb.Table('articles')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    headers = cors_headers()
    
    try:
        method = event.get('httpMethod', 'GET')
        
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        query_params = event.get('queryStringParameters') or {}
        action = query_params.get('action')
        
        if method == 'POST' and action == 'create':
            return create_comment(event)
        elif method == 'GET' and action == 'list':
            return list_comments(event)
        elif method == 'PUT' and action == 'update':
            return update_comment(event)
        elif method == 'DELETE' and action == 'delete':
            return delete_comment(event)
        elif method == 'GET' and action == 'admin_list':
            return admin_list_comments(event)
        elif method == 'PUT' and action == 'bulk_action':
            return bulk_comment_action(event)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Endpoint not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def create_comment(event):
    headers = cors_headers()
    
    try:
        user_info = extract_user_from_token(event)
        if not user_info:
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'error': 'Authentication required'})
            }
        
        body = json.loads(event['body'])
        
        comment_id = str(uuid.uuid4())
        article_id = body['article_id']
        content = body['content']
        parent_id = body.get('parent_id')
        
        author_name = get_user_name(user_info['email'])
        
        comment = {
            'comment_id': comment_id,
            'article_id': article_id,
            'content': content,
            'author': author_name,
            'author_email': user_info['email'],
            'parent_id': parent_id,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'is_deleted': False
        }
        
        comments_table.put_item(Item=comment)
        
        # Send notification if this is a reply
        if parent_id:
            try:
                parent_response = comments_table.get_item(Key={'comment_id': parent_id})
                parent_comment = parent_response.get('Item')
                if parent_comment and parent_comment.get('author_email') != user_info['email']:
                    article_response = articles_table.get_item(Key={'article_id': article_id})
                    article = article_response.get('Item', {})
                    article_title = article.get('title', 'an article')
                    
                    lambda_client.invoke(
                        FunctionName='notifications_api',
                        InvocationType='Event',
                        Payload=json.dumps({
                            'body': json.dumps({
                                'action': 'send_notification',
                                'type': 'comment_reply',
                                'recipient_email': parent_comment['author_email'],
                                'subject': 'New Reply to Your Comment',
                                'message': f"{author_name} replied to your comment on \"{article_title}\".",
                                'link': f'https://christianconservativestoday.com/article.html?id={article_id}#comment-{comment_id}'
                            })
                        })
                    )
            except Exception as e:
                print(f'Notification error: {e}')
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Comment created successfully',
                'comment_id': comment_id,
                'comment': convert_decimals(comment)
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def list_comments(event):
    headers = cors_headers()
    
    try:
        query_params = event.get('queryStringParameters') or {}
        article_id = query_params.get('article_id')
        
        if not article_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'article_id required'})
            }
        
        response = comments_table.scan(
            FilterExpression='article_id = :aid AND is_deleted = :deleted',
            ExpressionAttributeValues={
                ':aid': article_id,
                ':deleted': False
            }
        )
        
        comments = response.get('Items', [])
        comments.sort(key=lambda x: x.get('created_at', ''))
        
        parent_comments = []
        replies = {}
        
        for comment in comments:
            if comment.get('parent_id'):
                parent_id = comment['parent_id']
                if parent_id not in replies:
                    replies[parent_id] = []
                replies[parent_id].append(comment)
            else:
                comment['replies'] = []
                parent_comments.append(comment)
        
        for parent_comment in parent_comments:
            comment_id = parent_comment['comment_id']
            if comment_id in replies:
                parent_comment['replies'] = replies[comment_id]
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'comments': convert_decimals(parent_comments),
                'count': len(comments)
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def update_comment(event):
    headers = cors_headers()
    
    try:
        user_info = extract_user_from_token(event)
        if not user_info:
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'error': 'Authentication required'})
            }
        
        body = json.loads(event['body'])
        comment_id = body.get('comment_id')
        new_content = body.get('content')
        
        if not comment_id or not new_content:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'comment_id and content required'})
            }
        
        response = comments_table.get_item(Key={'comment_id': comment_id})
        comment = response.get('Item')
        
        if not comment:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Comment not found'})
            }
        
        if (user_info['email'] != comment.get('author_email') and 
            user_info['role'] not in ['admin', 'super_user']):
            return {
                'statusCode': 403,
                'headers': headers,
                'body': json.dumps({'error': 'You can only edit your own comments'})
            }
        
        comments_table.update_item(
            Key={'comment_id': comment_id},
            UpdateExpression='SET content = :content, updated_at = :updated',
            ExpressionAttributeValues={
                ':content': new_content,
                ':updated': datetime.utcnow().isoformat()
            }
        )
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Comment updated successfully'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def delete_comment(event):
    headers = cors_headers()
    
    try:
        user_info = extract_user_from_token(event)
        if not user_info:
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'error': 'Authentication required'})
            }
        
        query_params = event.get('queryStringParameters') or {}
        comment_id = query_params.get('comment_id')
        
        if not comment_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'comment_id required'})
            }
        
        response = comments_table.get_item(Key={'comment_id': comment_id})
        comment = response.get('Item')
        
        if not comment:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Comment not found'})
            }
        
        if (user_info['email'] != comment.get('author_email') and 
            user_info['role'] not in ['admin', 'super_user']):
            return {
                'statusCode': 403,
                'headers': headers,
                'body': json.dumps({'error': 'You can only delete your own comments'})
            }
        
        comments_table.update_item(
            Key={'comment_id': comment_id},
            UpdateExpression='SET is_deleted = :deleted, updated_at = :updated',
            ExpressionAttributeValues={
                ':deleted': True,
                ':updated': datetime.utcnow().isoformat()
            }
        )
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Comment deleted successfully'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def extract_user_from_token(event):
    try:
        auth_header = event.get('headers', {}).get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        payload_data = parts[1]
        payload_data += '=' * (4 - len(payload_data) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_data))
        
        return {
            'user_id': payload.get('user_id'),
            'email': payload.get('email'),
            'role': payload.get('role')
        }
    except Exception:
        return None

def get_user_name(email):
    try:
        response = users_table.query(
            IndexName='email-index',
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        
        users = response.get('Items', [])
        if users:
            user = users[0]
            first_name = user.get('first_name', '')
            last_name = user.get('last_name', '')
            
            if first_name and last_name:
                return f"{first_name} {last_name}"
            elif first_name:
                return first_name
            elif last_name:
                return last_name
        
        return email
    except Exception:
        return email

def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_decimals(value) for key, value in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj

def admin_list_comments(event):
    headers = cors_headers()
    
    try:
        user_info = extract_user_from_token(event)
        if not user_info or user_info['role'] not in ['admin', 'super_user']:
            return {
                'statusCode': 403,
                'headers': headers,
                'body': json.dumps({'error': 'Admin access required'})
            }
        
        # Get all comments for admin review
        response = comments_table.scan()
        comments = response.get('Items', [])
        
        # Sort by created_at descending (newest first)
        comments.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'comments': convert_decimals(comments),
                'count': len(comments)
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def bulk_comment_action(event):
    headers = cors_headers()
    
    try:
        user_info = extract_user_from_token(event)
        if not user_info or user_info['role'] not in ['admin', 'super_user']:
            return {
                'statusCode': 403,
                'headers': headers,
                'body': json.dumps({'error': 'Admin access required'})
            }
        
        body = json.loads(event['body'])
        comment_ids = body.get('comment_ids', [])
        action = body.get('action')  # 'delete', 'restore'
        
        if not comment_ids or not action:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'comment_ids and action required'})
            }
        
        updated_count = 0
        
        for comment_id in comment_ids:
            try:
                if action == 'delete':
                    comments_table.update_item(
                        Key={'comment_id': comment_id},
                        UpdateExpression='SET is_deleted = :deleted, updated_at = :updated',
                        ExpressionAttributeValues={
                            ':deleted': True,
                            ':updated': datetime.utcnow().isoformat()
                        }
                    )
                elif action == 'restore':
                    comments_table.update_item(
                        Key={'comment_id': comment_id},
                        UpdateExpression='SET is_deleted = :deleted, updated_at = :updated',
                        ExpressionAttributeValues={
                            ':deleted': False,
                            ':updated': datetime.utcnow().isoformat()
                        }
                    )
                updated_count += 1
            except Exception:
                continue
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': f'{updated_count} comments {action}d successfully',
                'updated_count': updated_count
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
    }