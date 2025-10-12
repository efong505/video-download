import json
import boto3
import os
import uuid
from datetime import datetime
from decimal import Decimal

sns_client = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')
jobs_table = dynamodb.Table('download-jobs')
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
                return get_job_status()
        
        
        # Parse request body (POST)
        body = json.loads(event.get('body', '{}'))
        url = body.get('url')
        owner_email = body.get('owner', 'system')
        
        if not url:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Missing url parameter'})
            }
        
        # Check storage quota for non-system users
        if owner_email != 'system':
            quota_check = check_storage_quota(owner_email)
            if not quota_check['allowed']:
                return {
                    'statusCode': 403,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({
                        'error': 'Storage quota exceeded',
                        'message': quota_check['message'],
                        'current_usage': quota_check['usage']
                    })
                }
        
        # Create job entry
        job_id = str(uuid.uuid4())
        output_name = body.get('output_name', 'video.mp4')
        
        try:
            jobs_table.put_item(
                Item={
                    'job_id': job_id,
                    'url': url,
                    'filename': output_name,
                    'title': body.get('title', ''),
                    'tags': body.get('tags', []),
                    'status': 'pending',
                    'started_at': datetime.now().isoformat(),
                    'progress': 0
                }
            )
        except Exception as e:
            print(f"Failed to create job entry: {e}")
        
        # Send initiation notification
        try:
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="🚀 Video Download Started",
                Message=f"A new video download has been initiated.\n\n"
                       f"Job ID: {job_id}\n"
                       f"URL: {url}\n"
                       f"Output: {output_name}\n"
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
                'job_id': job_id,
                'url': url,
                'format': 'best',
                'output_name': output_name,
                'title': body.get('title', ''),
                'tags': body.get('tags', []),
                'owner': body.get('owner', 'system'),
                'visibility': body.get('visibility', 'public')
            })
        )
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'Download started',
                'job_id': job_id
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

def check_storage_quota(owner_email):
    """Check if user has available storage quota"""
    try:
        users_table = dynamodb.Table('users')
        
        # Get user by email
        response = users_table.query(
            IndexName='email-index',
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={':email': owner_email}
        )
        
        if not response['Items']:
            return {'allowed': False, 'message': 'User not found', 'usage': {}}
        
        user = response['Items'][0]
        storage_used = user.get('storage_used', 0)
        storage_limit = user.get('storage_limit', 2147483648)  # 2GB default
        video_count = user.get('video_count', 0)
        video_limit = user.get('video_limit', 50)
        
        # Check video count limit
        if video_limit > 0 and video_count >= video_limit:
            return {
                'allowed': False,
                'message': f'Video limit reached ({video_count}/{video_limit}). Upgrade your plan to upload more videos.',
                'usage': {
                    'storage_used': storage_used,
                    'storage_limit': storage_limit,
                    'video_count': video_count,
                    'video_limit': video_limit
                }
            }
        
        # Check storage limit (allow some buffer for video processing)
        storage_buffer = 0.9  # Use 90% of limit as threshold
        if storage_limit > 0 and storage_used >= (storage_limit * storage_buffer):
            return {
                'allowed': False,
                'message': f'Storage limit nearly reached ({storage_used / (1024**3):.1f}GB / {storage_limit / (1024**3):.1f}GB). Upgrade your plan for more storage.',
                'usage': {
                    'storage_used': storage_used,
                    'storage_limit': storage_limit,
                    'video_count': video_count,
                    'video_limit': video_limit
                }
            }
        
        return {
            'allowed': True,
            'message': 'Quota available',
            'usage': {
                'storage_used': storage_used,
                'storage_limit': storage_limit,
                'video_count': video_count,
                'video_limit': video_limit
            }
        }
        
    except Exception as e:
        print(f"Error checking quota: {e}")
        return {'allowed': True, 'message': 'Quota check failed, allowing download', 'usage': {}}

def get_job_status():
    try:
        # Get all jobs (scan without filter)
        response = jobs_table.scan()
        jobs = response.get('Items', [])
        
        # Filter jobs from last 24 hours in Python
        from datetime import timedelta
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        recent_jobs_filtered = []
        for job in jobs:
            try:
                job_time = datetime.fromisoformat(job.get('started_at', ''))
                if job_time > cutoff_time:
                    recent_jobs_filtered.append(job)
            except:
                # Include jobs with invalid timestamps
                recent_jobs_filtered.append(job)
        
        # Separate active and completed jobs
        active_jobs = [job for job in recent_jobs_filtered if job.get('status') in ['pending', 'processing', 'downloading']]
        recent_jobs = [job for job in recent_jobs_filtered if job.get('status') in ['completed', 'failed']]
        
        # Sort by started_at (most recent first)
        active_jobs.sort(key=lambda x: x.get('started_at', ''), reverse=True)
        recent_jobs.sort(key=lambda x: x.get('started_at', ''), reverse=True)
        
        # Convert Decimal objects to int/float for JSON serialization
        def convert_decimals(obj):
            if isinstance(obj, list):
                return [convert_decimals(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: convert_decimals(value) for key, value in obj.items()}
            elif isinstance(obj, Decimal):
                return int(obj) if obj % 1 == 0 else float(obj)
            return obj
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'active': convert_decimals(active_jobs[:10]),
                'recent': convert_decimals(recent_jobs[:20])
            })
        }
    except Exception as e:
        print(f"Error getting job status: {e}")
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'active': [], 'recent': []})
        }