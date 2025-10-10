# AWS Video Downloader System

A complete serverless video downloading and gallery system built on AWS with intelligent routing, automatic thumbnails, and cost optimization.

## 🎯 Overview

This system automatically downloads videos from various platforms (YouTube, Rumble, etc.) and creates a beautiful web gallery with thumbnail previews. It intelligently routes downloads between AWS Lambda (fast, cheap) and AWS Fargate (unlimited time) based on estimated processing time.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   User Request  │───▶│    Router    │───▶│ Lambda/Fargate  │
│                 │    │   Lambda     │    │   Downloader    │
└─────────────────┘    └──────────────┘    └─────────────────┘
                              │                       │
                              ▼                       ▼
                       ┌──────────────┐    ┌─────────────────┐
                       │ Cost & Time  │    │  S3 Storage     │
                       │ Estimation   │    │ videos/         │
                       └──────────────┘    │ thumbnails/     │
                                          └─────────────────┘
                                                   │
                                                   ▼
                                          ┌─────────────────┐
                                          │ CloudFront CDN  │
                                          │ Web Gallery     │
                                          └─────────────────┘
```

## 📁 Project Structure

```
Downloader/
├── README.md                    # This file
├── video-commands.md           # API usage examples
├── download.ps1               # PowerShell download script
├── download.sh               # Bash download script
├── deploy-all.ps1           # Deploy both Lambda and Fargate
├── rebuild-fargate.ps1      # Deploy Fargate container only
├── get-last-failure-logs.ps1 # Debug failed downloads
├── generate_thumbnails.py   # Generate thumbnails for existing videos
├── videos.html             # Web gallery interface
├── index.html             # Main website page
├── router/
│   └── index.py          # Router Lambda (intelligent routing)
├── downloader/
│   └── index.py         # Lambda downloader (fast downloads)
├── video_list_api/
│   └── index.py        # API to list videos dynamically
├── tag_api/            # Phase 1: Video tagging system
│   └── index.py       # Tag management CRUD API
├── fargate_downloader.py # Fargate container (long downloads)
├── cookie_manager.py    # YouTube cookie management
└── Dockerfile          # Fargate container definition
```

## 🚀 Quick Start

### 1. Download a Video
```powershell
# PowerShell
.\download.ps1 "https://youtube.com/watch?v=VIDEO_ID" "my_video.mp4"

# Force Fargate for long videos
.\download.ps1 "https://youtube.com/watch?v=VIDEO_ID" "my_video.mp4" -ForceFargate

# Specify format
.\download.ps1 "https://youtube.com/watch?v=VIDEO_ID" "my_video.mp4" -Format "hls-720"

# Download with tags (Phase 1 feature)
.\download.ps1 "https://youtube.com/watch?v=VIDEO_ID" "my_video.mp4" -Tags "news","politics","2024"
```

```bash
# Bash
./download.sh "https://youtube.com/watch?v=VIDEO_ID" "my_video.mp4"

# Force Fargate
./download.sh "https://youtube.com/watch?v=VIDEO_ID" "my_video.mp4" --force-fargate

# Specify format
./download.sh "https://youtube.com/watch?v=VIDEO_ID" "my_video.mp4" --format "hls-720"
```

### 2. View Your Videos
Visit your CloudFront URL: `https://your-domain.cloudfront.net/videos.html`

### 3. Tag API Usage (Phase 1 Feature)
**Base URL**: `https://h4hoegi26b.execute-api.us-east-1.amazonaws.com/prod/tags`

#### Get All Tags
```powershell
Invoke-RestMethod -Uri "https://h4hoegi26b.execute-api.us-east-1.amazonaws.com/prod/tags?action=get_all_tags" -Method GET

# Response: { "tags": ["news", "demo", "test"], "count": 3 }
```

#### Add Video Metadata
```powershell
$body = @{
    filename = "my-video.mp4"
    tags = @("news", "politics", "2024")
    title = "My Video Title"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://h4hoegi26b.execute-api.us-east-1.amazonaws.com/prod/tags?action=add_video" -Method POST -ContentType "application/json" -Body $body
```

#### Get Videos by Tag
```powershell
Invoke-RestMethod -Uri "https://h4hoegi26b.execute-api.us-east-1.amazonaws.com/prod/tags?action=get_videos_by_tag&tag=news" -Method GET
```

