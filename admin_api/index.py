import json
import boto3
from datetime import datetime
import base64
import hmac
import hashlib
from decimal import Decimal
import os

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')
users_table = dynamodb.Table('users')
metadata_table = dynamodb.Table('video-metadata')
book_subscribers_table = dynamodb.Table('book-subscribers')

JWT_SECRET = os.environ.get('JWT_SECRET', 'your-jwt-secret-key')

def lambda_handler(event, context):
    try:
        method = event.get('httpMethod', 'GET')
        
        # Handle OPTIONS request first, before token verification
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({})
            }
        
        query_params = event.get('queryStringParameters') or {}
        action = query_params.get('action')
        
        # Handle upload_url with regular user token verification
        if method == 'POST' and action == 'upload_url':
            auth_result = verify_token_only(event)
            if auth_result['statusCode'] != 200:
                return auth_result
            return get_upload_url(event)
        
        # Handle upload_image with regular user token verification
        if method == 'POST' and action == 'upload_image':
            auth_result = verify_token_only(event)
            if auth_result['statusCode'] != 200:
                return auth_result
            return upload_image(event)
        
        # Verify admin token for all other requests
        auth_result = verify_admin_token(event)
        if auth_result['statusCode'] != 200:
            return auth_result
        
        if method == 'GET' and action == 'users':
            return get_all_users(event)
        elif method == 'GET' and action == 'list_book_subscribers':
            return list_book_subscribers(event)
        elif method == 'PUT' and action == 'update_book_subscriber':
            return update_book_subscriber(event)
        elif method == 'DELETE' and action == 'delete_book_subscriber':
            return delete_book_subscriber(event)
        elif method == 'GET' and action == 'videos':
            return get_all_videos(event)
        elif method == 'PUT' and action == 'user_role':
            return update_user_role(event)
        elif method == 'PUT' and action == 'reset_password':
            return reset_user_password(event)
        elif method == 'DELETE' and action == 'user':
            return delete_user(event)
        elif method == 'DELETE' and action == 'video':
            return delete_video(event)
        elif method == 'POST' and action == 'generate_thumbnail':
            return generate_thumbnail(event)
        elif method == 'PUT' and action == 'user_subscription':
            return update_user_subscription(event)
        else:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Endpoint not found'})
            }
    except Exception as e:
        print(f"Lambda error: {str(e)}")
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
        # Simple JWT decode without library
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError('Invalid token format')
        
        # Decode payload
        payload_data = parts[1]
        # Add padding if needed
        payload_data += '=' * (4 - len(payload_data) % 4)
        payload = json.loads(base64.b64decode(payload_data))
        
        user_role = payload.get('role')
        if user_role not in ['super_user', 'admin']:
            return {
                'statusCode': 403,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Admin or Super User access required'})
            }
        return {'statusCode': 200, 'user': payload}
    except Exception as e:
        return {
            'statusCode': 401,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'Invalid token'})
        }

def verify_token_only(event):
    """Verify token without role restrictions"""
    auth_header = event.get('headers', {}).get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return {
            'statusCode': 401,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'Missing token'})
        }
    
    token = auth_header.split(' ')[1]
    
    try:
        # Simple JWT decode without library
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError('Invalid token format')
        
        # Decode payload
        payload_data = parts[1]
        # Add padding if needed
        payload_data += '=' * (4 - len(payload_data) % 4)
        payload = json.loads(base64.b64decode(payload_data))
        
        return {'statusCode': 200, 'user': payload}
    except Exception as e:
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
            'first_name': item.get('first_name', ''),
            'last_name': item.get('last_name', ''),
            'role': item['role'],
            'created_at': item['created_at'],
            'active': item.get('active', True),
            'subscription_tier': item.get('subscription_tier', 'free'),
            'subscription_status': item.get('subscription_status', 'active'),
            'next_billing_date': item.get('next_billing_date'),
            'storage_used': int(item.get('storage_used', 0)),
            'storage_limit': int(item.get('storage_limit', 2147483648)),
            'video_count': int(item.get('video_count', 0)),
            'video_limit': int(item.get('video_limit', 50))
        })
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'users': users,
            'count': len(users)
        })
    }

def list_book_subscribers(event):
    response = book_subscribers_table.scan()
    subscribers = response.get('Items', [])
    subscribers.sort(key=lambda x: x.get('subscribed_at', ''), reverse=True)
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({'subscribers': subscribers}, cls=DecimalEncoder)
    }

