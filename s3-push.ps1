param(
    [Parameter(Mandatory=$true, ValueFromRemainingArguments=$true)]
    [string[]]$Files
)

$bucket = "my-video-downloads-bucket"

foreach ($file in $Files) {
    if (Test-Path $file) {
        Write-Host "Uploading $file to s3://$bucket/"
        aws s3 cp $file "s3://$bucket/"
    } else {
        Write-Host "File not found: $file" -ForegroundColor Red
    }
}
