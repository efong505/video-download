"""
Comments Handler Lambda
Handles CRUD operations for comments on articles and videos
"""
import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
comments_table = dynamodb.Table('content-comments')
users_table = dynamodb.Table('users')

def lambda_handler(event, context):
    """Main handler for comments API"""
    print(f"Event: {json.dumps(event)}")
    
    method = event.get('httpMethod', event.get('requestContext', {}).get('http', {}).get('method', ''))
    params = event.get('queryStringParameters') or {}
    
    if method == 'OPTIONS':
        return cors_response(200, {'message': 'OK'})
    
    action = params.get('action', '')
    
    if action == 'get_comments':
        return get_comments(params)
    elif action == 'get_comment_count':
        return get_comment_count(params)
    elif action == 'get_all_comments':
        return get_all_comments(params)
    elif method == 'POST':
        body = json.loads(event.get('body', '{}'))
        action = body.get('action', '')
        
        if action == 'add_comment':
            return add_comment(body)
        elif action == 'update_comment':
            return update_comment(body)
        elif action == 'delete_comment':
            return delete_comment(body)
        elif action == 'moderate_comment':
            return moderate_comment(body)
        else:
            return cors_response(400, {'error': 'Invalid action'})
    else:
        return cors_response(400, {'error': 'Invalid request'})

def get_comments(params):
    """Get all comments for a specific content item"""
    try:
        content_id = params.get('content_id', '')
        if not content_id:
            return cors_response(400, {'error': 'content_id required'})
        
        # Query comments for this content, sorted by created_at
        response = comments_table.query(
            IndexName='CreatedAtIndex',
            KeyConditionExpression='content_id = :cid',
            ExpressionAttributeValues={':cid': content_id},
            ScanIndexForward=False  # Newest first
        )
        
        comments = response.get('Items', [])
        
        # Convert Decimal to int/float
        comments = convert_decimals(comments)
        
        # Filter out deleted/hidden comments for non-admins
        comments = [c for c in comments if c.get('status', 'approved') != 'deleted']
        
        return cors_response(200, {'comments': comments, 'count': len(comments)})
    except Exception as e:
        print(f"Get comments error: {str(e)}")
        return cors_response(500, {'error': 'Failed to get comments'})

def get_comment_count(params):
    """Get comment count for a content item"""
    try:
        content_id = params.get('content_id', '')
        if not content_id:
            return cors_response(400, {'error': 'content_id required'})
        
        response = comments_table.query(
            KeyConditionExpression='content_id = :cid',
            ExpressionAttributeValues={':cid': content_id},
            Select='COUNT'
        )
        
        return cors_response(200, {'count': response.get('Count', 0)})
    except Exception as e:
        print(f"Get comment count error: {str(e)}")
        return cors_response(500, {'error': 'Failed to get count'})

def get_all_comments(params):
    """Get all comments across all content (admin only)"""
    try:
        limit = int(params.get('limit', '50'))
        
        response = comments_table.scan(Limit=limit)
        comments = response.get('Items', [])
        
        # Sort by created_at descending
        comments.sort(key=lambda x: x.get('created_at', 0), reverse=True)
        
        comments = convert_decimals(comments)
        
        return cors_response(200, {'comments': comments, 'count': len(comments)})
    except Exception as e:
        print(f"Get all comments error: {str(e)}")
        return cors_response(500, {'error': 'Failed to get comments'})

def add_comment(body):
    """Add a new comment"""
    try:
        content_id = body.get('content_id', '').strip()
        content_type = body.get('content_type', 'article')  # article or video
        user_email = body.get('user_email', '').strip()
        user_name = body.get('user_name', '').strip()
        comment_text = body.get('comment_text', '').strip()
        parent_comment_id = body.get('parent_comment_id')  # For replies
        
        if not content_id or not user_email or not comment_text:
            return cors_response(400, {'error': 'Missing required fields'})
        
        if len(comment_text) > 2000:
            return cors_response(400, {'error': 'Comment too long (max 2000 characters)'})
        
        # Get user info
        user_response = users_table.get_item(Key={'email': user_email})
        user = user_response.get('Item', {})
        
        comment_id = str(uuid.uuid4())
        timestamp = int(datetime.now().timestamp())
        
        comment = {
            'content_id': content_id,
            'comment_id': comment_id,
            'content_type': content_type,
            'user_email': user_email,
            'user_name': user_name or user.get('first_name', 'Anonymous'),
            'comment_text': comment_text,
            'created_at': timestamp,
            'created_at_iso': datetime.now().isoformat(),
            'status': 'approved',  # Can be: approved, pending, flagged, deleted
            'likes': 0,
            'replies_count': 0
        }
        
        if parent_comment_id:
            comment['parent_comment_id'] = parent_comment_id
            # Increment reply count on parent
            try:
                comments_table.update_item(
                    Key={'content_id': content_id, 'comment_id': parent_comment_id},
                    UpdateExpression='ADD replies_count :inc',
                    ExpressionAttributeValues={':inc': 1}
                )
            except:
                pass
        
        comments_table.put_item(Item=comment)
        
        return cors_response(200, {
            'message': 'Comment added',
            'comment_id': comment_id,
            'comment': convert_decimals(comment)
        })
    except Exception as e:
        print(f"Add comment error: {str(e)}")
        import traceback
        traceback.print_exc()
        return cors_response(500, {'error': 'Failed to add comment'})

