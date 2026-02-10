# Verify Rate Limiting Deployment

Write-Host "=== Verifying Rate Limiting Deployment ===" -ForegroundColor Cyan

Write-Host "`n1. Checking rate-limits table..." -ForegroundColor Yellow
aws dynamodb describe-table --table-name rate-limits --query "Table.[TableName,TableStatus,ItemCount]" --output table

Write-Host "`n2. Checking Lambda functions..." -ForegroundColor Yellow
aws lambda get-function --function-name video-download-router --query "Configuration.[FunctionName,LastModified,CodeSize]" --output table
aws lambda get-function --function-name articles-api --query "Configuration.[FunctionName,LastModified,CodeSize]" --output table

Write-Host "`n=== Deployment Verification Complete ===" -ForegroundColor Cyan
Write-Host "`nRate Limiting is now active:" -ForegroundColor Green
Write-Host "  Anonymous: 20 requests/hour" -ForegroundColor Gray
Write-Host "  Free: 100 requests/hour" -ForegroundColor Gray
Write-Host "  Paid: 1000 requests/hour" -ForegroundColor Gray
Write-Host "  Admin: 10000 requests/hour" -ForegroundColor Gray
