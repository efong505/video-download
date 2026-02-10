# Notification System Integrations

## Completed Integrations

### 1. Comment Reply Notifications ✅
**Location:** `comments_api/index.py`

**Trigger:** When a user replies to another user's comment

**Implementation:**
```python
# In create_comment() function after saving comment
if parent_id:
    parent_comment = get_parent_comment(parent_id)
    if parent_comment['author_email'] != current_user_email:
        send_notification(
            type='comment_reply',
            recipient=parent_comment['author_email'],
            subject='New Reply to Your Comment',
            message=f'{author_name} replied to your comment',
            link=f'article.html?id={article_id}#comment-{comment_id}'
        )
```

**Status:** Deployed to `comments-api` Lambda

---

### 2. Prayer Request Answered Notifications ✅
**Location:** `prayer_api/index.py`

**Trigger:** When admin marks prayer request as "answered"

**Implementation:**
```python
# In update_prayer() function when status changes to 'answered'
if status_changed_to_answered:
    prayer = get_prayer(request_id)
    send_notification(
        type='prayer_update',
        recipient=prayer['submitted_by'],
        subject='Prayer Request Answered!',
        message=f'Your prayer "{prayer["title"]}" has been answered',
        link='prayer-wall.html'
    )
```

**Status:** Deployed to `prayer_api` Lambda

---

### 3. Article Publication Notifications 📝
**Location:** Helper script `send_article_notification.py`

**Trigger:** When admin publishes a new article

**Implementation:**
To integrate into admin_api, add this code when publishing articles:

```python
from send_article_notification import notify_article_published

# After article is published
notify_article_published(article_id, article_title)
```

**Status:** Helper script created, needs integration into admin_api

**Manual Integration Steps:**
1. Copy `send_article_notification.py` content into `admin_api/index.py`
2. Call `notify_article_published()` in the publish article function
3. Redeploy admin_api Lambda

---

### 4. Admin Alert Notifications 🚨
**Location:** Helper script `send_admin_alert.py`

**Trigger:** When users submit content that needs moderation

**Implementation:**
```python
from send_admin_alert import notify_admins

# When new content is submitted
notify_admins(
    alert_type='new_comment',  # or 'new_prayer', 'new_video', 'reported_content'
    message='A new comment has been submitted and needs review',
    link='admin.html#comments'
)
```

**Status:** Helper script created, needs integration

**Integration Points:**
- Comments API: When comment is created
- Prayer API: When prayer request is submitted (if moderation enabled)
- Video Upload: When user uploads video
- Content Reports: When user reports content

---

## Testing Notifications

### Test Comment Reply
1. User A posts a comment on an article
2. User B replies to User A's comment
3. User A should receive email notification

### Test Prayer Answered
1. User submits prayer request
2. Admin marks prayer as "answered"
3. User should receive email notification

### Test Article Publication
1. Admin publishes new article
2. All active subscribers should receive email notification

### Test Admin Alert
1. User submits content (comment, prayer, video)
2. All admins should receive email notification

---

## Notification Preferences

Users can manage their notification preferences at:
`notification-settings.html`

Available toggles:
- ✅ Comment Replies
- ✅ Article Published
- ✅ Prayer Updates
- ✅ Event Reminders
- ✅ Admin Alerts (admin only)

---

## API Endpoint

**Notifications API:** `https://lc7w6ebg4m.execute-api.us-east-1.amazonaws.com/prod/notifications`

**Actions:**
- `send_notification` - Send email notification
- `get_user_notifications` - Get user's notification history
- `mark_read` - Mark notification as read
- `get_preferences` - Get user's notification preferences
- `update_preferences` - Update user's notification preferences

---

## Database Tables

### notifications
- `notification_id` (PK) - email#timestamp
- `recipient_email`
- `type` - comment_reply, article_published, prayer_update, event_reminder, admin_alert
- `subject`
- `message`
- `link`
- `read` - Boolean
- `created_at`

### users (notification_preferences field)
```json
{
  "notification_preferences": {
    "comment_reply_email": true,
    "article_published_email": true,
    "prayer_update_email": true,
    "event_reminder_email": true,
    "admin_alert_email": true
  }
}
```

---

## Future Enhancements

- [ ] Event reminder notifications (24 hours before event)
- [ ] Weekly digest emails
- [ ] Push notifications (browser)
- [ ] SMS notifications
- [ ] Notification batching (group multiple notifications)
- [ ] Rich email templates per notification type
- [ ] Notification analytics (open rates, click rates)
