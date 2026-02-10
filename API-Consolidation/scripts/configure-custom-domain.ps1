# configure-custom-domain.ps1
# Configures custom domain for unified API Gateway

param(
    [Parameter(Mandatory=$false)]
    [string]$ApiId,
    
    [Parameter(Mandatory=$true)]
    [string]$CertificateArn,
    
    [string]$DomainName = "api.christianconservativestoday.com",
    [string]$Region = "us-east-1"
)

# Load API ID from file if not provided
if (-not $ApiId) {
    if (Test-Path "api-id.txt") {
        $ApiId = Get-Content "api-id.txt"
        Write-Host "📝 Loaded API ID from file: $ApiId" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Error: API ID not provided and api-id.txt not found" -ForegroundColor Red
        Write-Host "Usage: .\configure-custom-domain.ps1 -ApiId YOUR_API_ID -CertificateArn YOUR_CERT_ARN" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "`n🚀 Configuring Custom Domain..." -ForegroundColor Cyan

# Step 1: Create custom domain
Write-Host "`n📝 Step 1: Creating custom domain name..." -ForegroundColor Yellow

try {
    $domainResponse = aws apigateway create-domain-name `
        --domain-name $DomainName `
        --certificate-arn $CertificateArn `
        --endpoint-configuration types=REGIONAL `
        --region $Region | ConvertFrom-Json
    
    $targetDomain = $domainResponse.regionalDomainName
    Write-Host "✅ Custom domain created!" -ForegroundColor Green
    Write-Host "   Target: $targetDomain" -ForegroundColor Gray
} catch {
    Write-Host "⚠️  Domain may already exist, continuing..." -ForegroundColor Yellow
    $domainResponse = aws apigateway get-domain-name `
        --domain-name $DomainName `
        --region $Region | ConvertFrom-Json
    $targetDomain = $domainResponse.regionalDomainName
}

# Step 2: Create base path mapping
Write-Host "`n📝 Step 2: Creating base path mapping..." -ForegroundColor Yellow

try {
    aws apigateway create-base-path-mapping `
        --domain-name $DomainName `
        --rest-api-id $ApiId `
        --stage prod `
        --region $Region | Out-Null
    
    Write-Host "✅ Base path mapping created!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Base path mapping may already exist" -ForegroundColor Yellow
}

# Step 3: Get Route 53 hosted zone
Write-Host "`n📝 Step 3: Finding Route 53 hosted zone..." -ForegroundColor Yellow

$hostedZones = aws route53 list-hosted-zones-by-name `
    --dns-name christianconservativestoday.com `
    --query "HostedZones[0]" | ConvertFrom-Json

$zoneId = $hostedZones.Id -replace "/hostedzone/", ""
Write-Host "✅ Found hosted zone: $zoneId" -ForegroundColor Green

# Step 4: Create Route 53 record
Write-Host "`n📝 Step 4: Creating Route 53 DNS record..." -ForegroundColor Yellow

$changeBatch = @{
    Changes = @(
        @{
            Action = "UPSERT"
            ResourceRecordSet = @{
                Name = $DomainName
                Type = "CNAME"
                TTL = 300
                ResourceRecords = @(
                    @{ Value = $targetDomain }
                )
            }
        }
    )
} | ConvertTo-Json -Depth 10

$changeBatch | Out-File -FilePath "change-batch.json" -Encoding utf8

aws route53 change-resource-record-sets `
    --hosted-zone-id $zoneId `
    --change-batch file://change-batch.json | Out-Null

Remove-Item "change-batch.json"

Write-Host "✅ DNS record created!" -ForegroundColor Green

# Summary
Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "🎉 CUSTOM DOMAIN CONFIGURED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "`nCustom Domain: https://$DomainName" -ForegroundColor Yellow
Write-Host "Target Domain: $targetDomain" -ForegroundColor Gray
Write-Host "`nAPI Endpoints:" -ForegroundColor Cyan
Write-Host "  Admin:         https://$DomainName/admin/"
Write-Host "  Auth:          https://$DomainName/auth/"
Write-Host "  Articles:      https://$DomainName/articles/"
Write-Host "  Videos:        https://$DomainName/videos/"
Write-Host "  News:          https://$DomainName/news/"
Write-Host "  Resources:     https://$DomainName/resources/"
Write-Host "  Contributors:  https://$DomainName/contributors/"
Write-Host "  Comments:      https://$DomainName/comments/"
Write-Host "  Tags:          https://$DomainName/tags/"
Write-Host "  Prayer:        https://$DomainName/prayer/"
Write-Host "  Events:        https://$DomainName/events/"
Write-Host "  Email:         https://$DomainName/email/"
Write-Host "  Ministry:      https://$DomainName/ministry/"
Write-Host "  Notifications: https://$DomainName/notifications/"
Write-Host "  URL Analysis:  https://$DomainName/url-analysis/"
Write-Host "  PayPal:        https://$DomainName/paypal/"
Write-Host "  Download:      https://$DomainName/download/"
Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "1. Wait 5-10 minutes for DNS propagation"
Write-Host "2. Test endpoints: .\test-unified-api.ps1"
Write-Host "3. Update frontend URLs: .\update-frontend-urls.ps1"
Write-Host "`n" + "="*60 -ForegroundColor Cyan
