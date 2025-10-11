import json
import boto3
import os

lambda_client = boto3.client('lambda')
ecs_client = boto3.client('ecs')

def lambda_handler(event, context):
    """
    Simple router without yt-dlp estimation
    """
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
        body = json.loads(event.get('body', '{}'))
        url = body.get('url')
        format_id = body.get('format', 'best')
        output_name = body.get('output_name', 'video.mp4')
        force_fargate = body.get('force_fargate', False)
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
        
        # Simple routing: use Fargate if forced, otherwise Lambda
        if force_fargate:
            response = start_fargate_task(url, format_id, output_name, tags)
            method = "fargate"
        else:
            response = invoke_lambda_downloader(url, format_id, output_name, tags)
            method = "lambda"
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': json.dumps({
                'message': 'Download initiated',
                'method': method,
                'url': url,
                'output_name': output_name
            })
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
            },
            'body': json.dumps({'error': str(e)})
        }

def invoke_lambda_downloader(url, format_id, output_name, tags):
    """Invoke Lambda downloader function asynchronously"""
    payload = {
        'url': url,
        'format': format_id,
        'output_name': output_name,
        'tags': tags
    }
    
    response = lambda_client.invoke(
        FunctionName=os.environ['DOWNLOADER_LAMBDA_ARN'],
        InvocationType='Event',  # Async
        Payload=json.dumps(payload)
    )
    
    return {'type': 'lambda', 'status': 'invoked'}

def start_fargate_task(url, format_id, output_name, tags):
    """Start Fargate ECS task"""
    environment = [
        {'name': 'VIDEO_URL', 'value': url},
        {'name': 'FORMAT_ID', 'value': format_id},
        {'name': 'OUTPUT_NAME', 'value': output_name},
        {'name': 'S3_BUCKET', 'value': os.environ['S3_BUCKET']}
    ]
    
    if tags:
        environment.append({'name': 'TAGS', 'value': ','.join(tags)})
    
    response = ecs_client.run_task(
        cluster=os.environ['ECS_CLUSTER_NAME'],
        taskDefinition=os.environ['ECS_TASK_DEFINITION'],
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': os.environ['SUBNET_IDS'].split(','),
                'assignPublicIp': 'ENABLED'
            }
        },
        overrides={
            'containerOverrides': [{
                'name': 'video-downloader',
                'environment': environment
            }]
        }
    )
    
    task_arn = response['tasks'][0]['taskArn']
    return {'type': 'fargate', 'task_arn': task_arn}