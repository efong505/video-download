# Update Production HTML Files to Use Unified API Gateway
# Only replaces API Gateway IDs, preserves all other code

$files = @(
    "create-article.html",
    "edit-article.html",
    "admin.html",
    "admin-contributors.html",
    "admin-resources.html",
    "admin-templates.html",
    "create-news.html",
    "edit-news.html",
    "news.html",
    "articles.html",
    "draft-manager.html",
    "article-preview.html"
)

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

foreach ($file in $files) {
    $path = "c:\Users\Ed\Documents\Programming\AWS\Downloader\$file"
    
    if (Test-Path $path) {
        $content = Get-Content $path -Raw
        $modified = $false
        
        foreach ($old in $replacements.Keys) {
            if ($content -match $old) {
                $content = $content -replace $old, $replacements[$old]
                $modified = $true
            }
        }
        
        if ($modified) {
            Set-Content $path $content -NoNewline
            Write-Host "✓ Updated: $file" -ForegroundColor Green
        } else {
            Write-Host "- Skipped: $file (no changes needed)" -ForegroundColor Gray
        }
    } else {
        Write-Host "✗ Not found: $file" -ForegroundColor Yellow
    }
}

Write-Host "`nDone! Review changes with git diff before committing." -ForegroundColor Cyan
