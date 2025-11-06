# analyze-root-files.ps1 - Categorize root directory files

Write-Host "=== Root Directory File Analysis ===" -ForegroundColor Cyan
Write-Host ""

$rootPath = "C:\Users\Ed\Documents\Programming\AWS\Downloader"
Set-Location $rootPath

# Categorize Python files
$pythonFiles = Get-ChildItem *.py -File

$categories = @{
    "Election Data Management" = @()
    "Database Utilities" = @()
    "One-Time Fixes" = @()
    "Image/Video Processing" = @()
    "Development/Testing" = @()
    "Active Utilities" = @()
}

foreach ($file in $pythonFiles) {
    $name = $file.Name
    
    # Election data scripts
    if ($name -match "upload_.*_(candidates|races|data|summary)" -or 
        $name -match "delete_.*_data" -or 
        $name -match "update_.*_data" -or
        $name -match "get_.*_races" -or
        $name -match "hawaii|nebraska|virginia|texas|ohio|florida|california|new-jersey|new-mexico") {
        $categories["Election Data Management"] += $name
    }
    # One-time fixes
    elseif ($name -match "^fix_" -or 
            $name -match "^check_" -or 
            $name -match "^verify_" -or
            $name -match "^audit_" -or
            $name -match "^smart_fix" -or
            $name -match "auto_fix") {
        $categories["One-Time Fixes"] += $name
    }
    # Database setup/migration
    elseif ($name -match "^create_.*_table" -or 
            $name -match "^migrate_" -or 
            $name -match "^update_.*_(schema|roles|names)" -or
            $name -match "seed_") {
        $categories["Database Utilities"] += $name
    }
    # Image/video processing
    elseif ($name -match "thumbnail" -or 
            $name -match "preview" -or 
            $name -match "convert_base64") {
        $categories["Image/Video Processing"] += $name
    }
    # Development/testing
    elseif ($name -match "fargate_downloader" -or 
            $name -match "find_video") {
        $categories["Development/Testing"] += $name
    }
    # Active utilities
    else {
        $categories["Active Utilities"] += $name
    }
}

# Display categorized results
foreach ($category in $categories.Keys | Sort-Object) {
    $files = $categories[$category]
    if ($files.Count -gt 0) {
        Write-Host "[$category] ($($files.Count) files)" -ForegroundColor Green
        $files | Sort-Object | ForEach-Object {
            Write-Host "  - $_" -ForegroundColor Gray
        }
        Write-Host ""
    }
}

# Recommendations
Write-Host "=== Recommendations ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ KEEP (Active Utilities):" -ForegroundColor Green
$categories["Active Utilities"] | ForEach-Object {
    Write-Host "  - $_" -ForegroundColor White
}
Write-Host ""

Write-Host "MOVE to Scripts/election/:" -ForegroundColor Yellow
$electionCount = $categories['Election Data Management'].Count
Write-Host "  - All Election Data Management files ($electionCount files)" -ForegroundColor Gray
Write-Host ""

Write-Host "MOVE to Scripts/database/:" -ForegroundColor Yellow
$dbCount = $categories['Database Utilities'].Count
Write-Host "  - All Database Utilities files ($dbCount files)" -ForegroundColor Gray
Write-Host ""

Write-Host "MOVE to Scripts/maintenance/:" -ForegroundColor Yellow
$fixCount = $categories['One-Time Fixes'].Count
Write-Host "  - All One-Time Fixes files ($fixCount files)" -ForegroundColor Gray
Write-Host ""

Write-Host "MOVE to Scripts/media/:" -ForegroundColor Yellow
$mediaCount = $categories['Image/Video Processing'].Count
Write-Host "  - All Image/Video Processing files ($mediaCount files)" -ForegroundColor Gray
Write-Host ""

Write-Host "🗑️  ARCHIVE (Development/Testing):" -ForegroundColor Red
$categories["Development/Testing"] | ForEach-Object {
    Write-Host "  - $_" -ForegroundColor Gray
}
Write-Host ""

# Summary
$totalFiles = $pythonFiles.Count
$canMove = $categories["Election Data Management"].Count + 
           $categories["Database Utilities"].Count + 
           $categories["One-Time Fixes"].Count + 
           $categories["Image/Video Processing"].Count
$canArchive = $categories["Development/Testing"].Count
$shouldKeep = $categories["Active Utilities"].Count

Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host "Total Python files: $totalFiles" -ForegroundColor White
Write-Host "Can organize: $canMove files" -ForegroundColor Yellow
Write-Host "Can archive: $canArchive files" -ForegroundColor Red
Write-Host "Should keep in root: $shouldKeep files" -ForegroundColor Green
Write-Host ""
Write-Host "Run .\organize-root-files.ps1 to automatically organize these files" -ForegroundColor Cyan
