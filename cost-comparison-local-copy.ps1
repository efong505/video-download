# Cost comparison: Both Local AND S3 copies
# Using the Trish video example

Write-Host "=== COST COMPARISON: Local + S3 Copies ===" -ForegroundColor Yellow
Write-Host ""

# Get file size from S3
$fileInfo = aws s3api head-object --bucket my-video-downloads-bucket --key "Trish.mp4" | ConvertFrom-Json
$fileSizeBytes = $fileInfo.ContentLength
$fileSizeMB = [math]::Round($fileSizeBytes / 1MB, 2)
$fileSizeGB = [math]::Round($fileSizeBytes / 1GB, 3)

Write-Host "Video File: Trish.mp4" -ForegroundColor Cyan
Write-Host "File Size: $fileSizeMB MB ($fileSizeGB GB)" -ForegroundColor White
Write-Host ""

# METHOD 1: AWS Script + Download to Local
Write-Host "=== METHOD 1: AWS Script + Download Local Copy ===" -ForegroundColor Green
$awsScriptCost = 0.002057
$s3DownloadCost = $fileSizeGB * 0.09  # $0.09 per GB for S3 download
$localElectricityDownload = 0.002     # ~2 minutes to download 35MB

Write-Host "Fargate Cost: `$$awsScriptCost" -ForegroundColor White
Write-Host "S3 Download Transfer: `$$([math]::Round($s3DownloadCost, 6))" -ForegroundColor White
Write-Host "Local Electricity (download): `$$localElectricityDownload" -ForegroundColor White

$method1Total = $awsScriptCost + $s3DownloadCost + $localElectricityDownload
Write-Host "Total Method 1: `$$([math]::Round($method1Total, 6))" -ForegroundColor Green
Write-Host ""

# METHOD 2: Local Download + Upload to S3
Write-Host "=== METHOD 2: Local Download + Upload to S3 ===" -ForegroundColor Blue
$s3PutCost = 0.0000005
$s3UploadCost = $fileSizeGB * 0.09    # $0.09 per GB for upload
$s3StorageCost = $fileSizeGB * 0.023 / 30
$localElectricityFull = 0.01          # 20 minutes full processing

Write-Host "Local Download (direct): `$0.00" -ForegroundColor White
Write-Host "S3 PUT Request: `$$s3PutCost" -ForegroundColor White
Write-Host "S3 Upload Transfer: `$$([math]::Round($s3UploadCost, 6))" -ForegroundColor White
Write-Host "S3 Storage: `$$([math]::Round($s3StorageCost, 6))" -ForegroundColor White
Write-Host "Local Electricity (full): `$$localElectricityFull" -ForegroundColor White

$method2Total = $s3PutCost + $s3UploadCost + $s3StorageCost + $localElectricityFull
Write-Host "Total Method 2: `$$([math]::Round($method2Total, 6))" -ForegroundColor Blue
Write-Host ""

# METHOD 3: Hybrid - AWS Script + Keep Local Processing
Write-Host "=== METHOD 3: AWS Script + Local Processing ===" -ForegroundColor Magenta
$hybridAws = 0.002057
$hybridLocal = 0.01                   # Still need local processing for your copy
$hybridDownload = $fileSizeGB * 0.09  # Download from original source locally

Write-Host "AWS Script (S3 copy): `$$hybridAws" -ForegroundColor White
Write-Host "Local Download (parallel): `$0.00" -ForegroundColor White
Write-Host "Local Processing: `$$hybridLocal" -ForegroundColor White

$method3Total = $hybridAws + $hybridLocal
Write-Host "Total Method 3: `$$([math]::Round($method3Total, 6))" -ForegroundColor Magenta
Write-Host ""

# Comparison
Write-Host "=== COST COMPARISON (Both Local + S3) ===" -ForegroundColor Yellow
Write-Host "Method 1 (AWS + Download): `$$([math]::Round($method1Total, 6))" -ForegroundColor Green
Write-Host "Method 2 (Local + Upload): `$$([math]::Round($method2Total, 6))" -ForegroundColor Blue
Write-Host "Method 3 (Parallel Processing): `$$([math]::Round($method3Total, 6))" -ForegroundColor Magenta

# Find cheapest
$cheapest = [math]::Min([math]::Min($method1Total, $method2Total), $method3Total)
Write-Host ""
if ($method1Total -eq $cheapest) {
    Write-Host "CHEAPEST: Method 1 (AWS + Download)" -ForegroundColor Green
} elseif ($method2Total -eq $cheapest) {
    Write-Host "CHEAPEST: Method 2 (Local + Upload)" -ForegroundColor Blue
} else {
    Write-Host "CHEAPEST: Method 3 (Parallel Processing)" -ForegroundColor Magenta
}

Write-Host ""
Write-Host "=== RECOMMENDATIONS ===" -ForegroundColor Cyan
Write-Host "💡 Method 1: Best for automation, reliable S3 copy" -ForegroundColor White
Write-Host "💡 Method 2: Best if you primarily want local copy" -ForegroundColor White
Write-Host "💡 Method 3: Best for speed, both copies simultaneously" -ForegroundColor White