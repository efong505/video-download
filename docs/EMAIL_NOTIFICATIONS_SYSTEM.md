# Email Notifications System

## Overview
Automated email notification system for user engagement and admin alerts. Built on existing SES infrastructure with user preference management.

## Features

### Notification Types
1. **Comment Replies** - User gets notified when someone replies to their comment
2. **Article Published** - Notify users when new articles are published
3. **Prayer Updates** - Notify when prayer requests are answered or updated
4. **Event Reminders** - Notify about upcoming events
5. **Admin Alerts** - Notify admins about new submissions, reports, or moderation needs

### User Preferences
- Toggle each notification type on/off
- Preferences stored in users table
- Respects opt-out choices
- Settings page: `notification-settings.html`

### Notification Storage
- All notifications stored in DynamoDB
- Users can view notification history
- Mark notifications as read
- Link to relevant content

## Technical Implementation

### DynamoDB Table: notifications
```
notification_id (String, Primary Key) - email#timestamp
recipient_email (String)
type (String) - comment_reply, article_published, prayer_update, event_reminder, admin_alert
subject (String)
message (String)
link (String) - URL to relevant content
read (Boolean)
created_at (String)
```

### Lambda Function: notifications_api
**Actions:**
- `send_notification` - Send email and store notification
- `get_user_notifications` - Get user's notifications
- `mark_read` - Mark notification as read
- `get_preferences` - Get user's notification preferences
- `update_preferences` - Update user's notification preferences

### Email Template
- Professional branded design
- Purple gradient header
- Clear call-to-action button
- Responsive layout

## Integration Points

### Comments System
When user replies to comment:
```javascript
fetch(NOTIFICATIONS_API, {
    method: 'POST',
    body: JSON.stringify({
        action: 'send_notification',
        type: 'comment_reply',
        recipient_email: originalCommentAuthor,
        subject: 'New Reply to Your Comment',
        message: `${replyAuthor} replied to your comment on "${articleTitle}"`,
        link: `https://christianconservativestoday.com/article.html?id=${articleId}#comment-${commentId}`
    })
});
```

### Article Publishing
When admin publishes article:
```javascript
// Get all users with article_published_email enabled
// Send notification to each
```

### Prayer Wall
When prayer is answered:
```javascript
fetch(NOTIFICATIONS_API, {
    method: 'POST',
    body: JSON.stringify({
        action: 'send_notification',
        type: 'prayer_update',
        recipient_email: prayerAuthor,
        subject: 'Prayer Request Update',
        message: `Your prayer request has been marked as answered!`,
        link: `https://christianconservativestoday.com/prayer-wall.html`
    })
});
```

### Admin Alerts
When user submits content:
```javascript
// Get all admins
// Send notification to each admin
```

## Deployment

### Create DynamoDB Table
```bash
aws dynamodb create-table \
  --table-name notifications \
  --attribute-definitions AttributeName=notification_id,AttributeType=S \
  --key-schema AttributeName=notification_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

### Deploy Lambda Function
```bash
cd notifications_api
tar -a -c -f ../notifications_api.zip index.py
cd ..
aws lambda create-function \
  --function-name notifications_api \
  --runtime python3.12 \
  --role arn:aws:iam::ACCOUNT_ID:role/lambda-execution-role \
  --handler index.lambda_handler \
  --zip-file fileb://notifications_api.zip \
  --timeout 30 \
  --memory-size 256
```

### Create API Gateway Endpoint
1. Create REST API
2. Create resource `/notifications`
3. Create methods: GET, POST, OPTIONS
4. Enable CORS
5. Deploy to prod stage
6. Update `notification-settings.html` with API URL

### Upload Frontend
```bash
aws s3 cp notification-settings.html s3://my-video-downloads-bucket/
```

## Usage

### User Settings
Users access `notification-settings.html` to:
- Toggle notification types
- View notification history
- Mark notifications as read

### Sending Notifications
From any Lambda function or frontend:
```python
import boto3
import json

lambda_client = boto3.client('lambda')

lambda_client.invoke(
    FunctionName='notifications_api',
    InvocationType='Event',  # Async
    Payload=json.dumps({
        'body': json.dumps({
            'action': 'send_notification',
            'type': 'comment_reply',
            'recipient_email': 'user@example.com',
            'subject': 'New Reply',
            'message': 'Someone replied to your comment',
            'link': 'https://example.com/article'
        })
    })
)
```

## Future Enhancements
- Push notifications (browser)
- SMS notifications
- Notification batching (digest)
- Notification scheduling
- Rich email templates per type
- Unsubscribe links
- Notification analytics
