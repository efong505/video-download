# Tutorial Readiness Check
# Verifies all tutorial files are in place and prerequisites are met

Write-Host "=== Terraform Tutorial Readiness Check ===" -ForegroundColor Green
Write-Host ""

$allGood = $true

# Check 1: Documentation files
Write-Host "1. Checking documentation files..." -ForegroundColor Yellow
$docFiles = @(
    "README.md",
    "QUICK-START.md",
    "START-HERE.md",
    "TUTORIAL-COMPLETE.md",
    "docs\STEP-01-ACCOUNT-SETUP.md",
    "docs\STEP-02-IAM-ROLES.md",
    "docs\STEP-03-TERRAFORM-CONFIG.md",
    "docs\STEP-04-DEPLOY.md",
    "docs\STEP-05-VERIFY.md",
    "docs\STEP-06-CLEANUP.md",
    "docs\TROUBLESHOOTING.md"
)

$missingDocs = @()
foreach ($file in $docFiles) {
    if (-not (Test-Path $file)) {
        $missingDocs += $file
    }
}

if ($missingDocs.Count -eq 0) {
    Write-Host "   ✅ All documentation files present ($($docFiles.Count) files)" -ForegroundColor Green
} else {
    Write-Host "   ❌ Missing documentation files:" -ForegroundColor Red
    $missingDocs | ForEach-Object { Write-Host "      - $_" -ForegroundColor Red }
    $allGood = $false
}

# Check 2: Script files
Write-Host "`n2. Checking automation scripts..." -ForegroundColor Yellow
$scriptFiles = @(
    "scripts\setup-accounts.ps1",
    "scripts\verify-deployment.ps1",
    "scripts\cleanup.ps1",
    "scripts\reset-tutorial.ps1"
)

$missingScripts = @()
foreach ($file in $scriptFiles) {
    if (-not (Test-Path $file)) {
        $missingScripts += $file
    }
}

if ($missingScripts.Count -eq 0) {
    Write-Host "   ✅ All automation scripts present ($($scriptFiles.Count) files)" -ForegroundColor Green
} else {
    Write-Host "   ❌ Missing script files:" -ForegroundColor Red
    $missingScripts | ForEach-Object { Write-Host "      - $_" -ForegroundColor Red }
    $allGood = $false
}

# Check 3: Configuration files
Write-Host "`n3. Checking configuration files..." -ForegroundColor Yellow
$configFiles = @(
    ".gitignore",
    "terraform\terraform.tfvars.example"
)

$missingConfig = @()
foreach ($file in $configFiles) {
    if (-not (Test-Path $file)) {
        $missingConfig += $file
    }
}

if ($missingConfig.Count -eq 0) {
    Write-Host "   ✅ All configuration files present ($($configFiles.Count) files)" -ForegroundColor Green
} else {
    Write-Host "   ❌ Missing configuration files:" -ForegroundColor Red
    $missingConfig | ForEach-Object { Write-Host "      - $_" -ForegroundColor Red }
    $allGood = $false
}

# Check 4: Directories
Write-Host "`n4. Checking directory structure..." -ForegroundColor Yellow
$directories = @(
    "docs",
    "scripts",
    "terraform",
    "lambda-code"
)

$missingDirs = @()
foreach ($dir in $directories) {
    if (-not (Test-Path $dir -PathType Container)) {
        $missingDirs += $dir
    }
}

if ($missingDirs.Count -eq 0) {
    Write-Host "   ✅ All directories present ($($directories.Count) directories)" -ForegroundColor Green
} else {
    Write-Host "   ❌ Missing directories:" -ForegroundColor Red
    $missingDirs | ForEach-Object { Write-Host "      - $_" -ForegroundColor Red }
    $allGood = $false
}

# Check 5: Prerequisites
Write-Host "`n5. Checking prerequisites..." -ForegroundColor Yellow

# Check AWS CLI
try {
    $awsVersion = aws --version 2>&1
    Write-Host "   ✅ AWS CLI installed: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ AWS CLI not installed" -ForegroundColor Red
    $allGood = $false
}

# Check Terraform
try {
    $tfVersion = terraform version -json | ConvertFrom-Json
    Write-Host "   ✅ Terraform installed: $($tfVersion.terraform_version)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Terraform not installed" -ForegroundColor Red
    $allGood = $false
}

# Check PowerShell version
$psVersion = $PSVersionTable.PSVersion
if ($psVersion.Major -ge 7) {
    Write-Host "   ✅ PowerShell $($psVersion.Major).$($psVersion.Minor) (compatible)" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  PowerShell $($psVersion.Major).$($psVersion.Minor) (recommend 7+)" -ForegroundColor Yellow
}

# Check AWS credentials
Write-Host "`n6. Checking AWS credentials..." -ForegroundColor Yellow
try {
    $identity = aws sts get-caller-identity 2>&1 | ConvertFrom-Json
    Write-Host "   ✅ AWS credentials configured" -ForegroundColor Green
    Write-Host "      Account: $($identity.Account)" -ForegroundColor Cyan
    Write-Host "      User: $($identity.Arn)" -ForegroundColor Cyan
    
    if ($identity.Account -eq "371751795928") {
        Write-Host "      ✅ Using production account" -ForegroundColor Green
    } else {
        Write-Host "      ⚠️  Not using production account (371751795928)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ AWS credentials not configured" -ForegroundColor Red
    Write-Host "      Run: aws configure" -ForegroundColor Yellow
    $allGood = $false
}

# Summary
Write-Host "`n=== Readiness Summary ===" -ForegroundColor Green
Write-Host ""

if ($allGood) {
    Write-Host "✅ Tutorial is ready to use!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Read START-HERE.md for overview" -ForegroundColor Yellow
    Write-Host "  2. Read README.md for detailed introduction" -ForegroundColor Yellow
    Write-Host "  3. Choose your path:" -ForegroundColor Yellow
    Write-Host "     - Quick Start: Get-Content QUICK-START.md" -ForegroundColor Yellow
    Write-Host "     - Full Tutorial: Get-Content docs\STEP-01-ACCOUNT-SETUP.md" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To begin:" -ForegroundColor Cyan
    Write-Host "  Get-Content START-HERE.md" -ForegroundColor Yellow
} else {
    Write-Host "❌ Some issues need to be resolved" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please fix the issues above before starting the tutorial." -ForegroundColor Yellow
}

Write-Host ""
