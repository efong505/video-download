# Deploy all email marketing Lambda functions

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deploying Email Marketing System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$functions = @(
    "email_subscribers_api",
    "email_campaigns_api",
    "email_sender",
    "email_tracking_api"
)

$successCount = 0
$failCount = 0

foreach ($func in $functions) {
    Write-Host "`nDeploying $func..." -ForegroundColor Yellow
    
    Push-Location "$func"
    
    if (Test-Path "deploy.ps1") {
        .\deploy.ps1
        
        if ($LASTEXITCODE -eq 0) {
            $successCount++
            Write-Host "✓ $func deployed successfully" -ForegroundColor Green
        } else {
            $failCount++
            Write-Host "✗ $func deployment failed" -ForegroundColor Red
        }
    } else {
        Write-Host "✗ deploy.ps1 not found for $func" -ForegroundColor Red
        $failCount++
    }
    
    Pop-Location
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Deployment Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Successful: $successCount" -ForegroundColor Green
Write-Host "✗ Failed: $failCount" -ForegroundColor Red

if ($failCount -eq 0) {
    Write-Host "`n🎉 All functions deployed successfully!" -ForegroundColor Green
} else {
    Write-Host "`n⚠️  Some deployments failed. Check logs above." -ForegroundColor Yellow
}
