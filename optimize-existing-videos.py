#!/usr/bin/env python3
"""
Re-optimize existing S3 videos with FFmpeg faststart for progressive streaming.
Downloads videos from S3, optimizes with -movflags +faststart, re-uploads.
"""

import boto3
import subprocess
import os
import sys
from datetime import datetime

# Configuration
S3_BUCKET = 'my-video-downloads-bucket'
VIDEO_PREFIX = 'videos/'
TEMP_DIR = 'temp_optimize'

s3_client = boto3.client('s3')

def list_videos():
    """List all videos in S3 bucket"""
    print(f"Scanning S3 bucket: {S3_BUCKET}/{VIDEO_PREFIX}")
    
    videos = []
    paginator = s3_client.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=VIDEO_PREFIX):
        if 'Contents' not in page:
            continue
            
        for obj in page['Contents']:
            key = obj['Key']
            size_mb = obj['Size'] / (1024 * 1024)
            
            # Only process video files
            if key.endswith(('.mp4', '.webm', '.mkv')):
                videos.append({
                    'key': key,
                    'filename': os.path.basename(key),
                    'size_mb': size_mb,
                    'last_modified': obj['LastModified']
                })
    
    return videos

def check_if_optimized(video_path):
    """Check if video already has faststart (moov atom at beginning)"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 
             'format_tags=major_brand', '-of', 'default=noprint_wrappers=1:nokey=1', 
             video_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Simple heuristic: if moov atom is at beginning, file is optimized
        # More accurate: check file structure, but this is faster
        file_size = os.path.getsize(video_path)
        
        # Read first 8KB to check for moov atom
        with open(video_path, 'rb') as f:
            header = f.read(8192)
            if b'moov' in header:
                return True
        
        return False
    except Exception as e:
        print(f"  Warning: Could not check optimization status: {e}")
        return False

def optimize_video(video_key, filename):
    """Download, optimize, and re-upload video"""
    
    # Create temp directory
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    original_path = os.path.join(TEMP_DIR, filename)
    optimized_path = os.path.join(TEMP_DIR, f"optimized_{filename}")
    
    try:
        # Download from S3
        print(f"  Downloading {filename}...")
        s3_client.download_file(S3_BUCKET, video_key, original_path)
        
        file_size_mb = os.path.getsize(original_path) / (1024 * 1024)
        print(f"  Downloaded: {file_size_mb:.1f} MB")
        
        # Check if already optimized
        if check_if_optimized(original_path):
            print(f"  ✓ Already optimized, skipping")
            os.remove(original_path)
            return 'skipped'
        
        # Optimize with FFmpeg
        print(f"  Optimizing with FFmpeg...")
        cmd = [
            'ffmpeg',
            '-i', original_path,
            '-c', 'copy',  # Copy streams without re-encoding
            '-movflags', '+faststart',  # Move moov atom to beginning
            '-y',  # Overwrite output
            optimized_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode != 0:
            print(f"  ✗ FFmpeg failed: {result.stderr}")
            return 'failed'
        
        # Verify optimized file
        if not os.path.exists(optimized_path):
            print(f"  ✗ Optimized file not created")
            return 'failed'
        
        optimized_size_mb = os.path.getsize(optimized_path) / (1024 * 1024)
        print(f"  Optimized: {optimized_size_mb:.1f} MB")
        
        # Backup original (rename with .backup suffix)
        backup_key = f"{video_key}.backup"
        print(f"  Creating backup...")
        s3_client.copy_object(
            Bucket=S3_BUCKET,
            CopySource={'Bucket': S3_BUCKET, 'Key': video_key},
            Key=backup_key
        )
        
        # Upload optimized version
        print(f"  Uploading optimized version...")
        content_type = 'video/mp4' if filename.endswith('.mp4') else 'video/webm'
        s3_client.upload_file(
            optimized_path,
            S3_BUCKET,
            video_key,
            ExtraArgs={
                'ContentType': content_type,
                'ContentDisposition': 'inline'
            }
        )
        
        print(f"  ✓ Optimized and uploaded")
        
        # Cleanup
        os.remove(original_path)
        os.remove(optimized_path)
        
        return 'success'
        
    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout during optimization")
        return 'timeout'
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return 'error'
    finally:
        # Cleanup temp files
        for path in [original_path, optimized_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass

def main():
    print("=" * 60)
    print("S3 Video Optimization Script")
    print("Adds FFmpeg faststart for progressive streaming")
    print("=" * 60)
    print()
    
    # List all videos
    videos = list_videos()
    
    if not videos:
        print("No videos found in S3 bucket")
        return
    
    print(f"\nFound {len(videos)} videos")
    print()
    
    # Show summary
    total_size_mb = sum(v['size_mb'] for v in videos)
    print(f"Total size: {total_size_mb:.1f} MB ({total_size_mb/1024:.2f} GB)")
    print()
    
    # Filter options
    print("Filter options:")
    print("1. Optimize ALL videos")
    print("2. Optimize videos larger than 100 MB")
    print("3. Optimize videos larger than 500 MB")
    print("4. Optimize videos larger than 1 GB")
    print("5. Exit")
    print()
    
    choice = input("Select option (1-5): ").strip()
    
    if choice == '5':
        print("Exiting...")
        return
    
    # Filter videos based on choice
    if choice == '2':
        videos = [v for v in videos if v['size_mb'] > 100]
    elif choice == '3':
        videos = [v for v in videos if v['size_mb'] > 500]
    elif choice == '4':
        videos = [v for v in videos if v['size_mb'] > 1024]
    
    if not videos:
        print("No videos match the filter criteria")
        return
    
    print(f"\nWill optimize {len(videos)} videos")
    print()
    
    # Confirm
    confirm = input("Continue? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Cancelled")
        return
    
    print()
    print("=" * 60)
    print("Starting optimization...")
    print("=" * 60)
    print()
    
    # Process each video
    results = {'success': 0, 'skipped': 0, 'failed': 0, 'timeout': 0, 'error': 0}
    
    for i, video in enumerate(videos, 1):
        print(f"[{i}/{len(videos)}] {video['filename']} ({video['size_mb']:.1f} MB)")
        
        result = optimize_video(video['key'], video['filename'])
        results[result] += 1
        
        print()
    
    # Summary
    print("=" * 60)
    print("OPTIMIZATION COMPLETE")
    print("=" * 60)
    print(f"✓ Success:  {results['success']}")
    print(f"⊘ Skipped:  {results['skipped']} (already optimized)")
    print(f"✗ Failed:   {results['failed']}")
    print(f"⏱ Timeout:  {results['timeout']}")
    print(f"⚠ Error:    {results['error']}")
    print()
    print("Backups created with .backup suffix")
    print("To restore: aws s3 cp s3://bucket/videos/file.mp4.backup s3://bucket/videos/file.mp4")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
