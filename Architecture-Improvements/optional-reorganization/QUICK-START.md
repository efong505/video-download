# Quick Start - Safe Root Cleanup

## 5-Minute Quick Start

```powershell
# Navigate to project root (NOT the optional-reorganization folder)
cd C:\Users\Ed\Documents\Programming\AWS\Downloader

# Step 1: See what would happen (no changes)
.\Architecture-Improvements\optional-reorganization\safe-root-cleanup.ps1 -DryRun

# Step 2: Run for real (creates archive)
.\Architecture-Improvements\optional-reorganization\safe-root-cleanup.ps1

# Step 3: Verify site works
.\Architecture-Improvements\optional-reorganization\verify-cleanup.ps1

# Step 4: If issues, rollback (use your actual archive folder name)
.\Architecture-Improvements\optional-reorganization\rollback-cleanup.ps1 -ArchiveDir archive_20251106_143022
```

**IMPORTANT:** Run from `Downloader\` root, not from `optional-reorganization\` folder.

## What This Does

**Cleans up:**
- ✅ 50+ backup files (*.backup, *.backup_*)
- ✅ 30+ old deployment packages (*-api.zip)
- ✅ 20+ test files (test-*.html, test-*.json)
- ✅ 10+ temp files (response*.json, payload.json)

**Keeps safe:**
- ❌ Working HTML files (index.html, videos.html, etc.)
- ❌ Lambda code folders (auth_api/, articles_api/, etc.)
- ❌ Deployment scripts (deploy-*.ps1)
- ❌ Active directories (assets/, docs/, icons/)

## Safety Features

1. **Archive Created** - All files backed up before removal
2. **Dry Run Mode** - Test before making changes
3. **Verification Script** - Confirm site still works
4. **Easy Rollback** - One command to undo everything

## Expected Results

**Before:**
```
Downloader/
├── index.html
├── videos.html
├── index.html.backup
├── videos.html.backup_20251024
├── admin-api.zip
├── articles-api-fixed.zip
├── test-video.html
├── test-payload.json
└── ... (200+ files)
```

**After:**
```
Downloader/
├── index.html
├── videos.html
├── archive_20251106_143022/  (all backups here)
│   ├── backups/
│   ├── old-deployments/
│   └── test-files/
└── tests/
    ├── integration/  (test files moved here)
    └── payloads/     (temp files moved here)
```

## Timeline

- **Dry Run:** 2 minutes
- **Actual Cleanup:** 5 minutes
- **Verification:** 3 minutes
- **Total:** 10 minutes

## Risk Level

**Very Low** - This only cleans up backup and test files. Your working site files are not touched.

## When to Use

✅ **Use this if:**
- First time cleaning up
- Working on production system
- Want maximum safety
- Need easy rollback

❌ **Skip this if:**
- Very experienced with codebase
- Development environment only
- Don't need archive

## Next Steps

After successful cleanup:
1. Keep archive for 30 days
2. Proceed to Phase 1 (Create New Structure)
3. See SAFE-REORGANIZATION-GUIDE.md for full plan

## Rollback Instructions

If anything goes wrong after cleanup:

```powershell
# 1. Find your archive folder name
dir archive_*

# 2. Run rollback with that folder name
.\Architecture-Improvements\optional-reorganization\rollback-cleanup.ps1 -ArchiveDir archive_20251106_143022
```

The rollback will:
- Restore all backup files to root
- Restore all deployment ZIPs to root
- Restore all test files to root
- Restore all temp files to root
- Remove organized directories if empty

## Troubleshooting

**Q: Dry run shows 0 files?**
A: Make sure you're in `Downloader\` root, not `optional-reorganization\` folder.

**Q: Site doesn't work after cleanup?**
A: Run rollback immediately with your archive folder name.

**Q: Can I delete the archive?**
A: Wait 30 days to ensure everything works, then yes.

**Q: What if I want to skip the archive?**
A: Run with `-SkipArchive` flag (not recommended for first time).

## Support

If you encounter issues:
1. Run rollback script
2. Check archive folder exists
3. Verify site works before proceeding
4. Review SAFE-REORGANIZATION-GUIDE.md

---

**Ready? Start with the dry run!**

```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader
.\Architecture-Improvements\optional-reorganization\safe-root-cleanup.ps1 -DryRun
```
