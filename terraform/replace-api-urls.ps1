# Replace Old API URLs with New Unified API URLs
# Creates backup before making changes

$downloaderPath = "C:\Users\Ed\Documents\Programming\AWS\Downloader"
$findingsFile = "$PSScriptRoot\api-url-findings.json"
$newBaseUrl = "https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod"

if (-not (Test-Path $findingsFile)) {
    Write-Host "❌ Run find-api-urls.ps1 first!" -ForegroundColor Red
    exit 1
}

$findings = Get-Content $findingsFile -Raw | ConvertFrom-Json

Write-Host "`n=== API URL Replacement Tool ===" -ForegroundColor Cyan
Write-Host "Found $($findings.Count) URLs to replace`n" -ForegroundColor Yellow

# Create backup directory
$backupDir = "$downloaderPath\backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "Creating backup: $backupDir" -ForegroundColor Gray
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

# Group by file
$byFile = $findings | Group-Object File

$filesUpdated = 0
$urlsReplaced = 0

foreach ($group in $byFile) {
    $fileName = $group.Name
    $filePath = Get-ChildItem -Path $downloaderPath -Filter $fileName -Recurse -ErrorAction SilentlyContinue | 
        Where-Object { $_.FullName -notmatch "node_modules|\.git|backup" } | 
        Select-Object -First 1
    
    if (-not $filePath) {
        Write-Host "⚠ Could not find: $fileName" -ForegroundColor Yellow
        continue
    }
    
    Write-Host "`n📄 Processing: $fileName" -ForegroundColor Cyan
    
    # Backup original file
    Copy-Item $filePath.FullName "$backupDir\$fileName" -Force
    
    # Read content
    $content = Get-Content $filePath.FullName -Raw
    $originalContent = $content
    
    # Replace each URL
    foreach ($finding in $group.Group) {
        if ($finding.NewURL) {
            $oldUrl = $finding.OldURL
            $newUrl = $finding.NewURL
            
            if ($content -match [regex]::Escape($oldUrl)) {
                $content = $content -replace [regex]::Escape($oldUrl), $newUrl
                Write-Host "  ✓ Replaced: $oldUrl" -ForegroundColor Green
                Write-Host "           → $newUrl" -ForegroundColor Green
                $urlsReplaced++
            }
        }
    }
    
    # Save if changed
    if ($content -ne $originalContent) {
        $content | Out-File $filePath.FullName -Encoding UTF8 -NoNewline
        $filesUpdated++
        Write-Host "  ✓ File updated" -ForegroundColor Green
    }
}

Write-Host "`n`n=== Replacement Summary ===" -ForegroundColor Cyan
Write-Host "Files updated: $filesUpdated" -ForegroundColor Green
Write-Host "URLs replaced: $urlsReplaced" -ForegroundColor Green
Write-Host "Backup location: $backupDir" -ForegroundColor Gray

Write-Host "`n=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Test your HTML files locally (open in browser)" -ForegroundColor Yellow
Write-Host "2. If everything works, deploy to S3:" -ForegroundColor Yellow
Write-Host "   cd $downloaderPath" -ForegroundColor White
Write-Host "   .\s3-push.ps1" -ForegroundColor White
Write-Host "3. If something breaks, restore from backup:" -ForegroundColor Yellow
Write-Host "   Copy-Item $backupDir\* $downloaderPath -Force" -ForegroundColor White

Write-Host "`n✓ Replacement complete!" -ForegroundColor Green
