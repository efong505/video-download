# Automatically configure email authentication in Route53
# Sets up SPF, DKIM, and DMARC records

$domain = "christianconservativestoday.com"
$region = "us-east-1"

Write-Host ""
Write-Host "Setting up email authentication for $domain..." -ForegroundColor Cyan
Write-Host ""

# Get hosted zone ID
Write-Host "Finding Route53 hosted zone..." -ForegroundColor Yellow
$hostedZoneId = aws route53 list-hosted-zones --query "HostedZones[?Name=='${domain}.'].Id" --output text
$hostedZoneId = $hostedZoneId -replace '/hostedzone/', ''

if (-not $hostedZoneId) {
    Write-Host "Error: Hosted zone not found for $domain" -ForegroundColor Red
    exit 1
}

Write-Host "Found hosted zone: $hostedZoneId" -ForegroundColor Green
Write-Host ""

# Get DKIM tokens
Write-Host "Getting DKIM tokens from SES..." -ForegroundColor Yellow
$dkimTokens = aws ses verify-domain-dkim --domain $domain --region $region --query "DkimTokens" --output json | ConvertFrom-Json

# Create Route53 change batch
$changes = @()

# Add 3 DKIM CNAME records
foreach ($token in $dkimTokens) {
    $changes += @{
        Action = "UPSERT"
        ResourceRecordSet = @{
            Name = "${token}._domainkey.${domain}"
            Type = "CNAME"
            TTL = 1800
            ResourceRecords = @(
                @{ Value = "${token}.dkim.amazonses.com" }
            )
        }
    }
}

# Add SPF TXT record
$changes += @{
    Action = "UPSERT"
    ResourceRecordSet = @{
        Name = $domain
        Type = "TXT"
        TTL = 300
        ResourceRecords = @(
            @{ Value = "`"v=spf1 include:amazonses.com ~all`"" }
        )
    }
}

# Add DMARC TXT record
$changes += @{
    Action = "UPSERT"
    ResourceRecordSet = @{
        Name = "_dmarc.${domain}"
        Type = "TXT"
        TTL = 300
        ResourceRecords = @(
            @{ Value = "`"v=DMARC1; p=quarantine; rua=mailto:dmarc@${domain}`"" }
        )
    }
}

# Convert to JSON
$changeBatch = @{
    Changes = $changes
} | ConvertTo-Json -Depth 10

# Apply changes
Write-Host "Adding DNS records to Route53..." -ForegroundColor Yellow
$changeBatch | Out-File -FilePath "temp_changes.json" -Encoding ASCII
aws route53 change-resource-record-sets --hosted-zone-id $hostedZoneId --change-batch file://temp_changes.json
Remove-Item "temp_changes.json" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "SUCCESS!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Added the following records to Route53:"
Write-Host ""
Write-Host "- 3 DKIM CNAME records"
Write-Host "- SPF TXT record"
Write-Host "- DMARC TXT record"
Write-Host ""

Write-Host "DNS propagation may take 5-30 minutes." -ForegroundColor Yellow
Write-Host ""

Write-Host "To verify DKIM status:" -ForegroundColor Cyan
Write-Host "aws ses get-identity-dkim-attributes --identities $domain --region $region"
Write-Host ""

Write-Host "After propagation, your emails will be verified and trusted!" -ForegroundColor Green
Write-Host ""
