param([string]$TaskId)

if (-not $TaskId) {
    Write-Host "Finding running downloads..." -ForegroundColor Cyan
    $tasks = aws ecs list-tasks --cluster video-downloader-cluster --desired-status RUNNING --query "taskArns" --output text
    
    if ($tasks) {
        $taskIds = $tasks -split "`t" | ForEach-Object { ($_ -split "/")[-1] }
        Write-Host "Running tasks:" -ForegroundColor Yellow
        $taskIds | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }
        
        if ($taskIds.Count -eq 1) {
            $TaskId = $taskIds[0]
        } else {
            Write-Host "Usage: .\live-logs.ps1 TASK_ID" -ForegroundColor Gray
            exit 0
        }
    } else {
        Write-Host "No running downloads found" -ForegroundColor Red
        exit 0
    }
}

Write-Host "📺 Live Download Logs for Task: $TaskId" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop monitoring" -ForegroundColor Gray
Write-Host ""

$logStream = "ecs/video-downloader/$TaskId"
$startTime = [int64](([datetime]::UtcNow.AddMinutes(-5)).Subtract([datetime]'1970-01-01')).TotalMilliseconds

while ($true) {
    try {
        $logs = aws logs get-log-events --log-group-name "/ecs/video-downloader" --log-stream-name $logStream --start-time $startTime --query "events[*].[timestamp,message]" --output json | ConvertFrom-Json
        
        if ($logs) {
            foreach ($log in $logs) {
                $timestamp = [datetime]::UnixEpoch.AddMilliseconds($log[0]).ToString("HH:mm:ss")
                $message = $log[1]
                
                # Highlight download progress
                if ($message -match '\[download\]') {
                    Write-Host "[$timestamp] $message" -ForegroundColor Green
                } elseif ($message -match 'Error|ERROR|Failed') {
                    Write-Host "[$timestamp] $message" -ForegroundColor Red
                } elseif ($message -match 'Complete|Success|uploaded') {
                    Write-Host "[$timestamp] $message" -ForegroundColor Cyan
                } else {
                    Write-Host "[$timestamp] $message" -ForegroundColor White
                }
                
                $startTime = $log[0] + 1
            }
        }
    } catch {
        Write-Host "Log check failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    Start-Sleep 2
}