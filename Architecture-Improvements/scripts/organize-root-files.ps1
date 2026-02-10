# organize-root-files.ps1 - Safely organize Python files from root

param(
    [switch]$DryRun
)

$rootPath = "C:\Users\Ed\Documents\Programming\AWS\Downloader"
Set-Location $rootPath

Write-Host "=== Organize Root Python Files ===" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No files will be moved" -ForegroundColor Yellow
    Write-Host ""
}

# Create target directories
$directories = @(
    "Scripts\election",
    "Scripts\database",
    "Scripts\maintenance",
    "Scripts\media",
    "archive\development"
)

Write-Host "[1/6] Creating directories..." -ForegroundColor Green
foreach ($dir in $directories) {
    if ($DryRun) {
        Write-Host "  Would create: $dir" -ForegroundColor Yellow
    } else {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Host "  ✅ Created: $dir" -ForegroundColor White
        } else {
            Write-Host "  ⏭️  Exists: $dir" -ForegroundColor Gray
        }
    }
}
Write-Host ""

# Election Data Management files
$electionFiles = @(
    "check_virginia_counts.py", "delete_hawaii_data.py", "delete_nebraska_data.py",
    "delete_new-jersey_data.py", "delete_new-mexico_data.py", "delete_state_data.py",
    "delete_virginia_data.py", "fix_virginia_summary_counts.py", "get_hawaii_races.py",
    "get_nebraska_georgia.py", "get_texas_races.py", "hawaii_upload_data.py",
    "nebraska_update_uploade.py", "new-mexico_update_uploade.py", "update_new-jersey_data.py",
    "update_virginia_data.py", "upload_2026_candidates.py", "upload_2026_races.py",
    "upload_california_batch2.py", "upload_california_summary.py", "upload_florida_candidates.py",
    "upload_florida_data.py", "upload_hawaii_candidates.py", "upload_nebraska_georgia.py",
    "upload_nebraska_georgia_summaries.py", "upload_new_mexico_summary.py", "upload_ohio_candidates.py",
    "upload_ohio_data.py", "upload_texas_candidates.py", "upload_virginia_candidates.py"
)

Write-Host "[2/6] Moving election data files..." -ForegroundColor Green
foreach ($file in $electionFiles) {
    if (Test-Path $file) {
        if ($DryRun) {
            Write-Host "  Would move: $file -> Scripts\election\" -ForegroundColor Yellow
        } else {
            Move-Item $file "Scripts\election\" -Force
            Write-Host "  ✅ Moved: $file" -ForegroundColor White
        }
    }
}
Write-Host ""

# Database Utilities
$dbFiles = @(
    "create_events_table.py", "create_newsletter_tables.py", "create_prayer_table.py",
    "migrate_news_author_names.py", "seed_campaigns.py", "update_article_author_names.py",
    "update_news_author_names.py", "update_subscriber_schema.py", "update_user_roles.py"
)

Write-Host "[3/6] Moving database utility files..." -ForegroundColor Green
foreach ($file in $dbFiles) {
    if (Test-Path $file) {
        if ($DryRun) {
            Write-Host "  Would move: $file -> Scripts\database\" -ForegroundColor Yellow
        } else {
            Move-Item $file "Scripts\database\" -Force
            Write-Host "  ✅ Moved: $file" -ForegroundColor White
        }
    }
}
Write-Host ""

# One-Time Fixes
$fixFiles = @(
    "audit_all_states_data.py", "auto_fix_summary_counts.py", "check_article_images.py",
    "check_jd_vance.py", "check_missing_summaries.py", "check_new_jersey_counts.py",
    "check_race_dates.py", "check_summaries_table.py", "check_summary_format.py",
    "check_table_key.py", "check_table_structure.py", "fix_all_state_summaries.py",
    "fix_all_summary_guides.py", "fix_cloudfront_urls.py", "fix_new_jersey_counts_final.py",
    "fix_new_jersey_summary_counts.py", "fix_new_mexico_summary_counts.py", "fix_orphaned_candidates.py",
    "fix_summary_counts_auto.py", "fix_summary_counts_in_dynamodb.py", "fix_thumbnail.py",
    "smart_fix_race_ids.py", "verify_new_mexico_counts.py"
)

Write-Host "[4/6] Moving one-time fix files..." -ForegroundColor Green
foreach ($file in $fixFiles) {
    if (Test-Path $file) {
        if ($DryRun) {
            Write-Host "  Would move: $file -> Scripts\maintenance\" -ForegroundColor Yellow
        } else {
            Move-Item $file "Scripts\maintenance\" -Force
            Write-Host "  ✅ Moved: $file" -ForegroundColor White
        }
    }
}
Write-Host ""

# Image/Video Processing
$mediaFiles = @(
    "convert_base64_to_s3.py", "generate_all_previews.py", "generate_article_preview.py",
    "generate_missing_thumbnails.py", "generate_news_preview.py", "generate_thumbnails.py",
    "manual_thumbnail.py", "regenerate_all_article_previews.py"
)

Write-Host "[5/6] Moving media processing files..." -ForegroundColor Green
foreach ($file in $mediaFiles) {
    if (Test-Path $file) {
        if ($DryRun) {
            Write-Host "  Would move: $file -> Scripts\media\" -ForegroundColor Yellow
        } else {
            Move-Item $file "Scripts\media\" -Force
            Write-Host "  ✅ Moved: $file" -ForegroundColor White
        }
    }
}
Write-Host ""

# Development/Testing (archive)
$devFiles = @(
    "fargate_downloader.py", "find_video_url.py"
)

Write-Host "[6/6] Archiving development files..." -ForegroundColor Green
foreach ($file in $devFiles) {
    if (Test-Path $file) {
        if ($DryRun) {
            Write-Host "  Would archive: $file -> archive\development\" -ForegroundColor Yellow
        } else {
            Move-Item $file "archive\development\" -Force
            Write-Host "  ✅ Archived: $file" -ForegroundColor White
        }
    }
}
Write-Host ""

# Summary
Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "This was a DRY RUN - no files were moved" -ForegroundColor Yellow
    Write-Host "Run without -DryRun to organize files" -ForegroundColor Yellow
} else {
    Write-Host "✅ Files organized successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Remaining in root (active utilities):" -ForegroundColor White
    Get-ChildItem *.py -File | ForEach-Object {
        Write-Host "  - $($_.Name)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "1. Verify site still works" -ForegroundColor Gray
Write-Host "2. Update any scripts that reference moved files" -ForegroundColor Gray
Write-Host "3. Proceed with SQS deployment" -ForegroundColor Gray
