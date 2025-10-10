import json
import boto3
import subprocess
import os
import re
from datetime import datetime

ecs_client = boto3.client('ecs')
lambda_client = boto3.client('lambda')
logs_client = boto3.client('logs')

def estimate_download_time(url):
    """
    Use yt-dlp to get video info and estimate download time.
    Returns dict with estimated seconds, filesize, duration, and reasoning.
    """
    try:
        # Get video info without downloading
        # Use yt-dlp from Lambda layer
        result = subprocess.run(
            ['/opt/bin/yt-dlp', '--dump-json', url],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            info = json.loads(result.stdout)
            
            # Get filesize (bytes) or duration (seconds)
            filesize = info.get('filesize') or info.get('filesize_approx', 0)
            duration = info.get('duration', 0)
            title = info.get('title', 'Unknown')
            
            # Estimate: assume 5 Mbps download speed
            # Convert to seconds: (bytes * 8 bits) / (5 * 1024 * 1024 bits/sec)
            if filesize > 0:
                estimated_seconds = (filesize * 8) / (5 * 1024 * 1024)
                # Add 20% buffer
                estimated_seconds = estimated_seconds * 1.2
                reasoning = f"Based on file size: {format_bytes(filesize)}"
            elif duration > 3600:  # > 1 hour
                estimated_seconds = 900  # Assume 15+ minutes
                reasoning = f"Long video ({format_duration(duration)}), estimated 15+ minutes"
            else:
                estimated_seconds = 300  # Default to 5 minutes
                reasoning = f"Default estimate for {format_duration(duration)} video"
            
            return {
                'seconds': estimated_seconds,
                'filesize': filesize,
                'duration': duration,
                'title': title,
                'reasoning': reasoning
            }
            
    except Exception as e:
        print(f"Error estimating: {e}")
        # Default to safe choice (Fargate) on error
        return {
            'seconds': 1000,
            'filesize': 0,
            'duration': 0,
            'title': 'Unknown',
            'reasoning': f"Error getting video info: {str(e)}"
        }
    
    return {
        'seconds': 1000,
        'filesize': 0,
        'duration': 0,
        'title': 'Unknown',
        'reasoning': 'Failed to get video information'
    }

def format_bytes(bytes_val):
    """Convert bytes to human readable format"""
    if bytes_val == 0:
        return "Unknown size"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} TB"

def format_duration(seconds):
    """Convert seconds to human readable format"""
    if seconds == 0:
        return "Unknown duration"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def calculate_cost_estimate(method, estimated_seconds):
    """Calculate cost estimate based on method and time"""
    if method == "lambda":
        # Lambda: $0.0000166667 per GB-second + $0.0000002 per request
        # Assume 1GB memory, add request cost
        gb_seconds = estimated_seconds * 1  # 1GB
        compute_cost = gb_seconds * 0.0000166667
        request_cost = 0.0000002
        total_cost = compute_cost + request_cost
        return {
            'total': total_cost,
            'breakdown': f"Compute: ${compute_cost:.6f}, Request: ${request_cost:.6f}"
        }
    else:  # fargate
        # Fargate: $0.04048 per vCPU hour + $0.004445 per GB hour
        # 0.5 vCPU, 1GB RAM
        hours = estimated_seconds / 3600
        vcpu_cost = hours * 0.5 * 0.04048
        memory_cost = hours * 1 * 0.004445
        total_cost = vcpu_cost + memory_cost
        return {
            'total': total_cost,
            'breakdown': f"vCPU: ${vcpu_cost:.6f}, Memory: ${memory_cost:.6f}"
        }

def lambda_handler(event, context):
    """
    Routes video download or checks status based on path.
    """
    try:
        # Check if this is a status request
        path = event.get('path', '')
        if '/status/' in path:
            task_id = path.split('/status/')[-1]
            return get_download_status(task_id)
        
        # Parse request body for download
        body = json.loads(event.get('body', '{}'))
        url = body.get('url')
        format_id = body.get('format', 'best')
        output_name = body.get('output_name', 'video.mp4')
        force_fargate = body.get('force_fargate', False)
        
        if not url:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({'error': 'Missing url parameter'})
            }
        
        # Estimate download time
        estimate_info = estimate_download_time(url)
        estimated_seconds = estimate_info['seconds']
        print(f"Estimated download time: {estimated_seconds}s")
        
        # Route decision: Check force_fargate first, then time estimate
        if force_fargate:
            print("Routing to Fargate (forced)")
            response = start_fargate_task(url, format_id, output_name)
            method = "fargate"
            method_reason = "Forced Fargate routing - bypassing smart routing"
        elif estimated_seconds < 720:
            print("Routing to Lambda")
            response = invoke_lambda_downloader(url, format_id, output_name)
            method = "lambda"
            method_reason = "Fast download (< 12 minutes) - using cost-effective Lambda"
        else:
            print("Routing to Fargate")
            response = start_fargate_task(url, format_id, output_name)
            method = "fargate"
            method_reason = "Long download (≥ 12 minutes) - using reliable Fargate (1hr timeout)"
        
        # Calculate cost estimates
        cost_info = calculate_cost_estimate(method, estimated_seconds)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'message': 'Download initiated',
                'video_info': {
                    'title': estimate_info['title'],
                    'size': format_bytes(estimate_info['filesize']),
                    'duration': format_duration(estimate_info['duration']),
                    'selected_format': format_id
                },
                'routing': {
                    'method': method,
                    'reason': method_reason,
                    'estimated_time': format_duration(estimated_seconds),
                    'estimated_time_seconds': estimated_seconds,
                    'reasoning': estimate_info['reasoning'],
                    'forced_fargate': force_fargate
                },
                'cost_estimate': {
                    'total_usd': f"${cost_info['total']:.6f}",
                    'breakdown': cost_info['breakdown']
                },
                'response': response,
                'task_id': extract_task_id(response)
            })
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({'error': str(e)})
        }

