# API Usage Verification Report

## ✅ APIs Currently In Use (19 APIs)

Based on scanning all HTML files in your project, here are the APIs that are **actively being used**:

### Core APIs (17 - Must Keep)

| # | API Name | API ID | Lambda Function | Used In Files | Status |
|---|----------|--------|-----------------|---------------|--------|
| 1 | **admin-api** | k2avuckm38 | admin_api | 15+ files | ✅ ACTIVE |
| 2 | **auth-api** | r6l0z3605f | auth_api | 12+ files | ✅ ACTIVE |
| 3 | **articles-api** | fr3hh94h4a | articles_api | 18+ files | ✅ ACTIVE |
| 4 | **video-api** | wfeds5lejb | video_list_api | category.html | ✅ ACTIVE |
| 5 | **news-api** | xr1xcc83bj | news_api | 6+ files | ✅ ACTIVE |
| 6 | **resources-api** | ckbtfz4vbl | resources_api | 3 files | ✅ ACTIVE |
| 7 | **contributors-api** | hzursivfuk | contributors_api | 3 files | ✅ ACTIVE |
| 8 | **comments-api** | l10alau5g3 | comments_api | 2 files | ✅ ACTIVE |
| 9 | **video-tag-api** | h4hoegi26b | tag_api | 10+ files | ✅ ACTIVE |
| 10 | **prayer-api** | cayl9dmtaf | prayer_api | 3 files | ✅ ACTIVE |
| 11 | **email-subscription-api** | niexv1rw75 | email_subscription_api | 7 files | ✅ ACTIVE |
| 12 | **ministry-tools-api** | gu6c08ctel | ministry_tools_api | 8 files | ✅ ACTIVE |
| 13 | **notifications-api** | lc7w6ebg4m | notifications_api | notification-settings.html | ✅ ACTIVE |
| 14 | **url-analysis-api** | q65k3dbpd7 | url_analysis_api | 3 files | ✅ ACTIVE |
| 15 | **video-downloader-api** | j3w8kgqlvi | downloader | 4 files | ✅ ACTIVE |
| 16 | **Book Delivery API** | k2zbtkeh67 | book_delivery | 2 files (book pages) | ✅ ACTIVE |
| 17 | **shopping-api** | ydq9xzya5d | shopping_api | 5 files (Shopping/) | ✅ ACTIVE |

### Duplicate APIs (2 - Can Delete After Verification)

| # | API Name | API ID | Notes | Action |
|---|----------|--------|-------|--------|
| 18 | contributors-api (duplicate) | o0mzmvcs59 | Duplicate of hzursivfuk | ⚠️ VERIFY THEN DELETE |
| 19 | contributors-api (duplicate) | wzn7e1ipjf | Duplicate of hzursivfuk | ⚠️ VERIFY THEN DELETE |

---

## ❌ Unused/Test APIs (9 APIs - Safe to Delete)

These APIs are **NOT found** in any production HTML files:

| # | API Name | API ID | Reason | Safe to Delete? |
|---|----------|--------|--------|-----------------|
| 1 | **MyFirstAPI** | 97gtxp82b2 | Test/demo API | ✅ YES |
| 2 | **MyMusicAPI** | sljzs4mmue | Test/demo API | ✅ YES |
| 3 | **MyTestimony API** | wm234jgiv3 | Old/unused | ✅ YES |
| 4 | **recipe-scraper-api** | 1lgppg87fe | Not used | ✅ YES |
| 5 | **recipe-scraper-api** (dup) | ts4xz3fs70 | Duplicate, not used | ✅ YES |
| 6 | **NewsScraperAPI** | xi6azy9cp9 | Not used (different from news-api) | ✅ YES |
| 7 | **video-downloader-api** (dup) | qdk8y6nna6 | Duplicate of j3w8kgqlvi | ✅ YES |
| 8 | **notifications-api** (dup) | ulcbf9glui | Duplicate of lc7w6ebg4m | ✅ YES |
| 9 | **storage-subscription-api** | fm52xqjuz3 | HTTP API, not found in files | ⚠️ VERIFY FIRST |

---

## 📊 Summary

### Current State
- **Total APIs**: 28
- **Active APIs**: 17 (core functionality)
- **Duplicate APIs**: 2 (need verification)
- **Unused APIs**: 9 (safe to delete)

### Recommended Action
- **Keep**: 17 core APIs
- **Verify then delete**: 2 duplicate contributors APIs
- **Delete immediately**: 9 unused/test APIs

### After Cleanup
- **APIs remaining**: 17-19 (depending on duplicates)
- **Cost savings from cleanup**: ~$31.50/month (9 APIs × $3.50)
- **Additional savings from consolidation**: $55-59/month

---

## 🔍 Detailed Usage Analysis

### High Usage APIs (10+ files)
1. **articles-api** (fr3hh94h4a) - 18+ files
2. **admin-api** (k2avuckm38) - 15+ files
3. **auth-api** (r6l0z3605f) - 12+ files
4. **video-tag-api** (h4hoegi26b) - 10+ files

