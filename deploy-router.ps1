# Deploy updated router Lambda with force_fargate support
Write-Host "Deploying router Lambda with force_fargate support..." -ForegroundColor Yellow

# Create deployment package
cd router
Compress-Archive -Path * -DestinationPath ../router-updated.zip -Force
cd ..

# Update Lambda function
aws lambda update-function-code --function-name video-download-router --zip-file fileb://router-updated.zip

Write-Host "Router Lambda updated successfully!" -ForegroundColor Green
Write-Host "The -ForceFargate flag will now work properly." -ForegroundColor Cyan