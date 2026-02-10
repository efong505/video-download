# Email Authentication Setup for AWS SES
# Sets up SPF, DKIM, and DMARC records to prevent spam warnings

$domain = "christianconservativestoday.com"
$region = "us-east-1"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Email Authentication Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Enable DKIM for domain
Write-Host "Step 1: Enabling DKIM signing..." -ForegroundColor Yellow
aws ses verify-domain-dkim --domain $domain --region $region

Write-Host "`nDKIM tokens generated. You need to add these as CNAME records in your DNS.`n" -ForegroundColor Green

# Step 2: Get DKIM tokens
Write-Host "Step 2: Getting DKIM tokens..." -ForegroundColor Yellow
$dkimTokens = aws ses verify-domain-dkim --domain $domain --region $region --query "DkimTokens" --output json | ConvertFrom-Json

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "DNS RECORDS TO ADD" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# DKIM Records
Write-Host "1. DKIM RECORDS (Add 3 CNAME records):" -ForegroundColor Green
$i = 1
foreach ($token in $dkimTokens) {
    Write-Host "`n   Record ${i}:" -ForegroundColor Yellow
    Write-Host "   Type:  CNAME"
    Write-Host "   Name:  ${token}._domainkey.$domain"
    Write-Host "   Value: ${token}.dkim.amazonses.com"
    $i++
}

# SPF Record
Write-Host "`n2. SPF RECORD (Add TXT record):" -ForegroundColor Green
Write-Host "   Type:  TXT"
Write-Host "   Name:  $domain"
Write-Host "   Value: v=spf1 include:amazonses.com ~all"

# DMARC Record
Write-Host "`n3. DMARC RECORD (Add TXT record):" -ForegroundColor Green
Write-Host "   Type:  TXT"
Write-Host "   Name:  _dmarc.$domain"
Write-Host "   Value: v=DMARC1; p=quarantine; rua=mailto:dmarc@$domain"

# Custom MAIL FROM (Optional but recommended)
Write-Host "`n4. CUSTOM MAIL FROM (Optional - Recommended):" -ForegroundColor Green
Write-Host "   Type:  MX"
Write-Host "   Name:  mail.$domain"
Write-Host "   Value: 10 feedback-smtp.$region.amazonses.com"
Write-Host "`n   Type:  TXT"
Write-Host "   Name:  mail.$domain"
Write-Host "   Value: v=spf1 include:amazonses.com ~all"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "1. Log into your domain registrar (GoDaddy, Namecheap, etc.)"
Write-Host "2. Go to DNS settings for $domain"
Write-Host "3. Add all the records shown above"
Write-Host "4. Wait 24-48 hours for DNS propagation"
Write-Host "5. Verify DKIM status:"
Write-Host "   aws ses get-identity-dkim-attributes --identities $domain --region $region`n"

Write-Host "After setup, emails will show as verified and trusted!`n" -ForegroundColor Green
