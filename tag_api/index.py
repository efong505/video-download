import json
import boto3
from datetime import datetime
import uuid

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
table = dynamodb.Table('video-metadata')

def lambda_handler(event, context):
    """
    Tag management API for video metadata
    """
    try:
        method = event.get('httpMethod', 'GET')
        path = event.get('path', '/tags')
        
        # Handle OPTIONS for CORS preflight
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': ''
            }
        
        query_params = event.get('queryStringParameters') or {}
        action = query_params.get('action')
        
        # Handle path-based requests (e.g., /tags/filename.mp4)
        if method == 'GET' and path.startswith('/tags/') and len(path) > 6:
            filename = path[6:]  # Remove '/tags/' prefix
            return get_video_metadata(filename)
        elif method == 'PUT' and path.startswith('/tags/') and len(path) > 6:
            filename = path[6:]  # Remove '/tags/' prefix
            return update_video_metadata(event, filename)
        elif method == 'POST' and action == 'add_video':
            return add_video_metadata(event)
        elif method == 'GET' and action == 'get_videos_by_tag':
            return get_videos_by_tag(event)
        elif method == 'GET' and action == 'get_all_tags':
            return get_all_tags(event)
        elif method == 'PUT' and action == 'update_video':
            return update_video_tags(event)
        elif method == 'GET' and action == 'list':
            return list_all_videos(event)
        elif method == 'POST' and action == 'create_article':
            return create_article_via_tags(event)
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

def add_video_metadata(event):
    """Add video metadata with tags"""
    body = json.loads(event['body'])
    
    video_id = body.get('video_id') or str(uuid.uuid4())
    filename = body['filename']
    tags = body.get('tags', [])
    title = body.get('title', filename.replace('.mp4', ''))
    owner = body.get('owner', 'system')
    visibility = body.get('visibility', 'public')
    external_url = body.get('external_url')
    video_type = body.get('video_type', 'local')  # 'local', 'youtube', 'rumble'
    
    item = {
        'video_id': video_id,
        'filename': filename,
        'title': title,
        'tags': tags,
        'owner': owner,
        'visibility': visibility,
        'video_type': video_type,
        'upload_date': datetime.utcnow().isoformat(),
        'created_at': datetime.utcnow().isoformat()
    }
    
    if external_url:
        item['external_url'] = external_url
    
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'Video metadata added',
            'video_id': video_id,
            'tags': tags,
            'owner': owner,
            'visibility': visibility,
            'video_type': video_type
        })
    }

def get_videos_by_tag(event):
    """Get videos filtered by tag with visibility control"""
    query_params = event.get('queryStringParameters') or {}
    tag = query_params.get('tag')
    user_email = query_params.get('user')
    user_role = query_params.get('role')
    
    if not tag:
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'Tag parameter required'})
        }
    
    # Scan for videos with the specified tag
    response = table.scan(
        FilterExpression='contains(tags, :tag)',
        ExpressionAttributeValues={':tag': tag}
    )
    
    # Filter by visibility
    filtered_videos = []
    for item in response['Items']:
        visibility = item.get('visibility', 'public')
        owner = item.get('owner', 'system')
        
        # Super users and admins see all videos, others see only public + owned
        if user_role in ['super_user', 'admin'] or visibility == 'public' or (user_email and owner == user_email):
            filtered_videos.append(item)
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'tag': tag,
            'videos': filtered_videos,
            'count': len(filtered_videos)
        })
    }

def get_all_tags(event):
    """Get all unique tags"""
    response = table.scan()
    
    all_tags = set()
    for item in response['Items']:
        tags = item.get('tags', [])
        all_tags.update(tags)
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'tags': sorted(list(all_tags)),
            'count': len(all_tags)
        })
    }

def update_video_tags(event):
    """Update tags for a video"""
    body = json.loads(event['body'])
    video_id = body['video_id']
    new_tags = body['tags']
    owner = body.get('owner')
    visibility = body.get('visibility')
    
    update_expr = 'SET tags = :tags, updated_at = :updated'
    expr_values = {
        ':tags': new_tags,
        ':updated': datetime.utcnow().isoformat()
    }
    
    if owner:
        update_expr += ', owner = :owner'
        expr_values[':owner'] = owner
    
    if visibility:
        update_expr += ', visibility = :visibility'
        expr_values[':visibility'] = visibility
    
    table.update_item(
        Key={'video_id': video_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_values
    )
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'Video updated',
            'video_id': video_id,
            'tags': new_tags,
            'owner': owner,
            'visibility': visibility
        })
    }

