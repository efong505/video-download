import json
import boto3
import subprocess
import os
import urllib.parse

s3_client = boto3.client('s3')

def generate_thumbnail(bucket, video_key, output_key):
    """Generate thumbnail from S3 video"""
    try:
        # Download video to /tmp
        video_path = f"/tmp/{os.path.basename(video_key)}"
        s3_client.download_file(bucket, video_key, video_path)
        
        # Generate thumbnail at 10 seconds
        thumb_path = f"/tmp/thumb.jpg"
        cmd = [
            'ffmpeg', '-ss', '10', '-i', video_path,
            '-vframes', '1', '-q:v', '2', '-y', thumb_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        
        if result.returncode == 0:
            # Upload thumbnail
            s3_client.upload_file(
                thumb_path, bucket, output_key,
                ExtraArgs={'ContentType': 'image/jpeg'}
            )
            print(f"Generated thumbnail: {output_key}")
            return True
        else:
            print(f"FFmpeg failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return False
    finally:
        # Cleanup
        for path in [video_path, thumb_path]:
            if os.path.exists(path):
                os.remove(path)

def lambda_handler(event, context):
    """Handle S3 upload events and generate thumbnails"""
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        
        # Only process video uploads to videos/ folder
        if key.startswith('videos/') and key.endswith('.mp4'):
            filename = key.replace('videos/', '')
            base_name = filename.replace('.mp4', '')
            
            # Generate thumbnail key
            thumb_key = f"thumbnails/{base_name}_thumb_2.jpg"
            
            print(f"Processing video upload: {key}")
            
            # Check if thumbnail already exists
            try:
                s3_client.head_object(Bucket=bucket, Key=thumb_key)
                print(f"Thumbnail already exists: {thumb_key}")
                continue
            except s3_client.exceptions.NoSuchKey:
                pass
            
            # Generate thumbnail
            if generate_thumbnail(bucket, key, thumb_key):
                print(f"Successfully generated thumbnail for {filename}")
            else:
                print(f"Failed to generate thumbnail for {filename}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Thumbnail processing complete')
    }