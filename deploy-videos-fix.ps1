# Deploy videos.html with token validator fix
Write-Host "Deploying videos.html with JWT token expiration check..." -ForegroundColor Cyan

aws s3 cp videos.html s3://my-video-downloads-bucket/videos.html --content-type "text/html"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ videos.html deployed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Token validator will now check JWT expiration on page load" -ForegroundColor Yellow
    Write-Host "Users with expired tokens will be automatically logged out" -ForegroundColor Yellow
} else {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
}
