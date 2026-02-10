# Deploy Rate Limiting Updates

Write-Host "=== Deploying Rate Limiting ===" -ForegroundColor Cyan

# Step 1: Create rate-limits table
Write-Host "`n1. Creating rate-limits DynamoDB table..." -ForegroundColor Yellow
.\create-rate-limit-table.ps1

# Step 2: Deploy Lambda updates
Write-Host "`n2. Deploying Lambda functions..." -ForegroundColor Yellow

$functions = @(
    @{Name="video-download-router"; Path="..\..\router"},
    @{Name="articles-api"; Path="..\..\articles_api"}
)

foreach ($func in $functions) {
    Write-Host "`nDeploying $($func.Name)..." -ForegroundColor Yellow
    
    $zipFile = "$($func.Name)-rl.zip"
    
    Push-Location $func.Path
    
    if (Test-Path $zipFile) {
        Remove-Item $zipFile
    }
    
    Compress-Archive -Path "index.py" -DestinationPath $zipFile
    
    aws lambda update-function-code `
        --function-name $func.Name `
        --zip-file "fileb://$zipFile"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $($func.Name) deployed" -ForegroundColor Green
    } else {
        Write-Host "✗ $($func.Name) failed" -ForegroundColor Red
    }
    
    Remove-Item $zipFile
    Pop-Location
    
    Start-Sleep -Seconds 2
}

Write-Host "`n=== Rate Limiting Deployment Complete ===" -ForegroundColor Cyan
Write-Host "`nRate Limits:" -ForegroundColor Yellow
Write-Host "  Anonymous: 20 requests/hour" -ForegroundColor Gray
Write-Host "  Free: 100 requests/hour" -ForegroundColor Gray
Write-Host "  Paid: 1000 requests/hour" -ForegroundColor Gray
Write-Host "  Admin: 10000 requests/hour" -ForegroundColor Gray
