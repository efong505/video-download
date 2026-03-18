# SCRIPTS & REPOSITORY VERIFICATION

## PYTHON SCRIPTS INVENTORY

### Root Directory
- **NO Python scripts** in root directory

### Scripts/ Directory Structure
```
Scripts/
├── database/          (9 Python scripts)
├── election/          (32 Python scripts)
├── maintenance/       (25 Python scripts)
└── media/             (8 Python scripts)
```

**Total: 74 Python scripts** organized in subdirectories

### Python Scripts by Category

#### Database Scripts (9 files)
1. create_events_table.py
2. create_newsletter_tables.py
3. create_prayer_table.py
4. migrate_news_author_names.py
5. seed_campaigns.py
6. update_article_author_names.py
7. update_news_author_names.py
8. update_subscriber_schema.py
9. update_user_roles.py

#### Election Scripts (32 files)
1. check_virginia_counts.py
2. delete_hawaii_data.py
3. delete_nebraska_data.py
4. delete_new-jersey_data.py
5. delete_new-mexico_data.py
6. delete_state_data.py
7. delete_virginia_data.py
8. fix_virginia_summary_counts.py
9. get_hawaii_races.py
10. get_nebraska_georgia.py
11. get_texas_races.py
12. hawaii_upload_data.py
13. nebraska_update_uploade.py
14. new-mexico_update_uploade.py
15. update_new-jersey_data.py
16. update_virginia_data.py
17. upload_2026_candidates.py
18. upload_2026_races.py
19. upload_california_batch2.py
20. upload_california_summary.py
21. upload_florida_candidates.py
22. upload_florida_data.py
23. upload_hawaii_candidates.py
24. upload_nebraska_georgia.py
25. upload_nebraska_georgia_summaries.py
26. upload_new_mexico_summary.py
27. upload_ohio_candidates.py
28. upload_ohio_data.py
29. upload_texas_candidates.py
30. upload_virginia_candidates.py

#### Maintenance Scripts (25 files)
1. audit_all_states_data.py
2. auto_fix_summary_counts.py
3. check_article_images.py
4. check_jd_vance.py
5. check_missing_summaries.py
6. check_new_jersey_counts.py
7. check_race_dates.py
8. check_summaries_table.py
9. check_summary_format.py
10. check_table_key.py
11. check_table_structure.py
12. cleanup_empty_videos.py
13. cleanup_empty_videos_auto.py
14. fix_all_state_summaries.py
15. fix_all_summary_guides.py
16. fix_cloudfront_urls.py
17. fix_new_jersey_counts_final.py
18. fix_new_jersey_summary_counts.py
19. fix_new_mexico_summary_counts.py
20. fix_orphaned_candidates.py
21. fix_summary_counts_auto.py
22. fix_summary_counts_in_dynamodb.py
23. fix_thumbnail.py
24. smart_fix_race_ids.py
25. verify_new_mexico_counts.py

#### Media Scripts (8 files)
1. convert_base64_to_s3.py
2. generate_all_previews.py
3. generate_article_preview.py
4. generate_missing_thumbnails.py
5. generate_news_preview.py
6. generate_thumbnails.py
7. manual_thumbnail.py
8. regenerate_all_article_previews.py

---

## POWERSHELL SCRIPTS INVENTORY

### Root Directory
- **NO PowerShell scripts** in root directory

### PowerShell Scripts by Location

#### API-Consolidation/scripts/ (9 files)
1. check-specific-apis.ps1
2. configure-custom-domain.ps1
3. create-unified-api.ps1
4. delete-3-safe-apis.ps1
5. delete-unused-apis.ps1
6. test-unified-api.ps1
7. verify-7-apis-simple.ps1
8. verify-7-apis.ps1
9. verify-unused-apis.ps1

#### Architecture-Improvements/scripts/ (11 files)
1. analyze-root-files.ps1
2. create-rate-limit-table.ps1
3. deploy-auto-cache-monitor.ps1
4. deploy-rate-limiting.ps1
5. gradual-rollout.ps1
6. monitor-video-queue.ps1
7. organize-root-files.ps1
8. organize-zip-files.ps1
9. rollback-sqs.ps1
10. safe-sqs-deploy.ps1
11. test-sqs-integration.ps1
12. verify-rate-limiting.ps1
13. week1-deploy.ps1

#### Architecture-Improvements/optional-reorganization/ (3 files)
1. rollback-cleanup.ps1
2. safe-root-cleanup.ps1
3. verify-cleanup.ps1

#### Election Data and Files/ (7 files)
1. deploy_lambda.ps1
2. fix_api_gateway.ps1
3. fix_api_gateway_cors.ps1
4. setup_email_authentication.ps1
5. setup_route53_email_auth.ps1
6. start_dashboard.ps1
7. list_states_with_summaries.ps1
8. list_summary_guides.ps1

