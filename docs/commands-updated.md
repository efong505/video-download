# AWS Video Downloader

Complete video downloading system using AWS Lambda and Fargate with ffmpeg conversion for browser compatibility.

## Quick Start

### PowerShell
```powershell
# Simple download
.\download.ps1 "https://rumble.com/video-url"

# Custom filename
.\download.ps1 "https://rumble.com/video-url" "my_video.mp4"
```

### Bash
```bash
# Simple download
./download.sh "https://rumble.com/video-url"

# Custom filename  
./download.sh "https://rumble.com/video-url" "my_video.mp4"
```

## Manual API Usage

### Start Download
```bash
curl -X POST "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/download" \
  -H "Content-Type: application/json" \
  -d '{"url":"VIDEO_URL","format":"best","output_name":"video.mp4"}'
```

### Check Status (Fargate only)
```bash
curl "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/status/TASK_ID"
```

### Get Video URL
```bash
curl "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/video/FILENAME"
```

## System Architecture

- **Router Lambda**: Analyzes video and routes to optimal service
- **Lambda Downloader**: Fast downloads (<12 min) with ffmpeg conversion
- **Fargate Downloader**: Long downloads (≥12 min) with progress tracking
- **S3 Storage**: Browser-compatible MP4 files with signed URLs

## Features

✅ **Smart Routing**: Automatic Lambda/Fargate selection based on video length
✅ **Cost Optimization**: Lambda ~$0.001-0.005, Fargate ~$0.007-0.020  
✅ **FFmpeg Conversion**: H.264/AAC for maximum browser compatibility
✅ **Progress Tracking**: Real-time monitoring for Fargate downloads
✅ **Multiple Platforms**: Rumble, YouTube, Facebook, and more
✅ **Browser Playback**: Direct video streaming with signed URLs

## Status Values

- **PENDING**: Queued, waiting to start
- **RUNNING**: Download in progress  
- **STOPPED**: Completed successfully
- **FAILED**: Download failed

## File Structure

```
AWS/Downloader/
├── download.ps1              # PowerShell download script
├── download.sh               # Bash download script
├── live-logs.ps1             # PowerShell live log monitor
├── live-logs.sh              # Bash live log monitor
├── status.ps1                # PowerShell status checker
├── downloader/index.py       # Lambda downloader
├── router/index.py           # Router Lambda
├── fargate_downloader.py     # Fargate container
├── video-downloader.html     # Web interface
└── README.md                 # This file
```

## Live Status Monitoring

### Real-Time Download Progress
```powershell
# PowerShell - Shows actual yt-dlp download progress
.\live-logs.ps1

# Or with specific task ID
.\live-logs.ps1 TASK_ID
```

```bash
# Bash - Shows actual yt-dlp download progress
./live-logs.sh

# Or with specific task ID  
./live-logs.sh TASK_ID
```

### Quick Status Check
```bash
# Check recent download activity
aws logs filter-log-events --log-group-name /ecs/video-downloader --start-time 1728350000000 --filter-pattern "[download]" --query "events[-10:].[timestamp,message]" --output table
```

### Troubleshooting Silent Tasks

**If no logs appear after 5 minutes:**

1. **Check task status:**
```bash
aws ecs describe-tasks --cluster video-downloader-cluster --tasks TASK_ARN --query "tasks[0].{status:lastStatus,created:createdAt,reason:stoppedReason}"
```

2. **Stop stuck task:**
```bash
aws ecs stop-task --cluster video-downloader-cluster --task TASK_ARN --reason "Manual stop"
```

**Common causes of no logs:**
- **Live streams** - yt-dlp hangs on live content
- **Platform blocking** - YouTube/Facebook blocking AWS IPs
- **Container startup** - Takes 1-2 minutes to initialize
- **Network issues** - Can't reach video URL
- **Container crash** - Failed before logging

**Rule:** If RUNNING status but no logs after 5 minutes = likely stuck

## Notes

- Video URLs expire after 24 hours
- Lambda has 15-minute timeout limit
- Fargate handles unlimited duration
- All downloads use ffmpeg for browser compatibility
- S3 bucket is publicly readable for direct access
- Live streams may cause tasks to hang indefinitely
