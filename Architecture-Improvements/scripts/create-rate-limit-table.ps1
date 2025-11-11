# Create DynamoDB table for rate limiting

Write-Host "Creating rate-limits DynamoDB table..." -ForegroundColor Cyan

aws dynamodb create-table `
    --table-name rate-limits `
    --attribute-definitions AttributeName=rate_key,AttributeType=S `
    --key-schema AttributeName=rate_key,KeyType=HASH `
    --billing-mode PAY_PER_REQUEST `
    --tags Key=Purpose,Value=RateLimiting Key=Cost,Value=Zero

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ rate-limits table created successfully" -ForegroundColor Green
    Write-Host "Waiting for table to become active..." -ForegroundColor Yellow
    aws dynamodb wait table-exists --table-name rate-limits
    Write-Host "✓ Table is active" -ForegroundColor Green
} else {
    Write-Host "✗ Table creation failed (may already exist)" -ForegroundColor Red
}
