# revert-book-page.ps1
# One-click revert: restores the-necessary-evil-book.html to the pre-marketing-plan version
# Usage: Right-click > Run with PowerShell, or: powershell -File revert-book-page.ps1

$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$backup = Join-Path $dir "the-necessary-evil-book.backup.html"
$live = Join-Path $dir "the-necessary-evil-book.html"

if (!(Test-Path $backup)) {
    Write-Host "ERROR: Backup file not found at $backup" -ForegroundColor Red
    exit 1
}

Copy-Item $backup $live -Force
Write-Host "REVERTED: the-necessary-evil-book.html restored to pre-marketing-plan version." -ForegroundColor Green
Write-Host "Backup file kept at: the-necessary-evil-book.backup.html" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Upload to S3:  aws s3 cp the-necessary-evil-book.html s3://YOUR-BUCKET/" -ForegroundColor Cyan
Write-Host "  2. Invalidate CF:  aws cloudfront create-invalidation --distribution-id YOUR-DIST --paths '/the-necessary-evil-book.html'" -ForegroundColor Cyan
