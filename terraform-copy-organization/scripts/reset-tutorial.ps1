# Reset Tutorial Script
# Completely resets the tutorial for a fresh practice run

param(
    [switch]$Force
)

Write-Host "=== Reset Tutorial Script ===" -ForegroundColor Green
Write-Host ""
Write-Host "This will:" -ForegroundColor Yellow
Write-Host "  1. Destroy all infrastructure" -ForegroundColor Yellow
Write-Host "  2. Remove Terraform state" -ForegroundColor Yellow
Write-Host "  3. Clean all local files" -ForegroundColor Yellow
Write-Host "  4. Prepare for fresh deployment" -ForegroundColor Yellow
Write-Host ""

if (-not $Force) {
    Write-Host "⚠️  Are you sure? Type 'yes' to confirm: " -ForegroundColor Yellow -NoNewline
    $confirmation = Read-Host
    
    if ($confirmation -ne "yes") {
        Write-Host "❌ Reset cancelled" -ForegroundColor Red
        exit 0
    }
}

# Step 1: Run cleanup script
Write-Host "`nStep 1: Running cleanup..." -ForegroundColor Yellow
& "$PSScriptRoot\cleanup.ps1" -Force

# Step 2: Remove all Terraform files
Write-Host "`nStep 2: Removing Terraform state..." -ForegroundColor Yellow
Push-Location terraform

Remove-Item .terraform -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item .terraform.lock.hcl -Force -ErrorAction SilentlyContinue
Remove-Item terraform.tfstate -Force -ErrorAction SilentlyContinue
Remove-Item terraform.tfstate.backup -Force -ErrorAction SilentlyContinue

Write-Host "✅ Terraform state removed" -ForegroundColor Green

Pop-Location

# Step 3: Reinitialize Terraform
Write-Host "`nStep 3: Reinitializing Terraform..." -ForegroundColor Yellow
Push-Location terraform

terraform init | Out-Null
Write-Host "✅ Terraform reinitialized" -ForegroundColor Green

Pop-Location

# Step 4: Verify configuration
Write-Host "`nStep 4: Verifying configuration..." -ForegroundColor Yellow

# Check terraform.tfvars
$tfvarsPath = "terraform\terraform.tfvars"
$placeholders = Get-Content $tfvarsPath | Select-String "REPLACE_WITH"

if ($placeholders) {
    Write-Host "⚠️  terraform.tfvars contains placeholders" -ForegroundColor Yellow
    Write-Host "   Run: .\scripts\setup-accounts.ps1 -ChildAccountId YOUR_ACCOUNT_ID" -ForegroundColor Yellow
} else {
    Write-Host "✅ terraform.tfvars configured" -ForegroundColor Green
}

# Check Lambda ZIP
if (Test-Path "lambda-code\sample-function\sample-function.zip") {
    Write-Host "✅ Lambda ZIP exists" -ForegroundColor Green
} else {
    Write-Host "⚠️  Lambda ZIP not found" -ForegroundColor Yellow
    Write-Host "   See docs\STEP-04-DEPLOY.md to create Lambda code" -ForegroundColor Yellow
}

# Final summary
Write-Host "`n=== Reset Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "✅ Infrastructure destroyed" -ForegroundColor Green
Write-Host "✅ Terraform state reset" -ForegroundColor Green
Write-Host "✅ Ready for fresh practice run" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Verify terraform.tfvars is configured" -ForegroundColor Yellow
Write-Host "  2. cd terraform" -ForegroundColor Yellow
Write-Host "  3. terraform plan" -ForegroundColor Yellow
Write-Host "  4. terraform apply" -ForegroundColor Yellow
Write-Host ""
