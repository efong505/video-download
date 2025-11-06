# verify-cleanup.ps1 - Verify site works after cleanup
# Created: November 6, 2025

Write-Host "=== Verifying Site After Cleanup ===" -ForegroundColor Cyan
Write-Host ""

# Test main pages
$pages = @(
    @{Url="https://christianconservativestoday.com"; Name="Homepage"},
    @{Url="https://christianconservativestoday.com/videos.html"; Name="Videos"},
    @{Url="https://christianconservativestoday.com/articles.html"; Name="Articles"},
    @{Url="https://christianconservativestoday.com/news.html"; Name="News"},
    @{Url="https://christianconservativestoday.com/election-map.html"; Name="Election Map"},
    @{Url="https://christianconservativestoday.com/resources.html"; Name="Resources"}
)

$allPassed = $true

foreach ($page in $pages) {
    try {
        $response = Invoke-WebRequest -Uri $page.Url -Method Head -TimeoutSec 10 -ErrorAction Stop
        Write-Host "✅ $($page.Name) - OK (Status: $($response.StatusCode))" -ForegroundColor Green
    } catch {
        Write-Host "❌ $($page.Name) - FAILED ($($_.Exception.Message))" -ForegroundColor Red
        $allPassed = $false
    }
}

Write-Host ""

if ($allPassed) {
    Write-Host "🎉 All pages verified successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Cleanup was successful. Site is working normally." -ForegroundColor White
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Keep archive folder for 30 days as backup" -ForegroundColor Gray
    Write-Host "2. Proceed to Phase 1 (Create New Structure)" -ForegroundColor Gray
} else {
    Write-Host "⚠️  Some pages failed verification" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Recommended actions:" -ForegroundColor Cyan
    Write-Host "1. Check if pages exist in S3 bucket" -ForegroundColor Gray
    Write-Host "2. Run: .\rollback-cleanup.ps1 if needed" -ForegroundColor Gray
    Write-Host "3. Review CloudFront cache settings" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== Verification Complete ===" -ForegroundColor Cyan