#### Update Video Tags
```powershell
$body = @{
    video_id = "video-id-here"
    tags = @("updated", "news", "politics")
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://h4hoegi26b.execute-api.us-east-1.amazonaws.com/prod/tags?action=update_video" -Method PUT -ContentType "application/json" -Body $body
```

## 📋 Script Reference

### Core Scripts

#### `download.ps1` / `download.sh`
**Purpose**: Main download interface with progress monitoring
**Usage**: 
```powershell
.\download.ps1 <URL> [output_name] [-ForceFargate] [-Format <format>]
```
**Features**:
- Automatic progress monitoring
- Cost estimation
- Smart routing display
- Real-time status updates

#### `deploy-all.ps1`
**Purpose**: Deploy both Lambda and Fargate components
**Usage**: `.\deploy-all.ps1`
**What it does**:
- Packages and deploys Lambda downloader
- Builds and pushes Fargate container to ECR
- Updates both services simultaneously

#### `rebuild-fargate.ps1`
**Purpose**: Deploy only the Fargate container
**Usage**: `.\rebuild-fargate.ps1`
**When to use**: After modifying `fargate_downloader.py` or `cookie_manager.py`

#### `get-last-failure-logs.ps1`
**Purpose**: Debug failed downloads
**Usage**: `.\get-last-failure-logs.ps1`
**Output**: Shows logs from the most recent failed Fargate task

#### `generate_thumbnails.py`
**Purpose**: Generate thumbnails for existing videos
**Usage**: `python generate_thumbnails.py`
**What it does**:
- Scans all videos in S3 `videos/` folder
- Downloads each video temporarily
- Extracts thumbnail at 50% duration
- Uploads to S3 `thumbnails/` folder

### Core Components

#### `router/index.py` - Router Lambda
**Purpose**: Intelligent routing between Lambda and Fargate
**Logic**:
- Estimates download time using video metadata
- Routes to Lambda if < 12 minutes estimated
- Routes to Fargate if ≥ 12 minutes estimated
- Supports manual Fargate forcing
- Provides cost estimates

**Key Functions**:
- `estimate_download_time()`: Analyzes video size/duration
- `calculate_cost_estimate()`: Compares Lambda vs Fargate costs
- `invoke_lambda_downloader()`: Routes to Lambda
- `start_fargate_task()`: Routes to Fargate

#### `downloader/index.py` - Lambda Downloader
**Purpose**: Fast downloads for videos < 15 minutes processing
**Features**:
- 15-minute timeout limit
- Intelligent format selection
- No FFmpeg re-encoding (speed optimization)
- Automatic thumbnail generation
- S3 upload with proper content types

**Key Functions**:
- `get_best_format()`: Selects optimal video quality
- `generate_thumbnails()`: Creates 3 thumbnails (10%, 50%, 90%)
- `lambda_handler()`: Main download orchestration

#### `fargate_downloader.py` - Fargate Container
**Purpose**: Unlimited time downloads for large videos
**Features**:
- 45-minute timeout (configurable)
- Supports up to 4K video quality
- Cookie management for restricted content
- Same thumbnail generation as Lambda
- Handles very large files (multi-GB)

**Key Functions**:
- `get_best_format()`: Format selection (up to 2160p)
- `generate_thumbnails()`: Same as Lambda version
- `main()`: Container entry point

#### `video_list_api/index.py` - Video List API
**Purpose**: Dynamic video gallery backend
**Features**:
- Lists all videos from S3 `videos/` folder
- Returns metadata (size, upload date, filename)
- Sorts by newest first
- CORS enabled for web access

#### `tag_api/index.py` - Tag Management API (Phase 1)
**Purpose**: Video tagging and metadata management
**Features**:
- Add video metadata with tags
- Get all available tags
- Filter videos by specific tags
- Update existing video tags
- DynamoDB integration for metadata storage
- CORS enabled for web access

**Key Functions**:
- `add_video_metadata()`: Store video tags and metadata
- `get_all_tags()`: List all unique tags in system
- `get_videos_by_tag()`: Filter videos by tag
- `update_video_tags()`: Modify existing video tags

**Database Schema**:
```json
{
  "video_id": "unique-id",
  "filename": "video.mp4",
  "title": "Video Title",
  "tags": ["news", "politics"],
  "upload_date": "2025-01-10T04:30:00.000Z",
  "created_at": "2025-01-10T04:30:00.000Z"
}
```

