param([string]$Url, [string]$OutputName = "video.mp4", [switch]$ForceFargate, [string]$Format = "auto")

if (-not $Url) {
    Write-Host "Usage: .\download.ps1 'video-url' ['output-name.mp4'] [-ForceFargate] [-Format 'format-id']"
    Write-Host "Examples:"
    Write-Host "  .\download.ps1 'video-url' 'video.mp4' -Format 'hls-2143'  # Force 720p"
    Write-Host "  .\download.ps1 'video-url' 'video.mp4' -Format 'auto'      # Auto-select best"
    exit 1
}

$API = "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod"

Write-Host "Downloading: $Url" -ForegroundColor Cyan

$body = @{ url = $Url; format = if($Format -eq "auto") { "best" } else { $Format }; output_name = $OutputName }
if ($ForceFargate) {
    $body.force_fargate = $true
}
$body = $body | ConvertTo-Json
$response = Invoke-RestMethod -Uri "$API/download" -Method POST -ContentType "application/json" -Body $body

Write-Host "Started: $($response.video_info.title)" -ForegroundColor Green
Write-Host "Method: $($response.routing.method)" -ForegroundColor White
Write-Host "Format: $($response.video_info.selected_format)" -ForegroundColor White
Write-Host "Cost: $($response.cost_estimate.total_usd)" -ForegroundColor White

if ($response.task_id) {
    Write-Host "Monitoring task: $($response.task_id)" -ForegroundColor Yellow
    do {
        Start-Sleep 5
        $status = Invoke-RestMethod -Uri "$API/status/$($response.task_id)" -ErrorAction SilentlyContinue
        if ($status) {
            Write-Host "Status: $($status.status) | $($status.progress)" -ForegroundColor Cyan
        }
    } while ($status.status -eq "RUNNING" -or $status.status -eq "PENDING")
}

Start-Sleep 10
$video = Invoke-RestMethod -Uri "$API/video/$OutputName" -ErrorAction SilentlyContinue
if ($video.signed_url) {
    Write-Host "Ready: $($video.signed_url)" -ForegroundColor Green
} else {
    Write-Host "Still processing..." -ForegroundColor Yellow
}