param(
    [int]$TimeoutMinutes = 60,
    [switch]$AutoKill = $false
)

Write-Host "🕐 Timeout Monitor - Will check for tasks running longer than $TimeoutMinutes minutes" -ForegroundColor Cyan
if ($AutoKill) {
    Write-Host "⚠️  AUTO-KILL MODE: Will automatically terminate stuck tasks" -ForegroundColor Red
} else {
    Write-Host "📊 MONITOR MODE: Will only report stuck tasks" -ForegroundColor Yellow
}
Write-Host ""

while ($true) {
    $tasks = aws ecs list-tasks --cluster video-downloader-cluster --desired-status RUNNING --query "taskArns" --output text
    
    if ($tasks) {
        $taskIds = $tasks -split "`t"
        
        foreach ($taskArn in $taskIds) {
            $taskId = ($taskArn -split "/")[-1]
            
            try {
                $taskInfo = aws ecs describe-tasks --cluster video-downloader-cluster --tasks $taskArn --query "tasks[0].{created:createdAt,status:lastStatus}" | ConvertFrom-Json
                
                $created = [datetime]$taskInfo.created
                $runtime = ([datetime]::Now - $created).TotalMinutes
                
                if ($runtime -gt $TimeoutMinutes) {
                    Write-Host "⚠️  STUCK TASK DETECTED:" -ForegroundColor Red
                    Write-Host "   Task ID: $taskId" -ForegroundColor White
                    Write-Host "   Runtime: $([math]::Round($runtime, 1)) minutes" -ForegroundColor White
                    Write-Host "   Status: $($taskInfo.status)" -ForegroundColor White
                    
                    if ($AutoKill) {
                        Write-Host "   🔪 TERMINATING..." -ForegroundColor Red
                        aws ecs stop-task --cluster video-downloader-cluster --task $taskArn --reason "Timeout: Exceeded $TimeoutMinutes minute limit"
                        Write-Host "   ✅ Task terminated" -ForegroundColor Green
                    } else {
                        Write-Host "   💡 To kill: aws ecs stop-task --cluster video-downloader-cluster --task $taskArn --reason 'Manual timeout'" -ForegroundColor Gray
                    }
                    Write-Host ""
                } else {
                    Write-Host "✅ Task $taskId running normally ($([math]::Round($runtime, 1)) min)" -ForegroundColor Green
                }
            } catch {
                Write-Host "❌ Error checking task $taskId" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "📭 No running tasks" -ForegroundColor Gray
    }
    
    Write-Host "Next check in 5 minutes..." -ForegroundColor Gray
    Start-Sleep 300  # 5 minutes
}