# Test Blue/Green Deployment for auth-api
# This script demonstrates zero-downtime deployment with Lambda versioning

Write-Host "`n=== Lambda Blue/Green Deployment Test ===" -ForegroundColor Cyan

# Step 1: Check current alias
Write-Host "`n1. Current alias configuration:" -ForegroundColor Yellow
aws lambda get-alias --function-name auth-api --name live --query '{Version:FunctionVersion,ARN:AliasArn}' --output table

# Step 2: List recent versions
Write-Host "`n2. Recent Lambda versions:" -ForegroundColor Yellow
aws lambda list-versions-by-function --function-name auth-api --query 'Versions[-5:].{Version:Version,LastModified:LastModified}' --output table

# Step 3: Simulate deploying new version (just republish current code)
Write-Host "`n3. Publishing new version (simulated deployment)..." -ForegroundColor Yellow
$result = aws lambda update-function-code --function-name auth-api --zip-file fileb://modules/lambda/placeholder.zip --publish | ConvertFrom-Json
$newVersion = $result.Version
Write-Host "   Created version: $newVersion" -ForegroundColor Green

# Step 4: Test new version directly (before switching alias)
Write-Host "`n4. Testing new version $newVersion directly..." -ForegroundColor Yellow
Write-Host "   (In production, you'd test the new version here)" -ForegroundColor Gray

# Step 5: Update alias to new version (BLUE/GREEN CUTOVER)
Write-Host "`n5. Updating 'live' alias to version $newVersion (instant cutover)..." -ForegroundColor Yellow
aws lambda update-alias --function-name auth-api --name live --function-version $newVersion | Out-Null
Write-Host "   ✓ Alias updated - all traffic now on version $newVersion" -ForegroundColor Green

# Step 6: Verify alias update
Write-Host "`n6. Verify alias now points to new version:" -ForegroundColor Yellow
aws lambda get-alias --function-name auth-api --name live --query '{Version:FunctionVersion,ARN:AliasArn}' --output table

# Step 7: Demonstrate rollback capability
Write-Host "`n7. Demonstrating instant rollback..." -ForegroundColor Yellow
$previousVersion = [int]$newVersion - 1
Write-Host "   Rolling back to version $previousVersion..." -ForegroundColor Gray
aws lambda update-alias --function-name auth-api --name live --function-version $previousVersion | Out-Null
Write-Host "   ✓ Rolled back - all traffic now on version $previousVersion" -ForegroundColor Green

# Step 8: Verify rollback
Write-Host "`n8. Verify rollback successful:" -ForegroundColor Yellow
aws lambda get-alias --function-name auth-api --name live --query '{Version:FunctionVersion,ARN:AliasArn}' --output table

# Step 9: Switch back to latest version
Write-Host "`n9. Switching back to version $newVersion..." -ForegroundColor Yellow
aws lambda update-alias --function-name auth-api --name live --function-version $newVersion | Out-Null
Write-Host "   ✓ Back on version $newVersion" -ForegroundColor Green

Write-Host "`n=== Test Complete ===" -ForegroundColor Cyan
Write-Host "`nKey Takeaways:" -ForegroundColor Yellow
Write-Host "  • New versions created with --publish flag" -ForegroundColor White
Write-Host "  • Alias update = instant cutover (< 1 second)" -ForegroundColor White
Write-Host "  • Rollback = instant (just update alias back)" -ForegroundColor White
Write-Host "  • Zero downtime, no API Gateway changes needed" -ForegroundColor White
Write-Host ""
