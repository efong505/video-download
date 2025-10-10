#!/usr/bin/env pwsh
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Url,
    [string]$OutputName = $null
)

$API_BASE = "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod"

# Generate output name if not provided
if (-not $OutputName) {
    $urlPart = ($Url -split '/')[-1] -replace '[^a-zA-Z0-9._-]', '_'
    $OutputName = $urlPart.Substring(0, [Math]::Min(50, $urlPart.Length)) + ".mp4"
}

Write-Host "🎥 AWS Video Downloader" -ForegroundColor Cyan
Write-Host "URL: $Url" -ForegroundColor Gray
Write-Host "Output: $OutputName" -ForegroundColor Gray
Write-Host ""

# Start download
$body = @{
    url = $Url
    format = "best"
    output_name = $OutputName
} | ConvertTo-Json

try {
    Write-Host "⏳ Starting download..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "$API_BASE/download" -Method POST -ContentType "application/json" -Body $body
    
    Write-Host "✅ Download initiated!" -ForegroundColor Green
    Write-Host "📹 Video: $($response.video_info.title)" -ForegroundColor White
    Write-Host "⏱️  Duration: $($response.video_info.duration)" -ForegroundColor White
    Write-Host "🔀 Method: $($response.routing.method) ($($response.routing.reason))" -ForegroundColor White
    Write-Host "💰 Cost: $($response.cost_estimate.total_usd)" -ForegroundColor White
    
    if ($response.task_id) {
        Write-Host "🔍 Task ID: $($response.task_id)" -ForegroundColor White
        Write-Host ""
        Write-Host "⏳ Monitoring progress..." -ForegroundColor Yellow
        
        while ($true) {
            Start-Sleep 5
            try {
                $status = Invoke-RestMethod -Uri "$API_BASE/status/$($response.task_id)"
                Write-Host "📊 Status: $($status.status) | Progress: $($status.progress) | Speed: $($status.speed)" -ForegroundColor Cyan
                
                if ($status.status -eq "STOPPED") {
                    Write-Host "✅ Download completed!" -ForegroundColor Green
                    break
                } elseif ($status.status -eq "FAILED") {
                    Write-Host "❌ Download failed!" -ForegroundColor Red
                    exit 1
                }
            } catch {
                Write-Host "⚠️  Status check failed, retrying..." -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "⏳ Lambda processing (no progress tracking)..." -ForegroundColor Yellow
        Write-Host "⏱️  Estimated completion: ~$($response.routing.estimated_time)" -ForegroundColor White
        Start-Sleep 30
    }
    
    # Get video URL
    Write-Host ""
    Write-Host "🔗 Getting video URL..." -ForegroundColor Yellow
    $videoResponse = Invoke-RestMethod -Uri "$API_BASE/video/$OutputName"
    
    if ($videoResponse.signed_url) {
        Write-Host "🎬 Video ready!" -ForegroundColor Green
        Write-Host "🔗 URL: $($videoResponse.signed_url)" -ForegroundColor White
        Write-Host "⏰ Expires: 24 hours" -ForegroundColor Gray
    } else {
        Write-Host "❌ Failed to get video URL" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}