# Toggle AI Summary Script
# Enables/disables AI summarization for URL Analysis API
# Usage: .\toggle-ai.ps1 enable|disable|status

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("enable", "disable", "status")]
    [string]$Action
)

$FunctionName = "url-analysis-api"

switch ($Action) {
    "enable" {
        Write-Host "Enabling AI Summary..." -ForegroundColor Yellow
        aws lambda update-function-configuration --function-name $FunctionName --environment "Variables={USE_AI_SUMMARY=true}"
        Write-Host "AI Summary enabled successfully!" -ForegroundColor Green
    }
    "disable" {
        Write-Host "Disabling AI Summary..." -ForegroundColor Yellow
        aws lambda update-function-configuration --function-name $FunctionName --environment "Variables={USE_AI_SUMMARY=false}"
        Write-Host "AI Summary disabled successfully!" -ForegroundColor Green
    }
    "status" {
        Write-Host "Checking AI Summary status..." -ForegroundColor Yellow
        $config = aws lambda get-function-configuration --function-name $FunctionName | ConvertFrom-Json
        $status = $config.Environment.Variables.USE_AI_SUMMARY
        Write-Host "AI Summary is currently: $status" -ForegroundColor Cyan
    }
}