def update_comment(body):
    """Update an existing comment (user can only edit their own)"""
    try:
        content_id = body.get('content_id', '').strip()
        comment_id = body.get('comment_id', '').strip()
        user_email = body.get('user_email', '').strip()
        comment_text = body.get('comment_text', '').strip()
        
        if not content_id or not comment_id or not comment_text:
            return cors_response(400, {'error': 'Missing required fields'})
        
        # Get existing comment
        response = comments_table.get_item(
            Key={'content_id': content_id, 'comment_id': comment_id}
        )
        
        if 'Item' not in response:
            return cors_response(404, {'error': 'Comment not found'})
        
        existing = response['Item']
        
        # Verify ownership
        if existing.get('user_email') != user_email:
            return cors_response(403, {'error': 'Not authorized'})
        
        # Update comment
        comments_table.update_item(
            Key={'content_id': content_id, 'comment_id': comment_id},
            UpdateExpression='SET comment_text = :text, edited_at = :ts, edited = :edited',
            ExpressionAttributeValues={
                ':text': comment_text,
                ':ts': datetime.now().isoformat(),
                ':edited': True
            }
        )
        
        return cors_response(200, {'message': 'Comment updated'})
    except Exception as e:
        print(f"Update comment error: {str(e)}")
        return cors_response(500, {'error': 'Failed to update comment'})

def delete_comment(body):
    """Delete a comment (user can delete their own, admin can delete any)"""
    try:
        content_id = body.get('content_id', '').strip()
        comment_id = body.get('comment_id', '').strip()
        user_email = body.get('user_email', '').strip()
        is_admin = body.get('is_admin', False)
        
        if not content_id or not comment_id:
            return cors_response(400, {'error': 'Missing required fields'})
        
        # Get existing comment
        response = comments_table.get_item(
            Key={'content_id': content_id, 'comment_id': comment_id}
        )
        
        if 'Item' not in response:
            return cors_response(404, {'error': 'Comment not found'})
        
        existing = response['Item']
        
        # Verify ownership or admin
        if not is_admin and existing.get('user_email') != user_email:
            return cors_response(403, {'error': 'Not authorized'})
        
        # Soft delete - mark as deleted
        comments_table.update_item(
            Key={'content_id': content_id, 'comment_id': comment_id},
            UpdateExpression='SET #status = :status, deleted_at = :ts',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'deleted',
                ':ts': datetime.now().isoformat()
            }
        )
        
        return cors_response(200, {'message': 'Comment deleted'})
    except Exception as e:
        print(f"Delete comment error: {str(e)}")
        return cors_response(500, {'error': 'Failed to delete comment'})

def moderate_comment(body):
    """Moderate a comment (admin only)"""
    try:
        content_id = body.get('content_id', '').strip()
        comment_id = body.get('comment_id', '').strip()
        status = body.get('status', 'approved')  # approved, pending, flagged, deleted
        
        if not content_id or not comment_id:
            return cors_response(400, {'error': 'Missing required fields'})
        
        comments_table.update_item(
            Key={'content_id': content_id, 'comment_id': comment_id},
            UpdateExpression='SET #status = :status, moderated_at = :ts',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': status,
                ':ts': datetime.now().isoformat()
            }
        )
        
        return cors_response(200, {'message': 'Comment moderated'})
    except Exception as e:
        print(f"Moderate comment error: {str(e)}")
        return cors_response(500, {'error': 'Failed to moderate comment'})

def convert_decimals(obj):
    """Convert Decimal to int/float for JSON serialization"""
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    else:
        return obj

def cors_response(status_code, body):
    """Return response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
