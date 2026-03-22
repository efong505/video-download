# Comments System Integration Guide

## Overview
A complete comments system has been added to ChristianConservativesToday.com with support for:
- ✅ Threaded replies
- ✅ Edit/delete own comments
- ✅ Admin moderation dashboard
- ✅ Real-time updates
- ✅ Character limits (2000 chars)
- ✅ User authentication required
- ✅ Bulk comment management
- ✅ Email notifications for replies

## API Endpoint
**Base URL**: `https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/comments`

## Admin Moderation Dashboard

The admin dashboard (`admin.html`) includes a full Comments tab with:

### Features:
- **View All Comments**: See all comments across articles and videos
- **Statistics**: Total, active, and deleted comment counts
- **Bulk Actions**: 
  - Delete multiple comments at once
  - Restore deleted comments
  - Select all/clear selection
- **Individual Actions**:
  - Delete single comment
  - Restore deleted comment
  - View full comment details
- **Filtering**: Comments show content ID, author, text preview, date, and status

### Access:
Navigate to `admin.html` → Click "Comments" tab

**Requirements**: Admin or Super User role

## Email Notifications

When a user replies to a comment, the original commenter receives an email notification:

### Features:
- Automatic email sent when someone replies to your comment
- Email includes:
  - Name of person who replied
  - Preview of the reply (first 100 characters)
  - Direct link to the comment thread
- No notification if you reply to your own comment
- Async processing (doesn't slow down comment posting)

### Technical Details:
- Uses AWS Lambda `notifications_api` function
- Invoked asynchronously (Event invocation type)
- Graceful failure - comment still posts even if notification fails
- Links format: `https://christianconservativestoday.com/article.html?id={content_id}#comment-{comment_id}`

## How to Add Comments to Any Page

### Step 1: Add CSS and JS to your HTML
```html
<link rel="stylesheet" href="comments.css">
<script src="comments.js"></script>
```

### Step 2: Add Comments Container
```html
<!-- For Articles -->
<div id="comments-section" 
     data-content-id="article-123" 
     data-content-type="article">
</div>

<!-- For Videos -->
<div id="comments-section" 
     data-content-id="video-456" 
     data-content-type="video">
</div>
```

### Step 3: Initialize Comments
```html
<script>
    // Initialize after page load
    document.addEventListener('DOMContentLoaded', function() {
        initComments();
    });
</script>
```

## Example: Adding to articles.html

Add this before the closing `</body>` tag:

```html
<!-- Comments Section -->
<link rel="stylesheet" href="comments.css">
<div id="comments-section" 
     data-content-id="<%= article.article_id %>" 
     data-content-type="article">
</div>
<script src="comments.js"></script>
<script>initComments();</script>
```

## Example: Adding to videos.html

```html
<!-- Comments Section -->
<link rel="stylesheet" href="comments.css">
<div id="comments-section" 
     data-content-id="<%= video.video_id %>" 
     data-content-type="video">
</div>
<script src="comments.js"></script>
<script>initComments();</script>
```

## Features

### For Users:
- Post comments (requires login)
- Reply to comments
- Edit own comments
- Delete own comments
- See comment count
- Real-time character counter

### For Admins:
- Delete any comment
- Moderate comments
- View all comments across site

## API Actions

### Get All Comments (Admin)
```javascript
GET /comments?action=get_all_comments&limit=1000
```

### Moderate Comment (Admin)
```javascript
POST /comments
{
  "action": "moderate_comment",
  "content_id": "article-123",
  "comment_id": "uuid",
  "status": "approved"  // approved | pending | flagged | deleted
}
```

### Get Comments
```javascript
GET /comments?action=get_comments&content_id=article-123
```

### Add Comment
```javascript
POST /comments
{
  "action": "add_comment",
  "content_id": "article-123",
  "content_type": "article",
  "user_email": "user@example.com",
  "user_name": "John Doe",
  "comment_text": "Great article!",
  "parent_comment_id": null  // Optional, for replies
}
```

### Delete Comment
```javascript
POST /comments
{
  "action": "delete_comment",
  "content_id": "article-123",
  "comment_id": "uuid",
  "user_email": "user@example.com",
  "is_admin": false
}
```

### Update Comment
```javascript
POST /comments
{
  "action": "update_comment",
  "content_id": "article-123",
  "comment_id": "uuid",
  "user_email": "user@example.com",
  "comment_text": "Updated comment text"
}
```

## DynamoDB Table Structure

**Table**: `content-comments`

**Keys**:
- Partition Key: `content_id` (String)
- Sort Key: `comment_id` (String)

**Attributes**:
- `content_type`: article | video
- `user_email`: Commenter's email
- `user_name`: Display name
- `comment_text`: Comment content (max 2000 chars)
- `created_at`: Unix timestamp
- `created_at_iso`: ISO date string
- `status`: approved | pending | flagged | deleted
- `parent_comment_id`: For threaded replies
- `likes`: Number of likes (future feature)
- `replies_count`: Number of replies
- `edited`: Boolean
- `edited_at`: ISO date string

## Styling

The comments system uses Bootstrap 5 classes and custom CSS. You can customize colors by modifying `comments.css`:

```css
.comments-title {
    color: #2c5aa0;  /* Change primary color */
}

.comment-author {
    color: #2c5aa0;  /* Change author name color */
}
```

## Security

- ✅ Users must be logged in to comment
- ✅ Users can only edit/delete their own comments
- ✅ Admins can moderate any comment
- ✅ XSS protection via HTML escaping
- ✅ Character limits enforced
- ✅ Soft delete (comments marked as deleted, not removed)

## Next Steps

1. ✅ Add comments to `articles.html` (article detail page)
2. ✅ Add comments to `videos.html` (video detail page)  
3. ✅ Create admin moderation dashboard
4. ✅ Add email notifications for replies
5. ☐ Add like/upvote functionality
6. ☐ Move to Phase 2: Content & Growth features

## Recent Updates (March 2026)

### Email Notifications Added
- Implemented reply notifications using notifications_api Lambda
- Async invocation to avoid slowing down comment posting
- Includes reply preview and direct link to comment
- Graceful failure handling

### Admin Dashboard Integration
- Fixed API endpoint mismatch between `comments_api` and `comments-handler`
- Updated admin.html to use correct action: `get_all_comments` instead of `admin_list`
- Fixed field name mappings: `comment_text`, `content_id`, `user_name`, `status`
- Resolved quote escaping issues in View button using event listeners
- Added comprehensive logging for debugging
- Bulk delete and restore now working correctly

## Deployment

To deploy the comments handler with email notifications:

```powershell
.\deploy-comments-handler.ps1
```

Or manually:
```bash
cd comments-handler
zip lambda.zip lambda_function.py
aws lambda update-function-code --function-name comments-handler --zip-file fileb://lambda.zip --region us-east-1
```

## Testing

Test the comments system at:
- Any article page with comments enabled
- Any video page with comments enabled

**API Endpoint**: https://gu6c08ctel.execute-api.us-east-1.amazonaws.com/prod/comments

All deployed and ready to use! 🎉
