# Deploy downloader Lambda function with FFmpeg faststart optimization
Write-Host "Deploying downloader Lambda function..." -ForegroundColor Yellow

# Package Lambda function
Write-Host "1. Packaging Lambda function..." -ForegroundColor Cyan
Set-Location downloader
Compress-Archive -Path * -DestinationPath ../downloader-deployment.zip -Force
Set-Location ..

# Update Lambda function
Write-Host "2. Updating Lambda function code..." -ForegroundColor Cyan
aws lambda update-function-code --function-name video-downloader --zip-file fileb://downloader-deployment.zip

# Wait for update to complete
Write-Host "3. Waiting for update to complete..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# Verify deployment
Write-Host "4. Verifying deployment..." -ForegroundColor Cyan
aws lambda get-function --function-name video-downloader --query 'Configuration.[FunctionName,LastModified,State]' --output table

Write-Host "`n✅ Deployment complete!" -ForegroundColor Green
Write-Host "Videos will now start playing immediately with FFmpeg faststart optimization." -ForegroundColor White
Write-Host "`nTest by downloading a large video and checking playback." -ForegroundColor Yellow