#### `cookie_manager.py` - Cookie Management
**Purpose**: Handle authentication for restricted videos
**Features**:
- YouTube cookie extraction
- Cookie validation
- Automatic refresh mechanisms

### Web Interface

#### `videos.html` - Video Gallery
**Purpose**: Beautiful web interface for video browsing
**Features**:
- Dynamic video loading from API
- Thumbnail previews with click-to-play
- Responsive 3-column layout
- Fallback support for old/new thumbnail formats
- Auto-updates when new videos are added

#### `index.html` - Main Page
**Purpose**: Landing page with interactive fireworks
**Features**:
- Interactive fireworks animation
- Link to video gallery
- Responsive design

## ⚙️ System Configuration

### Timeouts
- **Lambda**: 15 minutes (AWS limit)
- **Fargate**: 45 minutes (configurable in `fargate_downloader.py`)
- **Router Safety**: 12 minutes (80% of Lambda limit)

### Storage Structure
```
S3 Bucket:
├── videos/                 # All video files
│   ├── video1.mp4
│   └── video2.mp4
├── thumbnails/            # Thumbnail images
│   ├── video1_thumb_1.jpg  # 10% timestamp
│   ├── video1_thumb_2.jpg  # 50% timestamp (used by gallery)
│   ├── video1_thumb_3.jpg  # 90% timestamp
│   └── video1_thumb.jpg    # Legacy single thumbnail
├── index.html            # Main page
└── videos.html          # Gallery page
```

### Cost Optimization
- **Lambda**: $0.0000166667 per GB-second + $0.0000002 per request
- **Fargate**: $0.04048 per vCPU-hour + $0.004445 per GB-hour
- **Savings**: 76-80% cost reduction vs EC2
- **Smart Routing**: Automatically chooses cheapest option

## 🔧 Performance Optimizations

### Speed Improvements
1. **No FFmpeg Re-encoding**: Uses `--merge-output-format mp4` instead of `--recode-video`
2. **Result**: 10-20x speed improvement (2+ hours → 10-15 minutes)
3. **Quality**: Identical output, just container remuxing

### Format Selection
- **Lambda**: Up to 1080p (memory constraints)
- **Fargate**: Up to 4K/2160p (more resources)
- **Auto-selection**: Chooses best available HLS format
- **Fallback**: Uses `best[height<=limit]` if HLS unavailable

## 🐛 Troubleshooting

### Common Issues

#### "No videos found" on gallery page
- Check if API is working: Visit `https://your-api-gateway-url/prod/api/videos`
- Verify S3 permissions for `video-list-api` Lambda
- Check CloudFront cache (may need 5-10 minutes to update)

#### Download fails immediately
- Check video URL is accessible
- Verify format availability with `yt-dlp --list-formats URL`
- Check Lambda/Fargate logs in CloudWatch

#### Thumbnails not showing
- Run `python generate_thumbnails.py` to create missing thumbnails
- Check S3 `thumbnails/` folder exists
- Verify thumbnail naming: `videoname_thumb_2.jpg`

#### Video plays audio only
- Check video file isn't corrupted
- Verify proper content-type in S3 (`video/mp4`)
- Try different browser

### Debug Commands
```powershell
# Check last failure
.\get-last-failure-logs.ps1

# Test API directly
Invoke-RestMethod "https://your-api-gateway-url/prod/api/videos"

# List S3 contents
aws s3 ls s3://your-bucket/videos/
aws s3 ls s3://your-bucket/thumbnails/

# Check Lambda logs
aws logs describe-log-streams --log-group-name /aws/lambda/video-downloader
```

## 📊 Monitoring

### CloudWatch Metrics
- Lambda execution duration
- Fargate task completion rates
- S3 storage usage
- API Gateway request counts

### Cost Tracking
- Lambda GB-seconds usage
- Fargate vCPU/memory hours
- S3 storage and requests
- CloudFront data transfer

## 🔄 Updates and Maintenance

### Updating Components
```powershell
# Update both Lambda and Fargate
.\deploy-all.ps1

# Update only Fargate
.\rebuild-fargate.ps1

# Update website
aws s3 cp videos.html s3://your-bucket/ --content-type "text/html"
```

### Regular Maintenance
1. **Monitor costs** in AWS Cost Explorer
2. **Clean old videos** if storage grows large
3. **Update yt-dlp** periodically for new site support
4. **Check logs** for any recurring errors

