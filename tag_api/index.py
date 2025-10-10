import json
import boto3
from datetime import datetime
import uuid

dynamodb = boto3.resource('dynamodb')
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
    
    item = {
        'video_id': video_id,
        'filename': filename,
        'title': title,
        'tags': tags,
        'upload_date': datetime.utcnow().isoformat(),
        'created_at': datetime.utcnow().isoformat()
    }
    
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'Video metadata added',
            'video_id': video_id,
            'tags': tags
        })
    }

def get_videos_by_tag(event):
    """Get videos filtered by tag"""
    tag = event['queryStringParameters'].get('tag') if event.get('queryStringParameters') else None
    
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
    
    videos = response['Items']
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'tag': tag,
            'videos': videos,
            'count': len(videos)
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
    
    table.update_item(
        Key={'video_id': video_id},
        UpdateExpression='SET tags = :tags, updated_at = :updated',
        ExpressionAttributeValues={
            ':tags': new_tags,
            ':updated': datetime.utcnow().isoformat()
        }
    )
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'Tags updated',
            'video_id': video_id,
            'tags': new_tags
        })
    }

def get_video_metadata(filename):
    """Get metadata for a specific video"""
    try:
        response = table.get_item(
            Key={'video_id': filename}
        )
        
        if 'Item' in response:
            item = response['Item']
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({
                    'filename': item.get('filename', filename),
                    'title': item.get('title', filename),
                    'tags': item.get('tags', [])
                })
            }
        else:
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({
                    'filename': filename,
                    'title': filename,
                    'tags': []
                })
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
    
    item = {
        'video_id': filename,
        'filename': filename,
        'title': title,
        'tags': tags,
        'updated_at': datetime.utcnow().isoformat()
    }
    
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'Video metadata updated',
            'filename': filename,
            'title': title,
            'tags': tags
        })
    }

def cors_headers():
    """CORS headers for API responses"""
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS'
    }