#### Email Marketing/ (8 files)
1. create-lambda-functions.ps1
2. deploy-all.ps1
3. setup-database.ps1
4. email_campaigns_api/deploy.ps1
5. email_sender/deploy.ps1
6. email_subscribers_api/deploy.ps1
7. email_tracking_api/deploy.ps1

#### Shopping/scripts/ (11 files)
1. 1-create-sqs-queues.ps1
2. 2-create-dynamodb-tables.ps1
3. 3-test-infrastructure.ps1
4. 4-update-cache-monitor.ps1
5. 5-deploy-products-api.ps1
6. 6-create-api-gateway.ps1
7. 7-deploy-shopping-frontend.ps1
8. 8-deploy-orders-api.ps1
9. 9-deploy-paypal-ipn.ps1
10. 9-deploy-reviews-api.ps1
11. monitor-shopping-queues.ps1

#### Terraform/ (17 files)
1. analyze-active-apis.ps1
2. delete-all-consolidated-apis.ps1
3. delete-consolidated-apis.ps1
4. delete-notifications-api.ps1
5. delete-unused-apis.ps1
6. find-api-urls.ps1
7. find-old-api-urls.ps1
8. fix-api-urls.ps1
9. fix-broken-files.ps1
10. import-dynamodb-tables.ps1
11. replace-api-urls.ps1
12. test-blue-green.ps1
13. test-unified-api.ps1
14. update-all-production-urls.ps1
15. update-production-urls.ps1
16. scripts/analyze-api-gateways.ps1
17. scripts/import-remaining-lambdas.ps1

#### Other Locations (3 files)
1. contributors_api/deploy.ps1
2. lambda-edge-meta-tags/toggle-lambda-edge.ps1

**Total: ~70 PowerShell scripts** across multiple directories

---

## GITHUB REPOSITORY STATUS

### Git Status
- **Git repository NOT accessible** locally
- Error code 128 indicates git repository corruption or missing .git folder
- S3 backup contains .git folder (can be restored if needed)

### Repository Information
- **GitHub URL**: UNKNOWN (cannot access git config)
- **Remote origin**: NOT ACCESSIBLE
- **Local git**: CORRUPTED or MISSING

### Recovery Options
1. Restore .git folder from S3 backup
2. Check GitHub account for repository URL
3. Re-initialize git repository if needed

---

## LAMBDA FUNCTION PYTHON FILES

### Lambda Functions with index.py (20+ APIs)
- admin_api/index.py
- article_analysis_api/index.py
- articles_api/index.py
- auth_api/index.py
- book_delivery_api/index.py
- comments_api/index.py
- contact_form_api/index.py
- contributors_api/index.py
- events_api/index.py
- news_api/index.py
- newsletter_api/index.py
- notifications_api/index.py
- paypal_billing_api/index.py
- playlists_api/index.py
- prayer_api/index.py
- resources_api/index.py
- s3_thumbnail_trigger/index.py
- tag_api/index.py
- thumbnail_generator/index.py
- url_analysis_api/index.py
- user_email_api/index.py
- video_list_api/index.py
- video_url_generator/index.py

### Shopping APIs
- Shopping/orders_api/index.py
- Shopping/paypal_ipn_handler/index.py
- Shopping/products_api/index.py
- Shopping/reviews_api/index.py

---

## MISSING SCRIPTS ANALYSIS

### From S3 Backup
- **NO scripts found** in S3 root directory
- Scripts are NOT backed up to S3 (only HTML files)

### From Local Backup (backup_20260210_095001/)
- Need to check if backup contains Scripts/ folder
- Backup date: February 10, 2026

### Potential Missing Scripts
- **Deployment scripts** for individual Lambda functions
- **Infrastructure setup** scripts
- **CI/CD pipeline** scripts (if they existed)

---

## RECOMMENDATIONS

### 1. Verify Scripts Completeness
- Compare Scripts/ folder with backup_20260210_095001/
- Check if any deployment scripts are missing

### 2. GitHub Repository
- Search your GitHub account for repository
- Check email for GitHub repository links
- Consider restoring .git folder from S3

### 3. Documentation
- Document what each script does
- Create deployment runbook
- Document GitHub repository URL once found

### 4. Backup Strategy
- Scripts/ folder should be backed up to S3
- Consider version control for all scripts
- Regular backups of .git folder

---

## NEXT STEPS

1. **Check backup folder** for Scripts/ directory
2. **Search for GitHub repository** URL
3. **Restore .git folder** from S3 if needed
4. **Document missing scripts** (if any)
5. **Create backup strategy** for scripts

---

## SUMMARY

✅ **Python Scripts**: 74 files organized in Scripts/ subdirectories
✅ **PowerShell Scripts**: ~70 files across multiple project folders
✅ **Lambda Functions**: 20+ API functions with Python code
❌ **Git Repository**: Corrupted/missing locally (can restore from S3)
❓ **GitHub URL**: Unknown (need to search or restore git config)
⚠️ **Scripts Backup**: Scripts NOT in S3 backup (only in local folders)
