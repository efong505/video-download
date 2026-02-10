# Upload files to S3 with date suffix
param(
    [Parameter(Mandatory=$true)]
    [string[]]$Files,
    
    [string]$Bucket = "techcross-videos"
)

$date = Get-Date -Format "yyyyMMdd_HHmmss"

foreach ($file in $Files) {
    if (Test-Path $file) {
        $name = [System.IO.Path]::GetFileNameWithoutExtension($file)
        $ext = [System.IO.Path]::GetExtension($file)
        $datedName = "${name}_${date}${ext}"
        
        Write-Host "Uploading $file as $datedName" -ForegroundColor Cyan
        aws s3 cp $file "s3://$Bucket/$datedName"
    }
}
