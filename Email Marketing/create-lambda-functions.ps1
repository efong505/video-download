# Create Lambda functions for email marketing system
# Run this ONCE to create the functions, then use deploy-all.ps1 to update them

Write-Host "Creating Lambda functions for Email Marketing System..." -ForegroundColor Cyan

$functions = @(
    @{
        Name = "email_subscribers_api"
        Description = "Email subscriber management API"
        Timeout = 30
        Memory = 512
    },
    @{
        Name = "email_campaigns_api"
        Description = "Email campaign management API"
        Timeout = 30
        Memory = 512
    },
    @{
        Name = "email_sender"
        Description = "Batch email sending with throttling"
        Timeout = 300
        Memory = 1024
    },
    @{
        Name = "email_tracking_api"
        Description = "Email open and click tracking"
        Timeout = 15
        Memory = 256
    }
)

foreach ($func in $functions) {
    Write-Host "`nCreating $($func.Name)..." -ForegroundColor Yellow
    
    # Create empty deployment package
    $tempFile = "temp-$($func.Name).py"
    "def lambda_handler(event, context): return {'statusCode': 200}" | Out-File -FilePath $tempFile -Encoding utf8
    Compress-Archive -Path $tempFile -DestinationPath "temp.zip" -Force
    
    # Create Lambda function
    aws lambda create-function `
        --function-name $func.Name `
        --runtime python3.12 `
        --role arn:aws:iam::YOUR-ACCOUNT-ID:role/lambda-execution-role `
        --handler index.lambda_handler `
        --timeout $func.Timeout `
        --memory-size $func.Memory `
        --description $func.Description `
        --zip-file fileb://temp.zip
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $($func.Name) created" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to create $($func.Name)" -ForegroundColor Red
    }
    
    # Cleanup
    Remove-Item $tempFile -ErrorAction SilentlyContinue
    Remove-Item "temp.zip" -ErrorAction SilentlyContinue
    
    Start-Sleep -Seconds 2
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✓ Lambda functions created!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Update IAM role ARN in this script (line 35)" -ForegroundColor White
Write-Host "2. Deploy actual code: .\deploy-all.ps1" -ForegroundColor White
Write-Host "3. Set up environment variables for each function" -ForegroundColor White

Write-Host "`nEnvironment variables needed:" -ForegroundColor Yellow
Write-Host "SES_FROM_EMAIL=newsletter@christianconservativestoday.com" -ForegroundColor White
Write-Host "SES_FROM_NAME=Christian Conservatives Today" -ForegroundColor White
Write-Host "SES_REPLY_TO=contact@christianconservativestoday.com" -ForegroundColor White
Write-Host "DOMAIN=christianconservativestoday.com" -ForegroundColor White