def update_book_subscriber(event):
    body = json.loads(event['body'])
    email = body['email']
    first_name = body.get('first_name', '')
    
    book_subscribers_table.update_item(
        Key={'email': email},
        UpdateExpression='SET first_name = :name',
        ExpressionAttributeValues={':name': first_name}
    )
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({'message': 'Subscriber updated'})
    }

def delete_book_subscriber(event):
    params = event.get('queryStringParameters') or {}
    email = params.get('email')
    
    if not email:
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'email required'})
        }
    
    book_subscribers_table.delete_item(Key={'email': email})
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({'message': 'Subscriber deleted'})
    }

def update_user_subscription(event):
    """Update user subscription details (admin only)"""
    body = json.loads(event['body'])
    user_id = body['user_id']
    subscription_tier = body['subscription_tier']
    subscription_status = body['subscription_status']
    storage_limit = body['storage_limit']
    video_limit = body['video_limit']
    next_billing_date = body.get('next_billing_date')
    
    # Build update expression
    update_expression = 'SET subscription_tier = :tier, subscription_status = :status, storage_limit = :storage, video_limit = :videos, updated_at = :updated'
    expression_values = {
        ':tier': subscription_tier,
        ':status': subscription_status,
        ':storage': storage_limit,
        ':videos': video_limit,
        ':updated': datetime.utcnow().isoformat()
    }
    
    if next_billing_date:
        update_expression += ', next_billing_date = :billing'
        expression_values[':billing'] = next_billing_date
    
    users_table.update_item(
        Key={'user_id': user_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values
    )
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'Subscription updated successfully',
            'user_id': user_id,
            'subscription_tier': subscription_tier,
            'subscription_status': subscription_status
        })
    }

def get_all_videos(event):
    # Get current user from token
    auth_result = verify_admin_token(event)
    current_user = auth_result['user']
    current_role = current_user.get('role')
    current_email = current_user.get('email')
    
    videos = []
    
    # Get ALL videos from metadata table (includes both local and external)
    metadata_response = metadata_table.scan()
    
    for metadata in metadata_response.get('Items', []):
        visibility = metadata.get('visibility', 'public')
        owner = metadata.get('owner', 'system')
        video_type = metadata.get('video_type', 'local')
        filename = metadata.get('filename', '')
        
        # Admin/Super users see all videos, others see only their own + public
        if current_role in ['admin', 'super_user'] or visibility == 'public' or owner == current_email:
            video_data = {
                'filename': filename,
                'tags': metadata.get('tags', []),
                'title': metadata.get('title', filename.replace('.mp4', '')),
                'owner': owner,
                'visibility': visibility,
                'video_type': video_type,
                'external_url': metadata.get('external_url', '')
            }
            
            # Get size from S3 for local videos only
            if video_type == 'local':
                try:
                    s3_obj = s3_client.head_object(
                        Bucket='my-video-downloads-bucket',
                        Key=f'videos/{filename}'
                    )
                    video_data['size'] = s3_obj['ContentLength']
                    video_data['size_formatted'] = format_file_size(s3_obj['ContentLength'])
                    video_data['last_modified'] = s3_obj['LastModified'].isoformat()
                except:
                    video_data['size'] = 0
                    video_data['size_formatted'] = '0 B'
                    video_data['last_modified'] = metadata.get('created_at', '')
            else:
                video_data['size'] = 0
                video_data['size_formatted'] = 'External'
                video_data['last_modified'] = metadata.get('created_at', '')
            
            videos.append(video_data)
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'videos': videos,
            'count': len(videos)
        })
    }

def update_user_role(event):
    # Get current user role from token
    auth_result = verify_admin_token(event)
    current_user = auth_result['user']
    current_role = current_user.get('role')
    
    body = json.loads(event['body'])
    user_id = body['user_id']
    new_role = body['role']
    first_name = body.get('first_name', '')
    last_name = body.get('last_name', '')
    
    # Get target user to check if they're super_user
    try:
        target_user_response = users_table.get_item(Key={'user_id': user_id})
        if 'Item' not in target_user_response:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'User not found'})
            }
        target_user = target_user_response['Item']
        
        # Prevent admin from modifying super_user
        if current_role == 'admin' and target_user.get('role') == 'super_user':
            return {
                'statusCode': 403,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Cannot modify Super User'})
            }
        
        # Prevent admin from creating super_user
        if current_role == 'admin' and new_role == 'super_user':
            return {
                'statusCode': 403,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Cannot create Super User'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }
    
    # Build update expression dynamically
    update_expression = 'SET #role = :role, updated_at = :updated'
    expression_names = {'#role': 'role'}
    expression_values = {
        ':role': new_role,
        ':updated': datetime.utcnow().isoformat()
    }
    
    if first_name is not None:
        update_expression += ', first_name = :first_name'
        expression_values[':first_name'] = first_name
    
    if last_name is not None:
        update_expression += ', last_name = :last_name'
        expression_values[':last_name'] = last_name
    
    users_table.update_item(
        Key={'user_id': user_id},
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_names,
        ExpressionAttributeValues=expression_values
    )
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'User updated successfully',
            'user_id': user_id,
            'role': new_role
        })
    }

