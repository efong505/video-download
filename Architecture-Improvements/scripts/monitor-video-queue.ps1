# monitor-video-queue.ps1 - Monitor video-processing-queue in real-time

$Region = "us-east-1"
$QueueUrl = "https://sqs.us-east-1.amazonaws.com/371751795928/video-processing-queue"
$DlqUrl = "https://sqs.us-east-1.amazonaws.com/371751795928/video-processing-dlq"

Write-Host "=== Video Processing Queue Monitor ===" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Gray
Write-Host ""

while ($true) {
    $timestamp = Get-Date -Format "HH:mm:ss"
    
    # Get queue stats
    $queueStats = aws sqs get-queue-attributes --queue-url $QueueUrl --attribute-names All --region $Region --output json | ConvertFrom-Json
    $messages = $queueStats.Attributes.ApproximateNumberOfMessages
    $inFlight = $queueStats.Attributes.ApproximateNumberOfMessagesNotVisible
    
    # Get DLQ stats
    $dlqStats = aws sqs get-queue-attributes --queue-url $DlqUrl --attribute-names ApproximateNumberOfMessages --region $Region --output json | ConvertFrom-Json
    $dlqMessages = $dlqStats.Attributes.ApproximateNumberOfMessages
    
    # Display
    Write-Host "[$timestamp] Queue: $messages | In-Flight: $inFlight | DLQ: $dlqMessages" -ForegroundColor $(if ($dlqMessages -gt 0) { "Red" } elseif ($inFlight -gt 0) { "Yellow" } else { "Green" })
    
    # Check recent Lambda logs
    $logs = aws logs tail /aws/lambda/video-downloader --since 30s --region $Region --format short 2>$null
    if ($logs) {
        Write-Host "Recent activity detected!" -ForegroundColor Cyan
    }
    
    Start-Sleep -Seconds 5
}
