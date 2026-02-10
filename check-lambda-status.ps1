# Check Lambda execution status for specific request IDs
$requestIds = @(
    "0cbd6a12-dbab-4f74-ae9d-a54daa93d22b",
    "b949ec34-40c1-4f9a-8782-f6c00a77a50c"
)

foreach ($requestId in $requestIds) {
    Write-Host "=== Checking Request ID: $requestId ===" -ForegroundColor Yellow
    
    # Get logs for this specific request
    aws logs filter-log-events `
        --log-group-name "/aws/lambda/video-downloader" `
        --filter-pattern "$requestId" `
        --query "events[*].[timestamp,message]" `
        --output table
    
    Write-Host ""
}

# Also check for any ERROR or timeout messages in recent logs
Write-Host "=== Recent Errors/Timeouts ===" -ForegroundColor Red
aws logs filter-log-events `
    --log-group-name "/aws/lambda/video-downloader" `
    --start-time $([DateTimeOffset]::UtcNow.AddHours(-2).ToUnixTimeMilliseconds()) `
    --filter-pattern "ERROR OR timeout OR Task timed out" `
    --query "events[*].[timestamp,message]" `
    --output table