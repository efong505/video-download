# Fix Election System API URL
Write-Host "Fixing Election System API URLs..." -ForegroundColor Yellow

$correctApiUrl = "https://hzursivfuk.execute-api.us-east-1.amazonaws.com/prod/contributors"

Write-Host "Updating HTML files with correct API URL: $correctApiUrl" -ForegroundColor Cyan

# Update election-map.html
(Get-Content election-map.html) -replace 'https://[a-z0-9]+\.execute-api\.[a-z0-9-]+\.amazonaws\.com/prod/contributors', $correctApiUrl | Set-Content election-map.html

# Update admin-contributors.html  
(Get-Content admin-contributors.html) -replace 'https://[a-z0-9]+\.execute-api\.[a-z0-9-]+\.amazonaws\.com/prod/contributors', $correctApiUrl | Set-Content admin-contributors.html

Write-Host "Uploading updated files to S3..." -ForegroundColor Yellow
aws s3 cp election-map.html s3://my-video-downloads-bucket/ --cache-control "max-age=0"
aws s3 cp admin-contributors.html s3://my-video-downloads-bucket/ --cache-control "max-age=0"

Write-Host "✅ API URLs updated!" -ForegroundColor Green
Write-Host "Clear your browser cache and try again" -ForegroundColor Cyan
