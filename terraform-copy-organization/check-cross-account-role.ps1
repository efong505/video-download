# Check Cross-Account Role

$childAccountId = "628478946937"
$roleName = "TerraformCrossAccountRole"
$roleArn = "arn:aws:iam::${childAccountId}:role/${roleName}"

Write-Host "=== Cross-Account Role Check ===" -ForegroundColor Green
Write-Host ""
Write-Host "Child Account ID: $childAccountId" -ForegroundColor Cyan
Write-Host "Role Name: $roleName" -ForegroundColor Cyan
Write-Host ""

# Test if we can assume the role
Write-Host "Testing role assumption..." -ForegroundColor Yellow

$output = aws sts assume-role `
    --role-arn $roleArn `
    --role-session-name "test-session" `
    --external-id "terraform-copy-tutorial" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Cross-account role EXISTS and is accessible!" -ForegroundColor Green
    Write-Host ""
    Write-Host "✅ You're ready to use the tutorial!" -ForegroundColor Green
} else {
    $errorMsg = $output | Out-String
    
    if ($errorMsg -like "*NoSuchEntity*" -or $errorMsg -like "*cannot be found*") {
        Write-Host "❌ Role does NOT exist in child account" -ForegroundColor Red
        Write-Host ""
        Write-Host "Create it using AWS Console:" -ForegroundColor Yellow
        Write-Host "   1. Log into child account (628478946937)" -ForegroundColor Cyan
        Write-Host "   2. IAM > Roles > Create Role" -ForegroundColor Cyan
        Write-Host "   3. Another AWS account: 371751795928" -ForegroundColor Cyan
        Write-Host "   4. Require external ID: terraform-copy-tutorial" -ForegroundColor Cyan
        Write-Host "   5. Attach: AdministratorAccess" -ForegroundColor Cyan
        Write-Host "   6. Name: TerraformCrossAccountRole" -ForegroundColor Cyan
    }
    elseif ($errorMsg -like "*AccessDenied*") {
        Write-Host "❌ Role exists but trust policy is wrong" -ForegroundColor Red
        Write-Host "   Trust policy must allow account 371751795928" -ForegroundColor Yellow
    }
    else {
        Write-Host "❌ Error: $errorMsg" -ForegroundColor Red
    }
}

Write-Host ""
