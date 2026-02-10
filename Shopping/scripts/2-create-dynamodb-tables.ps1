# Shopping System - Create DynamoDB Tables
# Week 1: Database Setup

Write-Host "Creating DynamoDB Tables for Shopping System..." -ForegroundColor Cyan

$region = "us-east-1"

# Table 1: Products
Write-Host "`nCreating Products table..." -ForegroundColor Yellow
aws dynamodb create-table `
    --table-name Products `
    --attribute-definitions `
        AttributeName=product_id,AttributeType=S `
        AttributeName=category,AttributeType=S `
        AttributeName=created_at,AttributeType=S `
        AttributeName=status,AttributeType=S `
        AttributeName=sales_count,AttributeType=N `
        AttributeName=featured,AttributeType=S `
    --key-schema AttributeName=product_id,KeyType=HASH `
    --billing-mode PAY_PER_REQUEST `
    --global-secondary-indexes file://products-gsi.json `
    --region $region | Out-Null

# Table 2: Orders
Write-Host "Creating Orders table..." -ForegroundColor Yellow
aws dynamodb create-table `
    --table-name Orders `
    --attribute-definitions `
        AttributeName=order_id,AttributeType=S `
        AttributeName=user_id,AttributeType=S `
        AttributeName=order_date,AttributeType=S `
        AttributeName=order_status,AttributeType=S `
        AttributeName=payment_status,AttributeType=S `
    --key-schema `
        AttributeName=order_id,KeyType=HASH `
        AttributeName=user_id,KeyType=RANGE `
    --billing-mode PAY_PER_REQUEST `
    --global-secondary-indexes file://orders-gsi.json `
    --region $region | Out-Null

# Table 4: Reviews
Write-Host "Creating Reviews table..." -ForegroundColor Yellow
aws dynamodb create-table `
    --table-name Reviews `
    --attribute-definitions `
        AttributeName=review_id,AttributeType=S `
        AttributeName=product_id,AttributeType=S `
        AttributeName=user_id,AttributeType=S `
        AttributeName=created_at,AttributeType=S `
    --key-schema `
        AttributeName=review_id,KeyType=HASH `
        AttributeName=product_id,KeyType=RANGE `
    --billing-mode PAY_PER_REQUEST `
    --global-secondary-indexes file://reviews-gsi.json `
    --region $region | Out-Null

Write-Host "`n✅ All DynamoDB tables created successfully!" -ForegroundColor Green
Write-Host "`nWaiting for tables to become active (this may take 1-2 minutes)...\" -ForegroundColor Yellow

# Wait for tables to be active
$tables = @("Products", "Orders", "Cart", "Reviews")
foreach ($table in $tables) {
    Write-Host "Waiting for $table..." -ForegroundColor Gray
    aws dynamodb wait table-exists --table-name $table --region $region
}

# Enable TTL on Cart table
Write-Host "`nEnabling TTL on Cart table..." -ForegroundColor Yellow
aws dynamodb update-time-to-live `
    --table-name Cart `
    --time-to-live-specification "Enabled=true,AttributeName=expires_at" `
    --region $region | Out-Null

Write-Host "`n✅ All tables are now active!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. Verify tables in AWS Console" -ForegroundColor White
Write-Host "  2. Run: .\3-test-infrastructure.ps1" -ForegroundColor White
