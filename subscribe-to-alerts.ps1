# Subscribe to CloudWatch Alerts
# Adds your email/phone to receive alarm notifications

param(
    [Parameter(Mandatory=$true)]
    [string]$Email,
    
    [Parameter(Mandatory=$false)]
    [string]$Phone
)

$topicArn = "arn:aws:sns:us-east-1:371751795928:platform-critical-alerts"

Write-Host "Subscribing to CloudWatch alerts..." -ForegroundColor Yellow

# Subscribe email
if ($Email) {
    Write-Host "`nSubscribing email: $Email" -ForegroundColor Cyan
    aws sns subscribe --topic-arn $topicArn --protocol email --notification-endpoint $Email
    Write-Host "✓ Email subscription created. CHECK YOUR EMAIL for confirmation link!" -ForegroundColor Green
}

# Subscribe phone (SMS)
if ($Phone) {
    Write-Host "`nSubscribing phone: $Phone" -ForegroundColor Cyan
    aws sns subscribe --topic-arn $topicArn --protocol sms --notification-endpoint $Phone
    Write-Host "✓ SMS subscription created." -ForegroundColor Green
}

Write-Host "`n📧 IMPORTANT: Check your email and click the confirmation link!" -ForegroundColor Yellow
Write-Host "You won't receive alerts until you confirm the subscription." -ForegroundColor Yellow

Write-Host "`n✅ Subscription complete!" -ForegroundColor Green
Write-Host "You'll now receive alerts when:" -ForegroundColor Cyan
Write-Host "  - Lambda functions error" -ForegroundColor White
Write-Host "  - API Gateway has 5XX errors" -ForegroundColor White
Write-Host "  - Functions exceed duration thresholds" -ForegroundColor White
Write-Host "  - Functions are throttled" -ForegroundColor White