def invoke_lambda_downloader(url, format_id, output_name):
    """Invoke Lambda downloader function asynchronously"""
    payload = {
        'url': url,
        'format': format_id,
        'output_name': output_name
    }
    
    response = lambda_client.invoke(
        FunctionName=os.environ['DOWNLOADER_LAMBDA_ARN'],
        InvocationType='Event',  # Async
        Payload=json.dumps(payload)
    )
    
    return {'type': 'lambda', 'status': 'invoked'}

def start_fargate_task(url, format_id, output_name):
    """Start Fargate ECS task"""
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
                'environment': [
                    {'name': 'VIDEO_URL', 'value': url},
                    {'name': 'FORMAT_ID', 'value': format_id},
                    {'name': 'OUTPUT_NAME', 'value': output_name},
                    {'name': 'S3_BUCKET', 'value': os.environ['S3_BUCKET']}
                ]
            }]
        }
    )
    
    task_arn = response['tasks'][0]['taskArn']
    return {'type': 'fargate', 'task_arn': task_arn}

def extract_task_id(response):
    """Extract task ID from response"""
    if response.get('type') == 'fargate':
        task_arn = response.get('task_arn', '')
        return task_arn.split('/')[-1] if task_arn else None
    return None

def get_download_status(task_id):
    """Get download status and progress"""
    try:
        # Get task status
        task_arn = f"arn:aws:ecs:us-east-1:371751795928:task/video-downloader-cluster/{task_id}"
        
        response = ecs_client.describe_tasks(
            cluster='video-downloader-cluster',
            tasks=[task_arn]
        )
        
        if not response['tasks']:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Task not found'})
            }
        
        task = response['tasks'][0]
        task_status = task['lastStatus']
        
        # Get logs for progress
        log_stream = f"ecs/video-downloader/{task_id}"
        progress_info = get_progress_from_logs(log_stream)
        
        # Determine overall status
        if task_status == 'RUNNING':
            status = 'RUNNING'
        elif task_status == 'STOPPED':
            exit_code = task['containers'][0].get('exitCode', 1)
            status = 'STOPPED' if exit_code == 0 else 'FAILED'
        else:
            status = 'PENDING'
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'task_id': task_id,
                'status': status,
                'task_status': task_status,
                'progress': progress_info.get('progress', 'Unknown'),
                'speed': progress_info.get('speed', 'Unknown'),
                'eta': progress_info.get('eta', 'Unknown'),
                'last_update': progress_info.get('timestamp', 'Unknown')
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

def get_progress_from_logs(log_stream):
    """Parse progress from CloudWatch logs"""
    try:
        response = logs_client.get_log_events(
            logGroupName='/ecs/video-downloader',
            logStreamName=log_stream,
            startFromHead=False,
            limit=50
        )
        
        progress_info = {
            'progress': 'Starting...',
            'speed': 'Unknown',
            'eta': 'Unknown',
            'timestamp': 'Unknown'
        }
        
        # Parse recent log events for progress
        for event in reversed(response['events']):
            message = event['message']
            timestamp = datetime.fromtimestamp(event['timestamp'] / 1000).strftime('%H:%M:%S')
            
            # Look for yt-dlp progress patterns
            if '[download]' in message:
                # Pattern: [download]  45.2% of 123.45MiB at 1.23MiB/s ETA 01:23
                progress_match = re.search(r'(\d+\.\d+)%', message)
                speed_match = re.search(r'at\s+([\d\.]+\w+/s)', message)
                eta_match = re.search(r'ETA\s+(\d+:\d+)', message)
                
                if progress_match:
                    progress_info['progress'] = f"{progress_match.group(1)}%"
                if speed_match:
                    progress_info['speed'] = speed_match.group(1)
                if eta_match:
                    progress_info['eta'] = eta_match.group(1)
                progress_info['timestamp'] = timestamp
                break
            
            # Look for other status messages
            elif 'Download complete' in message:
                progress_info['progress'] = '100%'
                progress_info['speed'] = 'Complete'
                progress_info['eta'] = '00:00'
                progress_info['timestamp'] = timestamp
                break
            elif 'Uploading to S3' in message:
                progress_info['progress'] = 'Uploading...'
                progress_info['timestamp'] = timestamp
                break
        
        return progress_info
        
    except Exception as e:
        print(f"Error getting logs: {e}")
        return {
            'progress': 'Unknown',
            'speed': 'Unknown', 
            'eta': 'Unknown',
            'timestamp': 'Unknown'
        }