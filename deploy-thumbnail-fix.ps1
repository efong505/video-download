# Deploy thumbnail generation fix for external videos
Write-Host "Deploying thumbnail generation fix..." -ForegroundColor Cyan

# Deploy thumbnail_generator Lambda
Write-Host "`nDeploying thumbnail-generator Lambda..." -ForegroundColor Yellow
Set-Location thumbnail_generator
if (Test-Path "deployment.zip") { Remove-Item "deployment.zip" }
Compress-Archive -Path index.py -DestinationPath deployment.zip
aws lambda update-function-code --function-name thumbnail-generator --zip-file fileb://deployment.zip --region us-east-1
Remove-Item deployment.zip
Set-Location ..

# Deploy admin_api Lambda
Write-Host "`nDeploying admin-api Lambda..." -ForegroundColor Yellow
Set-Location admin_api
if (Test-Path "deployment.zip") { Remove-Item "deployment.zip" }
Compress-Archive -Path index.py -DestinationPath deployment.zip
aws lambda update-function-code --function-name admin-api --zip-file fileb://deployment.zip --region us-east-1
Remove-Item deployment.zip
Set-Location ..

# Upload updated HTML files to S3
Write-Host "`nUploading updated HTML files to S3..." -ForegroundColor Yellow
aws s3 cp admin.html s3://my-video-downloads-bucket/ --content-type "text/html"
aws s3 cp user-upload.html s3://my-video-downloads-bucket/ --content-type "text/html"

Write-Host "`nDeployment complete!" -ForegroundColor Green
Write-Host "External videos will now automatically fetch thumbnails from YouTube/Rumble/Facebook" -ForegroundColor Green
