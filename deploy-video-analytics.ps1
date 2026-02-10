# Deploy Video Analytics System

Write-Host "Deploying Video Analytics System..." -ForegroundColor Green

# 1. Create DynamoDB table
Write-Host "`n1. Creating video-analytics DynamoDB table..." -ForegroundColor Yellow
python create_video_analytics_table.py

# 2. Deploy TAG API with analytics functions
Write-Host "`n2. Deploying TAG API..." -ForegroundColor Yellow
cd tag_api
Compress-Archive -Path index.py -DestinationPath ../tag_api.zip -Force
cd ..
aws lambda update-function-code --function-name tag-api --zip-file fileb://tag_api.zip --region us-east-1
Remove-Item tag_api.zip

# 3. Upload video-analytics.html to S3
Write-Host "`n3. Uploading video-analytics.html to S3..." -ForegroundColor Yellow
aws s3 cp video-analytics.html s3://my-video-downloads-bucket/ --region us-east-1

# 4. Upload updated videos.html to S3
Write-Host "`n4. Uploading updated videos.html to S3..." -ForegroundColor Yellow
aws s3 cp videos.html s3://my-video-downloads-bucket/ --region us-east-1

# 5. Invalidate CloudFront cache
Write-Host "`n5. Invalidating CloudFront cache..." -ForegroundColor Yellow
aws cloudfront create-invalidation --distribution-id E3N00R2D2NE9C5 --paths "/video-analytics.html" "/videos.html" --region us-east-1

Write-Host "`nVideo Analytics System deployed successfully!" -ForegroundColor Green
Write-Host "Access at: https://christianconservativestoday.com/video-analytics.html" -ForegroundColor Cyan
