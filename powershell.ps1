# Download and monitor progress

Write-Host "Starting download..."
$body = @{
    url = "https://rumble.com/v700fs6-an-assault-on-the-constitutional-republic.html"
    format = "best"
    output_name = "assault.mp4"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/download" -Method POST -ContentType "application/json" -Body $body

Write-Host "Response:" ($response | ConvertTo-Json -Depth 3)

$taskId = $response.task_id

if ($taskId) {
    Write-Host "Monitoring progress for task: $taskId"
    
    do {
        $status = Invoke-RestMethod -Uri "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/status/$taskId"
        
        Write-Host "$(Get-Date -Format 'HH:mm:ss'): [$($status.status)] $($status.progress) @ $($status.speed)"
        
        if ($status.status -eq "completed" -or $status.status -eq "failed") {
            Write-Host "Download $($status.status)!"
            break
        }
        
        Start-Sleep 10
    } while ($true)
} else {
    Write-Host "No task ID - likely completed via Lambda"
}