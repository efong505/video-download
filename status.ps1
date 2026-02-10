param([string]$TaskId)

$API = "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod"

if (-not $TaskId) {
    Write-Host "Finding running downloads..." -ForegroundColor Cyan
    $tasks = aws ecs list-tasks --cluster video-downloader-cluster --desired-status RUNNING --query "taskArns" --output text
    
    if ($tasks) {
        $taskIds = $tasks -split "`t" | ForEach-Object { ($_ -split "/")[-1] }
        Write-Host "Running tasks:" -ForegroundColor Yellow
        $taskIds | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }
        
        if ($taskIds.Count -eq 1) {
            $TaskId = $taskIds[0]
            Write-Host "Checking: $TaskId" -ForegroundColor Green
        } else {
            Write-Host "Usage: .\status.ps1 TASK_ID" -ForegroundColor Gray
            exit 0
        }
    } else {
        Write-Host "No running downloads found" -ForegroundColor Red
        exit 0
    }
}

Write-Host "Monitoring: $TaskId (Press Ctrl+C to stop)" -ForegroundColor Cyan

while ($true) {
    try {
        $status = Invoke-RestMethod -Uri "$API/status/$TaskId" -ErrorAction Stop
        $time = Get-Date -Format "HH:mm:ss"
        
        Write-Host "[$time] $($status.status) | $($status.progress) | $($status.speed)" -ForegroundColor Cyan
        
        if ($status.status -eq "STOPPED" -or $status.status -eq "FAILED") {
            break
        }
    } catch {
        Write-Host "Status check failed" -ForegroundColor Yellow
    }
    
    Start-Sleep 3
}