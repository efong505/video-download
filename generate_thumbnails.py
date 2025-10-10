#!/usr/bin/env python3
import boto3
import subprocess
import os
import tempfile
from pathlib import Path
import time

s3_client = boto3.client('s3')
BUCKET = 'my-video-downloads-bucket'

def generate_thumbnail_for_video(video_key):
    """Generate thumbnail for a single video"""
    temp_video_path = None
    temp_thumb_path = None
    
    try:
        video_name = Path(video_key).stem  # Remove .mp4 extension
        print(f"Processing {video_name}...")
        
        # Create temp file paths
        temp_video_path = f"temp_{video_name}.mp4"
        temp_thumb_path = f"temp_{video_name}_thumb.jpg"
        
        # Download video
        print(f"  Downloading {video_key}...")
        s3_client.download_file(BUCKET, video_key, temp_video_path)
        
        # Get video duration
        duration_cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', temp_video_path]
        duration_result = subprocess.run(duration_cmd, capture_output=True, text=True)
        duration = float(duration_result.stdout.strip())
        
        # Generate thumbnail at 50% of video duration
        timestamp = duration * 0.5
        thumb_name = f"{video_name}_thumb.jpg"
        
        print(f"  Generating thumbnail at {timestamp:.1f}s...")
        
        # Extract frame at timestamp
        cmd = ['ffmpeg', '-ss', str(timestamp), '-i', temp_video_path, '-vframes', '1', '-q:v', '2', temp_thumb_path, '-y']
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        
        if result.returncode == 0:
            # Upload thumbnail to S3
            thumb_key = f"thumbnails/{thumb_name}"
            print(f"  Uploading {thumb_key}...")
            s3_client.upload_file(temp_thumb_path, BUCKET, thumb_key, ExtraArgs={'ContentType': 'image/jpeg'})
            print(f"  SUCCESS: Created {thumb_key}")
        else:
            print(f"  ERROR: FFmpeg failed")
        
    except Exception as e:
        print(f"  ERROR: Processing {video_key}: {e}")
    
    finally:
        # Cleanup temp files
        if temp_video_path and os.path.exists(temp_video_path):
            try:
                os.unlink(temp_video_path)
            except:
                pass
        if temp_thumb_path and os.path.exists(temp_thumb_path):
            try:
                os.unlink(temp_thumb_path)
            except:
                pass

def main():
    """Generate thumbnails for all videos in the videos/ folder"""
    print("Generating thumbnails for existing videos...")
    
    # List all videos in the videos/ folder
    response = s3_client.list_objects_v2(Bucket=BUCKET, Prefix='videos/')
    
    if 'Contents' not in response:
        print("No videos found in videos/ folder")
        return
    
    video_files = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.mp4')]
    
    print(f"Found {len(video_files)} videos to process")
    
    for video_key in video_files:
        generate_thumbnail_for_video(video_key)
    
    print("\nThumbnail generation complete!")

if __name__ == '__main__':
    main()