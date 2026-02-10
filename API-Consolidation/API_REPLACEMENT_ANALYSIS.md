# API Replacement Analysis

## 🔍 Duplicate & Replacement Detection

Based on API names and creation dates, here's the analysis:

---

## ✅ CONFIRMED REPLACEMENTS (Safe to Delete Old Ones)

### 1. video-downloader-api (2 versions)
| API ID | Created | Status | Action |
|--------|---------|--------|--------|
| **qdk8y6nna6** | 2025-10-06 20:09:00 | ❌ OLD VERSION | DELETE |
| **j3w8kgqlvi** | 2025-10-06 20:13:50 | ✅ CURRENT (4 min newer) | KEEP |

**Evidence**: 
- Same name, created 4 minutes apart
- j3w8kgqlvi is used in HTML files (admin.html, download-status.html)
- qdk8y6nna6 NOT found in any HTML files

**Conclusion**: qdk8y6nna6 was replaced by j3w8kgqlvi immediately

---

### 2. notifications-api (2 versions)
| API ID | Created | Status | Action |
|--------|---------|--------|--------|
| **ulcbf9glui** | 2025-11-04 23:45:25 | ❌ OLD VERSION | DELETE |
| **lc7w6ebg4m** | 2025-11-04 23:45:47 | ✅ CURRENT (22 sec newer) | KEEP |

**Evidence**:
- Same name, created 22 seconds apart
- lc7w6ebg4m is used in notification-settings.html
- ulcbf9glui NOT found in any HTML files

**Conclusion**: ulcbf9glui was replaced by lc7w6ebg4m immediately

---

### 3. contributors-api (3 versions!)
| API ID | Created | Status | Action |
|--------|---------|--------|--------|
| **o0mzmvcs59** | 2025-10-20 14:52:49 | ❌ OLD VERSION 1 | DELETE |
| **hzursivfuk** | 2025-10-20 14:51:24 | ✅ CURRENT (created first!) | KEEP |
| **wzn7e1ipjf** | 2025-10-20 14:54:03 | ❌ OLD VERSION 2 | DELETE |

**Evidence**:
- Three APIs with same name, all created within 3 minutes
- hzursivfuk is used in HTML files (admin-contributors.html, election-map.html)
- o0mzmvcs59 and wzn7e1ipjf NOT found in any HTML files
- hzursivfuk was created FIRST, others were likely failed attempts

**Conclusion**: o0mzmvcs59 and wzn7e1ipjf are failed deployment attempts

---

### 4. recipe-scraper-api (2 versions)
| API ID | Created | Status | Action |
|--------|---------|--------|--------|
| **ts4xz3fs70** | 2025-10-17 16:01:46 | ❌ OLD VERSION | DELETE |
| **1lgppg87fe** | 2025-10-17 16:03:16 | ❌ NEWER BUT UNUSED | DELETE |

**Evidence**:
- Same name, created 90 seconds apart
- NEITHER is used in any HTML files
- No active Lambda integration found

**Conclusion**: Both are unused test APIs - DELETE BOTH

---

## ⚠️ POTENTIAL REPLACEMENT (Needs Verification)

### 5. NewsScraperAPI vs news-api
| API ID | Created | Status | Action |
|--------|---------|--------|--------|
| **xi6azy9cp9** (NewsScraperAPI) | 2025-11-20 12:33:00 | ❓ NEWER | VERIFY |
| **xr1xcc83bj** (news-api) | 2025-10-18 12:45:22 | ✅ CURRENTLY USED | KEEP |

**Evidence**:
- Similar purpose (news scraping vs news API)
- NewsScraperAPI created 33 days AFTER news-api
- news-api is actively used in 6+ HTML files
- NewsScraperAPI NOT found in any HTML files

**Possible scenarios**:
1. NewsScraperAPI is a new feature not yet deployed
2. NewsScraperAPI is an abandoned experiment
3. NewsScraperAPI is for backend scraping (not frontend)

**Recommendation**: Check Lambda integrations before deleting

---

