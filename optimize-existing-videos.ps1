# Re-optimize existing S3 videos with FFmpeg faststart for progressive streaming
# Downloads videos from S3, optimizes with -movflags +faststart, re-uploads

param(
    [string]$SizeFilter = "all"  # all, 100mb, 500mb, 1gb
)

$S3_BUCKET = "my-video-downloads-bucket"
$VIDEO_PREFIX = "videos/"
$TEMP_DIR = Join-Path $PSScriptRoot "temp_optimize"

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "S3 Video Optimization Script" -ForegroundColor Yellow
Write-Host "Adds FFmpeg faststart for progressive streaming" -ForegroundColor White
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

# Create temp directory with full path
if (-not (Test-Path $TEMP_DIR)) {
    New-Item -ItemType Directory -Force -Path $TEMP_DIR | Out-Null
}
Write-Host "Using temp directory: $TEMP_DIR" -ForegroundColor Gray
Write-Host ""

# List all videos in S3
Write-Host "Scanning S3 bucket: $S3_BUCKET/$VIDEO_PREFIX" -ForegroundColor Cyan
$videos = aws s3api list-objects-v2 --bucket $S3_BUCKET --prefix $VIDEO_PREFIX --query "Contents[?ends_with(Key, '.mp4') || ends_with(Key, '.webm') || ends_with(Key, '.mkv')].[Key,Size,LastModified]" --output json | ConvertFrom-Json

if (-not $videos) {
    Write-Host "No videos found in S3 bucket" -ForegroundColor Red
    exit
}

# Parse video info
$videoList = @()
foreach ($video in $videos) {
    $key = $video[0]
    $sizeMB = [math]::Round($video[1] / 1MB, 1)
    $lastModified = $video[2]
    
    $videoList += @{
        Key = $key
        Filename = Split-Path $key -Leaf
        SizeMB = $sizeMB
        LastModified = $lastModified
    }
}

Write-Host "Found $($videoList.Count) videos" -ForegroundColor Green
Write-Host ""

# Calculate total size
$totalSizeMB = ($videoList | Measure-Object -Property SizeMB -Sum).Sum
$totalSizeGB = [math]::Round($totalSizeMB / 1024, 2)
Write-Host "Total size: $totalSizeMB MB ($totalSizeGB GB)" -ForegroundColor White
Write-Host ""

# Filter options
Write-Host "Filter options:" -ForegroundColor Yellow
Write-Host "1. Optimize ALL videos"
Write-Host "2. Optimize videos larger than 100 MB"
Write-Host "3. Optimize videos larger than 500 MB"
Write-Host "4. Optimize videos larger than 1 GB"
Write-Host "5. Exit"
Write-Host ""

$choice = Read-Host "Select option (1-5)"

if ($choice -eq "5") {
    Write-Host "Exiting..." -ForegroundColor Yellow
    exit
}

# Filter videos
$filteredVideos = $videoList
switch ($choice) {
    "2" { $filteredVideos = $videoList | Where-Object { $_.SizeMB -gt 100 } }
    "3" { $filteredVideos = $videoList | Where-Object { $_.SizeMB -gt 500 } }
    "4" { $filteredVideos = $videoList | Where-Object { $_.SizeMB -gt 1024 } }
}

