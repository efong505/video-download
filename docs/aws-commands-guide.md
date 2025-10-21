# AWS Video Downloader Command Guide

## Quick Scripts

### PowerShell
```powershell
# Download with auto-generated filename
.\aws-download.ps1 "https://rumble.com/video-url"

# Download with custom filename
.\aws-download.ps1 "https://rumble.com/video-url" "my_video.mp4"
```

### Bash
```bash
# Download with auto-generated filename
./aws-download.sh "https://rumble.com/video-url"

# Download with custom filename
./aws-download.sh "https://rumble.com/video-url" "my_video.mp4"
```

## Manual Commands

### 1. Start Download

**PowerShell:**
```powershell
$body = @{
    url = "https://rumble.com/video-url"
    format = "best"
    output_name = "video.mp4"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/download" -Method POST -ContentType "application/json" -Body $body

# Show response
$response | ConvertTo-Json -Depth 3
```

**Bash:**
```bash
curl -X POST "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/download" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://rumble.com/video-url","format":"best","output_name":"video.mp4"}' | jq
```

### 2. Check Status (Fargate only)

**PowerShell:**
```powershell
$taskId = "your-task-id"
Invoke-RestMethod -Uri "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/status/$taskId" | ConvertTo-Json
```

**Bash:**
```bash
TASK_ID="your-task-id"
curl -s "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/status/$TASK_ID" | jq
```

### 3. Get Video URL

**PowerShell:**
```powershell
$filename = "video.mp4"
Invoke-RestMethod -Uri "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/video/$filename" | ConvertTo-Json
```

**Bash:**
```bash
FILENAME="video.mp4"
curl -s "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/video/$FILENAME" | jq
```

## Response Examples

### Download Response
```json
{
  "message": "Download initiated",
  "video_info": {
    "title": "Video Title",
    "size": "Unknown size",
    "duration": "4m 43s"
  },
  "routing": {
    "method": "lambda",
    "reason": "Fast download (< 12 minutes) - using cost-effective Lambda",
    "estimated_time": "5m 0s"
  },
  "cost_estimate": {
    "total_usd": "$0.005000"
  },
  "task_id": null
}
```

### Status Response (Fargate)
```json
{
  "task_id": "abc123",
  "status": "RUNNING",
  "progress": "45.2%",
  "speed": "1.23MiB/s",
  "eta": "01:23"
}
```

### Video URL Response
```json
{
  "signed_url": "https://s3-presigned-url",
  "expires_in": 3600
}
```

## Status Values

- **PENDING**: Task queued, waiting to start
- **RUNNING**: Download in progress
- **STOPPED**: Download completed successfully
- **FAILED**: Download failed

## Notes

- **Lambda downloads**: No progress tracking, faster for short videos
- **Fargate downloads**: Real-time progress tracking, better for long videos
- **Video URLs**: Expire after 24 hours
- **Cost**: Lambda ~$0.001-0.005, Fargate ~$0.007-0.020
- **Browser compatibility**: All downloads now use ffmpeg for optimal playback