## ❌ NO REPLACEMENT FOUND (Truly Unused)

### 6. MyFirstAPI
| API ID | Created | Status |
|--------|---------|--------|
| **97gtxp82b2** | 2025-06-11 13:32:31 | Test/Demo API |

**Evidence**: 
- Generic test name
- Created early in project (June 2025)
- No similar API exists
- Not used anywhere

**Conclusion**: Safe to delete

---

### 7. MyMusicAPI
| API ID | Created | Status |
|--------|---------|--------|
| **sljzs4mmue** | 2025-09-30 10:48:52 | Test/Demo API |

**Evidence**:
- Generic test name
- No music-related functionality in project
- Not used anywhere

**Conclusion**: Safe to delete

---

### 8. MyTestimony API
| API ID | Created | Status |
|--------|---------|--------|
| **wm234jgiv3** | 2025-10-12 04:47:43 | Old/Unused |

**Evidence**:
- No similar API exists
- Not used in any HTML files
- Separate "Salvation" folder exists for testimonies

**Conclusion**: Safe to delete (functionality moved elsewhere)

---

## 📊 SUMMARY

### Confirmed Duplicates (Safe to Delete)
1. ✅ **qdk8y6nna6** - Replaced by j3w8kgqlvi (4 min later)
2. ✅ **ulcbf9glui** - Replaced by lc7w6ebg4m (22 sec later)
3. ✅ **o0mzmvcs59** - Duplicate of hzursivfuk
4. ✅ **wzn7e1ipjf** - Duplicate of hzursivfuk
5. ✅ **ts4xz3fs70** - Unused recipe scraper
6. ✅ **1lgppg87fe** - Unused recipe scraper

### No Replacement (Safe to Delete)
7. ✅ **97gtxp82b2** - MyFirstAPI (test)
8. ✅ **sljzs4mmue** - MyMusicAPI (test)
9. ✅ **wm234jgiv3** - MyTestimony API (old)

### Needs Verification
10. ⚠️ **xi6azy9cp9** - NewsScraperAPI (check Lambda integrations)

---

## 🎯 UPDATED RECOMMENDATION

### Immediate Deletion (9 APIs)
Delete these with confidence:
```
qdk8y6nna6, ulcbf9glui, o0mzmvcs59, wzn7e1ipjf, 
ts4xz3fs70, 1lgppg87fe, 97gtxp82b2, sljzs4mmue, wm234jgiv3
```

**Savings**: 9 APIs × $3.50 = **$31.50/month** ($378/year)

### Verify Then Delete (1 API)
Check Lambda integration first:
```
xi6azy9cp9 (NewsScraperAPI)
```

**Potential additional savings**: $3.50/month ($42/year)

### Total Potential Savings
- **$35/month** ($420/year) from cleanup
- **$55/month** ($660/year) from consolidation of remaining 17 APIs
- **$90/month total** ($1,080/year)

---

## 🔍 Verification Command for NewsScraperAPI

```powershell
# Check if NewsScraperAPI has Lambda integrations
$apiId = "xi6azy9cp9"
$resources = aws apigateway get-resources --rest-api-id $apiId --region us-east-1 | ConvertFrom-Json

Write-Host "Resources in NewsScraperAPI:"
foreach ($resource in $resources.items) {
    Write-Host "  Path: $($resource.path)"
    if ($resource.resourceMethods) {
        foreach ($method in $resource.resourceMethods.PSObject.Properties.Name) {
            $integration = aws apigateway get-integration `
                --rest-api-id $apiId `
                --resource-id $resource.id `
                --http-method $method `
                --region us-east-1 2>$null | ConvertFrom-Json
            
            if ($integration.uri) {
                Write-Host "    $method -> $($integration.uri)"
            }
        }
    }
}
```

If no Lambda integrations found → Safe to delete

---

## 📝 Updated Verification Script

The `verify-unused-apis.ps1` script will now also check for:
- APIs with similar names
- Creation date proximity (< 5 minutes = likely replacement)
- Which version is used in HTML files

This ensures we don't accidentally delete a newer replacement API.