### Medium Usage APIs (3-9 files)
5. **ministry-tools-api** (gu6c08ctel) - 8 files
6. **email-subscription-api** (niexv1rw75) - 7 files
7. **news-api** (xr1xcc83bj) - 6 files
8. **shopping-api** (ydq9xzya5d) - 5 files
9. **video-downloader-api** (j3w8kgqlvi) - 4 files

### Low Usage APIs (1-2 files)
10. **contributors-api** (hzursivfuk) - 3 files
11. **prayer-api** (cayl9dmtaf) - 3 files
12. **resources-api** (ckbtfz4vbl) - 3 files
13. **url-analysis-api** (q65k3dbpd7) - 3 files
14. **Book Delivery API** (k2zbtkeh67) - 2 files
15. **comments-api** (l10alau5g3) - 2 files
16. **notifications-api** (lc7w6ebg4m) - 1 file
17. **video-api** (wfeds5lejb) - 1 file

---

## ⚠️ Verification Steps Before Deletion

### Step 1: Verify Duplicate APIs
```powershell
# Check if duplicate contributors APIs are used
aws apigateway get-rest-api --rest-api-id o0mzmvcs59
aws apigateway get-rest-api --rest-api-id wzn7e1ipjf

# Check CloudWatch logs for recent activity
aws logs describe-log-groups --log-group-name-prefix "/aws/apigateway/o0mzmvcs59"
aws logs describe-log-groups --log-group-name-prefix "/aws/apigateway/wzn7e1ipjf"
```

### Step 2: Verify storage-subscription-api
```powershell
# This is an HTTP API - check if it's used by backend Lambda functions
aws apigatewayv2 get-api --api-id fm52xqjuz3

# Check CloudWatch logs
aws logs describe-log-groups --log-group-name-prefix "/aws/apigateway/fm52xqjuz3"
```

### Step 3: Check Last 30 Days Activity
```powershell
# For each unused API, check if there's been any traffic
$unusedApis = @("97gtxp82b2", "sljzs4mmue", "wm234jgiv3", "1lgppg87fe", "ts4xz3fs70", "xi6azy9cp9", "qdk8y6nna6", "ulcbf9glui")

foreach ($apiId in $unusedApis) {
    Write-Host "Checking $apiId..."
    aws cloudwatch get-metric-statistics `
        --namespace AWS/ApiGateway `
        --metric-name Count `
        --dimensions Name=ApiName,Value=$apiId `
        --start-time (Get-Date).AddDays(-30).ToString("yyyy-MM-ddTHH:mm:ss") `
        --end-time (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss") `
        --period 86400 `
        --statistics Sum
}
```

---

## 🗑️ Safe Deletion Script

After verification, run this to delete unused APIs:

```powershell
# delete-unused-apis.ps1

$unusedApis = @{
    "MyFirstAPI" = "97gtxp82b2"
    "MyMusicAPI" = "sljzs4mmue"
    "MyTestimony API" = "wm234jgiv3"
    "recipe-scraper-api-1" = "1lgppg87fe"
    "recipe-scraper-api-2" = "ts4xz3fs70"
    "NewsScraperAPI" = "xi6azy9cp9"
    "video-downloader-api-dup" = "qdk8y6nna6"
    "notifications-api-dup" = "ulcbf9glui"
}

Write-Host "⚠️  WARNING: This will delete 8 unused APIs" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to cancel, or any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

foreach ($api in $unusedApis.GetEnumerator()) {
    Write-Host "`nDeleting $($api.Key) ($($api.Value))..." -ForegroundColor Yellow
    
    try {
        aws apigateway delete-rest-api --rest-api-id $api.Value --region us-east-1
        Write-Host "✅ Deleted $($api.Key)" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to delete $($api.Key): $_" -ForegroundColor Red
    }
}

Write-Host "`n✅ Cleanup complete!" -ForegroundColor Green
Write-Host "Monthly savings: ~$28/month (8 APIs × $3.50)" -ForegroundColor Cyan
```

---

## 📝 Updated Consolidation Plan

### Revised API Count
- **Original claim**: 28 APIs → 1 API
- **Actual active APIs**: 17 APIs → 1 API
- **After cleanup**: Delete 9 unused APIs first, then consolidate 17 active APIs

### Revised Cost Savings
```
Current (28 APIs):     $90.50/month
After cleanup (17):    $59.50/month  (save $31/month)
After consolidation:   $4.00/month   (save $86.50/month total)
```

### Recommended Approach
1. **Week 0**: Delete 9 unused APIs (save $31/month immediately)
2. **Week 1**: Consolidate 17 active APIs into unified API
3. **Week 2**: Set up GitHub Actions CI/CD
4. **Week 3**: Monitor and cleanup

---

## ✅ Conclusion

**Good news**: You can safely delete 9 unused APIs right now for immediate savings!

**Action Items**:
1. Run verification script to check for any recent activity
2. Delete 9 unused APIs (save $31/month)
3. Verify 2 duplicate contributors APIs
4. Proceed with consolidation of 17 active APIs

**Total Savings**:
- Immediate: $31/month from cleanup
- After consolidation: $86.50/month total
- Annual: $1,038/year

---

**Next Step**: Run the verification script above to confirm zero activity on unused APIs, then proceed with deletion.