## 🎯 Advanced Usage

### Custom Format Selection
```powershell
# List available formats
yt-dlp --list-formats "https://youtube.com/watch?v=VIDEO_ID"

# Download specific format
.\download.ps1 "URL" "video.mp4" -Format "hls-1080"
```

### Batch Processing
```powershell
# Download multiple videos
$urls = @(
    "https://youtube.com/watch?v=VIDEO1",
    "https://youtube.com/watch?v=VIDEO2"
)

foreach ($url in $urls) {
    .\download.ps1 $url "video_$(Get-Random).mp4"
    Start-Sleep 30  # Avoid rate limiting
}
```

### Tag API Integration (Phase 1)
```powershell
# Get all available tags
$tags = Invoke-RestMethod -Uri "https://h4hoegi26b.execute-api.us-east-1.amazonaws.com/prod/tags?action=get_all_tags" -Method GET
Write-Host "Available tags: $($tags.tags -join ', ')"

# Find videos with specific tag
$newsVideos = Invoke-RestMethod -Uri "https://h4hoegi26b.execute-api.us-east-1.amazonaws.com/prod/tags?action=get_videos_by_tag&tag=news" -Method GET
Write-Host "Found $($newsVideos.count) news videos"

# Add metadata for existing video
$metadata = @{
    filename = "existing-video.mp4"
    tags = @("archive", "important")
    title = "Important Archive Video"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://h4hoegi26b.execute-api.us-east-1.amazonaws.com/prod/tags?action=add_video" -Method POST -ContentType "application/json" -Body $metadata
```

### API Integration
See `video-commands.md` for complete API usage examples including:
- Direct REST API calls
- Progress monitoring
- Batch operations
- Custom integrations
- Tag management workflows

## 📈 System Limits

### AWS Service Limits
- **Lambda**: 15-minute timeout, 10GB temp storage
- **Fargate**: 4 vCPU, 30GB memory max
- **S3**: Unlimited storage
- **API Gateway**: 10,000 requests/second

### Practical Limits
- **Video Size**: ~50GB (Fargate temp storage)
- **Concurrent Downloads**: 10 (configurable)
- **Supported Sites**: 1000+ (yt-dlp supported)

## 🔐 Security

### IAM Permissions
- Lambda execution role with S3 read/write
- Fargate task role with S3 access
- API Gateway invoke permissions

### Network Security
- Fargate runs in private subnets
- S3 bucket policies restrict access
- CloudFront provides DDoS protection

This system provides a complete, production-ready video downloading and gallery solution with enterprise-grade reliability and cost optimization.

## 📚 Implementation Tutorials

### Phase 1: Video Tagging System Implementation

This tutorial shows how to add video tagging capabilities to the existing downloader system.

#### Prerequisites
- Working AWS Video Downloader System (baseline)
- AWS CLI configured
- Git for version control

#### Step 1: Set Up Version Control
```powershell
# Create backup of working system
cd c:\Users\Ed\Documents\Programming\AWS
Copy-Item -Recurse Downloader Downloader_backup_working

# Initialize Git repository
cd Downloader
git init
git add .
git commit -m "Initial commit: Working video downloader system"

# Create feature branch
git checkout -b feature/video-tagging
```

#### Step 2: Create DynamoDB Table
```powershell
# Create video metadata table
aws dynamodb create-table \
    --table-name video-metadata \
    --attribute-definitions \
        AttributeName=video_id,AttributeType=S \
    --key-schema \
        AttributeName=video_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```

#### Step 3: Create Tag Management API
```powershell
# Create directory structure
mkdir tag_api
```

Create `tag_api/index.py` with CRUD operations:
- `add_video_metadata()` - Store video tags
- `get_videos_by_tag()` - Filter videos by tag
- `get_all_tags()` - List all available tags
- `update_video_tags()` - Modify video tags