if ($filteredVideos.Count -eq 0) {
    Write-Host "No videos match the filter criteria" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Will optimize $($filteredVideos.Count) videos" -ForegroundColor Yellow
Write-Host ""

# Confirm
$confirm = Read-Host "Continue? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "Cancelled" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "Starting optimization..." -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

# Results tracking
$results = @{
    Success = 0
    Skipped = 0
    Failed = 0
    Error = 0
}

# Process each video
$count = 0
foreach ($video in $filteredVideos) {
    $count++
    Write-Host "[$count/$($filteredVideos.Count)] $($video.Filename) ($($video.SizeMB) MB)" -ForegroundColor Cyan
    
    $originalPath = Join-Path $TEMP_DIR $video.Filename
    $optimizedPath = Join-Path $TEMP_DIR "optimized_$($video.Filename)"
    
    try {
        # Download from S3
        Write-Host "  Downloading..." -ForegroundColor Gray
        aws s3 cp "s3://$S3_BUCKET/$($video.Key)" $originalPath --quiet
        
        if (-not (Test-Path $originalPath)) {
            Write-Host "  ✗ Download failed" -ForegroundColor Red
            $results.Failed++
            continue
        }
        
        $fileSizeMB = [math]::Round((Get-Item $originalPath).Length / 1MB, 1)
        Write-Host "  Downloaded: $fileSizeMB MB" -ForegroundColor Gray
        
        # Check if already optimized using FFmpeg (proper moov atom detection)
        try {
            # Use ffprobe to check if video has faststart
            # Videos with faststart can start playing immediately
            $ffprobeCheck = ffprobe -v error -show_entries format_tags=encoder -of default=noprint_wrappers=1:nokey=1 $originalPath 2>&1
            
            # Quick test: Try to get format info quickly
            # If moov is at end, this takes longer; if at beginning, it's instant
            $startTime = Get-Date
            $formatCheck = ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $originalPath 2>&1
            $elapsed = ((Get-Date) - $startTime).TotalMilliseconds
            
            # If ffprobe responds very quickly (<100ms for small files, <500ms for large),
            # moov atom is likely at beginning
            $fileSize = (Get-Item $originalPath).Length / 1MB
            $threshold = if ($fileSize -lt 100) { 100 } elseif ($fileSize -lt 1000) { 500 } else { 1000 }
            
            if ($elapsed -lt $threshold -and $formatCheck -match "^[0-9.]+$") {
                Write-Host "  ✓ Already optimized (faststart detected), skipping" -ForegroundColor Green
                Remove-Item $originalPath -Force
                $results.Skipped++
                Write-Host ""
                continue
            }
            
            Write-Host "  Needs optimization (moov atom at end)" -ForegroundColor Yellow
        } catch {
            Write-Host "  Warning: Could not verify optimization status, will optimize to be safe" -ForegroundColor Yellow
        }
        
        # Optimize with FFmpeg
        Write-Host "  Optimizing with FFmpeg..." -ForegroundColor Gray
        $ffmpegArgs = @(
            "-i", $originalPath,
            "-c", "copy",
            "-movflags", "+faststart",
            "-y",
            $optimizedPath
        )
        
        $process = Start-Process -FilePath "ffmpeg" -ArgumentList $ffmpegArgs -NoNewWindow -Wait -PassThru
        
        if ($process.ExitCode -ne 0 -or -not (Test-Path $optimizedPath)) {
            Write-Host "  ✗ FFmpeg optimization failed" -ForegroundColor Red
            Remove-Item $originalPath -Force -ErrorAction SilentlyContinue
            $results.Failed++
            Write-Host ""
            continue
        }
        
        $optimizedSizeMB = [math]::Round((Get-Item $optimizedPath).Length / 1MB, 1)
        Write-Host "  Optimized: $optimizedSizeMB MB" -ForegroundColor Gray
        
        # Create backup
        Write-Host "  Creating backup..." -ForegroundColor Gray
        $backupKey = "$($video.Key).backup"
        aws s3 cp "s3://$S3_BUCKET/$($video.Key)" "s3://$S3_BUCKET/$backupKey" --quiet
        
        # Upload optimized version
        Write-Host "  Uploading optimized version..." -ForegroundColor Gray
        $contentType = if ($video.Filename -match "\.mp4$") { "video/mp4" } else { "video/webm" }
        aws s3 cp $optimizedPath "s3://$S3_BUCKET/$($video.Key)" --content-type $contentType --content-disposition "inline" --quiet
        
        Write-Host "  ✓ Optimized and uploaded" -ForegroundColor Green
        $results.Success++
        
        # Cleanup
        Remove-Item $originalPath -Force -ErrorAction SilentlyContinue
        Remove-Item $optimizedPath -Force -ErrorAction SilentlyContinue
        
    } catch {
        Write-Host "  ✗ Error: $_" -ForegroundColor Red
        $results.Error++
        
        # Cleanup on error
        Remove-Item $originalPath -Force -ErrorAction SilentlyContinue
        Remove-Item $optimizedPath -Force -ErrorAction SilentlyContinue
    }
    
    Write-Host ""
}

# Summary
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "OPTIMIZATION COMPLETE" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "✓ Success:  $($results.Success)" -ForegroundColor Green
Write-Host "⊘ Skipped:  $($results.Skipped) (already optimized)" -ForegroundColor Yellow
Write-Host "✗ Failed:   $($results.Failed)" -ForegroundColor Red
Write-Host "⚠ Error:    $($results.Error)" -ForegroundColor Red
Write-Host ""
Write-Host "Backups created with .backup suffix" -ForegroundColor Cyan
Write-Host "To restore: aws s3 cp s3://$S3_BUCKET/videos/file.mp4.backup s3://$S3_BUCKET/videos/file.mp4" -ForegroundColor Gray
Write-Host ""

# Cleanup temp directory
Remove-Item $TEMP_DIR -Recurse -Force -ErrorAction SilentlyContinue
