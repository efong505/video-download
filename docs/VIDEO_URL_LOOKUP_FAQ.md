# Video URL Lookup FAQ

---

## 🔄 Chat Context Prompt

To restart a chat session with this context, use the following prompt:

```
I need help with my AWS video downloader project. The project uses:
- Lambda functions for video downloading (downloader/index.py)
- Router Lambda for job management (router/index.py)
- DynamoDB tables: 'video-metadata' and 'download-jobs'
- yt-dlp for video extraction
- S3 for video storage

I want to understand how to:
1. Find the original source URL for downloaded videos
2. Query DynamoDB tables to retrieve video metadata
3. Identify which video formats include both audio and video streams
4. Search for specific videos by title or keywords

Please reference the documentation in docs/VIDEO_URL_LOOKUP_FAQ.md for context.
```

---

## Q: How do I find out what URL was used to download a video?

### A: General Methods

The URL used to download a video can be found through several approaches:

#### Browser-based methods:
- **Developer Tools**: Press F12 → Network tab → filter by media/video → look for video file requests
- **Browser History**: Check your download history (Ctrl+J in Chrome/Edge, Ctrl+Shift+Y in Firefox)
- **View Page Source**: Right-click → View Source → search for video tags or URLs

#### Command-line tools:
- **yt-dlp**: `yt-dlp --get-url [video_page_url]` - shows direct download URLs
- **youtube-dl**: `youtube-dl --get-url [video_page_url]` - similar functionality
- **curl with verbose**: `curl -v [url]` - shows redirect chains and final URLs

#### Programmatic approaches:
```python
import requests

# Get final URL after redirects
response = requests.head(url, allow_redirects=True)
final_url = response.url
```

#### File metadata:
- **Windows**: Right-click file → Properties → Details tab
- **macOS**: Get Info → More Info section
- **Linux**: `exiftool filename.mp4` or `ffprobe filename.mp4`

---

## Q: How do I find the URL for a specific video in this project?

### A: Project-Specific Solution

In this video downloader project, URLs are stored in DynamoDB tables.

#### Method 1: Query by filename
```python
import boto3

def get_video_url(filename):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('video-metadata')
    
    response = table.get_item(Key={'video_id': filename})
    if 'Item' in response:
        return response['Item']['url']
    return None
```

#### Method 2: Query by job ID
```python
def get_url_by_job_id(job_id):
    dynamodb = boto3.resource('dynamodb')
    jobs_table = dynamodb.Table('download-jobs')
    
    response = jobs_table.get_item(Key={'job_id': job_id})
    if 'Item' in response:
        return response['Item']['url']
    return None
```

#### Method 3: Search by title/keywords
```python
import boto3

def find_video_url(search_term):
    dynamodb = boto3.resource('dynamodb')
    
    # Search in video-metadata table
    metadata_table = dynamodb.Table('video-metadata')
    response = metadata_table.scan()
    
    for item in response['Items']:
        title = item.get('title', '').lower()
        if search_term.lower() in title:
            print(f"Title: {item.get('title')}")
            print(f"Filename: {item.get('filename')}")
            print(f"URL: {item.get('url')}")
            print(f"Upload Date: {item.get('upload_date')}")
```

#### AWS CLI approach:
```bash
# Get URL from video metadata
aws dynamodb get-item --table-name video-metadata --key '{"video_id":{"S":"filename.mp4"}}'

# Get URL from job record
aws dynamodb get-item --table-name download-jobs --key '{"job_id":{"S":"your-job-id"}}'
```

---

## Q: How would I find the "Chicago ICE Arrest Over 1,500 Illegals" URL?

### A: Specific Example

Using the search script created for this project:

**Result:**
- **Title:** Chicago ICE Arrest Over 1,500 Illegals
- **Filename:** chicago-ice.mp4
- **URL:** https://x.com/DHSgov/status/1977881560641638834
- **Upload Date:** 2025-10-14T20:40:27.072988
- **Job ID:** e8032503-ccde-43a0-ab52-b303512a224e
- **Status:** completed

This video was downloaded from a Twitter/X post by the Department of Homeland Security (@DHSgov).

---

## Q: Which video format has both video and audio?

### A: Format Selection Guide

When examining yt-dlp format output, formats are categorized as follows:

#### Formats with BOTH video and audio:
- **http-632** (320x568, ~6.15MiB) - lowest quality with audio
- **http-950** (480x852, ~9.24MiB) - medium quality with audio  
- **http-2176** (720x1280, ~21.16MiB) - **recommended** high quality with audio
- **http-10368** (1080x1920, ~100.83MiB) - highest quality with audio

#### Formats with ONLY video or audio:
- **hls-audio-*** formats - audio only streams
- **hls-*** formats (without "audio" in name) - video only streams

### Recommendation:
For the downloader project, use **http-2176** for 720p quality with reasonable file size, or **http-10368** for maximum 1080p quality.

To use a specific format, modify the format parameter from 'best' to the specific format ID like 'http-2176'.

---

## Storage Locations

### DynamoDB Tables:
1. **video-metadata** - Stores permanent video information including source URL
2. **download-jobs** - Stores job history including source URL

### Key Fields:
- `url` - Original source URL
- `video_id` / `filename` - Video identifier
- `title` - Video title
- `upload_date` - When video was uploaded
- `job_id` - Unique job identifier
- `status` - Job completion status

---

## Utility Script

A utility script `find_video_url.py` has been created in the project root to search for videos by title or keywords:

```python
python find_video_url.py
```

This script searches both DynamoDB tables and displays all matching videos with their URLs.
