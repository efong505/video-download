import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal
import base64
import os

# Initialize AWS services
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
lambda_client = boto3.client('lambda')
news_table = dynamodb.Table('news-table')
users_table = dynamodb.Table('users')
subscribers_table = dynamodb.Table('email_subscribers')

# Configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-jwt-secret-key')
S3_BUCKET = 'my-video-downloads-bucket'
CLOUDFRONT_URL = 'https://christianconservativestoday.com'

def lambda_handler(event, context):
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    try:
        # Handle preflight OPTIONS request
        http_method = event.get('httpMethod', 'GET')
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'CORS preflight'})
            }
        
        # Get action from query parameters
        query_params = event.get('queryStringParameters') or {}
        action = query_params.get('action', 'list')
        
        # Route based on HTTP method and action
        if action == 'upload':
            return upload_image(event, headers)
        elif http_method == 'POST' or action == 'create':
            return create_news(event, headers)
        elif http_method == 'PUT' or action == 'update':
            return update_news(event, headers)
        elif http_method == 'DELETE' or action == 'delete':
            return delete_news(event, headers)
        elif action == 'get':
            return get_news(event, headers)
        else:
            return list_news(event, headers)
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e), 'type': type(e).__name__})
        }

def verify_token(event):
    """Verify JWT token and return user info"""
    try:
        headers = event.get('headers', {})
        auth_header = headers.get('Authorization') or headers.get('authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        # Decode payload
        payload_data = parts[1]
        payload_data += '=' * (4 - len(payload_data) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_data))
        
        # Check expiration
        if payload.get('exp', 0) < datetime.utcnow().timestamp():
            return None
        
        return payload
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        return None

def verify_admin_token(event):
    """Verify admin/super_user token"""
    user_info = verify_token(event)
    if not user_info:
        return None
    
    role = user_info.get('role', 'user')
    if role in ['admin', 'super_user']:
        return user_info
    return None

