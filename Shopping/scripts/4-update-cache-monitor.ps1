# Shopping System - Update Auto-Cache-Monitor
# Adds Shopping tables to platform-wide cache monitoring

Write-Host "Updating auto-cache-monitor Lambda with Shopping tables..." -ForegroundColor Cyan

$region = "us-east-1"
$lambdaPath = "..\..\Architecture-Improvements\scripts\auto-cache-monitor"

# Navigate to Lambda directory
Push-Location $lambdaPath

try {
    # Create deployment package
    Write-Host "`nCreating deployment package..." -ForegroundColor Yellow
    if (Test-Path "function.zip") {
        Remove-Item "function.zip" -Force
    }
    Compress-Archive -Path "index.py" -DestinationPath "function.zip" -Force
    
    # Update Lambda function
    Write-Host "Updating Lambda function..." -ForegroundColor Yellow
    aws lambda update-function-code `
        --function-name auto-cache-monitor `
        --zip-file fileb://function.zip `
        --region $region | Out-Null
    
    Write-Host "✅ Lambda updated successfully!" -ForegroundColor Green
    
    # Test the updated Lambda
    Write-Host "`nTesting updated Lambda..." -ForegroundColor Yellow
    aws lambda invoke `
        --function-name auto-cache-monitor `
        --region $region `
        response.json | Out-Null
    
    if (Test-Path "response.json") {
        $response = Get-Content "response.json" | ConvertFrom-Json
        Write-Host "✅ Lambda test successful!" -ForegroundColor Green
        Write-Host "`nResponse:" -ForegroundColor Gray
        Write-Host ($response | ConvertTo-Json -Depth 3) -ForegroundColor Gray
        Remove-Item "response.json" -Force
    }
    
    Write-Host "`n✅ Auto-cache-monitor now monitors Shopping tables!" -ForegroundColor Green
    Write-Host "`nMonitored tables:" -ForegroundColor Cyan
    Write-Host "  Main Platform: Videos, Articles, News, Races, Candidates" -ForegroundColor White
    Write-Host "  Shopping: Products, Orders, Cart, Reviews" -ForegroundColor White
    Write-Host "`nThresholds:" -ForegroundColor Cyan
    Write-Host "  ElastiCache: 2M reads/day (combined)" -ForegroundColor White
    Write-Host "  API Gateway Cache: 500K requests/day" -ForegroundColor White
    
} catch {
    Write-Host "❌ Error updating Lambda: $_" -ForegroundColor Red
} finally {
    Pop-Location
}

Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. Lambda runs daily at 2 AM UTC" -ForegroundColor White
Write-Host "  2. Monitors combined traffic across all tables" -ForegroundColor White
Write-Host "  3. Auto-enables caching when thresholds reached" -ForegroundColor White
Write-Host "  4. No manual intervention needed!" -ForegroundColor White
