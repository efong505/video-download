# Safe Project Reorganization Guide

## Overview

This guide provides a **production-safe** approach to reorganizing your Christian Conservatives Today project with built-in safety mechanisms, verification steps, and easy rollback.

**Timeline:** November 6, 2025 - December 4, 2025 (4 weeks)

---

## Phase 0: Root Directory Cleanup (Week of Nov 6-12, 2025) ✅ COMPLETED

**Time Required:** 2 hours
**Risk Level:** Very Low
**Rollback:** Easy (archive included)
**Status:** ✅ Successfully completed on November 6, 2025

### What Gets Cleaned

**Archived (not deleted):**
- ✅ *.backup, *.backup_* files (50+ files)
- ✅ *-api.zip, *-deployment.zip (30+ files)
- ✅ test-*.html, test-*.json (20+ files)
- ✅ response*.json, payload.json (10+ files)

**Stays in place:**
- ❌ index.html, videos.html, articles.html (working files)
- ❌ auth_api/, articles_api/ folders (Lambda code)
- ❌ deploy-*.ps1 scripts (deployment tools)
- ❌ assets/, docs/, icons/ (active directories)

### Step 1: Dry Run (5 minutes)

```powershell
# Navigate to project root
cd C:\Users\Ed\Documents\Programming\AWS\Downloader

# See what would happen (no changes made)
.\Architecture-Improvements\optional-reorganization\safe-root-cleanup.ps1 -DryRun
```

**Expected Output:**
```
=== Safe Root Directory Cleanup ===

DRY RUN MODE - No changes will be made

[1/5] Analyzing files...
  Backup files: 52
  Old ZIPs: 34
  Test files: 18
  Temp files: 12

[2/5] Would create archive: archive_20251106_143022

[3/5] Creating organized directories...
  Would create: archive
  Would create: tests\integration
  Would create: tests\payloads

[4/5] Cleaning up root directory...
  Would remove 52 backup files
  Would remove 34 old deployment packages
  Would move 18 test files to tests\
  Would move 12 temp files to tests\payloads\

[5/5] Summary
  This was a DRY RUN - no changes were made
  Run without -DryRun to apply changes
```

### Step 2: Run Cleanup (10 minutes)

```powershell
# Execute cleanup (creates archive first)
.\Architecture-Improvements\optional-reorganization\safe-root-cleanup.ps1
```

**Note the archive folder name** displayed in output (e.g., `archive_20251106_143022`). You'll need this for rollback if necessary.

**What Happens:**
1. Creates timestamped archive folder
2. Copies all files to archive (safety net)
3. Creates organized directories
4. Removes/moves files from root
5. Displays summary

### Step 3: Verify Site Works (5 minutes)

```powershell
# Verify site is still functional
.\Architecture-Improvements\optional-reorganization\verify-cleanup.ps1
```

**Expected Output:**
```
Verifying site after cleanup...

✅ https://christianconservativestoday.com - OK
✅ https://christianconservativestoday.com/videos.html - OK
✅ https://christianconservativestoday.com/articles.html - OK
✅ https://christianconservativestoday.com/election-map.html - OK

If all pages show OK, cleanup was successful!
```

### Step 4: Manual Verification (10 minutes)

Visit these pages in your browser:
- https://christianconservativestoday.com
- https://christianconservativestoday.com/videos.html
- https://christianconservativestoday.com/articles.html
- https://christianconservativestoday.com/news.html
- https://christianconservativestoday.com/election-map.html

**All should work exactly as before.**

### Step 5: Rollback (If Needed)

If anything doesn't work:

```powershell
# Find your archive folder
dir archive_*

# Restore from archive (use your actual folder name)
.\Architecture-Improvements\optional-reorganization\rollback-cleanup.ps1 -ArchiveDir archive_20251106_143022
```

**Replace `archive_20251106_143022` with your actual archive folder name.**

The rollback will:
1. Restore all backup files from archive to root
2. Restore all deployment ZIPs from archive to root
3. Restore all test files from archive to root
4. Restore all temp files from archive to root
5. Remove organized directories (tests/, archive/) if empty

After rollback, your directory will be exactly as it was before cleanup.

---

## Phase 1: Create New Structure (Week of Nov 13-19, 2025)

**Time Required:** 2 hours
**Risk Level:** Very Low (just creating directories)

### Step 1: Create Directory Structure

```powershell
# Run structure creation script
.\create-project-structure.ps1
```

