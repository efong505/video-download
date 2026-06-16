# Deploy Frontend to S3
Write-Host "Deploying Frontend to S3..." -ForegroundColor Green

# Prompt for bucket name
$BUCKET_NAME = Read-Host "Enter your S3 bucket name for frontend hosting"

# Create bucket if it doesn't exist
Write-Host "`nCreating/Verifying S3 bucket..." -ForegroundColor Cyan
aws s3 mb s3://$BUCKET_NAME 2>$null

# Configure bucket for static website hosting
Write-Host "Configuring static website hosting..." -ForegroundColor Yellow
aws s3 website s3://$BUCKET_NAME --index-document index.html --error-document index.html

# Set bucket policy for public read access
Write-Host "Setting bucket policy..." -ForegroundColor Yellow
$bucketPolicy = @"
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::$BUCKET_NAME/*"
        }
    ]
}
"@
$bucketPolicy | Out-File -FilePath "bucket-policy.json" -Encoding utf8
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file://bucket-policy.json
Remove-Item "bucket-policy.json"

# Sync frontend files
Write-Host "`nUploading frontend files..." -ForegroundColor Cyan
Set-Location "..\frontend"
aws s3 sync . s3://$BUCKET_NAME --exclude "*.md" --exclude ".git/*"

Set-Location "..\scripts"

$WEBSITE_URL = "http://$BUCKET_NAME.s3-website-us-east-1.amazonaws.com"

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Frontend Deployed Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Website URL: $WEBSITE_URL" -ForegroundColor Cyan
Write-Host "`nYou can now access your application at the URL above." -ForegroundColor Yellow