def reset_user_password(event):
    body = json.loads(event['body'])
    user_id = body['user_id']
    new_password = body['new_password']
    
    # Hash the new password
    password_hash = hashlib.sha256(new_password.encode()).hexdigest()
    
    users_table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET password_hash = :password, updated_at = :updated',
        ExpressionAttributeValues={
            ':password': password_hash,
            ':updated': datetime.utcnow().isoformat()
        }
    )
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'Password reset successfully',
            'user_id': user_id
        })
    }

def delete_user(event):
    # Get current user role from token
    auth_result = verify_admin_token(event)
    current_user = auth_result['user']
    current_role = current_user.get('role')
    
    query_params = event.get('queryStringParameters') or {}
    user_id = query_params.get('user_id')
    
    if not user_id:
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'user_id required'})
        }
    
    # Get target user to check if they're super_user
    try:
        target_user_response = users_table.get_item(Key={'user_id': user_id})
        if 'Item' not in target_user_response:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'User not found'})
            }
        target_user = target_user_response['Item']
        
        # Prevent admin from deleting super_user
        if current_role == 'admin' and target_user.get('role') == 'super_user':
            return {
                'statusCode': 403,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Cannot delete Super User'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
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

def send_admin_alert(alert_type, details):
    """Send alert notification to all admins"""
    try:
        response = users_table.scan(
            FilterExpression='#role IN (:admin, :super)',
            ExpressionAttributeNames={'#role': 'role'},
            ExpressionAttributeValues={':admin': 'admin', ':super': 'super_user'}
        )
        
        for admin in response.get('Items', []):
            try:
                lambda_client.invoke(
                    FunctionName='notifications_api',
                    InvocationType='Event',
                    Payload=json.dumps({
                        'action': 'send_notification',
                        'user_email': admin['email'],
                        'notification_type': 'admin_alert',
                        'title': f'Admin Alert: {alert_type}',
                        'message': details,
                        'link': '/admin.html'
                    })
                )
            except Exception as e:
                print(f"Failed to notify admin {admin['email']}: {str(e)}")
    except Exception as e:
        print(f"Failed to send admin alerts: {str(e)}")

def delete_video(event):
    query_params = event.get('queryStringParameters') or {}
    filename = query_params.get('filename')
    
    if not filename:
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'filename required'})
        }
    
    try:
        # First, find the video_id by scanning for this filename
        # This is necessary because video_id might not equal filename (e.g., old videos with UUID video_ids)
        scan_response = metadata_table.scan(
            FilterExpression='filename = :fn',
            ExpressionAttributeValues={':fn': filename}
        )
        
        if not scan_response.get('Items'):
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Video not found'})
            }
        
        metadata = scan_response['Items'][0]
        video_id = metadata['video_id']
        video_type = metadata.get('video_type', 'local')
        
        if video_type == 'local':
            # Delete from S3
            s3_client.delete_object(
                Bucket='my-video-downloads-bucket',
                Key=f'videos/{filename}'
            )
            
            # Delete thumbnails
            base_name = filename.rsplit('.', 1)[0]
            for i in range(1, 4):
                try:
                    s3_client.delete_object(
                        Bucket='my-video-downloads-bucket',
                        Key=f'thumbnails/{base_name}_thumb_{i}.jpg'
                    )
                except Exception as e:
                    print(f'Failed to delete thumbnail {i}: {e}')
        
        # Delete metadata using the correct video_id primary key
        metadata_table.delete_item(Key={'video_id': video_id})
        
        # Send admin alert
        try:
            send_admin_alert('video_deleted', f'Video deleted: {filename}')
        except Exception as e:
            print(f"Failed to send admin alert: {str(e)}")
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({
                'message': 'Video deleted successfully',
                'filename': filename,
                'video_id': video_id
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({
                'error': f'Failed to delete video: {str(e)}',
                'filename': filename
            })
        }

def upload_image(event):
    """Handle image upload to S3 from base64 JSON data"""
    import uuid
    import re
    
    try:
        body_str = event.get('body', '{}')
        is_base64 = event.get('isBase64Encoded', False)
        
        print(f"isBase64Encoded: {is_base64}, body length: {len(body_str) if body_str else 0}")
        
        # Try to parse as JSON first (new format)
        try:
            body = json.loads(body_str)
            file_data_base64 = body.get('file_data')
            file_ext = body.get('file_ext', 'jpg')
            
            if file_data_base64:
                # New JSON format
                file_data = base64.b64decode(file_data_base64)
                print(f"Using JSON format, file_ext: {file_ext}")
            else:
                raise ValueError("No file_data in JSON")
        except (json.JSONDecodeError, ValueError):
            # Old multipart format - body is base64 encoded multipart data
            print("Falling back to multipart format")
            
            # API Gateway should base64 encode binary data
            if not is_base64:
                raise ValueError('Binary data must be base64 encoded by API Gateway')
            
            body_bytes = base64.b64decode(body_str)
            
            # Extract file from multipart
            content_type = event.get('headers', {}).get('content-type', '') or event.get('headers', {}).get('Content-Type', '')
            boundary_match = re.search(r'boundary=([^;\s]+)', content_type)
            if not boundary_match:
                raise ValueError('No boundary in multipart')
            
            boundary = boundary_match.group(1).encode('ascii')
            parts = body_bytes.split(b'--' + boundary)
            
            file_data = None
            file_ext = 'jpg'
            
            for part in parts:
                if b'Content-Disposition' in part and b'filename=' in part:
                    filename_match = re.search(b'filename="([^"]+)"', part)
                    if filename_match:
                        filename = filename_match.group(1).decode('utf-8', errors='ignore')
                        if '.' in filename:
                            file_ext = filename.split('.')[-1].lower()
                    
                    header_end = part.find(b'\r\n\r\n')
                    if header_end != -1:
                        file_data = part[header_end + 4:]
                        if file_data.endswith(b'\r\n'):
                            file_data = file_data[:-2]
                        break
            
            if not file_data:
                raise ValueError('No file data in multipart')
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        s3_key = f'article-images/{unique_id}.{file_ext}'
        
        # Upload to S3
        s3_client.put_object(
            Bucket='my-video-downloads-bucket',
            Key=s3_key,
            Body=file_data,
            ContentType=f'image/{file_ext}'
        )
        
        # Return CloudFront URL
        cloudfront_url = f'https://d271vky579caz9.cloudfront.net/{s3_key}'
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({'url': cloudfront_url})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def get_upload_url(event):
    body = json.loads(event['body'])
    filename = body['filename']
    
    # Determine content type based on file extension
    content_type = 'text/html'
    if filename.lower().endswith('.mp4'):
        content_type = 'video/mp4'
    elif filename.lower().endswith('.webm'):
        content_type = 'video/webm'
    elif filename.lower().endswith('.mov'):
        content_type = 'video/quicktime'
    elif filename.lower().endswith('.avi'):
        content_type = 'video/x-msvideo'
    elif filename.lower().endswith('.html'):
        content_type = 'text/html'
    elif filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
        content_type = 'image/jpeg'
    elif filename.lower().endswith('.png'):
        content_type = 'image/png'
    
    upload_url = s3_client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': 'my-video-downloads-bucket',
            'Key': filename,
            'ContentType': content_type,
            'ContentDisposition': 'inline'
        },
        ExpiresIn=3600
    )
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'upload_url': upload_url,
            'filename': filename
        })
    }



def generate_thumbnail(event):
    body = json.loads(event['body'])
    filename = body['filename']
    video_type = body.get('video_type', 'local')
    external_url = body.get('external_url')
    
    lambda_client = boto3.client('lambda')
    try:
        # Use dedicated thumbnail generator Lambda
        payload = {
            'filename': filename,
            'bucket': 'my-video-downloads-bucket',
            'video_type': video_type
        }
        
        if external_url:
            payload['external_url'] = external_url
        
        lambda_client.invoke(
            FunctionName='thumbnail-generator',
            InvocationType='Event',
            Payload=json.dumps(payload)
        )
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({'message': 'Thumbnail generation started'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def format_file_size(bytes):
    """Format file size in human readable format"""
    if bytes == 0:
        return '0 B'
    k = 1024
    sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    i = int(bytes.bit_length() - 1) // 10 if bytes else 0
    if i >= len(sizes):
        i = len(sizes) - 1
    return f"{bytes / (k ** i):.1f} {sizes[i]}"

def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Max-Age': '86400'
    }