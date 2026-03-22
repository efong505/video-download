# Comments System Integration Guide

## Overview
A complete comments system has been added to ChristianConservativesToday.com with support for:
- ✅ Threaded replies
- ✅ Edit/delete own comments
- ✅ Admin moderation
- ✅ Real-time updates
- ✅ Character limits (2000 chars)
- ✅ User authentication required

## API Endpoint
**Base URL**: `https://gu6c08ctel.execute-api.us-east-1.amazonaws.com/prod/comments`

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

1. Add comments to `articles.html` (article detail page)
2. Add comments to `videos.html` (video detail page)
3. Create admin moderation dashboard
4. Add email notifications for replies
5. Add like/upvote functionality

## Testing

Test the comments system at:
- Any article page with comments enabled
- Any video page with comments enabled

**API Endpoint**: https://gu6c08ctel.execute-api.us-east-1.amazonaws.com/prod/comments

All deployed and ready to use! 🎉
