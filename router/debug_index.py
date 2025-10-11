import json
import boto3
import os

lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    """
    Simplified router for debugging
    """
    print(f"Event: {json.dumps(event)}")
    
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
        
        # Parse request body for download
        body_str = event.get('body', '{}')
        print(f"Body string: {body_str}")
        
        body = json.loads(body_str)
        print(f"Parsed body: {json.dumps(body)}")
        
        url = body.get('url')
        output_name = body.get('output_name', 'video.mp4')
        tags = body.get('tags', [])
        
        if not url:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
                },
                'body': json.dumps({'error': 'Missing url parameter'})
            }
        
        print(f"Starting download for URL: {url}")
        
        # Try to invoke the downloader Lambda
        payload = {
            'url': url,
            'format': 'best',
            'output_name': output_name,
            'tags': tags
        }
        
        print(f"Invoking Lambda with payload: {json.dumps(payload)}")
        
        response = lambda_client.invoke(
            FunctionName=os.environ['DOWNLOADER_LAMBDA_ARN'],
            InvocationType='Event',  # Async
            Payload=json.dumps(payload)
        )
        
        print(f"Lambda invoke response: {response}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': json.dumps({
                'message': 'Download initiated successfully',
                'url': url,
                'output_name': output_name,
                'lambda_response': str(response)
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': json.dumps({'error': str(e)})
        }