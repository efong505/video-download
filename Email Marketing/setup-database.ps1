# Create DynamoDB tables for email marketing system

Write-Host "Creating DynamoDB tables for Email Marketing System..." -ForegroundColor Cyan

# Create EmailSubscribers table
Write-Host "`nCreating EmailSubscribers table..." -ForegroundColor Yellow
aws dynamodb create-table `
    --table-name EmailSubscribers `
    --attribute-definitions `
        AttributeName=email,AttributeType=S `
        AttributeName=status,AttributeType=S `
    --key-schema `
        AttributeName=email,KeyType=HASH `
    --global-secondary-indexes `
        "IndexName=StatusIndex,KeySchema=[{AttributeName=status,KeyType=HASH}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}" `
    --billing-mode PAY_PER_REQUEST

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ EmailSubscribers table created" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create EmailSubscribers table" -ForegroundColor Red
}

Start-Sleep -Seconds 2

# Create EmailCampaigns table
Write-Host "`nCreating EmailCampaigns table..." -ForegroundColor Yellow
aws dynamodb create-table `
    --table-name EmailCampaigns `
    --attribute-definitions `
        AttributeName=campaign_id,AttributeType=S `
        AttributeName=status,AttributeType=S `
    --key-schema `
        AttributeName=campaign_id,KeyType=HASH `
    --global-secondary-indexes `
        "IndexName=StatusIndex,KeySchema=[{AttributeName=status,KeyType=HASH}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}" `
    --billing-mode PAY_PER_REQUEST

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ EmailCampaigns table created" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create EmailCampaigns table" -ForegroundColor Red
}

Start-Sleep -Seconds 2

# Create EmailAnalytics table
Write-Host "`nCreating EmailAnalytics table..." -ForegroundColor Yellow
aws dynamodb create-table `
    --table-name EmailAnalytics `
    --attribute-definitions `
        AttributeName=event_id,AttributeType=S `
        AttributeName=campaign_id,AttributeType=S `
    --key-schema `
        AttributeName=event_id,KeyType=HASH `
    --global-secondary-indexes `
        "IndexName=CampaignIndex,KeySchema=[{AttributeName=campaign_id,KeyType=HASH}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}" `
    --billing-mode PAY_PER_REQUEST

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ EmailAnalytics table created" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create EmailAnalytics table" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Waiting for tables to become active..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

Start-Sleep -Seconds 10

# Verify tables
Write-Host "`nVerifying tables..." -ForegroundColor Yellow
aws dynamodb list-tables --query "TableNames[?contains(@, 'Email')]"

Write-Host "`n✓ Database setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Deploy Lambda functions: .\deploy-all.ps1" -ForegroundColor White
Write-Host "2. Set up AWS SES: See SETUP.md Step 1" -ForegroundColor White
Write-Host "3. Create API Gateway endpoints: See SETUP.md Step 4" -ForegroundColor White
