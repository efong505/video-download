# Deploy Video Playlists System

Write-Host "Deploying Video Playlists System..." -ForegroundColor Green

# 1. Create DynamoDB table
Write-Host "`n1. Creating video-playlists DynamoDB table..." -ForegroundColor Yellow
python create_playlists_table.py

# 2. Create Lambda function
Write-Host "`n2. Creating playlists-api Lambda function..." -ForegroundColor Yellow
cd playlists_api
Compress-Archive -Path index.py -DestinationPath ../playlists_api.zip -Force
cd ..

aws lambda create-function `
    --function-name playlists-api `
    --runtime python3.12 `
    --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-dynamodb-role `
    --handler index.lambda_handler `
    --zip-file fileb://playlists_api.zip `
    --timeout 30 `
    --region us-east-1

Remove-Item playlists_api.zip

# 3. Upload playlists.html to S3
Write-Host "`n3. Uploading playlists.html to S3..." -ForegroundColor Yellow
aws s3 cp playlists.html s3://my-video-downloads-bucket/ --region us-east-1

Write-Host "`nVideo Playlists System deployed!" -ForegroundColor Green
Write-Host "Next: Create API Gateway endpoint and update PLAYLISTS_API URL in playlists.html" -ForegroundColor Cyan
