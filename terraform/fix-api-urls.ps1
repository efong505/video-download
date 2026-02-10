# Fix API URLs - Simple Find & Replace
$files = @(
    "C:\Users\Ed\Documents\Programming\AWS\Downloader\create-article.html",
    "C:\Users\Ed\Documents\Programming\AWS\Downloader\edit-article.html"
)

$replacements = @{
    "r6l0z3605f" = "diz6ceeb22"
    "fr3hh94h4a" = "diz6ceeb22"
    "q65k3dbpd7" = "diz6ceeb22"
    "k2avuckm38" = "diz6ceeb22"
}

foreach ($file in $files) {
    $content = Get-Content $file -Raw
    
    foreach ($old in $replacements.Keys) {
        $new = $replacements[$old]
        $content = $content -replace $old, $new
    }
    
    $content | Out-File $file -Encoding UTF8 -NoNewline
    Write-Host "✓ Fixed: $(Split-Path $file -Leaf)" -ForegroundColor Green
}

Write-Host "`n✓ API URLs updated successfully!" -ForegroundColor Green
