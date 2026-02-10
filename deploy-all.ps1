# Deploy both Lambda downloader and Fargate container with format selection
Write-Host "Deploying Lambda downloader and Fargate container..." -ForegroundColor Yellow

# 1. Deploy Lambda downloader
Write-Host "1. Packaging Lambda downloader..." -ForegroundColor Cyan
cd downloader
Compress-Archive -Path * -DestinationPath ../downloader-updated.zip -Force
cd ..

Write-Host "2. Updating Lambda function..." -ForegroundColor Cyan
aws lambda update-function-code --function-name video-downloader --zip-file fileb://downloader-updated.zip

# 3. Deploy Fargate container
Write-Host "3. Building Fargate container..." -ForegroundColor Cyan
docker build -t video-downloader .

Write-Host "4. Tagging for ECR..." -ForegroundColor Cyan
docker tag video-downloader:latest 371751795928.dkr.ecr.us-east-1.amazonaws.com/video-downloader:latest

Write-Host "5. Logging into ECR..." -ForegroundColor Cyan
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 371751795928.dkr.ecr.us-east-1.amazonaws.com

Write-Host "6. Pushing to ECR..." -ForegroundColor Cyan
docker push 371751795928.dkr.ecr.us-east-1.amazonaws.com/video-downloader:latest

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "Both Lambda and Fargate now support intelligent format selection." -ForegroundColor White