#!/usr/bin/env python3
"""
Generate thumbnails for videos that don't have them
"""
import boto3
import requests
import subprocess
import os
import tempfile

s3_client = boto3.client('s3')
BUCKET = 'my-video-downloads-bucket'
CLOUDFRONT_URL = 'https://christianconservativestoday.com'

def generate_thumbnail_from_url(video_url, output_path):
    """Generate thumbnail from video URL using ffmpeg"""
    try:
        # Generate thumbnail at 10% of video duration
        cmd = [
            'ffmpeg', '-ss', '10', '-i', video_url, 
            '-vframes', '1', '-q:v', '2', '-y', output_path
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        return result.returncode == 0
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return False

def main():
    # Get all videos
    response = s3_client.list_objects_v2(Bucket=BUCKET, Prefix='videos/')
    videos = []
    if 'Contents' in response:
        videos = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.mp4')]
    
    # Get all thumbnails
    response = s3_client.list_objects_v2(Bucket=BUCKET, Prefix='thumbnails/')
    thumbnails = set()
    if 'Contents' in response:
        thumbnails = {obj['Key'] for obj in response['Contents']}
    
    # Find videos without thumbnails
    missing_thumbnails = []
    for video_key in videos:
        filename = video_key.replace('videos/', '')
        base_name = filename.replace('.mp4', '')
        
        # Check if any thumbnail exists for this video
        has_thumbnail = (
            f"thumbnails/{base_name}_thumb.jpg" in thumbnails or
            f"thumbnails/{base_name}_thumb_1.jpg" in thumbnails or
            f"thumbnails/{base_name}_thumb_2.jpg" in thumbnails
        )
        
        if not has_thumbnail:
            missing_thumbnails.append((video_key, filename, base_name))
    
    print(f"Found {len(missing_thumbnails)} videos without thumbnails:")
    for video_key, filename, base_name in missing_thumbnails:
        print(f"  - {filename}")
    
    # Generate missing thumbnails
    for video_key, filename, base_name in missing_thumbnails:
        print(f"\nGenerating thumbnail for {filename}...")
        
        video_url = f"{CLOUDFRONT_URL}/{video_key}"
        
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            if generate_thumbnail_from_url(video_url, tmp_file.name):
                # Upload thumbnail
                thumb_key = f"thumbnails/{base_name}_thumb_2.jpg"
                try:
                    s3_client.upload_file(
                        tmp_file.name, 
                        BUCKET, 
                        thumb_key,
                        ExtraArgs={'ContentType': 'image/jpeg'}
                    )
                    print(f"  SUCCESS: Uploaded {thumb_key}")
                except Exception as e:
                    print(f"  ERROR: Failed to upload: {e}")
            else:
                print(f"  ERROR: Failed to generate thumbnail")
            
            # Cleanup
            os.unlink(tmp_file.name)

if __name__ == '__main__':
    main()