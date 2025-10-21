# Fix admin.html navigation link issue
Write-Host "Fixing admin.html navigation..." -ForegroundColor Yellow

# Download current admin.html
aws s3 cp s3://my-video-downloads-bucket/admin.html admin.html.temp

# Remove the problematic election link if it was added incorrectly
$content = Get-Content admin.html.temp -Raw

# Remove any malformed election map links
$content = $content -replace '<a href="admin-contributors\.html" class="nav-link">🗺️ Contributors</a>\s*\n\s*', ''

# Save the fixed version
Set-Content admin.html.temp $content -NoNewline

# Upload back to S3
aws s3 cp admin.html.temp s3://my-video-downloads-bucket/admin.html --cache-control "max-age=0"

# Clean up
Remove-Item admin.html.temp

Write-Host "✅ Admin.html fixed!" -ForegroundColor Green
Write-Host "Clear browser cache and reload" -ForegroundColor Cyan
