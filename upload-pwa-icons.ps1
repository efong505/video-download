# Upload PWA Icons to S3
Write-Host "Uploading PWA icons to S3..." -ForegroundColor Yellow

# Upload all icon files
Write-Host "Uploading icon files..." -ForegroundColor Cyan
aws s3 cp icons/ s3://my-video-downloads-bucket/icons/ --recursive --content-type "image/png" --cache-control "max-age=31536000"

# Upload manifest.json
Write-Host "Uploading manifest.json..." -ForegroundColor Cyan
aws s3 cp manifest.json s3://my-video-downloads-bucket/manifest.json --content-type "application/json" --cache-control "max-age=86400"

# Upload service worker
Write-Host "Uploading service-worker.js..." -ForegroundColor Cyan
aws s3 cp service-worker.js s3://my-video-downloads-bucket/service-worker.js --content-type "application/javascript" --cache-control "max-age=0, must-revalidate"

# Upload PWA install script
Write-Host "Uploading pwa-install.js..." -ForegroundColor Cyan
aws s3 cp pwa-install.js s3://my-video-downloads-bucket/pwa-install.js --content-type "application/javascript" --cache-control "max-age=86400"

Write-Host "✅ PWA files uploaded successfully!" -ForegroundColor Green
Write-Host "Note: You may need to clear your browser cache and reinstall the PWA app" -ForegroundColor Yellow
