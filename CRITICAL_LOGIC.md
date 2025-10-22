# Critical Business Logic - DO NOT REMOVE

This document tracks critical business logic that must be preserved across refactors and updates.

## Admin/Super User Unlimited Access

**Files Affected:**
- `profile.html` (lines ~390-430)
- `user-upload.html` (quota checking logic)

**Logic:**
Users with `role === 'admin'` or `role === 'super_user'` must have:
- Unlimited storage (`storage_limit: -1`)
- Unlimited videos (`video_limit: -1`)
- Subscription tier displayed as "Admin (Unlimited)"
- No upgrade prompts shown

**Implementation in profile.html:**
```javascript
// CRITICAL: Admin/Super User Unlimited Access Logic
if (currentUser.role === 'admin' || currentUser.role === 'super_user') {
    // Fetch actual usage but set limits to unlimited (-1)
    subscriptionData = {
        subscription_tier: 'admin',
        subscription_status: 'active',
        storage_used: usageData.storage_used || 0,
        storage_limit: -1,  // Unlimited
        video_count: usageData.video_count || 0,
        video_limit: -1,    // Unlimited
        storage_percentage: 0,
        video_percentage: 0
    };
}
```

**Why This Exists:**
- Admins need to test and manage the platform without restrictions
- Super users are platform owners and should never hit limits
- This was accidentally removed in commit 52f7bff and had to be restored

**Testing:**
1. Log in as admin user
2. Go to profile page
3. Verify "Admin (Unlimited)" is displayed
4. Verify actual storage/video counts show with "Unlimited" limits
5. Verify no upgrade section is visible

---

## External Video Thumbnail Generation

**Files Affected:**
- `thumbnail_generator/index.py`
- `admin_api/index.py`
- `admin.html`
- `user-upload.html`

**Logic:**
When external videos (YouTube, Rumble, Facebook) are added:
1. Frontend calls `generate_thumbnail` API with `video_type` and `external_url`
2. Admin API passes these parameters to thumbnail-generator Lambda
3. Thumbnail generator fetches thumbnail from platform API (e.g., YouTube: `https://img.youtube.com/vi/{video_id}/maxresdefault.jpg`)
4. Thumbnail saved to S3 at `thumbnails/{video_id}_thumb_2.jpg`

**Why This Exists:**
- External videos don't trigger S3 upload events (no file uploaded)
- Thumbnails must be fetched from external platform APIs
- Without this, external videos show no thumbnails

**Testing:**
1. Add external YouTube video via admin dashboard
2. Check S3 bucket for thumbnail at `thumbnails/{video_id}_thumb_2.jpg`
3. Verify thumbnail displays in video gallery

---

## Two Separate Video Workflows

**Workflow 1: Download from URL**
- Downloads actual video file using yt-dlp
- Stores in S3 `videos/` folder
- Generates thumbnails using FFmpeg from downloaded file
- Handled by: `downloader/index.py`

**Workflow 2: Add External Video**
- Saves only the URL (no download)
- Stores metadata in DynamoDB
- Fetches thumbnails from platform APIs
- Handled by: `tag_api/index.py`, `thumbnail_generator/index.py`

**Why Both Exist:**
- Workflow 1: For archiving/hosting videos permanently
- Workflow 2: For embedding external videos without storage costs

**DO NOT:**
- Merge these workflows
- Remove either workflow
- Assume one replaces the other

---

## Update History

- **2025-10-22**: Restored admin unlimited access logic (was accidentally removed)
- **2025-10-22**: Fixed external video thumbnail generation
- **2025-10-22**: Created this documentation file
