# Fix: External Video Thumbnails Not Showing

## Issue
When adding an external video (YouTube, Rumble, Facebook), the thumbnail doesn't generate or display.

## Root Cause
The `thumbnail-generator` Lambda receives `external_url` but doesn't extract thumbnails from external video platforms. It only handles local S3 videos.

## Solution
Update `thumbnail-generator/index.py` to extract thumbnails from external URLs using yt-dlp:

```python
def lambda_handler(event, context):
    filename = event['filename']
    bucket = event['bucket']
    video_type = event.get('video_type', 'local')
    external_url = event.get('external_url')
    
    if video_type == 'external' and external_url:
        # Extract thumbnail from external URL
        return generate_external_thumbnail(external_url, filename, bucket)
    else:
        # Generate from local S3 video
        return generate_local_thumbnail(filename, bucket)

def generate_external_thumbnail(url, filename, bucket):
    import subprocess
    import os
    
    try:
        # Use yt-dlp to get thumbnail URL
        result = subprocess.run([
            'yt-dlp',
            '--get-thumbnail',
            '--no-warnings',
            url
        ], capture_output=True, text=True, timeout=30)
        
        thumbnail_url = result.stdout.strip()
        
        if thumbnail_url:
            # Download thumbnail
            import requests
            response = requests.get(thumbnail_url, timeout=10)
            
            if response.status_code == 200:
                # Upload to S3
                base_name = filename.rsplit('.', 1)[0]
                s3_key = f'thumbnails/{base_name}_thumb_1.jpg'
                
                s3_client.put_object(
                    Bucket=bucket,
                    Key=s3_key,
                    Body=response.content,
                    ContentType='image/jpeg'
                )
                
                # Update metadata
                metadata_table.update_item(
                    Key={'video_id': filename},
                    UpdateExpression='SET thumbnail_url = :thumb',
                    ExpressionAttributeValues={
                        ':thumb': f'https://d271vky579caz9.cloudfront.net/{s3_key}'
                    }
                )
                
                return {'statusCode': 200, 'message': 'External thumbnail generated'}
        
        return {'statusCode': 404, 'error': 'No thumbnail found'}
        
    except Exception as e:
        print(f'Error generating external thumbnail: {e}')
        return {'statusCode': 500, 'error': str(e)}
```

## Deployment
```powershell
cd thumbnail_generator
pip install requests -t .
powershell -Command "Compress-Archive -Path * -DestinationPath function.zip -Force"
aws lambda update-function-code --function-name thumbnail-generator --zip-file fileb://function.zip
```

## Verification
1. Add external video (YouTube/Rumble URL)
2. Check S3 `thumbnails/` folder for generated thumbnail
3. Check video-metadata table for `thumbnail_url` field
4. Verify thumbnail displays in videos.html

## Alternative: Use Platform APIs
For better reliability, use platform-specific APIs:
- YouTube: `https://img.youtube.com/vi/{VIDEO_ID}/maxresdefault.jpg`
- Rumble: Extract from embed page HTML
- Facebook: Use Graph API

## Quick Fix (Frontend Only)
Update admin.html to extract thumbnail URL directly:

```javascript
async function addExternalVideo() {
    const url = document.getElementById('external-video-url').value;
    
    // Extract thumbnail URL
    let thumbnailUrl = '';
    if (url.includes('youtube.com') || url.includes('youtu.be')) {
        const videoId = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)/)?.[1];
        if (videoId) {
            thumbnailUrl = `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
        }
    }
    
    // Add to metadata
    const videoData = {
        action: 'add_video',
        filename: title.replace(/[^a-zA-Z0-9]/g, '_') + '.mp4',
        tags: tags,
        title: title,
        visibility: visibility,
        video_type: 'external',
        external_url: url,
        thumbnail_url: thumbnailUrl  // Add this
    };
    
    await fetch(TAG_API, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + authToken
        },
        body: JSON.stringify(videoData)
    });
}
```

This frontend fix works immediately without Lambda changes.
