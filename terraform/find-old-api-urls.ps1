# Find files still using old API Gateway IDs
$oldApis = @{
    "xr1xcc83bj" = "news-api"
    "l10alau5g3" = "comments-api"
    "j3w8kgqlvi" = "video-downloader-api"
    "r6l0z3605f" = "auth-api"
    "k2avuckm38" = "admin-api"
    "fr3hh94h4a" = "articles-api"
    "h4hoegi26b" = "video-tag-api"
    "q65k3dbpd7" = "url-analysis-api"
    "ckbtfz4vbl" = "resources-api"
}

$searchPath = "c:\Users\Ed\Documents\Programming\AWS\Downloader"
$files = Get-ChildItem -Path $searchPath -Include *.html,*.js -Recurse -File | 
    Where-Object { $_.FullName -notmatch '\\node_modules\\|\\\.git\\|\\Downloader_backup' }

Write-Host "Scanning for old API Gateway IDs..." -ForegroundColor Cyan

$found = @{}
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if ($content) {
        foreach ($apiId in $oldApis.Keys) {
            if ($content -match $apiId) {
                if (-not $found.ContainsKey($file.Name)) {
                    $found[$file.Name] = @()
                }
                $found[$file.Name] += "$($oldApis[$apiId]) ($apiId)"
            }
        }
    }
}

if ($found.Count -eq 0) {
    Write-Host "No files found using old API Gateway IDs" -ForegroundColor Green
} else {
    Write-Host "`nFiles still using old API Gateway IDs:" -ForegroundColor Yellow
    foreach ($file in $found.Keys | Sort-Object) {
        Write-Host "`n$file" -ForegroundColor White
        foreach ($api in $found[$file]) {
            Write-Host "  - $api" -ForegroundColor Gray
        }
    }
}
