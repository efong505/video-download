# Email Dashboard Launcher
# Starts API server and opens dashboard in browser

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Email Subscriber Dashboard" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Flask is installed
$flaskInstalled = python -c "import flask" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host ""
}

# Start API server in background
Write-Host "Starting API server on http://localhost:5000..." -ForegroundColor Green
$apiProcess = Start-Process python -ArgumentList "dashboard_api.py" -PassThru -WindowStyle Minimized

# Wait for server to start
Write-Host "Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Test if server is running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/stats" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    Write-Host "API server started successfully!" -ForegroundColor Green
} catch {
    Write-Host "Warning: API server may not be ready yet" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Opening dashboard in browser..." -ForegroundColor Green
Start-Sleep -Seconds 1

# Open dashboard in default browser
Start-Process "dashboard_simple.html"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Dashboard is now running!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Dashboard: Opened in your browser" -ForegroundColor Cyan
Write-Host "API Server: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Keep script running and monitor API process
try {
    while ($apiProcess -and !$apiProcess.HasExited) {
        Start-Sleep -Seconds 1
    }
} finally {
    # Cleanup on exit
    if ($apiProcess -and !$apiProcess.HasExited) {
        Write-Host ""
        Write-Host "Stopping API server..." -ForegroundColor Yellow
        Stop-Process -Id $apiProcess.Id -Force
        Write-Host "Server stopped." -ForegroundColor Green
    }
}
