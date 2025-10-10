import json
import boto3
import os
from datetime import datetime

sns_client = boto3.client('sns')
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:371751795928:video-download-notifications'

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
        
        # Send initiation notification
        try:
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="🚀 Video Download Started",
                Message=f"A new video download has been initiated.\n\n"
                       f"URL: {url}\n"
                       f"Output: {body.get('output_name', 'video.mp4')}\n"
                       f"Title: {body.get('title', 'Not specified')}\n"
                       f"Tags: {', '.join(body.get('tags', [])) or 'None'}\n"
                       f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
            )
        except Exception as e:
            print(f"Failed to send initiation notification: {e}")
        
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