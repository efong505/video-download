# Add token-validator.js to all protected pages
$pages = @(
    "articles.html",
    "news.html",
    "resources.html",
    "create-article.html",
    "edit-article.html",
    "create-news.html",
    "edit-news.html",
    "admin.html",
    "admin-contributors.html",
    "admin-resources.html",
    "admin-templates.html",
    "profile.html",
    "user-page.html"
)

$scriptTag = '    <script src="assets/js/token-validator.js"></script>'

foreach ($page in $pages) {
    if (Test-Path $page) {
        $content = Get-Content $page -Raw
        
        # Check if already has token-validator
        if ($content -notmatch "token-validator\.js") {
            # Add after last stylesheet link in head
            $content = $content -replace '(</head>)', "$scriptTag`r`n`$1"
            Set-Content $page $content -NoNewline
            Write-Host "✅ Added token-validator to $page" -ForegroundColor Green
        } else {
            Write-Host "⏭️  $page already has token-validator" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ $page not found" -ForegroundColor Red
    }
}

Write-Host "`nDone! Deploy with: aws s3 sync . s3://my-video-downloads-bucket/ --exclude '*' --include '*.html'" -ForegroundColor Cyan
