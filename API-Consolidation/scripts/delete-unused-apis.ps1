# delete-unused-apis.ps1
# Deletes APIs that have been verified as unused
# ONLY run this after running verify-unused-apis.ps1

param(
    [switch]$DryRun = $false,
    [string]$Region = "us-east-1"
)

Write-Host "🗑️  API Deletion Script" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "⚠️  DRY RUN MODE - No APIs will be deleted" -ForegroundColor Yellow
    Write-Host ""
}

# Load the most recent verification report
$reportFiles = Get-ChildItem -Path "." -Filter "api-verification-report-*.json" | Sort-Object LastWriteTime -Descending
if ($reportFiles.Count -eq 0) {
    Write-Host "❌ ERROR: No verification report found!" -ForegroundColor Red
    Write-Host "Please run .\verify-unused-apis.ps1 first" -ForegroundColor Yellow
    exit 1
}

$reportFile = $reportFiles[0]
Write-Host "📄 Loading verification report: $($reportFile.Name)" -ForegroundColor Cyan
$verificationResults = Get-Content $reportFile.FullName | ConvertFrom-Json

# Filter for safe-to-delete APIs
$safeToDelete = $verificationResults | Where-Object { $_.Recommendation -like "*SAFE TO DELETE*" }

if ($safeToDelete.Count -eq 0) {
    Write-Host "`n✅ No APIs marked as safe to delete" -ForegroundColor Green
    Write-Host "All APIs show some activity or need manual review" -ForegroundColor Gray
    exit 0
}

# Display APIs to be deleted
Write-Host "`n📋 APIs marked as SAFE TO DELETE:" -ForegroundColor Yellow
Write-Host "="*80 -ForegroundColor Gray
foreach ($api in $safeToDelete) {
    Write-Host "  • $($api.Name) ($($api.Id))" -ForegroundColor White
    Write-Host "    Traffic: $($api.RequestCount) requests | Logs: $($api.HasLogs) | In HTML: $($api.InHTMLFiles)" -ForegroundColor Gray
}
Write-Host "="*80 -ForegroundColor Gray

$monthlySavings = $safeToDelete.Count * 3.50
$annualSavings = $monthlySavings * 12

Write-Host "`n💰 Savings after deletion:" -ForegroundColor Cyan
Write-Host "   Monthly: `$$monthlySavings" -ForegroundColor Green
Write-Host "   Annual: `$$annualSavings" -ForegroundColor Green

if ($DryRun) {
    Write-Host "`n✅ DRY RUN COMPLETE - No APIs were deleted" -ForegroundColor Green
    Write-Host "Remove -DryRun flag to actually delete these APIs" -ForegroundColor Yellow
    exit 0
}

# Confirmation prompt
Write-Host "`n⚠️  WARNING: This will permanently delete $($safeToDelete.Count) API Gateway(s)" -ForegroundColor Red
Write-Host "This action cannot be undone!" -ForegroundColor Red
Write-Host ""
Write-Host "Type 'DELETE' to confirm (or Ctrl+C to cancel): " -NoNewline -ForegroundColor Yellow
$confirmation = Read-Host

if ($confirmation -ne "DELETE") {
    Write-Host "`n❌ Deletion cancelled" -ForegroundColor Yellow
    exit 0
}

# Delete APIs
Write-Host "`n🗑️  Deleting APIs..." -ForegroundColor Cyan
$deleted = @()
$failed = @()

foreach ($api in $safeToDelete) {
    Write-Host "`nDeleting: $($api.Name) ($($api.Id))..." -NoNewline
    
    try {
        if ($api.Id -eq "fm52xqjuz3") {
            # HTTP API
            aws apigatewayv2 delete-api --api-id $api.Id --region $Region 2>&1 | Out-Null
        } else {
            # REST API
            aws apigateway delete-rest-api --rest-api-id $api.Id --region $Region 2>&1 | Out-Null
        }
        
        # Verify deletion
        Start-Sleep -Seconds 2
        try {
            if ($api.Id -eq "fm52xqjuz3") {
                aws apigatewayv2 get-api --api-id $api.Id --region $Region 2>&1 | Out-Null
                Write-Host " ⚠️  Still exists (may take time)" -ForegroundColor Yellow
            } else {
                aws apigateway get-rest-api --rest-api-id $api.Id --region $Region 2>&1 | Out-Null
                Write-Host " ⚠️  Still exists (may take time)" -ForegroundColor Yellow
            }
        } catch {
            Write-Host " ✅ DELETED" -ForegroundColor Green
            $deleted += $api
        }
    } catch {
        Write-Host " ❌ FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        $failed += $api
    }
}

# Summary
Write-Host "`n" + "="*80 -ForegroundColor Cyan
Write-Host "📊 DELETION SUMMARY" -ForegroundColor Yellow
Write-Host "="*80 -ForegroundColor Cyan

Write-Host "`n✅ Successfully deleted: $($deleted.Count)" -ForegroundColor Green
foreach ($api in $deleted) {
    Write-Host "   - $($api.Name) ($($api.Id))" -ForegroundColor Green
}

if ($failed.Count -gt 0) {
    Write-Host "`n❌ Failed to delete: $($failed.Count)" -ForegroundColor Red
    foreach ($api in $failed) {
        Write-Host "   - $($api.Name) ($($api.Id))" -ForegroundColor Red
    }
}

$actualSavings = $deleted.Count * 3.50 * 12
Write-Host "`n💰 Actual annual savings: `$$actualSavings" -ForegroundColor Green

# Create deletion log
$deletionLog = @{
    Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Deleted = $deleted
    Failed = $failed
    Savings = @{
        Monthly = $deleted.Count * 3.50
        Annual = $actualSavings
    }
}

$logFile = "api-deletion-log-$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
$deletionLog | ConvertTo-Json -Depth 10 | Out-File $logFile

Write-Host "`n📄 Deletion log saved to: $logFile" -ForegroundColor Cyan

Write-Host "`n🎯 NEXT STEPS:" -ForegroundColor Cyan
Write-Host "   1. Verify APIs are deleted in AWS Console" -ForegroundColor White
Write-Host "   2. Monitor CloudWatch for any errors" -ForegroundColor White
Write-Host "   3. Proceed with API consolidation plan" -ForegroundColor White

Write-Host "`n" + "="*80 -ForegroundColor Cyan
