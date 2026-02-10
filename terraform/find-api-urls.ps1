# Find and Report API Gateway URLs in HTML/JS Files
# Scans for execute-api URLs and generates replacement plan

$downloaderPath = "C:\Users\Ed\Documents\Programming\AWS\Downloader"
$newBaseUrl = "https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod"

# Endpoint mapping
$endpointMap = @{
    "admin-api" = "/admin"
    "auth-api" = "/auth"
    "articles-api" = "/articles"
    "news-api" = "/news"
    "comments-api" = "/comments"
    "contributors-api" = "/contributors"
    "resources-api" = "/resources"
    "video-list-api" = "/videos"
    "video-tag-api" = "/tags"
    "video-downloader-api" = "/download"
    "video-download-router" = "/download"
    "url-analysis-api" = "/analyze"
    "paypal-billing-api" = "/paypal"
    "prayer_api" = "/prayer"
    "notifications_api" = "/notifications"
}

Write-Host "`n=== Scanning for API Gateway URLs ===" -ForegroundColor Cyan
Write-Host "Directory: $downloaderPath`n" -ForegroundColor Yellow

# Find all HTML and JS files
$files = Get-ChildItem -Path $downloaderPath -Include *.html,*.js -Recurse -ErrorAction SilentlyContinue | 
    Where-Object { $_.FullName -notmatch "node_modules|\.git|backup" }

$findings = @()
$fileCount = 0

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    
    if ($content -match "execute-api\.us-east-1\.amazonaws\.com") {
        $fileCount++
        
        # Find all execute-api URLs
        $matches = [regex]::Matches($content, "https://[a-z0-9]+\.execute-api\.us-east-1\.amazonaws\.com/[a-z0-9/\-]*")
        
        foreach ($match in $matches) {
            $oldUrl = $match.Value
            
            # Try to determine which endpoint this is
            $suggestedNew = $null
            foreach ($key in $endpointMap.Keys) {
                if ($oldUrl -match $key) {
                    $suggestedNew = "$newBaseUrl$($endpointMap[$key])"
                    break
                }
            }
            
            $findings += [PSCustomObject]@{
                File = $file.Name
                OldURL = $oldUrl
                NewURL = $suggestedNew
                LinePreview = ($content -split "`n" | Where-Object { $_ -match [regex]::Escape($oldUrl) } | Select-Object -First 1).Trim()
            }
        }
    }
}

if ($findings.Count -eq 0) {
    Write-Host "✓ No old API Gateway URLs found!" -ForegroundColor Green
    Write-Host "  Your frontend may already be using the new unified API, or using direct Lambda invocation." -ForegroundColor Gray
    exit 0
}

Write-Host "Found $($findings.Count) API URLs in $fileCount files`n" -ForegroundColor Yellow

# Group by file
$byFile = $findings | Group-Object File

foreach ($group in $byFile) {
    Write-Host "`n📄 $($group.Name)" -ForegroundColor Cyan
    Write-Host ("=" * 80) -ForegroundColor Gray
    
    foreach ($finding in $group.Group) {
        Write-Host "`n  OLD: " -NoNewline -ForegroundColor Red
        Write-Host $finding.OldURL
        
        if ($finding.NewURL) {
            Write-Host "  NEW: " -NoNewline -ForegroundColor Green
            Write-Host $finding.NewURL
        } else {
            Write-Host "  NEW: " -NoNewline -ForegroundColor Yellow
            Write-Host "⚠ Manual review needed"
        }
        
        if ($finding.LinePreview) {
            Write-Host "  Context: " -NoNewline -ForegroundColor Gray
            Write-Host $finding.LinePreview.Substring(0, [Math]::Min(100, $finding.LinePreview.Length))
        }
    }
}

# Generate replacement script
Write-Host "`n`n=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Review the URLs above" -ForegroundColor Yellow
Write-Host "2. Run the auto-replacement script (will create backup):" -ForegroundColor Yellow
Write-Host "   .\replace-api-urls.ps1" -ForegroundColor White
Write-Host "3. Test your frontend thoroughly" -ForegroundColor Yellow
Write-Host "4. Deploy updated files to S3" -ForegroundColor Yellow

# Export to JSON for replacement script
$findings | ConvertTo-Json -Depth 10 | Out-File "$PSScriptRoot\api-url-findings.json" -Encoding UTF8
Write-Host "`n✓ Findings saved to api-url-findings.json" -ForegroundColor Green