def get_user_name(email):
    """Get user's display name from users table"""
    try:
        response = users_table.scan(
            FilterExpression='email = :email',
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

def create_news(event, headers):
    """Create new news item"""
    user_info = verify_admin_token(event)
    if not user_info:
        return {
            'statusCode': 403,
            'headers': headers,
            'body': json.dumps({'error': 'Admin access required'})
        }
    
    try:
        body = json.loads(event['body'])
        
        news_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        # Determine status based on scheduled_publish
        scheduled_publish = body.get('scheduled_publish', '')
        status = body.get('status', 'published')
        if scheduled_publish:
            try:
                scheduled_time = datetime.fromisoformat(scheduled_publish.replace('Z', '+00:00'))
                if scheduled_time > datetime.utcnow():
                    status = 'scheduled'
            except:
                pass
        
        # Get author_name from request or derive from email
        author_name = body.get('author_name', '')
        if not author_name:
            author_name = get_user_name(user_info['email'])
        
        news_item = {
            'news_id': news_id,
            'title': body['title'],
            'content': body.get('content', ''),
            'summary': body.get('summary', ''),
            'category': body.get('category', 'general'),
            'tags': body.get('tags', []),
            'state': body.get('state', ''),
            'author': user_info['email'],
            'author_name': author_name,
            'visibility': body.get('visibility', 'public'),
            'is_breaking': body.get('is_breaking', False),
            'external_url': body.get('external_url', ''),
            'featured_image': body.get('featured_image', ''),
            'scheduled_publish': scheduled_publish,
            'status': status,
            'created_at': now,
            'updated_at': now,
            'view_count': 0
        }
        
        news_table.put_item(Item=news_item)
        
        # Send notifications if published
        if status == 'published':
            try:
                send_article_notifications(news_id, body['title'])
            except Exception as e:
                print(f"Failed to send notifications: {str(e)}")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'News created successfully',
                'news_id': news_id
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def list_news(event, headers):
    """List news items with filtering"""
    try:
        params = event.get('queryStringParameters') or {}
        category = params.get('category')
        visibility = params.get('visibility')
        breaking_only = params.get('breaking') == 'true'
        state = params.get('state')
        
        # Scan news table
        scan_kwargs = {}
        filter_expressions = []
        expression_values = {}
        
        if category:
            filter_expressions.append('category = :category')
            expression_values[':category'] = category
        
        if visibility:
            filter_expressions.append('visibility = :visibility')
            expression_values[':visibility'] = visibility
        
        if breaking_only:
            filter_expressions.append('is_breaking = :breaking')
            expression_values[':breaking'] = True
        
        if state:
            filter_expressions.append('#state = :state')
            expression_values[':state'] = state
            if '#status' in scan_kwargs.get('ExpressionAttributeNames', {}):
                scan_kwargs['ExpressionAttributeNames']['#state'] = 'state'
            else:
                scan_kwargs['ExpressionAttributeNames'] = {'#state': 'state'}
        
        # Only show published items for non-admin users
        user_info = verify_token(event)
        if not user_info or user_info.get('role') not in ['admin', 'super_user']:
            filter_expressions.append('#status = :status')
            expression_values[':status'] = 'published'
            scan_kwargs['ExpressionAttributeNames'] = {'#status': 'status'}
        
        if filter_expressions:
            scan_kwargs['FilterExpression'] = ' AND '.join(filter_expressions)
            scan_kwargs['ExpressionAttributeValues'] = expression_values
        
        response = news_table.scan(**scan_kwargs)
        news_items = response.get('Items', [])
        
        # Sort by created_at descending
        news_items.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        # Convert Decimal objects to int/float
        for item in news_items:
            if 'view_count' in item:
                item['view_count'] = int(item['view_count'])
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(news_items, default=str)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def get_news(event, headers):
    """Get single news item by ID"""
    try:
        params = event.get('queryStringParameters') or {}
        news_id = params.get('news_id')
        
        if not news_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'news_id required'})
            }
        
        response = news_table.get_item(Key={'news_id': news_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'News not found'})
            }
        
        news_item = response['Item']
        
        # Increment view count
        try:
            news_table.update_item(
                Key={'news_id': news_id},
                UpdateExpression='SET view_count = view_count + :inc',
                ExpressionAttributeValues={':inc': 1}
            )
            news_item['view_count'] = int(news_item.get('view_count', 0)) + 1
        except:
            pass
        
        # Convert Decimal objects
        if 'view_count' in news_item:
            news_item['view_count'] = int(news_item['view_count'])
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(news_item, default=str)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def update_news(event, headers):
    """Update existing news item"""
    user_info = verify_admin_token(event)
    if not user_info:
        return {
            'statusCode': 403,
            'headers': headers,
            'body': json.dumps({'error': 'Admin access required'})
        }
    
    try:
        body = json.loads(event['body'])
        news_id = body.get('news_id')
        
        if not news_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'news_id required'})
            }
        
        # Build update expression
        update_expression = 'SET updated_at = :updated_at'
        expression_values = {':updated_at': datetime.utcnow().isoformat()}
        expression_names = {}
        
        # Update fields if provided
        fields = ['title', 'content', 'summary', 'category', 'tags', 'state', 'visibility', 
                 'is_breaking', 'external_url', 'featured_image', 'scheduled_publish', 'status', 'author_name']
        
        for field in fields:
            if field in body:
                if field == 'status':
                    # Use expression attribute name for reserved keyword
                    update_expression += ', #status = :status'
                    expression_names['#status'] = 'status'
                    expression_values[':status'] = body[field]
                else:
                    update_expression += f', {field} = :{field}'
                    expression_values[f':{field}'] = body[field]
        
        update_kwargs = {
            'Key': {'news_id': news_id},
            'UpdateExpression': update_expression,
            'ExpressionAttributeValues': expression_values
        }
        
        if expression_names:
            update_kwargs['ExpressionAttributeNames'] = expression_names
        
        news_table.update_item(**update_kwargs)
        
        # Send notifications if status changed to published
        if 'status' in body and body['status'] == 'published':
            try:
                response = news_table.get_item(Key={'news_id': news_id})
                if 'Item' in response:
                    send_article_notifications(news_id, response['Item'].get('title', 'New Article'))
            except Exception as e:
                print(f"Failed to send notifications: {str(e)}")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'News updated successfully'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def delete_news(event, headers):
    """Delete news item"""
    user_info = verify_admin_token(event)
    if not user_info:
        return {
            'statusCode': 403,
            'headers': headers,
            'body': json.dumps({'error': 'Admin access required'})
        }
    
    try:
        params = event.get('queryStringParameters') or {}
        news_id = params.get('news_id')
        
        if not news_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'news_id required'})
            }
        
        # Get the news item to check for featured image
        response = news_table.get_item(Key={'news_id': news_id})
        news_item = response.get('Item')
        
        if news_item:
            # Delete featured image from S3 if it exists
            featured_image = news_item.get('featured_image', '')
            if featured_image and 'my-video-downloads-bucket' in featured_image:
                try:
                    # Extract S3 key from URL
                    key = featured_image.split('.com/')[-1]
                    s3.delete_object(Bucket=S3_BUCKET, Key=key)
                    print(f'Deleted S3 image: {key}')
                except Exception as e:
                    print(f'Failed to delete S3 image: {e}')
        
        # Delete the news item from DynamoDB
        news_table.delete_item(Key={'news_id': news_id})
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'News deleted successfully'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def send_article_notifications(news_id, title):
    """Send notifications to subscribers about new article"""
    try:
        response = subscribers_table.scan(
            FilterExpression='#status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': 'active'}
        )
        
        for subscriber in response.get('Items', []):
            try:
                lambda_client.invoke(
                    FunctionName='notifications_api',
                    InvocationType='Event',
                    Payload=json.dumps({
                        'action': 'send_notification',
                        'user_email': subscriber['email'],
                        'notification_type': 'article_published',
                        'title': 'New Article Published',
                        'message': f'Check out our latest article: {title}',
                        'link': f'/news.html?id={news_id}'
                    })
                )
            except Exception as e:
                print(f"Failed to notify {subscriber['email']}: {str(e)}")
    except Exception as e:
        print(f"Failed to send article notifications: {str(e)}")

def upload_image(event, headers):
    """Upload image to S3"""
    user_info = verify_admin_token(event)
    if not user_info:
        return {
            'statusCode': 403,
            'headers': headers,
            'body': json.dumps({'error': 'Admin access required'})
        }
    
    try:
        body = json.loads(event['body'])
        image_data = body.get('image')
        filename = body.get('filename', f'news-{uuid.uuid4()}.jpg')
        
        if not image_data:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Image data required'})
            }
        
        # Decode base64 image
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        
        # Upload to S3
        s3_key = f'news-images/{filename}'
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=image_bytes,
            ContentType='image/jpeg',
            CacheControl='max-age=31536000'
        )
        
        image_url = f'{CLOUDFRONT_URL}/{s3_key}'
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Image uploaded successfully',
                'url': image_url
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }