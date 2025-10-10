# Get logs from the most recent failed Fargate task
Write-Host "Finding most recent failed task logs..." -ForegroundColor Yellow

# Get the most recent log stream (which corresponds to the latest task)
$logStreamInfo = aws logs describe-log-streams --log-group-name "/ecs/video-downloader" --order-by LastEventTime --descending --max-items 1 | ConvertFrom-Json

if (-not $logStreamInfo.logStreams -or $logStreamInfo.logStreams.Count -eq 0) {
    Write-Host "No log streams found" -ForegroundColor Red
    exit 1
}

$logStream = $logStreamInfo.logStreams[0].logStreamName

Write-Host "Latest log stream: $logStream" -ForegroundColor Cyan
Write-Host ""

# Get the log events and display as table
Write-Host "=== FAILURE LOGS ===" -ForegroundColor Red
aws logs get-log-events --log-group-name "/ecs/video-downloader" --log-stream-name "$logStream" --query "events[].message" --output table