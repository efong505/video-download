# Setup Accounts Script
# Automates AWS account setup for the tutorial

param(
    [string]$ChildAccountId = "",
    [switch]$SkipRoleCreation
)

Write-Host "=== AWS Multi-Account Setup Script ===" -ForegroundColor Green
Write-Host ""

# Step 1: Verify AWS credentials
Write-Host "Step 1: Verifying AWS credentials..." -ForegroundColor Yellow
try {
    $identity = aws sts get-caller-identity | ConvertFrom-Json
    Write-Host "✅ Authenticated as: $($identity.Arn)" -ForegroundColor Green
    Write-Host "   Account: $($identity.Account)" -ForegroundColor Green
    
    if ($identity.Account -ne "371751795928") {
        Write-Host "⚠️  Warning: Not using production account (371751795928)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ AWS credentials not configured" -ForegroundColor Red
    Write-Host "   Run: aws configure" -ForegroundColor Yellow
    exit 1
}

# Step 2: Check AWS Organizations
Write-Host "`nStep 2: Checking AWS Organizations..." -ForegroundColor Yellow
try {
    $org = aws organizations describe-organization | ConvertFrom-Json
    Write-Host "✅ Organization exists: $($org.Organization.Id)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Organization not found. Creating..." -ForegroundColor Yellow
    try {
        $org = aws organizations create-organization --feature-set ALL | ConvertFrom-Json
        Write-Host "✅ Organization created: $($org.Organization.Id)" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to create organization" -ForegroundColor Red
        Write-Host "   You may need root account access" -ForegroundColor Yellow
        exit 1
    }
}

# Step 3: Get or validate child account ID
Write-Host "`nStep 3: Validating child account..." -ForegroundColor Yellow
if (-not $ChildAccountId) {
    Write-Host "⚠️  Child account ID not provided" -ForegroundColor Yellow
    Write-Host "   Listing accounts in organization..." -ForegroundColor Yellow
    
    $accounts = aws organizations list-accounts | ConvertFrom-Json
    Write-Host "`nAccounts in organization:" -ForegroundColor Cyan
    foreach ($account in $accounts.Accounts) {
        Write-Host "   - $($account.Name) ($($account.Id)) - $($account.Email)" -ForegroundColor Cyan
    }
    
    Write-Host "`nPlease enter the child account ID (ed@ekewaka):" -ForegroundColor Yellow
    $ChildAccountId = Read-Host
}

Write-Host "✅ Using child account: $ChildAccountId" -ForegroundColor Green

# Step 4: Test cross-account role
Write-Host "`nStep 4: Testing cross-account role..." -ForegroundColor Yellow
$roleArn = "arn:aws:iam::${ChildAccountId}:role/TerraformCrossAccountRole"

try {
    $assumeRole = aws sts assume-role `
        --role-arn $roleArn `
        --role-session-name "setup-test" `
        --external-id "terraform-copy-tutorial" | ConvertFrom-Json
    
    Write-Host "✅ Cross-account role is accessible" -ForegroundColor Green
    Write-Host "   Role ARN: $roleArn" -ForegroundColor Green
} catch {
    Write-Host "❌ Cannot assume cross-account role" -ForegroundColor Red
    
    if (-not $SkipRoleCreation) {
        Write-Host "`n⚠️  Role needs to be created in child account" -ForegroundColor Yellow
        Write-Host "   Options:" -ForegroundColor Yellow
        Write-Host "   1. Create manually via AWS Console (recommended for first time)" -ForegroundColor Yellow
        Write-Host "   2. Use AWS CLI if you have child account credentials configured" -ForegroundColor Yellow
        Write-Host "`n   See docs\STEP-01-ACCOUNT-SETUP.md for detailed instructions" -ForegroundColor Cyan
    }
    exit 1
}

# Step 5: Update terraform.tfvars
Write-Host "`nStep 5: Updating terraform.tfvars..." -ForegroundColor Yellow
$tfvarsPath = "terraform\terraform.tfvars"

if (Test-Path $tfvarsPath) {
    $content = Get-Content $tfvarsPath -Raw
    
    # Replace child account ID
    $content = $content -replace 'REPLACE_WITH_YOUR_CHILD_ACCOUNT_ID', $ChildAccountId
    
    # Save updated file
    $content | Out-File -FilePath $tfvarsPath -Encoding utf8 -NoNewline
    
    Write-Host "✅ terraform.tfvars updated with child account ID" -ForegroundColor Green
} else {
    Write-Host "❌ terraform.tfvars not found at $tfvarsPath" -ForegroundColor Red
    exit 1
}

# Step 6: Verify Lambda code
Write-Host "`nStep 6: Verifying Lambda code..." -ForegroundColor Yellow
$lambdaZip = "lambda-code\sample-function\sample-function.zip"

if (Test-Path $lambdaZip) {
    Write-Host "✅ Lambda ZIP exists" -ForegroundColor Green
} else {
    Write-Host "⚠️  Lambda ZIP not found. Creating..." -ForegroundColor Yellow
    
    $lambdaDir = "lambda-code\sample-function"
    if (Test-Path "$lambdaDir\index.py") {
        Compress-Archive -Path "$lambdaDir\index.py" -DestinationPath $lambdaZip -Force
        Write-Host "✅ Lambda ZIP created" -ForegroundColor Green
    } else {
        Write-Host "❌ index.py not found in $lambdaDir" -ForegroundColor Red
        Write-Host "   Run through STEP-04-DEPLOY.md to create Lambda code" -ForegroundColor Yellow
        exit 1
    }
}

# Step 7: Initialize Terraform
Write-Host "`nStep 7: Initializing Terraform..." -ForegroundColor Yellow
Push-Location terraform

try {
    terraform init
    Write-Host "✅ Terraform initialized" -ForegroundColor Green
} catch {
    Write-Host "❌ Terraform initialization failed" -ForegroundColor Red
    Pop-Location
    exit 1
}

# Step 8: Validate Terraform
Write-Host "`nStep 8: Validating Terraform configuration..." -ForegroundColor Yellow
try {
    terraform validate
    Write-Host "✅ Terraform configuration is valid" -ForegroundColor Green
} catch {
    Write-Host "❌ Terraform validation failed" -ForegroundColor Red
    Pop-Location
    exit 1
}

Pop-Location

# Summary
Write-Host "`n=== Setup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "✅ AWS credentials configured" -ForegroundColor Green
Write-Host "✅ AWS Organizations set up" -ForegroundColor Green
Write-Host "✅ Child account: $ChildAccountId" -ForegroundColor Green
Write-Host "✅ Cross-account role accessible" -ForegroundColor Green
Write-Host "✅ terraform.tfvars configured" -ForegroundColor Green
Write-Host "✅ Lambda code ready" -ForegroundColor Green
Write-Host "✅ Terraform initialized and validated" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  cd terraform" -ForegroundColor Yellow
Write-Host "  terraform plan    # Preview changes" -ForegroundColor Yellow
Write-Host "  terraform apply   # Deploy infrastructure" -ForegroundColor Yellow
Write-Host ""
Write-Host "For detailed instructions, see docs\STEP-04-DEPLOY.md" -ForegroundColor Cyan
