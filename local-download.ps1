param(
    [Parameter(Mandatory=$true)]
    [string]$Url,
    [string]$OutputName = "video.mp4"
)

Write-Host "Downloading video locally..."

# Download with yt-dlp locally
$tempFile = "temp_$OutputName"
& yt-dlp -f "best[ext=mp4]/best" --recode-video mp4 -o $tempFile $Url

if (Test-Path $tempFile) {
    Write-Host "Upload to S3..."
    aws s3 cp $tempFile "s3://my-video-downloads-bucket/$OutputName" --content-type "video/mp4"
    
    Write-Host "Video available at: https://my-video-downloads-bucket.s3.amazonaws.com/$OutputName"
    
    Remove-Item $tempFile
} else {
    Write-Host "Download failed"
}