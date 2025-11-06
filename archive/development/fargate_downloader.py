import os
import boto3
import subprocess
from datetime import datetime
from cookie_manager import get_fresh_youtube_cookies, test_cookies

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def get_best_format(url):
    """
    Get the best available format for the video by parsing format list.
    """
    try:
        # Get available formats
        result = subprocess.run(
            ['yt-dlp', '--list-formats', url],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"Format listing failed: {result.stderr}")
            return 'best[height<=2160]'  # fallback (Fargate can handle 4K)
        
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
                            # Fargate can handle up to 4K (2160p)
                            if height <= 2160 and height > best_resolution:
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
        return 'best[height<=2160]'
        
    except Exception as e:
        print(f"Error getting formats: {e}")
        return 'best[height<=2160]'

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

def main():
    try:
        url = os.environ['VIDEO_URL']
        format_id = os.environ.get('FORMAT_ID', None)
        output_name = os.environ['OUTPUT_NAME']
        tags = os.environ.get('TAGS', '').split(',') if os.environ.get('TAGS') else []
        bucket = os.environ['S3_BUCKET']
        
        output_path = f"/tmp/{output_name}"
        
        # Get best format if not specified
        if not format_id or format_id == 'best':
            format_id = get_best_format(url)
        
        print(f"Final selected format: {format_id}")
        print("Attempting download...")
        
        # Build command - NO RE-ENCODING for speed
        cmd = [
            'yt-dlp',
            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            '--add-header', 'Accept-Language:en-US,en;q=0.9',
            '--extractor-args', 'youtube:player_client=web,mweb',
            '--no-check-certificate',
            '-f', format_id,
            '--merge-output-format', 'mp4',  # Just remux to MP4 container
            '-o', output_path, url
        ]
        
        print(f"Executing: {' '.join(cmd)}")
        print(f"Selected format: {format_id}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=2700)  # 45 minute timeout
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            exit(1)
            
        print("Download complete, uploading to S3...")
        
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
            ExtraArgs={'ContentType': content_type}
        )
        
        print(f"Successfully uploaded to s3://{bucket}/{video_key}")
        
        # Save metadata to DynamoDB
        if tags:
            try:
                table = dynamodb.Table('video-metadata')
                table.put_item(
                    Item={
                        'video_id': output_name,
                        'tags': tags,
                        'upload_date': datetime.now().isoformat(),
                        's3_key': video_key,
                        'url': url
                    }
                )
                print(f"Saved metadata for {output_name} with tags: {tags}")
            except Exception as e:
                print(f"Failed to save metadata: {e}")
        
        # Generate thumbnails in thumbnails/ directory
        generate_thumbnails(output_path, output_name, bucket)
        
        # Cleanup video file
        os.remove(output_path)
        
    except subprocess.TimeoutExpired:
        print("Download timeout: Process exceeded 45 minute limit")
        print("Possible causes: Live stream, very large file, or network issues")
        exit(2)  # Different exit code for timeout
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(3)
    


if __name__ == '__main__':
    main()