param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("enable", "disable", "status")]
    [string]$Action
)

$DISTRIBUTION_ID = "E3N00R2D2NE9C5"
$LAMBDA_ARN = "arn:aws:lambda:us-east-1:371751795928:function:article-meta-tags-edge:5"

function Get-Status {
    Write-Host "`nChecking Lambda@Edge status..." -ForegroundColor Cyan
    $config = aws cloudfront get-distribution-config --id $DISTRIBUTION_ID --output json | ConvertFrom-Json
    $associations = $config.DistributionConfig.DefaultCacheBehavior.LambdaFunctionAssociations
    
    if ($associations.Quantity -gt 0) {
        Write-Host "Lambda@Edge is ENABLED" -ForegroundColor Green
        Write-Host "  Function: $($associations.Items[0].LambdaFunctionARN)" -ForegroundColor Gray
        Write-Host "  Event: $($associations.Items[0].EventType)" -ForegroundColor Gray
    } else {
        Write-Host "Lambda@Edge is DISABLED" -ForegroundColor Yellow
    }
    
    Write-Host "`nDistribution Status: $($config.ETag)" -ForegroundColor Gray
}

function Disable-LambdaEdge {
    Write-Host "`nDisabling Lambda@Edge..." -ForegroundColor Yellow
    
    # Get current config
    $configJson = aws cloudfront get-distribution-config --id $DISTRIBUTION_ID --output json
    $config = $configJson | ConvertFrom-Json
    $etag = $config.ETag
    
    # Remove Lambda association
    $config.DistributionConfig.DefaultCacheBehavior.LambdaFunctionAssociations = @{
        Quantity = 0
    }
    
    # Save config
    $config.DistributionConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath "cloudfront-config-disabled.json" -Encoding ascii
    
    # Update distribution
    aws cloudfront update-distribution --id $DISTRIBUTION_ID --if-match $etag --distribution-config file://cloudfront-config-disabled.json --output json | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Lambda@Edge disabled successfully" -ForegroundColor Green
        Write-Host "  Propagation time: 15-30 minutes" -ForegroundColor Gray
        Write-Host "  All article shares will now show default meta tags" -ForegroundColor Gray
    } else {
        Write-Host "Failed to disable Lambda@Edge" -ForegroundColor Red
    }
}

function Enable-LambdaEdge {
    Write-Host "`nEnabling Lambda@Edge..." -ForegroundColor Cyan
    
    # Get current config
    $configJson = aws cloudfront get-distribution-config --id $DISTRIBUTION_ID --output json
    $config = $configJson | ConvertFrom-Json
    $etag = $config.ETag
    
    # Add Lambda association
    $config.DistributionConfig.DefaultCacheBehavior.LambdaFunctionAssociations = @{
        Quantity = 1
        Items = @(
            @{
                LambdaFunctionARN = $LAMBDA_ARN
                EventType = "viewer-request"
                IncludeBody = $false
            }
        )
    }
    
    # Save config
    $config.DistributionConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath "cloudfront-config-enabled.json" -Encoding ascii
    
    # Update distribution
    aws cloudfront update-distribution --id $DISTRIBUTION_ID --if-match $etag --distribution-config file://cloudfront-config-enabled.json --output json | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Lambda@Edge enabled successfully" -ForegroundColor Green
        Write-Host "  Propagation time: 15-30 minutes" -ForegroundColor Gray
        Write-Host "  Article shares will show article-specific meta tags" -ForegroundColor Gray
    } else {
        Write-Host "Failed to enable Lambda@Edge" -ForegroundColor Red
    }
}

# Main execution
switch ($Action) {
    "status" { Get-Status }
    "disable" { Disable-LambdaEdge }
    "enable" { Enable-LambdaEdge }
}

Write-Host ""
