# Delete unused duplicate API Gateways
# Run analyze-active-apis.ps1 first to verify which are unused!

param(
    [switch]$DryRun = $true  # Default to dry run for safety
)

Write-Host "=== Delete Unused API Gateways ===" -ForegroundColor Cyan
Write-Host "Mode: $(if ($DryRun) { 'DRY RUN (no changes)' } else { 'LIVE DELETE' })" -ForegroundColor $(if ($DryRun) { 'Yellow' } else { 'Red' })

# List of API Gateway IDs to delete (unused duplicates)
$apisToDelete = @(
    # Add the unused contributors-api IDs here after verification
    # Example: "abc123xyz",
    # Example: "def456uvw"
    # Add the unused video-downloader-api ID here after verification
    # Example: "ghi789rst"
    "qdk8y6nna6", "o0mzmvcs59", "wzn7e1ipjf"
)

if ($apisToDelete.Count -eq 0) {
    Write-Host "`nNo APIs specified for deletion." -ForegroundColor Yellow
    Write-Host "Edit this script and add the API Gateway IDs to delete." -ForegroundColor Yellow
    Write-Host "`nSteps:" -ForegroundColor Cyan
    Write-Host "1. Run: .\analyze-active-apis.ps1" -ForegroundColor White
    Write-Host "2. Identify unused duplicate APIs" -ForegroundColor White
    Write-Host "3. Add their IDs to `$apisToDelete array in this script" -ForegroundColor White
    Write-Host "4. Run: .\delete-unused-apis.ps1 -DryRun" -ForegroundColor White
    Write-Host "5. Verify the list, then run: .\delete-unused-apis.ps1 -DryRun:`$false" -ForegroundColor White
    exit
}

# Get details for each API
Write-Host "`nAPIs to delete:" -ForegroundColor Yellow
foreach ($apiId in $apisToDelete) {
    try {
        $api = aws apigateway get-rest-api --rest-api-id $apiId --output json 2>$null | ConvertFrom-Json
        if ($api) {
            Write-Host "  - $($api.name) ($apiId)" -ForegroundColor White
            Write-Host "    Created: $($api.createdDate)" -ForegroundColor Gray
        } else {
            Write-Host "  - $apiId (NOT FOUND - may already be deleted)" -ForegroundColor Red
        }
    } catch {
        Write-Host "  - $apiId (ERROR: $_)" -ForegroundColor Red
    }
}

if ($DryRun) {
    Write-Host "`n[DRY RUN] No changes made." -ForegroundColor Yellow
    Write-Host "Run with -DryRun:`$false to actually delete these APIs." -ForegroundColor Yellow
    exit
}

# Confirm deletion
Write-Host "`nWARNING: This will permanently delete $($apisToDelete.Count) API Gateway(s)!" -ForegroundColor Red
$confirm = Read-Host "Type 'DELETE' to confirm"

if ($confirm -ne 'DELETE') {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit
}

# Delete each API
Write-Host "`nDeleting APIs..." -ForegroundColor Yellow
foreach ($apiId in $apisToDelete) {
    try {
        Write-Host "Deleting $apiId..." -ForegroundColor White
        aws apigateway delete-rest-api --rest-api-id $apiId
        Write-Host "  ✓ Deleted successfully" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ Failed: $_" -ForegroundColor Red
    }
}

Write-Host "`nDeletion complete!" -ForegroundColor Green
Write-Host "Verify in AWS Console: https://console.aws.amazon.com/apigateway" -ForegroundColor Cyan
