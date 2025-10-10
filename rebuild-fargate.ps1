# Rebuild and deploy Fargate container with fixed Python code
Write-Host "Rebuilding Fargate container with fixed syntax..." -ForegroundColor Yellow

# Build new Docker image
docker build -t video-downloader .

# Tag for ECR
docker tag video-downloader:latest 371751795928.dkr.ecr.us-east-1.amazonaws.com/video-downloader:latest

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 371751795928.dkr.ecr.us-east-1.amazonaws.com

# Push to ECR
docker push 371751795928.dkr.ecr.us-east-1.amazonaws.com/video-downloader:latest

Write-Host "Fargate container rebuilt and deployed!" -ForegroundColor Green
Write-Host "The -ForceFargate flag should now work without syntax errors." -ForegroundColor Cyan