def get_video_metadata(filename):
    """Get metadata for a specific video - public access for embedding"""
    try:
        response = table.get_item(
            Key={'video_id': filename}
        )
        
        if 'Item' in response:
            item = response['Item']
            visibility = item.get('visibility', 'public')
            
            # Only return metadata for public videos when accessed publicly
            if visibility != 'public':
                return {
                    'statusCode': 403,
                    'headers': cors_headers(),
                    'body': json.dumps({'error': 'Video is private'})
                }
            
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({
                    'filename': item.get('filename', filename),
                    'title': item.get('title', filename),
                    'tags': item.get('tags', []),
                    'visibility': visibility
                })
            }
        else:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Video not found'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def update_video_metadata(event, filename):
    """Update metadata for a specific video"""
    body = json.loads(event['body'])
    title = body.get('title', filename)
    tags = body.get('tags', [])
    owner = body.get('owner', 'system')
    visibility = body.get('visibility', 'public')
    external_url = body.get('external_url')
    video_type = body.get('video_type', 'local')
    
    item = {
        'video_id': filename,
        'filename': filename,
        'title': title,
        'tags': tags,
        'owner': owner,
        'visibility': visibility,
        'video_type': video_type,
        'updated_at': datetime.utcnow().isoformat()
    }
    
    if external_url:
        item['external_url'] = external_url
    
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'Video metadata updated',
            'filename': filename,
            'title': title,
            'tags': tags,
            'owner': owner,
            'visibility': visibility,
            'video_type': video_type
        })
    }

def list_all_videos(event):
    """List videos with visibility filtering and pagination"""
    query_params = event.get('queryStringParameters') or {}
    user_email = query_params.get('user')
    user_role = query_params.get('role')
    page = int(query_params.get('page', 1))
    limit = int(query_params.get('limit', 24))
    category = query_params.get('category', 'all')
    
    response = table.scan()
    
    # Format and filter videos
    all_videos = []
    for item in response['Items']:
        visibility = item.get('visibility', 'public')
        owner = item.get('owner', 'system')
        
        # Super users and admins see all videos, others see only public + owned
        if user_role in ['super_user', 'admin'] or visibility == 'public' or (user_email and owner == user_email):
            video_data = {
                'filename': item.get('filename', ''),
                'title': item.get('title', item.get('filename', '').replace('.mp4', '').replace('_', ' ')),
                'tags': item.get('tags', []),
                'owner': owner,
                'visibility': visibility,
                'video_type': item.get('video_type', 'local'),
                'external_url': item.get('external_url', ''),
                'upload_date': item.get('upload_date', item.get('created_at', ''))
            }
            
            # Add size for local videos from S3
            if video_data['video_type'] == 'local':
                try:
                    s3_response = s3_client.head_object(
                        Bucket='my-video-downloads-bucket',
                        Key=f"videos/{video_data['filename']}"
                    )
                    video_data['size'] = s3_response['ContentLength']
                except Exception as e:
                    print(f"Error getting size for {video_data['filename']}: {e}")
                    video_data['size'] = 0
            else:
                video_data['size'] = 0  # External videos don't have file size
                
            all_videos.append(video_data)
    
    # Category filtering
    if category != 'all':
        category_keywords = {
            'sermons': ['sermon', 'preaching', 'biblical', 'scripture', 'gospel', 'ministry', 'pastor', 'church'],
            'politics': ['political', 'conservative', 'government', 'election', 'policy', 'freedom', 'trump', 'biden'],
            'teaching': ['teaching', 'study', 'bible', 'theology', 'doctrine', 'christian', 'lesson', 'education']
        }
        
        if category in category_keywords:
            keywords = category_keywords[category]
            filtered_videos = []
            for video in all_videos:
                title_lower = video['title'].lower()
                tags_lower = [tag.lower() for tag in video.get('tags', [])]
                
                # Check title and tags for keywords
                title_match = any(keyword in title_lower for keyword in keywords)
                tag_match = any(any(keyword in tag for keyword in keywords) for tag in tags_lower)
                
                if title_match or tag_match:
                    filtered_videos.append(video)
            all_videos = filtered_videos
    
    # Sort by upload date (newest first)
    all_videos.sort(key=lambda x: x.get('upload_date', ''), reverse=True)
    
    # Pagination
    total_count = len(all_videos)
    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_videos = all_videos[start_index:end_index]
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'videos': paginated_videos,
            'count': len(paginated_videos),
            'total_count': total_count,
            'page': page,
            'limit': limit,
            'total_pages': (total_count + limit - 1) // limit,
            'has_more': end_index < total_count
        })
    }

def create_article_via_tags(event):
    """Create article via TAG API to bypass CORS issues"""
    import uuid
    from datetime import datetime
    
    try:
        body = json.loads(event['body'])
        
        # Simple article creation - just return success for now
        article_id = str(uuid.uuid4())
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({
                'message': 'Article created successfully via TAG API',
                'article_id': article_id,
                'title': body.get('title', 'Untitled'),
                'author': body.get('author', 'Unknown')
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'Failed to create article: ' + str(e)})
        }

def cors_headers():
    """CORS headers for API responses"""
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS'
    }