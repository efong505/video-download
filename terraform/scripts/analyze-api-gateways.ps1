# Analyze API Gateway Structure
# This script discovers all APIs and their Lambda integrations

$ErrorActionPreference = "Stop"

Write-Host "`n=== API Gateway Analysis ===" -ForegroundColor Cyan
Write-Host "Discovering all API Gateways and their configurations`n" -ForegroundColor Cyan

# Step 1: Get all REST APIs
Write-Host "[1/4] Fetching REST APIs..." -ForegroundColor Yellow
$restApis = aws apigateway get-rest-apis --query 'items' --output json | ConvertFrom-Json

Write-Host "  Found $($restApis.Count) REST APIs" -ForegroundColor Green

# Step 2: Get all HTTP APIs
Write-Host "`n[2/4] Fetching HTTP APIs..." -ForegroundColor Yellow
$httpApis = aws apigatewayv2 get-apis --query 'Items' --output json | ConvertFrom-Json

Write-Host "  Found $($httpApis.Count) HTTP APIs" -ForegroundColor Green

# Step 3: Analyze REST APIs
Write-Host "`n[3/4] Analyzing REST API integrations..." -ForegroundColor Yellow
$restApiDetails = @()

foreach ($api in $restApis) {
    Write-Host "  Analyzing: $($api.name)" -ForegroundColor Gray
    
    # Get resources (endpoints)
    $resources = aws apigateway get-resources --rest-api-id $api.id --query 'items' --output json | ConvertFrom-Json
    
    $integrations = @()
    foreach ($resource in $resources) {
        # Check each HTTP method
        if ($resource.resourceMethods) {
            foreach ($method in $resource.resourceMethods.PSObject.Properties.Name) {
                $integration = aws apigateway get-integration --rest-api-id $api.id --resource-id $resource.id --http-method $method --query 'uri' --output text 2>$null
                
                if ($integration -match 'lambda') {
                    # Extract Lambda function name from ARN
                    if ($integration -match 'function:([^/]+)') {
                        $lambdaName = $matches[1]
                        $integrations += @{
                            Path = $resource.path
                            Method = $method
                            Lambda = $lambdaName
                        }
                    }
                }
            }
        }
    }
    
    $restApiDetails += @{
        Name = $api.name
        ID = $api.id
        Type = "REST"
        CreatedDate = $api.createdDate
        Integrations = $integrations
    }
}

# Step 4: Analyze HTTP APIs
Write-Host "`n[4/4] Analyzing HTTP API integrations..." -ForegroundColor Yellow
$httpApiDetails = @()

foreach ($api in $httpApis) {
    Write-Host "  Analyzing: $($api.Name)" -ForegroundColor Gray
    
    # Get integrations
    $integrations = aws apigatewayv2 get-integrations --api-id $api.ApiId --query 'Items' --output json | ConvertFrom-Json
    
    $integrationsDetails = @()
    foreach ($integration in $integrations) {
        if ($integration.IntegrationUri -match 'lambda') {
            # Extract Lambda function name
            if ($integration.IntegrationUri -match 'function:([^/]+)') {
                $lambdaName = $matches[1]
                $integrationsDetails += @{
                    IntegrationType = $integration.IntegrationType
                    Lambda = $lambdaName
                }
            }
        }
    }
    
    $httpApiDetails += @{
        Name = $api.Name
        ID = $api.ApiId
        Type = $api.ProtocolType
        CreatedDate = $api.CreatedDate
        Integrations = $integrationsDetails
    }
}

# Generate Report
Write-Host "`n=== Analysis Report ===" -ForegroundColor Cyan

Write-Host "`nTotal APIs: $($restApis.Count + $httpApis.Count)" -ForegroundColor White
Write-Host "  REST APIs: $($restApis.Count)" -ForegroundColor White
Write-Host "  HTTP APIs: $($httpApis.Count)" -ForegroundColor White

Write-Host "`n--- REST APIs ---" -ForegroundColor Yellow
foreach ($api in $restApiDetails) {
    Write-Host "`n$($api.Name) (ID: $($api.ID))" -ForegroundColor Cyan
    Write-Host "  Created: $($api.CreatedDate)" -ForegroundColor Gray
    Write-Host "  Integrations: $($api.Integrations.Count)" -ForegroundColor Gray
    
    foreach ($integration in $api.Integrations) {
        Write-Host "    $($integration.Method) $($integration.Path) → $($integration.Lambda)" -ForegroundColor DarkGray
    }
}

Write-Host "`n--- HTTP APIs ---" -ForegroundColor Yellow
foreach ($api in $httpApiDetails) {
    Write-Host "`n$($api.Name) (ID: $($api.ID))" -ForegroundColor Cyan
    Write-Host "  Protocol: $($api.Type)" -ForegroundColor Gray
    Write-Host "  Created: $($api.CreatedDate)" -ForegroundColor Gray
    Write-Host "  Integrations: $($api.Integrations.Count)" -ForegroundColor Gray
    
    foreach ($integration in $api.Integrations) {
        Write-Host "    $($integration.IntegrationType) → $($integration.Lambda)" -ForegroundColor DarkGray
    }
}

# Export to JSON for later use
$report = @{
    TotalAPIs = $restApis.Count + $httpApis.Count
    RESTAPIs = $restApiDetails
    HTTPAPIs = $httpApiDetails
    AnalysisDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
}

$reportPath = "api-gateway-analysis.json"
$report | ConvertTo-Json -Depth 10 | Out-File $reportPath

Write-Host "`n=== Cost Analysis ===" -ForegroundColor Cyan
$restCost = $restApis.Count * 3.50
$httpCost = $httpApis.Count * 1.00
$totalCost = $restCost + $httpCost

Write-Host "Current Monthly Cost:" -ForegroundColor White
Write-Host "  REST APIs: $($restApis.Count) × `$3.50 = `$$restCost" -ForegroundColor Gray
Write-Host "  HTTP APIs: $($httpApis.Count) × `$1.00 = `$$httpCost" -ForegroundColor Gray
Write-Host "  Total: `$$totalCost/month" -ForegroundColor Yellow

Write-Host "`nAfter Consolidation (1 REST API):" -ForegroundColor White
Write-Host "  Cost: `$3.50/month" -ForegroundColor Green
Write-Host "  Savings: `$$($totalCost - 3.50)/month (`$$([math]::Round(($totalCost - 3.50) * 12, 2))/year)" -ForegroundColor Green

Write-Host "`n=== Report Saved ===" -ForegroundColor Cyan
Write-Host "Full analysis saved to: $reportPath" -ForegroundColor White
Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "1. Review the analysis above" -ForegroundColor White
Write-Host "2. Identify which APIs can be consolidated" -ForegroundColor White
Write-Host "3. Design unified API structure" -ForegroundColor White
