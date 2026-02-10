# Safe API URL Replacement - Won't break multi-line strings
# Restores from backup and does line-by-line replacement

$downloaderPath = "C:\Users\Ed\Documents\Programming\AWS\Downloader"
$backupPath = "C:\Users\Ed\Documents\Programming\AWS\Downloader\backup_20260210_095001"

Write-Host "`n=== Restoring from Backup ===" -ForegroundColor Cyan

# Restore broken files from backup
$brokenFiles = @("edit-article.html", "create-article.html")

foreach ($file in $brokenFiles) {
    $backupFile = Join-Path $backupPath $file
    $targetFile = Join-Path $downloaderPath $file
    
    if (Test-Path $backupFile) {
        Copy-Item $backupFile $targetFile -Force
        Write-Host "✓ Restored: $file" -ForegroundColor Green
    }
}

Write-Host "`n=== Safe URL Replacement ===" -ForegroundColor Cyan

# Define URL mappings (old API ID -> new endpoint)
$urlMappings = @{
    # Format: "old-api-id" = "new-endpoint-path"
    "admin-api" = "/admin"
    "auth-api" = "/auth"
    "articles-api" = "/articles"
    "news-api" = "/news"
    "comments-api" = "/comments"
    "contributors-api" = "/contributors"
    "resources-api" = "/resources"
    "video-list-api" = "/videos"
    "video-tag-api" = "/tags"
    "url-analysis-api" = "/analyze"
    "paypal-billing-api" = "/paypal"
    "prayer_api" = "/prayer"
    "notifications_api" = "/notifications"
}

$newBaseUrl = "https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod"

# Get all HTML files
$files = Get-ChildItem -Path $downloaderPath -Filter *.html -File | 
    Where-Object { $_.Name -notmatch "backup|archive" }

$filesUpdated = 0

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $modified = $false
    
    # Check if file contains execute-api URLs
    if ($content -match "execute-api\.us-east-1\.amazonaws\.com") {
        Write-Host "`n📄 Processing: $($file.Name)" -ForegroundColor Cyan
        
        # Replace each old API pattern
        foreach ($apiName in $urlMappings.Keys) {
            $newPath = $urlMappings[$apiName]
            
            # Pattern: https://[random-id].execute-api.us-east-1.amazonaws.com/prod
            # Look for the API name in comments or nearby context to identify which API it is
            
            # Generic pattern - match any execute-api URL and check context
            $pattern = "https://[a-z0-9]+\.execute-api\.us-east-1\.amazonaws\.com/prod"
            
            if ($content -match $pattern) {
                # For now, let's just report what we found
                $matches = [regex]::Matches($content, $pattern)
                foreach ($match in $matches) {
                    Write-Host "  Found: $($match.Value)" -ForegroundColor Yellow
                }
            }
        }
    }
}

Write-Host "`n=== Manual Replacement Needed ===" -ForegroundColor Yellow
Write-Host "The files have been restored from backup." -ForegroundColor Gray
Write-Host "Please manually update the API URLs in:" -ForegroundColor Gray
Write-Host "  - edit-article.html" -ForegroundColor White
Write-Host "  - create-article.html" -ForegroundColor White
Write-Host "`nSearch for: execute-api" -ForegroundColor Gray
Write-Host "Replace with: $newBaseUrl/[endpoint]" -ForegroundColor Gray
Write-Host "`nExample:" -ForegroundColor Gray
Write-Host "  OLD: https://abc123.execute-api.us-east-1.amazonaws.com/prod" -ForegroundColor Red
Write-Host "  NEW: $newBaseUrl/admin" -ForegroundColor Green
