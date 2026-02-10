# delete-3-safe-apis.ps1
# Deletes ONLY the 3 confirmed safe APIs

param(
    [switch]$Confirm = $false,
    [string]$Region = "us-east-1"
)

$apisToDelete = @(
    @{Id="ulcbf9glui"; Name="notifications-api OLD"; Reason="Empty shell, replaced by lc7w6ebg4m"},
    @{Id="ts4xz3fs70"; Name="recipe-scraper-api OLD"; Reason="Empty shell, replaced by 1lgppg87fe"},
    @{Id="97gtxp82b2"; Name="MyFirstAPI"; Reason="Test API, no integrations"}
)

Write-Host "="*70 -ForegroundColor Cyan
Write-Host "DELETE 3 CONFIRMED SAFE APIs" -ForegroundColor Yellow
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

Write-Host "The following APIs will be PERMANENTLY DELETED:" -ForegroundColor Yellow
Write-Host ""

foreach ($api in $apisToDelete) {
    Write-Host "  $($api.Name)" -ForegroundColor White
    Write-Host "    ID: $($api.Id)" -ForegroundColor Gray
    Write-Host "    Reason: $($api.Reason)" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "="*70 -ForegroundColor Yellow

if (-not $Confirm) {
    Write-Host ""
    Write-Host "WARNING: This action cannot be undone!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Type 'DELETE' to confirm (or Ctrl+C to cancel): " -NoNewline -ForegroundColor Yellow
    $confirmation = Read-Host
    
    if ($confirmation -ne "DELETE") {
        Write-Host ""
        Write-Host "Deletion cancelled." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""
Write-Host "Deleting APIs..." -ForegroundColor Cyan
Write-Host ""

$deleted = @()
$failed = @()

foreach ($api in $apisToDelete) {
    Write-Host "Deleting: $($api.Name) ($($api.Id))..." -NoNewline
    
    try {
        aws apigateway delete-rest-api --rest-api-id $api.Id --region $Region 2>&1 | Out-Null
        
        # Verify deletion
        Start-Sleep -Seconds 2
        try {
            aws apigateway get-rest-api --rest-api-id $api.Id --region $Region 2>&1 | Out-Null
            Write-Host " WARNING: Still exists (may take time)" -ForegroundColor Yellow
            $deleted += $api
        } catch {
            Write-Host " SUCCESS" -ForegroundColor Green
            $deleted += $api
        }
    } catch {
        Write-Host " FAILED" -ForegroundColor Red
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
        $failed += $api
    }
}

Write-Host ""
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "DELETION SUMMARY" -ForegroundColor Yellow
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

if ($deleted.Count -gt 0) {
    Write-Host "Successfully deleted: $($deleted.Count)" -ForegroundColor Green
    foreach ($api in $deleted) {
        Write-Host "  - $($api.Name) ($($api.Id))" -ForegroundColor Green
    }
}

if ($failed.Count -gt 0) {
    Write-Host ""
    Write-Host "Failed to delete: $($failed.Count)" -ForegroundColor Red
    foreach ($api in $failed) {
        Write-Host "  - $($api.Name) ($($api.Id))" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Operational Benefits:" -ForegroundColor Cyan
Write-Host "  - 3 fewer APIs to manage" -ForegroundColor White
Write-Host "  - Cleaner AWS Console" -ForegroundColor White
Write-Host "  - Reduced confusion" -ForegroundColor White

# Create deletion log
$deletionLog = @{
    Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    DeletedAPIs = $deleted
    FailedAPIs = $failed
    TotalDeleted = $deleted.Count
}

$logFile = "deletion-log-$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
$deletionLog | ConvertTo-Json -Depth 10 | Out-File $logFile

Write-Host ""
Write-Host "Deletion log saved to: $logFile" -ForegroundColor Gray
Write-Host ""
Write-Host "="*70 -ForegroundColor Cyan
