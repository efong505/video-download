param([string]$TaskId)

if (-not $TaskId) {
    $tasks = aws ecs list-tasks --cluster video-downloader-cluster --desired-status RUNNING --query "taskArns" --output text
    if ($tasks) {
        $TaskId = ($tasks -split "`t")[0] -replace '.*/', ''
    } else {
        Write-Host "No running tasks found" -ForegroundColor Red
        exit 0
    }
}

Write-Host "🔍 Diagnosing Task: $TaskId" -ForegroundColor Cyan

# 1. Check ECS task status
Write-Host "`n1. ECS Task Status:" -ForegroundColor Yellow
$taskStatus = aws ecs describe-tasks --cluster video-downloader-cluster --tasks "arn:aws:ecs:us-east-1:371751795928:task/video-downloader-cluster/$TaskId" --query "tasks[0].{status:lastStatus,health:healthStatus,createdAt:createdAt,stoppedReason:stoppedReason,exitCode:containers[0].exitCode}" | ConvertFrom-Json
$taskStatus | Format-List

# 2. Check log stream
Write-Host "2. Log Stream Status:" -ForegroundColor Yellow
$logStream = aws logs describe-log-streams --log-group-name /ecs/video-downloader --log-stream-name-prefix "ecs/video-downloader/$TaskId" --query "logStreams[0].{name:logStreamName,created:creationTime,lastEvent:lastEventTime,size:storedBytes}" | ConvertFrom-Json
$logStream | Format-List

# 3. Check recent logs
Write-Host "3. Recent Log Events:" -ForegroundColor Yellow
try {
    $logs = aws logs get-log-events --log-group-name /ecs/video-downloader --log-stream-name "ecs/video-downloader/$TaskId" --limit 10 --query "events[*].message" --output text
    if ($logs) {
        $logs -split "`t" | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
    } else {
        Write-Host "  No log events found" -ForegroundColor Red
    }
} catch {
    Write-Host "  Log stream may not exist or be empty" -ForegroundColor Red
}

# 4. Possible reasons for no logs
Write-Host "`n4. Possible Issues:" -ForegroundColor Yellow
Write-Host "  • Container is starting up (can take 1-2 minutes)" -ForegroundColor Gray
Write-Host "  • Network issues downloading video" -ForegroundColor Gray  
Write-Host "  • YouTube/platform blocking AWS IPs" -ForegroundColor Gray
Write-Host "  • Container crashed before logging" -ForegroundColor Gray
Write-Host "  • Environment variables missing" -ForegroundColor Gray

# 5. Recommendations
Write-Host "`n5. Next Steps:" -ForegroundColor Yellow
Write-Host "  • Wait 2-3 minutes for container startup" -ForegroundColor Green
Write-Host "  • Check if task is still RUNNING" -ForegroundColor Green
Write-Host "  • Try with Rumble URL (more reliable than YouTube)" -ForegroundColor Green
Write-Host "  • Use: .\live-logs.ps1 $TaskId to monitor" -ForegroundColor Green