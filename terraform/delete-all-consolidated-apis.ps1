# Delete all consolidated API Gateways
# These have been replaced by unified API: diz6ceeb22

$apisToDelete = @(
    @{id='r6l0z3605f'; name='auth-api'},
    @{id='fr3hh94h4a'; name='articles-api'},
    @{id='q65k3dbpd7'; name='url-analysis-api'},
    @{id='k2avuckm38'; name='admin-api'},
    @{id='xr1xcc83bj'; name='news-api'},
    @{id='h4hoegi26b'; name='video-tag-api'},
    @{id='l10alau5g3'; name='comments-api'},
    @{id='ckbtfz4vbl'; name='resources-api'}
)

Write-Host "=== Delete Consolidated API Gateways ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will delete 8 standalone APIs that have been consolidated into:" -ForegroundColor Yellow
Write-Host "https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod" -ForegroundColor Cyan
Write-Host ""

foreach ($api in $apisToDelete) {
    Write-Host "  - $($api.name) ($($api.id))" -ForegroundColor White
}

Write-Host ""
Write-Host "WARNING: This action cannot be undone!" -ForegroundColor Red
$confirm = Read-Host "Type 'DELETE ALL' to confirm"

if ($confirm -ne "DELETE ALL") {
    Write-Host "Deletion cancelled" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
$successCount = 0
$failCount = 0

foreach ($api in $apisToDelete) {
    Write-Host "Deleting $($api.name)..." -ForegroundColor Yellow
    aws apigateway delete-rest-api --rest-api-id $api.id 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Deleted $($api.name)" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "  ✗ Failed to delete $($api.name)" -ForegroundColor Red
        $failCount++
    }
}

Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host "Successfully deleted: $successCount" -ForegroundColor Green
Write-Host "Failed: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })
Write-Host ""
Write-Host "All traffic now uses unified API: diz6ceeb22" -ForegroundColor Cyan
