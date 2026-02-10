# CORRECTED API Analysis - Do NOT Delete These!

## ⚠️ IMPORTANT CORRECTIONS

Based on your clarification, here are the APIs that MUST BE KEPT:

---

## ✅ KEEP - Active Projects

### 1. MyTestimony API (wm234jgiv3)
**Status**: ✅ KEEP - Active project
**Used by**: music.mytestimony.click
**Created**: 2025-10-12
**Reason**: Separate active project, not worked on recently but still needed

---

### 2. NewsScraperAPI (xi6azy9cp9)
**Status**: ✅ KEEP - Active scraper
**Used by**: news.mytestimony.click webscraper
**Created**: 2025-11-20 (recent!)
**Reason**: Active news scraping functionality

---

### 3. recipe-scraper-api (1lgppg87fe & ts4xz3fs70)
**Status**: ✅ KEEP - Same as NewsScraperAPI
**Used by**: news.mytestimony.click webscraper
**Created**: 2025-10-17
**Reason**: Same scraper system as NewsScraperAPI
**Note**: May have 2 versions - need to verify which is active

---

### 4. storage-subscription-api (fm52xqjuz3)
**Status**: ⚠️ VERIFY - May be replaced
**Type**: HTTP API (not REST)
**Created**: 2025-11-17 (recent!)
**Possible replacement**: PayPal billing API or email subscription API?
**Action needed**: Check if this is still used for subscriptions

---

## 🔍 API Charging - IMPORTANT!

### YES, you are charged even if APIs are not used!

**API Gateway Pricing**:
- **REST APIs**: $3.50/month per API (even with 0 requests)
- **HTTP APIs**: $1.00/month per API (even with 0 requests)

**You pay for**:
- ✅ API existence (monthly fee)
- ✅ Requests (per million)
- ✅ Data transfer

**You DON'T pay for**:
- ❌ APIs that are deleted

### Current Monthly Charges (Estimated)
```
25 REST APIs × $3.50 = $87.50/month
3 HTTP APIs × $1.00 = $3.00/month
Total: $90.50/month = $1,086/year
```

**Even if an API receives ZERO requests, you still pay the monthly fee!**

---

## 🎯 REVISED DELETION LIST

### Safe to Delete (Confirmed Duplicates Only)

#### 1. video-downloader-api DUPLICATE
- **DELETE**: qdk8y6nna6 (old version from 20:09)
- **KEEP**: j3w8kgqlvi (current version from 20:13, used in HTML)
- **Savings**: $3.50/month

#### 2. notifications-api DUPLICATE
- **DELETE**: ulcbf9glui (old version from 23:45:25)
- **KEEP**: lc7w6ebg4m (current version from 23:45:47, used in HTML)
- **Savings**: $3.50/month

#### 3. contributors-api DUPLICATES
- **DELETE**: o0mzmvcs59 (duplicate)
- **DELETE**: wzn7e1ipjf (duplicate)
- **KEEP**: hzursivfuk (current version, used in HTML)
- **Savings**: $7.00/month

#### 4. Test APIs (if truly not needed)
- **MyFirstAPI** (97gtxp82b2) - Generic test API
- **MyMusicAPI** (sljzs4mmue) - Generic test API
- **Savings**: $7.00/month

**Total Safe Deletions**: 5 APIs = **$17.50/month** ($210/year)

---

## ⚠️ NEEDS VERIFICATION

### 1. recipe-scraper-api (2 versions)
**Question**: Which version is active for news.mytestimony.click?
- ts4xz3fs70 (created 16:01:46)
- 1lgppg87fe (created 16:03:16)

**Action**: Check which one is configured in news.mytestimony.click

### 2. storage-subscription-api (fm52xqjuz3)
**Question**: Is this still used or replaced by:
- email-subscription-api (niexv1rw75)?
- paypal-billing-api?
- ministry-tools-api (gu6c08ctel)?

**Action**: Check subscription flow in christianconservativestoday.com

---

## 🔍 Verification Commands

### Check recipe-scraper-api usage
```powershell
# Check which recipe-scraper has Lambda integrations
$apis = @("ts4xz3fs70", "1lgppg87fe")
foreach ($apiId in $apis) {
    Write-Host "`nChecking $apiId..."
    $resources = aws apigateway get-resources --rest-api-id $apiId --region us-east-1 | ConvertFrom-Json
    foreach ($resource in $resources.items) {
        if ($resource.resourceMethods) {
            Write-Host "  Has methods on: $($resource.path)"
        }
    }
}
```

### Check storage-subscription-api usage
```powershell
# Check HTTP API integrations
$integrations = aws apigatewayv2 get-integrations --api-id fm52xqjuz3 --region us-east-1 | ConvertFrom-Json
Write-Host "Integrations:"
foreach ($int in $integrations.Items) {
    Write-Host "  - $($int.IntegrationUri)"
}

# Search HTML files for this API
Select-String -Path "*.html" -Pattern "fm52xqjuz3" -Recurse
```

### Check if storage-subscription was replaced
```powershell
# Search for subscription-related API calls in HTML
Select-String -Path "*.html" -Pattern "subscription" -Recurse | Select-String -Pattern "execute-api"
```

---

## 💰 UPDATED COST ANALYSIS

### Current State (28 APIs)
```
REST APIs: 25 × $3.50 = $87.50/month
HTTP APIs: 3 × $1.00 = $3.00/month
Total: $90.50/month = $1,086/year
```

### After Safe Deletions (23 APIs)
```
REST APIs: 20 × $3.50 = $70.00/month
HTTP APIs: 3 × $1.00 = $3.00/month
Total: $73.00/month = $876/year
Savings: $17.50/month = $210/year
```

### After Full Consolidation (1 API)
```
REST APIs: 1 × $3.50 = $3.50/month
Custom Domain: $0.50/month
Total: $4.00/month = $48/year
Savings: $86.50/month = $1,038/year
```

---

## 🎯 RECOMMENDED ACTIONS

### Step 1: Verify Active APIs
Run these checks:
```powershell
cd API-Consolidation\scripts

# Check recipe-scraper versions
.\check-recipe-scraper.ps1

# Check storage-subscription usage
.\check-storage-subscription.ps1

# Full verification of all suspected unused
.\verify-unused-apis.ps1
```

### Step 2: Delete Only Confirmed Duplicates
**Safe to delete NOW** (5 APIs):
- qdk8y6nna6 (video-downloader duplicate)
- ulcbf9glui (notifications duplicate)
- o0mzmvcs59 (contributors duplicate)
- wzn7e1ipjf (contributors duplicate)
- 97gtxp82b2 (MyFirstAPI test)
- sljzs4mmue (MyMusicAPI test)

**Savings**: $21/month ($252/year)

### Step 3: Verify Then Decide
- recipe-scraper-api versions
- storage-subscription-api usage

### Step 4: Consolidate Remaining APIs
After cleanup, consolidate ~20 active APIs into 1 unified API.

---

## 📋 Projects Summary

### christianconservativestoday.com (Main Project)
- 17 active APIs
- Consolidation will save $55-60/month

### music.mytestimony.click
- MyTestimony API (wm234jgiv3) - KEEP

### news.mytestimony.click
- NewsScraperAPI (xi6azy9cp9) - KEEP
- recipe-scraper-api (1 or 2 versions) - KEEP (verify which)

---

**Next Step**: Run verification script to check storage-subscription-api and recipe-scraper versions before any deletion.
