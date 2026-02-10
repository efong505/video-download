# Shopping System - Monitor SQS Queues
# Real-time monitoring of queue depths and DLQ messages

param(
    [int]$RefreshSeconds = 5
)

$region = "us-east-1"

$queues = @(
    @{Name="order-processing-queue"; Color="Cyan"},
    @{Name="payment-processing-queue"; Color="Yellow"},
    @{Name="email-notification-queue"; Color="Green"},
    @{Name="inventory-update-queue"; Color="Magenta"}
)

$dlqs = @(
    "order-processing-dlq",
    "payment-processing-dlq",
    "email-notification-dlq",
    "inventory-update-dlq"
)

Write-Host "Shopping System Queue Monitor" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to exit`n" -ForegroundColor Gray

while ($true) {
    Clear-Host
    Write-Host "Shopping System Queue Monitor - $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Cyan
    Write-Host ("="*70) -ForegroundColor Gray
    
    # Monitor main queues
    Write-Host "`nMain Queues:" -ForegroundColor White
    foreach ($queue in $queues) {
        try {
            $queueUrl = aws sqs get-queue-url --queue-name $queue.Name --region $region --query 'QueueUrl' --output text 2>$null
            $attrs = aws sqs get-queue-attributes --queue-url $queueUrl --attribute-names ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible --region $region | ConvertFrom-Json
            
            $visible = $attrs.Attributes.ApproximateNumberOfMessages
            $inFlight = $attrs.Attributes.ApproximateNumberOfMessagesNotVisible
            
            $status = if ($visible -eq 0 -and $inFlight -eq 0) { "✅" } elseif ($visible -gt 10) { "⚠️ " } else { "📨" }
            
            Write-Host "  $status $($queue.Name.PadRight(30)) Visible: $($visible.ToString().PadLeft(3))  In-Flight: $($inFlight.ToString().PadLeft(3))" -ForegroundColor $queue.Color
        } catch {
            Write-Host "  ❌ $($queue.Name) - Error reading queue" -ForegroundColor Red
        }
    }
    
    # Monitor DLQs
    Write-Host "`nDead Letter Queues:" -ForegroundColor White
    $dlqHasMessages = $false
    foreach ($dlq in $dlqs) {
        try {
            $queueUrl = aws sqs get-queue-url --queue-name $dlq --region $region --query 'QueueUrl' --output text 2>$null
            $count = aws sqs get-queue-attributes --queue-url $queueUrl --attribute-names ApproximateNumberOfMessages --region $region --query 'Attributes.ApproximateNumberOfMessages' --output text
            
            if ($count -gt 0) {
                Write-Host "  🚨 $($dlq.PadRight(30)) Messages: $count" -ForegroundColor Red
                $dlqHasMessages = $true
            } else {
                Write-Host "  ✅ $($dlq.PadRight(30)) Messages: 0" -ForegroundColor Green
            }
        } catch {
            Write-Host "  ❌ $dlq - Error reading queue" -ForegroundColor Red
        }
    }
    
    if ($dlqHasMessages) {
        Write-Host "`n⚠️  WARNING: Dead letter queues have messages - check for failures!" -ForegroundColor Red
    }
    
    Write-Host "`n" + ("="*70) -ForegroundColor Gray
    Write-Host "Refreshing every $RefreshSeconds seconds... (Ctrl+C to exit)" -ForegroundColor Gray
    
    Start-Sleep -Seconds $RefreshSeconds
}
