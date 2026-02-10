# organize-zip-files.ps1 - Move old deployment ZIPs to archive

param(
    [switch]$DryRun
)

$rootPath = "C:\Users\Ed\Documents\Programming\AWS\Downloader"
Set-Location $rootPath

Write-Host "=== Organize ZIP Files ===" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No files will be moved" -ForegroundColor Yellow
    Write-Host ""
}

# Get all ZIP files
$zipFiles = Get-ChildItem *.zip -File

Write-Host "[1/2] Found $($zipFiles.Count) ZIP files" -ForegroundColor Green
$zipFiles | ForEach-Object {
    Write-Host "  - $($_.Name)" -ForegroundColor Gray
}
Write-Host ""

# Create archive directory
Write-Host "[2/2] Moving ZIP files..." -ForegroundColor Green

if ($DryRun) {
    Write-Host "  Would create: archive\old-deployments\" -ForegroundColor Yellow
    Write-Host "  Would move $($zipFiles.Count) files to archive\old-deployments\" -ForegroundColor Yellow
} else {
    if (-not (Test-Path "archive\old-deployments")) {
        New-Item -ItemType Directory -Path "archive\old-deployments" -Force | Out-Null
        Write-Host "  ✅ Created: archive\old-deployments\" -ForegroundColor White
    }
    
    foreach ($file in $zipFiles) {
        Move-Item $file.FullName "archive\old-deployments\" -Force
        Write-Host "  ✅ Moved: $($file.Name)" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "=== Complete ===" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "This was a DRY RUN - no files were moved" -ForegroundColor Yellow
    Write-Host "Run without -DryRun to move files" -ForegroundColor Yellow
} else {
    Write-Host "✅ All ZIP files moved to archive\old-deployments\" -ForegroundColor Green
    Write-Host ""
    Write-Host "Note: These are old Lambda deployment packages" -ForegroundColor Gray
    Write-Host "They can be safely deleted after 30 days" -ForegroundColor Gray
}