#### Step 4: Deploy Tag API
```powershell
# Package and deploy Lambda function
Compress-Archive -Path tag_api\* -DestinationPath tag_api.zip -Force
aws lambda create-function \
    --function-name video-tag-api \
    --runtime python3.9 \
    --role arn:aws:iam::ACCOUNT_ID:role/lambda-execution-role \
    --handler index.lambda_handler \
    --zip-file fileb://tag_api.zip \
    --timeout 30

# Create API Gateway
aws apigateway create-rest-api --name video-tag-api
aws apigateway create-resource --rest-api-id API_ID --parent-id ROOT_ID --path-part tags
aws apigateway put-method --rest-api-id API_ID --resource-id RESOURCE_ID --http-method ANY --authorization-type NONE
aws apigateway put-integration --rest-api-id API_ID --resource-id RESOURCE_ID --http-method ANY --type AWS_PROXY --integration-http-method POST --uri LAMBDA_URI
aws lambda add-permission --function-name video-tag-api --statement-id apigateway-invoke --action lambda:InvokeFunction --principal apigateway.amazonaws.com
aws apigateway create-deployment --rest-api-id API_ID --stage-name prod
```

#### Step 5: Update Download Scripts
Add `-Tags` parameter to `download.ps1`:
```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$Url,
    [string]$OutputName = "video.mp4",
    [switch]$ForceFargate,
    [string]$Format = "best",
    [string[]]$Tags = @()  # New parameter
)

# Add tags to request body
$requestBody = @{
    url = $Url
    output_name = $OutputName
    format = $Format
    force_fargate = $ForceFargate.IsPresent
    tags = $Tags  # Include tags
} | ConvertTo-Json
```

#### Step 6: Update Lambda Downloader
Add DynamoDB integration to `downloader/index.py`:
```python
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Extract tags from event
    tags = event.get('tags', [])
    
    # After successful upload, save metadata
    if tags:
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
```

#### Step 7: Update Fargate Downloader
Add similar DynamoDB integration to `fargate_downloader.py`:
```python
# Get tags from environment
tags = os.environ.get('TAGS', '').split(',') if os.environ.get('TAGS') else []

# Save metadata after upload
if tags:
    table = dynamodb.Table('video-metadata')
    table.put_item(Item={...})
```

#### Step 8: Update Router
Modify `router/index.py` to pass tags to downloaders:
```python
def lambda_handler(event, context):
    # Parse tags from request
    tags = body.get('tags', [])
    
    # Pass tags to both Lambda and Fargate
    if route_to_lambda:
        response = invoke_lambda_downloader(url, format_id, output_name, tags)
    else:
        response = start_fargate_task(url, format_id, output_name, tags)
```

#### Step 9: Deploy Updates
```powershell
# Update Lambda downloader
Compress-Archive -Path downloader\* -DestinationPath downloader.zip -Force
aws lambda update-function-code --function-name video-downloader --zip-file fileb://downloader.zip

# Update router
Compress-Archive -Path router\* -DestinationPath router.zip -Force
aws lambda update-function-code --function-name video-download-router --zip-file fileb://router.zip

# Rebuild Fargate container (requires Docker)
docker build -t video-downloader .
docker tag video-downloader:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/video-downloader:latest
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/video-downloader:latest
```

#### Step 10: Test the System
```powershell
# Test download with tags
.\download.ps1 "https://youtube.com/watch?v=VIDEO_ID" "test-video.mp4" -Tags "test","demo","phase1"

# Test tag API
Invoke-RestMethod -Uri "https://API_GATEWAY_URL/prod/tags/all" -Method GET
```

#### Step 11: Commit Changes
```powershell
git add .
git commit -m "Phase 1: Video Tagging System - Complete Implementation

✅ DynamoDB table 'video-metadata' created
✅ Tag management API deployed
✅ Download scripts enhanced with -Tags parameter
✅ Lambda and Fargate downloaders updated
✅ Router updated to pass tags
✅ Test download with tags successful"
```

#### Usage Examples
```powershell
# Download with tags
.\download.ps1 "video-url" "filename.mp4" -Tags "news","politics","2024"

# Get all tags
GET https://API_GATEWAY_URL/prod/tags/all

# Get videos by tag
GET https://API_GATEWAY_URL/prod/tags/videos?tag=news

# Add video metadata
POST https://API_GATEWAY_URL/prod/tags/video
{
  "filename": "video.mp4",
  "tags": ["news", "politics"],
  "title": "Video Title"
}
```

#### Key Benefits
- ✅ **Non-breaking**: All existing functionality preserved
- ✅ **Backward Compatible**: Tags parameter is optional
- ✅ **Scalable**: DynamoDB handles any number of videos/tags
- ✅ **API-driven**: RESTful interface for tag management
- ✅ **Version Controlled**: Safe rollback if issues arise

#### Next Phase
Phase 2 will add user authentication and admin dashboard, building on this tagging foundation.