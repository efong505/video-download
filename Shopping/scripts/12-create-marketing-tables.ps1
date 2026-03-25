# Week 8: Create Marketing Automation DynamoDB Tables
# Tables: MarketingQueue, EmailPreferences

$profile = "ekewaka"
$region = "us-east-1"

Write-Host "`n=== Week 8: Creating Marketing Tables ===" -ForegroundColor Cyan

# --- MarketingQueue Table ---
Write-Host "`nCreating MarketingQueue table..." -ForegroundColor Yellow
aws dynamodb create-table `
    --table-name MarketingQueue `
    --attribute-definitions `
        AttributeName=queue_id,AttributeType=S `
        AttributeName=sent,AttributeType=S `
        AttributeName=scheduled_send_time,AttributeType=S `
        AttributeName=user_email,AttributeType=S `
        AttributeName=trigger_type,AttributeType=S `
    --key-schema AttributeName=queue_id,KeyType=HASH `
    --global-secondary-indexes file://marketingqueue-gsi.json `
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 `
    --region $region --profile $profile --no-cli-pager | Out-Null

if ($LASTEXITCODE -eq 0) { Write-Host "  MarketingQueue created" -ForegroundColor Green }
else { Write-Host "  MarketingQueue may already exist" -ForegroundColor Yellow }

# --- EmailPreferences Table ---
Write-Host "`nCreating EmailPreferences table..." -ForegroundColor Yellow
aws dynamodb create-table `
    --table-name EmailPreferences `
    --attribute-definitions AttributeName=user_id,AttributeType=S `
    --key-schema AttributeName=user_id,KeyType=HASH `
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 `
    --region $region --profile $profile --no-cli-pager | Out-Null

if ($LASTEXITCODE -eq 0) { Write-Host "  EmailPreferences created" -ForegroundColor Green }
else { Write-Host "  EmailPreferences may already exist" -ForegroundColor Yellow }

# Enable TTL on MarketingQueue (30 days after sent)
Write-Host "`nWaiting for tables..." -ForegroundColor Yellow
aws dynamodb wait table-exists --table-name MarketingQueue --region $region --profile $profile
aws dynamodb wait table-exists --table-name EmailPreferences --region $region --profile $profile

aws dynamodb update-time-to-live `
    --table-name MarketingQueue `
    --time-to-live-specification "Enabled=true,AttributeName=expires_at" `
    --region $region --profile $profile --no-cli-pager 2>$null

# Verify
Write-Host "`n=== Verification ===" -ForegroundColor Cyan
$mqStatus = aws dynamodb describe-table --table-name MarketingQueue --query "Table.TableStatus" --output text --region $region --profile $profile
$epStatus = aws dynamodb describe-table --table-name EmailPreferences --query "Table.TableStatus" --output text --region $region --profile $profile
Write-Host "  MarketingQueue:    $mqStatus" -ForegroundColor $(if ($mqStatus -eq "ACTIVE") {"Green"} else {"Red"})
Write-Host "  EmailPreferences:  $epStatus" -ForegroundColor $(if ($epStatus -eq "ACTIVE") {"Green"} else {"Red"})

if ($mqStatus -eq "ACTIVE" -and $epStatus -eq "ACTIVE") {
    Write-Host "`n=== All marketing tables created! ===" -ForegroundColor Green
}
