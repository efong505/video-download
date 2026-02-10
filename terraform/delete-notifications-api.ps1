# Delete old standalone notifications API Gateway after consolidation
# API ID: lc7w6ebg4m

$apiId = "lc7w6ebg4m"
$apiName = "notifications-api"

Write-Host "=== Notifications API Deletion Script ===" -ForegroundColor Cyan
Write-Host ""

# Get API details
Write-Host "Fetching API details..." -ForegroundColor Yellow
$api = aws apigateway get-rest-api --rest-api-id $apiId 2>$null | ConvertFrom-Json

if (-not $api) {
    Write-Host "API $apiId not found or already deleted" -ForegroundColor Green
    exit 0
}

Write-Host "Found API: $($api.name) (ID: $apiId)" -ForegroundColor White
Write-Host "Created: $($api.createdDate)" -ForegroundColor Gray
Write-Host ""

# Confirmation
Write-Host "WARNING: This will permanently delete the standalone notifications API" -ForegroundColor Red
Write-Host "The unified API (diz6ceeb22) should already have /notifications endpoint" -ForegroundColor Yellow
Write-Host ""
$confirm = Read-Host "Type 'DELETE' to confirm deletion"

if ($confirm -ne "DELETE") {
    Write-Host "Deletion cancelled" -ForegroundColor Yellow
    exit 0
}

# Delete API
Write-Host ""
Write-Host "Deleting API Gateway $apiId..." -ForegroundColor Yellow
aws apigateway delete-rest-api --rest-api-id $apiId

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Successfully deleted $apiName" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to delete API" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Consolidation complete! All notifications traffic now uses:" -ForegroundColor Green
Write-Host "https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/notifications" -ForegroundColor Cyan
