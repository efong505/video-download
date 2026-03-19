# Create EventBridge schedule for drip processor
# Runs daily at 9am EST
# Run: .\create-drip-schedule.ps1

Write-Host "Creating EventBridge schedule for drip processor..." -ForegroundColor Green

# Create EventBridge rule
aws events put-rule `
    --name email-drip-processor-daily `
    --description "Trigger email drip processor daily at 9am EST" `
    --schedule-expression "cron(0 14 * * ? *)" `
    --region us-east-1 `
    --profile ekewaka

# Add Lambda permission for EventBridge
aws lambda add-permission `
    --function-name email-drip-processor `
    --statement-id EventBridgeDailyInvoke `
    --action lambda:InvokeFunction `
    --principal events.amazonaws.com `
    --source-arn arn:aws:events:us-east-1:371751795928:rule/email-drip-processor-daily `
    --region us-east-1 `
    --profile ekewaka

# Add Lambda as target
aws events put-targets `
    --rule email-drip-processor-daily `
    --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:371751795928:function:email-drip-processor" `
    --region us-east-1 `
    --profile ekewaka

Write-Host "`n[SUCCESS] EventBridge schedule created!" -ForegroundColor Green
Write-Host "Drip processor will run daily at 9am EST (2pm UTC)" -ForegroundColor Cyan
