import boto3
import subprocess
import os

# Download the video and create thumbnail locally, then upload
s3_client = boto3.client('s3')
bucket = 'my-video-downloads-bucket'
filename = '1000003114.mp4'

try:
    print("Downloading video...")
    video_path = f"temp_{filename}"
    s3_client.download_file(bucket, f"videos/{filename}", video_path)
    
    print("Generating thumbnail...")
    thumb_name = f"{filename.replace('.mp4', '')}_thumb_2.jpg"
    thumb_path = f"temp_{thumb_name}"
    
    # Generate thumbnail at 3 seconds (video is only 6 seconds long)
    cmd = ['ffmpeg', '-ss', '3', '-i', video_path, '-vframes', '1', '-q:v', '2', '-y', thumb_path]
    result = subprocess.run(cmd, capture_output=True, timeout=60)
    
    if result.returncode == 0:
        print("Uploading thumbnail...")
        thumb_key = f"thumbnails/{thumb_name}"
        s3_client.upload_file(thumb_path, bucket, thumb_key, ExtraArgs={'ContentType': 'image/jpeg'})
        print(f"Successfully created thumbnail: {thumb_key}")
        
        # Cleanup
        os.remove(video_path)
        os.remove(thumb_path)
    else:
        print(f"FFmpeg failed: {result.stderr.decode()}")
        
except Exception as e:
    print(f"Error: {e}")
    # Cleanup on error
    if os.path.exists(video_path):
        os.remove(video_path)
    if os.path.exists(thumb_path):
        os.remove(thumb_path)