param([string]$TaskId)

if (-not $TaskId) {
    $tasks = aws ecs list-tasks --cluster video-downloader-cluster --desired-status RUNNING --query "taskArns" --output text
    if ($tasks) {
        $TaskId = ($tasks -split "`t")[0] -replace '.*/', ''
        Write-Host "Found running task: $TaskId" -ForegroundColor Cyan
    } else {
        Write-Host "No running tasks found" -ForegroundColor Red
        exit 0
    }
}

Write-Host "🔍 Diagnosing Stuck Task: $TaskId" -ForegroundColor Cyan
Write-Host ""

# 1. Get task details
$taskInfo = aws ecs describe-tasks --cluster video-downloader-cluster --tasks "arn:aws:ecs:us-east-1:371751795928:task/video-downloader-cluster/$TaskId" --query "tasks[0]" | ConvertFrom-Json

$created = [datetime]$taskInfo.createdAt
$runtime = ([datetime]::Now - $created).TotalMinutes
$videoUrl = ($taskInfo.overrides.containerOverrides[0].environment | Where-Object {$_.name -eq "VIDEO_URL"}).value

Write-Host "📊 Task Information:" -ForegroundColor Yellow
Write-Host "  Status: $($taskInfo.lastStatus)" -ForegroundColor White
Write-Host "  Runtime: $([math]::Round($runtime, 1)) minutes" -ForegroundColor White
Write-Host "  Video URL: $videoUrl" -ForegroundColor White
Write-Host ""

# 2. Check if it's a live stream
if ($videoUrl -match "live|stream|broadcast") {
    Write-Host "⚠️  LIKELY CAUSE: Live Stream Detected" -ForegroundColor Red
    Write-Host "   Live streams cause yt-dlp to hang indefinitely" -ForegroundColor Gray
    Write-Host "   Recommendation: Stop this task immediately" -ForegroundColor Yellow
}

# 3. Check platform
if ($videoUrl -match "youtube|youtu.be") {
    Write-Host "⚠️  PLATFORM: YouTube (High blocking risk)" -ForegroundColor Red
} elseif ($videoUrl -match "facebook|fb.com") {
    Write-Host "⚠️  PLATFORM: Facebook (High blocking risk)" -ForegroundColor Red
} elseif ($videoUrl -match "rumble") {
    Write-Host "✅ PLATFORM: Rumble (Usually reliable)" -ForegroundColor Green
} else {
    Write-Host "❓ PLATFORM: Unknown - $($videoUrl -replace '.*://([^/]+).*', '$1')" -ForegroundColor Yellow
}

# 4. Check logs
Write-Host ""
Write-Host "📋 Recent Log Activity:" -ForegroundColor Yellow
try {
    $logs = aws logs get-log-events --log-group-name /ecs/video-downloader --log-stream-name "ecs/video-downloader/$TaskId" --limit 5 --query "events[*].message" --output text 2>$null
    if ($logs) {
        $logs -split "`t" | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
    } else {
        Write-Host "  No logs found - Container may be stuck before logging" -ForegroundColor Red
    }
} catch {
    Write-Host "  Unable to retrieve logs" -ForegroundColor Red
}

# 5. Recommendations
Write-Host ""
Write-Host "💡 Recommendations:" -ForegroundColor Yellow
if ($runtime -gt 10) {
    Write-Host "  🔪 STOP TASK: Running too long without progress" -ForegroundColor Red
    Write-Host "     aws ecs stop-task --cluster video-downloader-cluster --task arn:aws:ecs:us-east-1:371751795928:task/video-downloader-cluster/$TaskId --reason 'Stuck task'" -ForegroundColor Gray
} else {
    Write-Host "  ⏳ WAIT: Give it 2-3 more minutes for container startup" -ForegroundColor Yellow
}

if ($videoUrl -match "live|stream") {
    Write-Host "  🚫 AVOID: Don't download live streams" -ForegroundColor Red
}

Write-Host "  📊 MONITOR: Use .\live-logs.ps1 $TaskId to watch for activity" -ForegroundColor Green