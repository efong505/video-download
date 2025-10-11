import json
import boto3
import os

def lambda_handler(event, context):
    try:
        # Handle CORS preflight
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
                },
                'body': ''
            }
        
        # Handle status requests (GET)
        if event.get('httpMethod') == 'GET':
            query_params = event.get('queryStringParameters') or {}
            if query_params.get('action') == 'status':
                return {
                    'statusCode': 200,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'active': [], 'recent': []})
                }
        
        # Parse request body (POST)
        body = json.loads(event.get('body', '{}'))
        url = body.get('url')
        
        if not url:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Missing url parameter'})
            }
        
        # Just invoke the downloader Lambda directly
        lambda_client = boto3.client('lambda')
        lambda_client.invoke(
            FunctionName='video-downloader',
            InvocationType='Event',
            Payload=json.dumps({
                'url': url,
                'format': 'best',
                'output_name': body.get('output_name', 'video.mp4'),
                'title': body.get('title', ''),
                'tags': body.get('tags', [])
            })
        )
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Download started'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }