# safe-root-cleanup.ps1 - Production-ready root directory cleanup
# Created: November 6, 2025
# Purpose: Safely clean up root directory with archive and rollback capability

param(
    [switch]$DryRun,
    [switch]$SkipArchive
)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$archiveDir = "archive_$timestamp"

Write-Host "=== Safe Root Directory Cleanup ===" -ForegroundColor Cyan
Write-Host "Date: $(Get-Date -Format 'MMMM d, yyyy HH:mm')" -ForegroundColor Gray
Write-Host ""

if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
    Write-Host ""
}

# Step 1: Analyze what will be cleaned
Write-Host "[1/5] Analyzing files..." -ForegroundColor Green

$backupFiles = @(Get-ChildItem -File | Where-Object { $_.Name -like "*.backup*" })
$zipFiles = @(Get-ChildItem -File | Where-Object { $_.Name -like "*-api.zip" -or $_.Name -like "*-deployment.zip" -or $_.Name -like "*-lambda.zip" -or $_.Name -eq "function.zip" })
$testFiles = @(Get-ChildItem -File | Where-Object { $_.Name -like "test-*.html" -or $_.Name -like "test-*.json" -or $_.Name -like "*-payload.json" })
$tempFiles = @(Get-ChildItem -File | Where-Object { $_.Name -like "response*.json" -or $_.Name -eq "out.json" -or $_.Name -eq "payload.json" })

Write-Host "  Backup files: $($backupFiles.Count)" -ForegroundColor White
Write-Host "  Old ZIPs: $($zipFiles.Count)" -ForegroundColor White
Write-Host "  Test files: $($testFiles.Count)" -ForegroundColor White
Write-Host "  Temp files: $($tempFiles.Count)" -ForegroundColor White
Write-Host ""

# Step 2: Create archive (unless skipped)
if (-not $SkipArchive -and -not $DryRun) {
    Write-Host "[2/5] Creating archive..." -ForegroundColor Green
    
    mkdir "$archiveDir\backups" -Force | Out-Null
    mkdir "$archiveDir\old-deployments" -Force | Out-Null
    mkdir "$archiveDir\test-files" -Force | Out-Null
    mkdir "$archiveDir\temp-files" -Force | Out-Null
    
    if ($backupFiles) { Copy-Item $backupFiles "$archiveDir\backups\" -ErrorAction SilentlyContinue }
    if ($zipFiles) { Copy-Item $zipFiles "$archiveDir\old-deployments\" -ErrorAction SilentlyContinue }
    if ($testFiles) { Copy-Item $testFiles "$archiveDir\test-files\" -ErrorAction SilentlyContinue }
    if ($tempFiles) { Copy-Item $tempFiles "$archiveDir\temp-files\" -ErrorAction SilentlyContinue }
    
    Write-Host "  ✅ Archive created: $archiveDir" -ForegroundColor Green
} elseif ($DryRun) {
    Write-Host "[2/5] Would create archive: $archiveDir" -ForegroundColor Yellow
} else {
    Write-Host "[2/5] Skipping archive (--SkipArchive flag)" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Create organized directories
Write-Host "[3/5] Creating organized directories..." -ForegroundColor Green

$dirs = @(
    "archive",
    "tests\integration",
    "tests\payloads"
)

foreach ($dir in $dirs) {
    if ($DryRun) {
        Write-Host "  Would create: $dir" -ForegroundColor Yellow
    } else {
        mkdir $dir -Force -ErrorAction SilentlyContinue | Out-Null
        Write-Host "  ✅ Created: $dir" -ForegroundColor White
    }
}
Write-Host ""

# Step 4: Move/Remove files
Write-Host "[4/5] Cleaning up root directory..." -ForegroundColor Green

if ($DryRun) {
    Write-Host "  Would remove $($backupFiles.Count) backup files" -ForegroundColor Yellow
    Write-Host "  Would remove $($zipFiles.Count) old deployment packages" -ForegroundColor Yellow
    Write-Host "  Would move $($testFiles.Count) test files to tests\integration\" -ForegroundColor Yellow
    Write-Host "  Would move $($tempFiles.Count) temp files to tests\payloads\" -ForegroundColor Yellow
} else {
    # Remove backup files
    if ($backupFiles) {
        Remove-Item $backupFiles -Force -ErrorAction SilentlyContinue
        Write-Host "  ✅ Removed $($backupFiles.Count) backup files" -ForegroundColor White
    }
    
    # Remove old ZIPs
    if ($zipFiles) {
        Remove-Item $zipFiles -Force -ErrorAction SilentlyContinue
        Write-Host "  ✅ Removed $($zipFiles.Count) old deployment packages" -ForegroundColor White
    }
    
    # Move test files
    if ($testFiles) {
        Move-Item $testFiles tests\integration\ -Force -ErrorAction SilentlyContinue
        Write-Host "  ✅ Moved $($testFiles.Count) test files to tests\integration\" -ForegroundColor White
    }
    
    # Move temp files
    if ($tempFiles) {
        Move-Item $tempFiles tests\payloads\ -Force -ErrorAction SilentlyContinue
        Write-Host "  ✅ Moved $($tempFiles.Count) temp files to tests\payloads\" -ForegroundColor White
    }
}
Write-Host ""

# Step 5: Summary
Write-Host "[5/5] Summary" -ForegroundColor Green

if ($DryRun) {
    Write-Host "  This was a DRY RUN - no changes were made" -ForegroundColor Yellow
    Write-Host "  Run without -DryRun to apply changes" -ForegroundColor Yellow
} else {
    Write-Host "  ✅ Root directory cleaned" -ForegroundColor Green
    if (-not $SkipArchive) {
        Write-Host "  ✅ Archive saved: $archiveDir" -ForegroundColor Green
        Write-Host ""
        Write-Host "  To rollback: .\rollback-cleanup.ps1 -ArchiveDir $archiveDir" -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "=== Cleanup Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "1. Run: .\verify-cleanup.ps1" -ForegroundColor Gray
Write-Host "2. Visit: https://christianconservativestoday.com" -ForegroundColor Gray
Write-Host "3. If all works, proceed to Phase 1" -ForegroundColor Gray
