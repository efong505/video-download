param([string]$TaskId)

if (-not $TaskId) {
    # List all running tasks
    Write-Host "🔍 Finding running downloads..." -ForegroundColor Cyan
    $tasks = aws ecs list-tasks --cluster video-downloader-cluster --desired-status RUNNING --query "taskArns" --output text
    
    if ($tasks) {
        $taskIds = $tasks -split "`t" | ForEach-Object { ($_ -split "/")[-1] }
        Write-Host "📋 Running tasks:" -ForegroundColor Yellow
        $taskIds | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }
        
        if ($taskIds.Count -eq 1) {
            $TaskId = $taskIds[0]
            Write-Host "🎯 Checking status of: $TaskId" -ForegroundColor Green
        } else {
            Write-Host "💡 Usage: .\check-status.ps1 TASK_ID" -ForegroundColor Gray
            exit 0
        }
    } else {
        Write-Host "❌ No running downloads found" -ForegroundColor Red
        exit 0
    }
}

$API = "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod"

Write-Host "📊 Monitoring task: $TaskId" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop monitoring" -ForegroundColor Gray
Write-Host ""

while ($true) {
    try {
        $status = Invoke-RestMethod -Uri "$API/status/$TaskId" -ErrorAction Stop
        $timestamp = Get-Date -Format "HH:mm:ss"
        
        Write-Host "[$timestamp] Status: $($status.status) | Progress: $($status.progress) | Speed: $($status.speed) | ETA: $($status.eta)" -ForegroundColor Cyan
        
        if ($status.status -eq "STOPPED") {
            Write-Host "✅ Download completed!" -ForegroundColor Green
            break
        } elseif ($status.status -eq "FAILED") {
            Write-Host "❌ Download failed!" -ForegroundColor Red
            break
        }
    } catch {
        Write-Host "⚠️  Status check failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    Start-Sleep 3
}