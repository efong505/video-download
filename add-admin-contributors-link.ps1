# Properly add Contributors link to admin.html
Write-Host "Adding Contributors link to admin.html..." -ForegroundColor Yellow

# Download current admin.html
aws s3 cp s3://my-video-downloads-bucket/admin.html admin.html.temp

$content = Get-Content admin.html.temp -Raw

# Check if link already exists
if ($content -match 'admin-contributors.html') {
    Write-Host "Link already exists, skipping..." -ForegroundColor Gray
} else {
    # Add the link before the Profile link
    $contributorsLink = '<a href="admin-contributors.html" class="nav-link">🗺️ Contributors</a>'
    $content = $content -replace '(<a href="profile\.html" class="nav-link">)', "$contributorsLink`n                    `$1"
    
    Set-Content admin.html.temp $content -NoNewline
    
    # Upload back to S3
    aws s3 cp admin.html.temp s3://my-video-downloads-bucket/admin.html --cache-control "max-age=0"
    
    Write-Host "✅ Contributors link added!" -ForegroundColor Green
}

# Clean up
Remove-Item admin.html.temp

Write-Host "Clear browser cache and reload" -ForegroundColor Cyan
