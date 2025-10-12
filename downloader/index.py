import json
import boto3
import subprocess
import os
from datetime import datetime

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client('sns')
jobs_table = dynamodb.Table('download-jobs')

SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:371751795928:video-download-notifications'

def send_notification(subject, message):
    """Send SNS notification"""
    try:
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
        print(f"SNS notification sent: {subject}")
    except Exception as e:
        print(f"Failed to send SNS notification: {e}")

def update_job_status(job_id, status, progress=None, error=None):
    """Update job status in DynamoDB"""
    if not job_id:
        return
    
    try:
        update_expr = 'SET #status = :status, updated_at = :updated'
        expr_values = {
            ':status': status,
            ':updated': datetime.now().isoformat()
        }
        expr_names = {'#status': 'status'}
        
        if progress is not None:
            update_expr += ', progress = :progress'
            expr_values[':progress'] = progress
        
        if error:
            update_expr += ', error_message = :error'
            expr_values[':error'] = error
        
        if status == 'completed':
            update_expr += ', completed_at = :completed'
            expr_values[':completed'] = datetime.now().isoformat()
        
        jobs_table.update_item(
            Key={'job_id': job_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values,
            ExpressionAttributeNames=expr_names
        )
        print(f"Updated job {job_id} status to {status}")
    except Exception as e:
        print(f"Failed to update job status: {e}")

def generate_thumbnails(video_path, output_name, bucket):
    """Generate thumbnails at 10%, 50%, 90% of video duration"""
    try:
        # Get video duration
        duration_cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', video_path]
        duration_result = subprocess.run(duration_cmd, capture_output=True, text=True)
        duration = float(duration_result.stdout.strip())
        
        timestamps = [duration * 0.1, duration * 0.5, duration * 0.9]  # 10%, 50%, 90%
        base_name = output_name.rsplit('.', 1)[0]  # Remove extension
        
        for i, timestamp in enumerate(timestamps):
            thumb_name = f"{base_name}_thumb_{i+1}.jpg"
            thumb_path = f"/tmp/{thumb_name}"
            
            # Extract frame at timestamp
            cmd = ['ffmpeg', '-ss', str(timestamp), '-i', video_path, '-vframes', '1', '-q:v', '2', thumb_path]
            subprocess.run(cmd, capture_output=True, timeout=30)
            
            # Upload thumbnail to thumbnails/ directory
            thumb_key = f"thumbnails/{thumb_name}"
            s3_client.upload_file(thumb_path, bucket, thumb_key, ExtraArgs={'ContentType': 'image/jpeg'})
            os.remove(thumb_path)
            print(f"Uploaded thumbnail: {thumb_key}")
            
    except Exception as e:
        print(f"Thumbnail generation failed: {e}")

def get_best_format(url):
    """
    Get the best available format for the video by parsing format list.
    """
    try:
        # Keep original format selection logic
        
        # Get available formats
        result = subprocess.run(
            ['/opt/bin/yt-dlp', '--list-formats', url],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"Format listing failed: {result.stderr}")
            return 'best[height<=1080]'  # fallback
        
        formats = result.stdout
        print(f"Available formats:\n{formats}")
        
        # Parse format lines to find best HLS format
        best_format = None
        best_resolution = 0
        
        for line in formats.split('\n'):
            if 'hls-' in line and 'mp4' in line:
                parts = line.split()
                if len(parts) >= 3:
                    format_id = parts[0]  # e.g., 'hls-4500'
                    resolution_part = parts[2]  # e.g., '1920x1080'
                    
                    # Extract height from resolution (e.g., 1080 from '1920x1080')
                    if 'x' in resolution_part:
                        try:
                            height = int(resolution_part.split('x')[1])
                            # Prefer highest resolution up to 1080p for Lambda, 2160p for Fargate
                            if height <= 1080 and height > best_resolution:
                                best_resolution = height
                                best_format = format_id
                                print(f"Found format: {format_id} ({resolution_part})")
                        except ValueError:
                            continue
        
        if best_format:
            print(f"Selected best format: {best_format} ({best_resolution}p)")
            return best_format
        
        # Fallback to best available with reasonable height limit
        print("No HLS formats found, using fallback")
        return 'best[height<=1080]'
        
    except Exception as e:
        print(f"Error getting formats: {e}")
        return 'best[height<=1080]'

def lambda_handler(event, context):
    """
    Downloads video using yt-dlp and uploads to S3.
    """
    try:
        job_id = event.get('job_id')
        url = event['url']
        format_id = event.get('format', None)
        output_name = event['output_name']
        title = event.get('title', '')
        tags = event.get('tags', [])
        owner = event.get('owner', 'system')
        visibility = event.get('visibility', 'public')
        bucket = os.environ['S3_BUCKET']
        
        # Update job status to processing
        update_job_status(job_id, 'processing', 10)
        
        # Download to /tmp (Lambda's writable directory)
        output_path = f"/tmp/{output_name}"
        
        # Get best format if not specified
        if not format_id or format_id == 'best':
            format_id = get_best_format(url)
        
        print(f"Final selected format: {format_id}")
        
        # Build command with selected format - NO RE-ENCODING for speed
        cmd = [
            '/opt/bin/yt-dlp',
            '-f', format_id,
            '--merge-output-format', 'mp4',  # Just remux to MP4 container
            '-o', output_path
        ]
        
        # No special platform handling
        
        cmd.append(url)
        
        print(f"Executing: {' '.join(cmd)}")
        print(f"Using format: {format_id}")
        
        # Update job status to downloading
        update_job_status(job_id, 'downloading', 30)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=840  # 14 minutes (safety margin)
        )
        
        print(f"yt-dlp stdout: {result.stdout}")
        print(f"yt-dlp stderr: {result.stderr}")
        
        if result.returncode != 0:
            update_job_status(job_id, 'failed', error=f"Download failed: {result.stderr}")
            raise Exception(f"Download failed: {result.stderr}")
        
        print("Download complete, uploading to S3...")
        update_job_status(job_id, 'processing', 70)
        
        # Detect content type based on file extension
        if output_name.endswith('.mp4'):
            content_type = 'video/mp4'
        elif output_name.endswith('.webm'):
            content_type = 'video/webm'
        elif output_name.endswith('.mkv'):
            content_type = 'video/x-matroska'
        else:
            content_type = 'video/mp4'  # default
    
        
        # Upload video to videos/ directory
        video_key = f"videos/{output_name}"
        s3_client.upload_file(
            output_path,
            bucket,
            video_key,
            ExtraArgs={
                'ContentType': content_type,
                'ContentDisposition': 'inline'
            }
        )
        
        # Generate thumbnails in thumbnails/ directory
        generate_thumbnails(output_path, output_name, bucket)
        
        # Cleanup
        os.remove(output_path)
        
        print(f"Successfully uploaded to s3://{bucket}/{video_key}")
        
        # Update job status to completed
        update_job_status(job_id, 'completed', 100)
        
        # Send success notification
        send_notification(
            "✅ Video Download Successful",
            f"Video '{title or output_name}' has been successfully downloaded and uploaded.\n\n"
            f"Filename: {output_name}\n"
            f"URL: {url}\n"
            f"S3 Location: s3://{bucket}/{video_key}\n"
            f"Tags: {', '.join(tags) if tags else 'None'}\n"
            f"Owner: {owner}\n"
            f"Visibility: {visibility}\n"
            f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
        )
        
        # Save metadata to DynamoDB
        try:
            table = dynamodb.Table('video-metadata')
            # Use custom title if provided, otherwise use filename without extension
            display_title = title if title else output_name.rsplit('.', 1)[0]
            
            table.put_item(
                Item={
                    'video_id': output_name,
                    'filename': output_name,
                    'title': display_title,
                    'tags': tags,
                    'upload_date': datetime.now().isoformat(),
                    's3_key': video_key,
                    'url': url,
                    'owner': owner,
                    'visibility': visibility
                }
            )
            print(f"Saved metadata for {output_name} with title: '{display_title}', tags: {tags}, owner: {event.get('owner', 'system')}, visibility: {event.get('visibility', 'public')}")
        except Exception as e:
            print(f"Failed to save metadata: {e}")
        
        # Generate presigned URL with inline disposition
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket,
                'Key': video_key,
                'ResponseContentDisposition': 'inline',
                'ResponseContentType': content_type
            },
            ExpiresIn=86400  # 24 hours
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Download complete',
                's3_location': f"s3://{bucket}/{video_key}",
                'playback_url': presigned_url
            })
        }
        
    except subprocess.TimeoutExpired:
        print("Lambda timeout approaching, download took too long")
        update_job_status(event.get('job_id'), 'failed', error='Download timeout - Lambda time limit exceeded')
        send_notification(
            "⏰ Video Download Taking Too Long",
            f"Video download is taking longer than expected and may have timed out.\n\n"
            f"URL: {event.get('url', 'Unknown')}\n"
            f"Output: {event.get('output_name', 'Unknown')}\n"
            f"Owner: {event.get('owner', 'Unknown')}\n"
            f"This may require manual intervention or using Fargate for longer videos.\n"
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
        )
        return {
            'statusCode': 408,
            'body': json.dumps({'error': 'Download timeout'})
        }
    except Exception as e:
        print(f"Error: {e}")
        update_job_status(event.get('job_id'), 'failed', error=str(e))
        send_notification(
            "❌ Video Download Failed",
            f"Video download has failed with an error.\n\n"
            f"URL: {event.get('url', 'Unknown')}\n"
            f"Output: {event.get('output_name', 'Unknown')}\n"
            f"Owner: {event.get('owner', 'Unknown')}\n"
            f"Error: {str(e)}\n"
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
        )
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }