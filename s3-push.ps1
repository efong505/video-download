# S3 Push Script
# Uploads multiple files to S3 bucket
# Usage: .\s3-push.ps1 file1.html file2.js file3.css
#        .\s3-push.ps1 -S3Path "folder/" file1.html file2.js
#        .\s3-push.ps1 -PreserveStructure C:\Projects\*.html

param(
    [Parameter(Position=0, Mandatory=$false, ValueFromRemainingArguments=$true)]
    [string[]]$Files,
    
    [Parameter(Mandatory=$false)]
    [string]$S3Path = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$PreserveStructure
)

if (-not $Files -or $Files.Count -eq 0) {
    Write-Host "Usage: .\s3-push.ps1 file1 file2 ... [-S3Path 'folder/'] [-PreserveStructure]" -ForegroundColor Yellow
    exit 1
}

$bucket = "my-video-downloads-bucket"

Write-Host "Uploading $($Files.Count) file(s) to S3..." -ForegroundColor Cyan

foreach ($file in $Files) {
    if (Test-Path $file) {
        $destination = "s3://$bucket/$S3Path"
        
        if ($PreserveStructure) {
            # Preserve directory structure
            $relativePath = (Resolve-Path $file -Relative) -replace '^\.\\', ''
            $destination = "s3://$bucket/$relativePath"
        } else {
            # Just filename
            $destination += (Split-Path $file -Leaf)
        }
        
        Write-Host "Uploading $file to $destination"
        
        # Try to find AWS CLI
        $awsCli = $null
        if (Get-Command aws -ErrorAction SilentlyContinue) {
            $awsCli = "aws"
        } elseif (Test-Path "C:\Program Files\Amazon\AWSCLIV2\aws.exe") {
            $awsCli = "C:\Program Files\Amazon\AWSCLIV2\aws.exe"
        } elseif (Test-Path "$env:LOCALAPPDATA\Programs\Python\Python*\Scripts\aws.exe") {
            $awsCli = (Get-ChildItem "$env:LOCALAPPDATA\Programs\Python\Python*\Scripts\aws.exe" | Select-Object -First 1).FullName
        }
        
        if ($awsCli) {
            & $awsCli s3 cp $file $destination
        } else {
            Write-Host "AWS CLI not found. Install from https://aws.amazon.com/cli/" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "File not found: $file" -ForegroundColor Red
    }
}
