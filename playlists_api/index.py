import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
playlists_table = dynamodb.Table('video-playlists')

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        params = event.get('queryStringParameters') or {}
        action = params.get('action', 'list')
        
        if action == 'create':
            return create_playlist(event, headers)
        elif action == 'list':
            return list_playlists(event, headers)
        elif action == 'get':
            return get_playlist(event, headers)
        elif action == 'update':
            return update_playlist(event, headers)
        elif action == 'delete':
            return delete_playlist(event, headers)
        elif action == 'add_video':
            return add_video_to_playlist(event, headers)
        elif action == 'remove_video':
            return remove_video_from_playlist(event, headers)
        else:
            return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Invalid action'})}
    except Exception as e:
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': str(e)})}

def create_playlist(event, headers):
    body = json.loads(event['body'])
    playlist_id = str(uuid.uuid4())
    
    item = {
        'playlist_id': playlist_id,
        'name': body['name'],
        'description': body.get('description', ''),
        'owner': body.get('owner', 'system'),
        'videos': [],
        'created_at': datetime.utcnow().isoformat()
    }
    
    playlists_table.put_item(Item=item)
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Playlist created', 'playlist_id': playlist_id})}

def list_playlists(event, headers):
    params = event.get('queryStringParameters') or {}
    owner = params.get('owner')
    
    if owner:
        response = playlists_table.scan(
            FilterExpression='#owner = :owner',
            ExpressionAttributeNames={'#owner': 'owner'},
            ExpressionAttributeValues={':owner': owner}
        )
    else:
        response = playlists_table.scan()
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'playlists': response['Items']})}

def get_playlist(event, headers):
    params = event.get('queryStringParameters') or {}
    playlist_id = params.get('playlist_id')
    
    if not playlist_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'playlist_id required'})}
    
    response = playlists_table.get_item(Key={'playlist_id': playlist_id})
    
    if 'Item' not in response:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Playlist not found'})}
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'playlist': response['Item']})}

def update_playlist(event, headers):
    body = json.loads(event['body'])
    playlist_id = body['playlist_id']
    
    update_expr = 'SET #name = :name, description = :desc, updated_at = :updated'
    expr_values = {
        ':name': body['name'],
        ':desc': body.get('description', ''),
        ':updated': datetime.utcnow().isoformat()
    }
    
    playlists_table.update_item(
        Key={'playlist_id': playlist_id},
        UpdateExpression=update_expr,
        ExpressionAttributeNames={'#name': 'name'},
        ExpressionAttributeValues=expr_values
    )
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Playlist updated'})}

def delete_playlist(event, headers):
    params = event.get('queryStringParameters') or {}
    playlist_id = params.get('playlist_id')
    
    if not playlist_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'playlist_id required'})}
    
    playlists_table.delete_item(Key={'playlist_id': playlist_id})
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Playlist deleted'})}

def add_video_to_playlist(event, headers):
    body = json.loads(event['body'])
    playlist_id = body['playlist_id']
    video_id = body['video_id']
    
    response = playlists_table.get_item(Key={'playlist_id': playlist_id})
    
    if 'Item' not in response:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Playlist not found'})}
    
    videos = response['Item'].get('videos', [])
    
    if video_id not in videos:
        videos.append(video_id)
        playlists_table.update_item(
            Key={'playlist_id': playlist_id},
            UpdateExpression='SET videos = :videos',
            ExpressionAttributeValues={':videos': videos}
        )
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Video added to playlist'})}

def remove_video_from_playlist(event, headers):
    body = json.loads(event['body'])
    playlist_id = body['playlist_id']
    video_id = body['video_id']
    
    response = playlists_table.get_item(Key={'playlist_id': playlist_id})
    
    if 'Item' not in response:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Playlist not found'})}
    
    videos = response['Item'].get('videos', [])
    
    if video_id in videos:
        videos.remove(video_id)
        playlists_table.update_item(
            Key={'playlist_id': playlist_id},
            UpdateExpression='SET videos = :videos',
            ExpressionAttributeValues={':videos': videos}
        )
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Video removed from playlist'})}