**Creates:**
```
src/
├── frontend/
│   ├── public/
│   ├── admin/
│   ├── components/
│   └── assets/
├── backend/
│   ├── shared/
│   ├── api/
│   └── workers/
scripts/
├── deployment/
├── database/
└── election/
docs/
├── architecture/
└── features/
tests/
└── integration/
```

### Step 2: Verify Structure

```powershell
# List new structure
tree src /F
tree scripts /F
```

---

## Phase 2: Move Frontend Files (Week of Nov 20-26, 2025)

**Time Required:** 3 hours
**Risk Level:** Low (files copied, not moved initially)

### Step 1: Copy Files (Safe)

```powershell
# Copy (don't move) frontend files
.\copy-frontend-files.ps1
```

**What Happens:**
- Copies HTML files to src/frontend/
- Copies assets to src/frontend/assets/
- Original files stay in place (safety)

### Step 2: Update S3 Deployment

```powershell
# Update s3-push.ps1 to use new structure
.\update-s3-push.ps1
```

### Step 3: Test Deployment

```powershell
# Deploy from new location
.\scripts\deployment\s3-push.ps1
```

### Step 4: Verify Site Works

Visit site, test all pages. If works, proceed to remove old files.

---

## Phase 3: Reorganize Lambda Functions (Week of Nov 27 - Dec 3, 2025)

**Time Required:** 4 hours
**Risk Level:** Medium (requires Lambda redeployment)

### Step 1: Copy Lambda Code

```powershell
# Copy Lambda functions to new structure
.\copy-lambda-functions.ps1
```

### Step 2: Update Deployment Scripts

```powershell
# Update deploy scripts to use new paths
.\update-deploy-scripts.ps1
```

### Step 3: Test One Lambda

```powershell
# Deploy one Lambda as test
.\scripts\deployment\deploy-lambda.ps1 -FunctionName auth-api
```

### Step 4: Verify Lambda Works

Test the Lambda function. If works, deploy others.

---

## Phase 4: Final Cleanup (Week of Dec 4-10, 2025)

**Time Required:** 2 hours
**Risk Level:** Low (everything already working from new structure)

### Step 1: Remove Old Files

```powershell
# Remove old files (now that new structure works)
.\remove-old-files.ps1
```

### Step 2: Update Documentation

```powershell
# Update README and docs with new structure
.\update-documentation.ps1
```

---

## Rollback Procedures

### Rollback Phase 0 (Root Cleanup)

```powershell
# Find your archive folder name
dir archive_*

# Run rollback with that folder name
.\Architecture-Improvements\optional-reorganization\rollback-cleanup.ps1 -ArchiveDir archive_20251106_143022
```

**This restores all files from the archive back to their original locations.**

### Rollback Phase 2 (Frontend)

```powershell
# Revert s3-push.ps1 to original
git checkout s3-push.ps1

# Deploy from original location
.\s3-push.ps1
```

### Rollback Phase 3 (Lambda)

```powershell
# Revert deploy scripts
git checkout deploy-*.ps1

# Redeploy from original location
.\deploy-all.ps1
```

---

## Safety Checklist

Before each phase:
- [ ] Create backup/archive
- [ ] Run dry-run if available
- [ ] Test in development first
- [ ] Have rollback plan ready
- [ ] Verify site works after changes

---

## Timeline Summary

| Week | Phase | Time | Risk | Status |
|------|-------|------|------|--------|
| Nov 6-12 | Root Cleanup | 2h | Very Low | ✅ COMPLETED |
| Nov 13-19 | Create Structure | 2h | Very Low | ⏭️ Ready |
| Nov 20-26 | Move Frontend | 3h | Low | ⏭️ Ready |
| Nov 27-Dec 3 | Move Lambda | 4h | Medium | ⏭️ Ready |
| Dec 4-10 | Final Cleanup | 2h | Low | ⏭️ Ready |

**Total: 13 hours over 5 weeks**

---

## Success Criteria

✅ All files organized in logical directories
✅ No duplicate files
✅ Site works exactly as before
✅ Deployments work from new structure
✅ Easy to find files
✅ Documentation updated

---

## Getting Started

```powershell
# Navigate to project root (IMPORTANT)
cd C:\Users\Ed\Documents\Programming\AWS\Downloader

# Dry run first
.\Architecture-Improvements\optional-reorganization\safe-root-cleanup.ps1 -DryRun

# Review output, then run for real
.\Architecture-Improvements\optional-reorganization\safe-root-cleanup.ps1

# Note the archive folder name from output!

# Verify site works
.\Architecture-Improvements\optional-reorganization\verify-cleanup.ps1
```

**If all looks good, proceed to Phase 1 next week!**
