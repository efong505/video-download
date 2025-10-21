# Download Scripts Usage

## Setup
Replace `your-api-gateway-url` in both scripts with your actual API Gateway URL.

## Bash Usage (Linux/macOS/WSL)
```bash
# Make executable
chmod +x download.sh

# Download a video
./download.sh "https://www.youtube.com/watch?v=VIDEO_ID"
```

## PowerShell Usage (Windows)
```powershell
# Download a video
.\download.ps1 "https://www.youtube.com/watch?v=VIDEO_ID"
```

Both scripts will:
1. Initiate the download
2. Show real-time progress
3. Display final S3 location when complete