# Check Child Account Credentials

Write-Host "=== Child Account Credentials Check ===" -ForegroundColor Green
Write-Host ""

# Check AWS profiles
Write-Host "Checking AWS profiles..." -ForegroundColor Yellow
$profiles = aws configure list-profiles 2>$null

if ($profiles) {
    Write-Host "Configured profiles:" -ForegroundColor Cyan
    $profiles | ForEach-Object { Write-Host "   - $_" -ForegroundColor Cyan }
    
    if ($profiles -contains "child-account") {
        Write-Host "`n✅ 'child-account' profile found" -ForegroundColor Green
        
        # Test it
        try {
            $childIdentity = aws sts get-caller-identity --profile child-account 2>&1 | ConvertFrom-Json
            Write-Host "   Account: $($childIdentity.Account)" -ForegroundColor Cyan
        } catch {
            Write-Host "   ⚠️  Profile exists but credentials may be invalid" -ForegroundColor Yellow
        }
    } else {
        Write-Host "`n⚠️  'child-account' profile NOT found" -ForegroundColor Yellow
    }
} else {
    Write-Host "No profiles configured" -ForegroundColor Yellow
}

# Test default credentials
Write-Host "`nTesting default credentials..." -ForegroundColor Yellow
try {
    $defaultIdentity = aws sts get-caller-identity 2>&1 | ConvertFrom-Json
    Write-Host "✅ Default credentials work" -ForegroundColor Green
    Write-Host "   Account: $($defaultIdentity.Account)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Default credentials not configured" -ForegroundColor Red
}

Write-Host "`n=== Summary ===" -ForegroundColor Green
Write-Host ""
Write-Host "For this tutorial:" -ForegroundColor Cyan
Write-Host "   ✅ You only need production account credentials (default)" -ForegroundColor Green
Write-Host "   ✅ Terraform uses cross-account role to access child account" -ForegroundColor Green
Write-Host "   ⚠️  Child account profile is optional (only for manual verification)" -ForegroundColor Yellow
Write-Host ""
Write-Host "To configure child account profile:" -ForegroundColor Cyan
Write-Host "   aws configure --profile child-account" -ForegroundColor Yellow
Write-Host ""
