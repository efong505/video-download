# Cost comparison: AWS Script vs Local Download + Upload
# Using the Trish video example that took ~20 minutes on Fargate

Write-Host "=== COST COMPARISON: Trish Video Download ===" -ForegroundColor Yellow
Write-Host ""

# Get file size from S3
$fileInfo = aws s3api head-object --bucket my-video-downloads-bucket --key "Trish.mp4" | ConvertFrom-Json
$fileSizeBytes = $fileInfo.ContentLength
$fileSizeMB = [math]::Round($fileSizeBytes / 1MB, 2)
$fileSizeGB = [math]::Round($fileSizeBytes / 1GB, 3)

Write-Host "Video File: Trish.mp4" -ForegroundColor Cyan
Write-Host "File Size: $fileSizeMB MB ($fileSizeGB GB)" -ForegroundColor White
Write-Host ""

# AWS Script Method (Fargate) - Actual cost from output: $0.002057
$awsScriptCost = 0.002057
Write-Host "=== METHOD 1: AWS Script (Fargate) ===" -ForegroundColor Green
Write-Host "Fargate Cost: `$0.002057" -ForegroundColor White
Write-Host "Router Lambda: `$0.000001" -ForegroundColor White
Write-Host "S3 Storage: `$0.000001" -ForegroundColor White
Write-Host "Total AWS Script: `$0.002059" -ForegroundColor Green
Write-Host ""

# Local Download + Upload Method
Write-Host "=== METHOD 2: Local Download + S3 Upload ===" -ForegroundColor Blue

# S3 Upload costs
$s3PutCost = 0.0000005  # $0.0005 per 1000 PUT requests
$s3TransferCost = $fileSizeGB * 0.09  # $0.09 per GB for upload
$s3StorageCost = $fileSizeGB * 0.023 / 30  # $0.023 per GB per month (daily rate)

Write-Host "S3 PUT Request: `$$s3PutCost" -ForegroundColor White
Write-Host "S3 Upload Transfer: `$$([math]::Round($s3TransferCost, 6))" -ForegroundColor White
Write-Host "S3 Storage (1 day): `$$([math]::Round($s3StorageCost, 6))" -ForegroundColor White

# Local costs (electricity, internet, time)
$localElectricity = 0.01  # ~1 cent for 20 min of computer usage
$localInternet = 0.00     # Usually unlimited/flat rate
$localTime = 0.00         # Your time (priceless but free)

Write-Host "Local Electricity: `$$localElectricity" -ForegroundColor White
Write-Host "Local Internet: `$$localInternet" -ForegroundColor White
Write-Host "Your Time: `$$localTime (manual work)" -ForegroundColor White

$localTotalCost = $s3PutCost + $s3TransferCost + $s3StorageCost + $localElectricity + $localInternet + $localTime

Write-Host "Total Local Method: `$$([math]::Round($localTotalCost, 6))" -ForegroundColor Blue
Write-Host ""

# Comparison
Write-Host "=== COST COMPARISON ===" -ForegroundColor Yellow
Write-Host "AWS Script (Fargate): `$$awsScriptCost" -ForegroundColor Green
Write-Host "Local + Upload: `$$([math]::Round($localTotalCost, 6))" -ForegroundColor Blue

$savings = $localTotalCost - $awsScriptCost
if ($savings -gt 0) {
    Write-Host "AWS Script SAVES: `$$([math]::Round($savings, 6))" -ForegroundColor Green
} else {
    Write-Host "Local Method SAVES: `$$([math]::Round([math]::Abs($savings), 6))" -ForegroundColor Blue
}

Write-Host ""
Write-Host "=== ADDITIONAL BENEFITS OF AWS SCRIPT ===" -ForegroundColor Cyan
Write-Host "✅ Automated - no manual work" -ForegroundColor White
Write-Host "✅ No local storage used" -ForegroundColor White
Write-Host "✅ No local bandwidth used" -ForegroundColor White
Write-Host "✅ Runs while you do other things" -ForegroundColor White
Write-Host "✅ Browser-optimized output (H.264/AAC)" -ForegroundColor White
Write-Host "✅ Progress monitoring" -ForegroundColor White
Write-Host "✅ No software installation needed" -ForegroundColor White