# File Recovery Analysis - Downloader Directory

## CRITICAL FINDING
**ALL HTML files are missing from the local Downloader directory root!**

## S3 Live Files vs Local Backup Comparison

### Files on S3 (Live) - Last Modified Dates

#### Recently Updated (2026-02-10 or later):
- admin-book-subscribers.html (2026-02-10 12:06:54)
- admin-contributors.html (2026-02-10 12:06:18)
- admin-resources.html (2026-02-10 12:06:19)
- admin-templates.html (2026-02-10 12:06:21)
- admin.html (2026-02-10 12:33:25)
- article.html (2026-02-19 09:10:04) ⚠️ NEWER than backup
- articles.html (2026-02-10 12:06:25)
- authors.html (2026-02-10 12:06:56)
- category.html (2026-02-10 12:06:58)
- create-article-from-aws.html (2026-02-10 12:06:59)
- create-article-v2.html (2026-02-10 12:07:01)
- create-article.html (2026-02-13 10:59:14) ⚠️ NEWER than backup
- create-news.html (2026-02-10 12:59:30) ⚠️ NOT in backup
- debug-videos.html (2026-02-10 12:07:02)
- download-status.html (2026-02-10 12:33:17)
- edit-article.html (2026-02-10 12:06:35)
- edit-news.html (2026-02-27 21:04:28) ⚠️ MUCH NEWER than backup
- embed.html (2026-02-10 12:07:04)
- find-duplicates.html (2026-02-10 12:07:05)
- login.html (2026-02-10 12:07:06)
- news-article.html (2026-02-27 23:08:45) ⚠️ MUCH NEWER than backup
- news.html (2026-02-10 12:06:44)
- notification-settings.html (2026-02-10 13:23:48)
- playlists.html (2026-02-10 12:07:09)
- reset-subscription.html (2026-02-10 12:07:10)
- resources.html (2026-02-10 12:07:12)
- user-page.html (2026-02-10 12:07:13)
- user-upload.html (2026-02-10 12:07:15)
- video-analytics.html (2026-02-10 13:38:53) ⚠️ NOT in backup
- videos.html (2026-02-10 12:07:16)

#### User Email Campaign Files (NEW - March 2026):
- user-email-campaign-create.html (2026-03-15 13:03:23) ⚠️ NOT in backup
- user-email-dashboard.html (2026-03-15 13:03:22) ⚠️ NOT in backup
- user-email-subscribers.html (2026-03-15 15:43:10) ⚠️ NOT in backup

#### Book Related (Updated):
- book.html (2026-01-27 10:57:03) ⚠️ NOT in backup
- the-necessary-evil-book.html (2026-03-13 14:46:19) ⚠️ MUCH NEWER than backup
- thank-you-digital.html (2026-02-18 14:16:46) ⚠️ NOT in backup
- thank-you-paperback.html (2026-02-18 14:16:45) ⚠️ NOT in backup

#### Test/Order Files (NEW):
- test-confirmation-emails.html (2026-02-18 07:46:35) ⚠️ NOT in backup
- test-order-flow.html (2026-02-18 08:11:36) ⚠️ NOT in backup
- test-shopping-order-sns.html (2026-02-18 07:43:06) ⚠️ NOT in backup

### Files in Backup (2026-02-10) NOT on S3:
- admin-newsletters-new.html
- admin-products.html
- cart.html
- events-calendar-enhanced.html
- product.html
- shop.html
- test-article-lookup.html
- test-articles-api.html
- test-bible-lookup.html
- test-products.html
- test-rumble.html
- the-necessary-evil-book-original.html

## RECOVERY PLAN

### Phase 1: Import ALL HTML files from S3 (PRIMARY SOURCE)
These are the live production files and should be imported:
- All 60+ HTML files from S3 root directory

### Phase 2: Check GitHub for Scripts/Config Files
Need to verify GitHub has:
- PowerShell scripts (.ps1)
- Python scripts (.py)
- Configuration files
- Documentation files

### Phase 3: Restore from Backup (SELECTIVE)
Only restore from backup if:
- File doesn't exist on S3
- File is needed for development (test files, etc.)

## FILES DEFINITELY MISSING (Need from S3):
1. create-news.html (NEW - not in backup)
2. video-analytics.html (NEW - not in backup)
3. user-email-campaign-create.html (NEW - not in backup)
4. user-email-dashboard.html (NEW - not in backup)
5. user-email-subscribers.html (NEW - not in backup)
6. book.html (NEW - not in backup)
7. thank-you-digital.html (NEW - not in backup)
8. thank-you-paperback.html (NEW - not in backup)
9. test-confirmation-emails.html (NEW - not in backup)
10. test-order-flow.html (NEW - not in backup)
11. test-shopping-order-sns.html (NEW - not in backup)

## FILES WITH NEWER VERSIONS ON S3:
1. article.html (S3: 2026-02-19 vs Backup: 2026-02-10)
2. create-article.html (S3: 2026-02-13 vs Backup: 2026-02-10)
3. edit-news.html (S3: 2026-02-27 vs Backup: 2026-02-10)
4. news-article.html (S3: 2026-02-27 vs Backup: 2026-02-10)
5. the-necessary-evil-book.html (S3: 2026-03-13 vs Backup: 2026-02-03)

## RECOMMENDATION:
**Import ALL HTML files from S3 as they are the most current production versions.**

Backup folder is from 2026-02-10, but S3 has updates through 2026-03-15.
