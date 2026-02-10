# Verify S3 Bucket Names in All Files
# Scans for incorrect bucket names and reports them

$CORRECT_BUCKET = "my-video-downloads-bucket"
$INCORRECT_BUCKET = "techcross-videos"

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "S3 Bucket Name Verification" -ForegroundColor Yellow
Write-Host "Scanning for incorrect bucket names..." -ForegroundColor White
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

Write-Host "Correct bucket:   $CORRECT_BUCKET" -ForegroundColor Green
Write-Host "Incorrect bucket: $INCORRECT_BUCKET" -ForegroundColor Red
Write-Host ""

# File extensions to scan
$extensions = @("*.py", "*.ps1", "*.js", "*.html", "*.json", "*.md")

# Directories to exclude
$excludeDirs = @("node_modules", ".git", "env", "venv", "__pycache__", "temp_optimize")

$foundIssues = @()

# Scan files
foreach ($ext in $extensions) {
    $files = Get-ChildItem -Path . -Filter $ext -Recurse -File | Where-Object {
        $exclude = $false
        foreach ($dir in $excludeDirs) {
            if ($_.FullName -like "*\$dir\*") {
                $exclude = $true
                break
            }
        }
        -not $exclude
    }
    
    foreach ($file in $files) {
        $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
        
        if ($content -match $INCORRECT_BUCKET) {
            $foundIssues += @{
                File = $file.FullName.Replace((Get-Location).Path + "\", "")
                Type = $file.Extension
            }
        }
    }
}

# Report results
if ($foundIssues.Count -eq 0) {
    Write-Host "✓ No issues found! All files use correct bucket name." -ForegroundColor Green
} else {
    Write-Host "✗ Found $($foundIssues.Count) files with incorrect bucket name:" -ForegroundColor Red
    Write-Host ""
    
    foreach ($issue in $foundIssues) {
        Write-Host "  - $($issue.File)" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "Action Required:" -ForegroundColor Red
    Write-Host "Replace '$INCORRECT_BUCKET' with '$CORRECT_BUCKET' in the files above" -ForegroundColor White
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
