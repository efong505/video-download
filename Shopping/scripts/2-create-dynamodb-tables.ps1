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
    --global-secondary-indexes `
        "[{\"IndexName\":\"category-created_at-index\",\"KeySchema\":[{\"AttributeName\":\"category\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"created_at\",\"KeyType\":\"RANGE\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}},{\"IndexName\":\"status-sales_count-index\",\"KeySchema\":[{\"AttributeName\":\"status\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"sales_count\",\"KeyType\":\"RANGE\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}},{\"IndexName\":\"featured-created_at-index\",\"KeySchema\":[{\"AttributeName\":\"featured\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"created_at\",\"KeyType\":\"RANGE\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}}]" `
    --region $region

# Table 2: Orders
Write-Host "`nCreating Orders table..." -ForegroundColor Yellow
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
    --global-secondary-indexes `
        "[{\"IndexName\":\"user_id-order_date-index\",\"KeySchema\":[{\"AttributeName\":\"user_id\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"order_date\",\"KeyType\":\"RANGE\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}},{\"IndexName\":\"order_status-order_date-index\",\"KeySchema\":[{\"AttributeName\":\"order_status\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"order_date\",\"KeyType\":\"RANGE\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}},{\"IndexName\":\"payment_status-order_date-index\",\"KeySchema\":[{\"AttributeName\":\"payment_status\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"order_date\",\"KeyType\":\"RANGE\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}}]" `
    --region $region

# Table 3: Cart
Write-Host "`nCreating Cart table..." -ForegroundColor Yellow
aws dynamodb create-table `
    --table-name Cart `
    --attribute-definitions AttributeName=user_id,AttributeType=S `
    --key-schema AttributeName=user_id,KeyType=HASH `
    --billing-mode PAY_PER_REQUEST `
    --region $region

# Enable TTL on Cart table
Write-Host "Enabling TTL on Cart table..." -ForegroundColor Gray
aws dynamodb update-time-to-live `
    --table-name Cart `
    --time-to-live-specification "Enabled=true,AttributeName=expires_at" `
    --region $region

# Table 4: Reviews
Write-Host "`nCreating Reviews table..." -ForegroundColor Yellow
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
    --global-secondary-indexes `
        "[{\"IndexName\":\"product_id-created_at-index\",\"KeySchema\":[{\"AttributeName\":\"product_id\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"created_at\",\"KeyType\":\"RANGE\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}},{\"IndexName\":\"user_id-created_at-index\",\"KeySchema\":[{\"AttributeName\":\"user_id\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"created_at\",\"KeyType\":\"RANGE\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}}]" `
    --region $region

Write-Host "`n✅ All DynamoDB tables created successfully!" -ForegroundColor Green
Write-Host "`nWaiting for tables to become active (this may take 1-2 minutes)..." -ForegroundColor Yellow

# Wait for tables to be active
$tables = @("Products", "Orders", "Cart", "Reviews")
foreach ($table in $tables) {
    Write-Host "Waiting for $table..." -ForegroundColor Gray
    aws dynamodb wait table-exists --table-name $table --region $region
}

Write-Host "`n✅ All tables are now active!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. Verify tables in AWS Console" -ForegroundColor White
Write-Host "  2. Run: .\3-test-infrastructure.ps1" -ForegroundColor White
