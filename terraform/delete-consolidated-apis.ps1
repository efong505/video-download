# Delete old standalone APIs that are now consolidated into ministry-platform-api
# These APIs are replaced by the unified API Gateway (diz6ceeb22)

param(
    [switch]$DryRun = $true
)

Write-Host "=== Delete Consolidated API Gateways ===" -ForegroundColor Cyan
Write-Host "Mode: $(if ($DryRun) { 'DRY RUN' } else { 'LIVE DELETE' })" -ForegroundColor $(if ($DryRun) { 'Yellow' } else { 'Red' })

# Old standalone APIs now consolidated into ministry-platform-api (diz6ceeb22)
$consolidatedApis = @(
    @{ID="fr3hh94h4a"; Name="articles-api"},
    @{ID="h4hoegi26b"; Name="video-tag-api"},
    @{ID="j3w8kgqlvi"; Name="video-downloader-api"},
    @{ID="k2avuckm38"; Name="admin-api"},
    @{ID="l10alau5g3"; Name="comments-api"},
    @{ID="r6l0z3605f"; Name="auth-api"},
    @{ID="xr1xcc83bj"; Name="news-api"},
    @{ID="q65k3dbpd7"; Name="url-analysis-api"},
    @{ID="ckbtfz4vbl"; Name="resources-api"}
)

Write-Host "`nThese APIs are now consolidated into ministry-platform-api (diz6ceeb22):" -ForegroundColor Yellow
foreach ($api in $consolidatedApis) {
    Write-Host "  - $($api.Name) ($($api.ID))" -ForegroundColor White
}

Write-Host "`nBefore deleting, verify:" -ForegroundColor Cyan
Write-Host "1. All production HTML files use diz6ceeb22 (run update-all-production-urls.ps1)" -ForegroundColor White
Write-Host "2. Test the unified API endpoints work correctly" -ForegroundColor White
Write-Host "3. Check CloudWatch logs for any errors" -ForegroundColor White

if ($DryRun) {
    Write-Host "`n[DRY RUN] No changes made." -ForegroundColor Yellow
    Write-Host "Run with -DryRun:`$false to delete these APIs." -ForegroundColor Yellow
    exit
}

$confirm = Read-Host "`nType 'DELETE' to permanently remove these $($consolidatedApis.Count) APIs"
if ($confirm -ne 'DELETE') {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit
}

Write-Host "`nDeleting APIs..." -ForegroundColor Yellow
foreach ($api in $consolidatedApis) {
    try {
        Write-Host "Deleting $($api.Name) ($($api.ID))..." -ForegroundColor White
        aws apigateway delete-rest-api --rest-api-id $($api.ID)
        Write-Host "  ✓ Deleted" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ Failed: $_" -ForegroundColor Red
    }
}

Write-Host "`nDeletion complete!" -ForegroundColor Green
Write-Host "Remaining APIs: ministry-platform-api (diz6ceeb22) + unconsolidated APIs" -ForegroundColor Cyan
