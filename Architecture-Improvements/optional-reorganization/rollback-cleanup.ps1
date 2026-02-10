# rollback-cleanup.ps1 - Rollback cleanup changes
# Created: November 6, 2025

param(
    [string]$ArchiveDir
)

Write-Host "=== Rollback Cleanup Changes ===" -ForegroundColor Cyan
Write-Host ""

# Find most recent archive if not specified
if (-not $ArchiveDir) {
    $archives = Get-ChildItem archive_* -Directory | Sort-Object Name -Descending
    if ($archives) {
        $ArchiveDir = $archives[0].Name
        Write-Host "Using most recent archive: $ArchiveDir" -ForegroundColor Yellow
    } else {
        Write-Host "❌ No archive found. Cannot rollback." -ForegroundColor Red
        Write-Host ""
        Write-Host "Archives should be named: archive_YYYYMMDD_HHMMSS" -ForegroundColor Gray
        exit 1
    }
}

# Verify archive exists
if (-not (Test-Path $ArchiveDir)) {
    Write-Host "❌ Archive not found: $ArchiveDir" -ForegroundColor Red
    exit 1
}

Write-Host "Rolling back from: $ArchiveDir" -ForegroundColor White
Write-Host ""

# Restore files
Write-Host "[1/4] Restoring backup files..." -ForegroundColor Green
if (Test-Path "$ArchiveDir\backups") {
    Copy-Item "$ArchiveDir\backups\*" . -Force -ErrorAction SilentlyContinue
    $count = (Get-ChildItem "$ArchiveDir\backups").Count
    Write-Host "  ✅ Restored $count backup files" -ForegroundColor White
}

Write-Host "[2/4] Restoring deployment packages..." -ForegroundColor Green
if (Test-Path "$ArchiveDir\old-deployments") {
    Copy-Item "$ArchiveDir\old-deployments\*" . -Force -ErrorAction SilentlyContinue
    $count = (Get-ChildItem "$ArchiveDir\old-deployments").Count
    Write-Host "  ✅ Restored $count deployment packages" -ForegroundColor White
}

Write-Host "[3/4] Restoring test files..." -ForegroundColor Green
if (Test-Path "$ArchiveDir\test-files") {
    Copy-Item "$ArchiveDir\test-files\*" . -Force -ErrorAction SilentlyContinue
    $count = (Get-ChildItem "$ArchiveDir\test-files").Count
    Write-Host "  ✅ Restored $count test files" -ForegroundColor White
}

Write-Host "[4/4] Restoring temp files..." -ForegroundColor Green
if (Test-Path "$ArchiveDir\temp-files") {
    Copy-Item "$ArchiveDir\temp-files\*" . -Force -ErrorAction SilentlyContinue
    $count = (Get-ChildItem "$ArchiveDir\temp-files").Count
    Write-Host "  ✅ Restored $count temp files" -ForegroundColor White
}

Write-Host ""
Write-Host "✅ Rollback complete!" -ForegroundColor Green
Write-Host ""
Write-Host "All files restored from archive." -ForegroundColor White
Write-Host "Archive preserved at: $ArchiveDir" -ForegroundColor Gray
Write-Host ""
Write-Host "=== Rollback Complete ===" -ForegroundColor Cyan
