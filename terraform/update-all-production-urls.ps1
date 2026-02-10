# Update ALL HTML/JS Files to Use Unified API Gateway
# Only replaces the 14 APIs that were consolidated into diz6ceeb22

$replacements = @{
    "r6l0z3605f" = "diz6ceeb22"  # auth-api
    "fr3hh94h4a" = "diz6ceeb22"  # articles-api
    "q65k3dbpd7" = "diz6ceeb22"  # analyze-api
    "k2avuckm38" = "diz6ceeb22"  # admin-api
    "xr1xcc83bj" = "diz6ceeb22"  # news-api
    "h4hoegi26b" = "diz6ceeb22"  # tags-api
    "l10alau5g3" = "diz6ceeb22"  # comments-api
    "ckbtfz4vbl" = "diz6ceeb22"  # resources-api
}

Write-Host "Scanning all HTML and JS files..." -ForegroundColor Cyan

$files = Get-ChildItem -Path "c:\Users\Ed\Documents\Programming\AWS\Downloader" -Include *.html,*.js -Recurse | Where-Object { $_.FullName -notmatch "\\node_modules\\" -and $_.FullName -notmatch "\\\.git\\" }

$updatedCount = 0

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $modified = $false
    
    foreach ($old in $replacements.Keys) {
        if ($content -match $old) {
            $content = $content -replace $old, $replacements[$old]
            $modified = $true
        }
    }
    
    if ($modified) {
        Set-Content $file.FullName $content -NoNewline
        Write-Host "✓ Updated: $($file.Name)" -ForegroundColor Green
        $updatedCount++
    }
}

Write-Host "`nTotal files updated: $updatedCount" -ForegroundColor Cyan
Write-Host "Done! Review changes with git diff before committing." -ForegroundColor Yellow
