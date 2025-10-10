import json
import boto3
import subprocess
import os
import urllib.parse

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """Handle S3 events and generate thumbnails"""
    try:
        # Handle S3 event structure
        if 'Records' in event:
            for record in event['Records']:
                bucket = record['s3']['bucket']['name']
                key = urllib.parse.unquote_plus(record['s3']['object']['key'])
                
                # Only process video uploads to videos/ folder
                if key.startswith('videos/') and key.endswith('.mp4'):
                    filename = key.replace('videos/', '')
                    process_video(bucket, filename)
        else:
            # Handle direct invocation
            filename = event['filename']
            bucket = event.get('bucket', 'my-video-downloads-bucket')
            process_video(bucket, filename)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Thumbnail processing complete'})
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def process_video(bucket, filename):
    """Process a single video file"""
    base_name = filename.replace('.mp4', '')
    thumb_key = f"thumbnails/{base_name}_thumb_2.jpg"
    
    # Check if thumbnail already exists
    try:
        s3_client.head_object(Bucket=bucket, Key=thumb_key)
        print(f"Thumbnail already exists: {thumb_key}")
        return
    except s3_client.exceptions.NoSuchKey:
        pass
    
    print(f"Processing video: {filename}")
    
    # Download video from S3
    video_path = f"/tmp/{filename}"
    s3_client.download_file(bucket, f"videos/{filename}", video_path)
    
    # Generate thumbnails
    generate_thumbnails(video_path, filename, bucket)
    
    # Cleanup
    os.remove(video_path)

def generate_thumbnails(video_path, output_name, bucket):
    """Generate thumbnail at 10 seconds"""
    try:
        base_name = output_name.rsplit('.', 1)[0]
        thumb_name = f"{base_name}_thumb_2.jpg"
        thumb_path = f"/tmp/{thumb_name}"
        
        # Extract frame at 10 seconds
        cmd = ['ffmpeg', '-ss', '10', '-i', video_path, '-vframes', '1', '-q:v', '2', '-y', thumb_path]
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        
        if result.returncode == 0:
            # Upload thumbnail
            thumb_key = f"thumbnails/{thumb_name}"
            s3_client.upload_file(thumb_path, bucket, thumb_key, ExtraArgs={'ContentType': 'image/jpeg'})
            os.remove(thumb_path)
            print(f"Generated thumbnail: {thumb_key}")
        else:
            print(f"FFmpeg failed: {result.stderr}")
            
    except Exception as e:
        print(f"Thumbnail generation failed: {e}")