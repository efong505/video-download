# Content Scheduling System

## Overview
Automated content scheduling system that allows admins to schedule news articles for future publication. Articles are automatically published at their scheduled time without manual intervention.

## Features
- ✅ Schedule articles for future publication
- ✅ Automatic status change from 'scheduled' to 'published'
- ✅ Email notifications sent to subscribers when published
- ✅ Runs every 5 minutes to check for scheduled content
- ✅ Timezone-aware (uses UTC)

## How It Works

### 1. Creating Scheduled Content
When creating a news article in `create-news.html`:
1. Fill in article details (title, content, etc.)
2. Set the "Schedule Publish" datetime field to a future date/time
3. Set Status to "Scheduled"
4. Click "Create News Article"

The article will be saved with `status: 'scheduled'` and will NOT be visible to public users until the scheduled time.

### 2. Automatic Publishing
The `scheduled-publisher` Lambda function:
- Runs every 5 minutes via EventBridge (CloudWatch Events)
- Scans the `news-table` for items with `status: 'scheduled'`
- Checks if `scheduled_publish` time <= current time
- Updates status to `published` for eligible articles
- Sends email notifications to all active subscribers

### 3. Manual Override
Admins can manually publish scheduled articles:
1. Go to Admin Dashboard → News tab
2. Click "Edit" on the scheduled article
3. Change Status to "Published"
4. Save changes

## Architecture

```
┌─────────────────────┐
│  EventBridge Rule   │
│  (every 5 minutes)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ scheduled-publisher │
│   Lambda Function   │
└──────────┬──────────┘
           │
           ├──► DynamoDB (news-table)
           │    - Scan for scheduled items
           │    - Update status to published
           │
           └──► notifications_api Lambda
                - Send email notifications

```

## Database Schema

### news-table
```json
{
  "news_id": "uuid",
  "title": "string",
  "content": "string",
  "status": "scheduled|published|draft",
  "scheduled_publish": "2024-12-25T10:00:00Z",
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp"
}
```

## Deployment

### Deploy the Scheduler
```powershell
.\deploy-scheduled-publisher.ps1
```

This will:
1. Create/update the `scheduled-publisher` Lambda function
2. Create EventBridge rule to trigger every 5 minutes
3. Set up permissions for EventBridge to invoke Lambda

### Verify Deployment
```powershell
# Check Lambda function
aws lambda get-function --function-name scheduled-publisher --profile ekewaka

# Check EventBridge rule
aws events describe-rule --name scheduled-publisher-trigger --profile ekewaka

# View recent executions
aws logs tail /aws/lambda/scheduled-publisher --follow --profile ekewaka
```

## Testing

### Test Scheduled Publishing
1. Create a test article scheduled for 2 minutes in the future
2. Wait for the scheduler to run (max 5 minutes)
3. Check CloudWatch Logs for execution details
4. Verify article status changed to 'published'
5. Check that notifications were sent

### Manual Test Invocation
```powershell
aws lambda invoke --function-name scheduled-publisher --profile ekewaka output.json
cat output.json
```

## Monitoring

### CloudWatch Logs
View logs at: `/aws/lambda/scheduled-publisher`

Log messages include:
- Number of scheduled items found
- Items being published
- Notification sending status
- Any errors encountered

### Metrics to Monitor
- Lambda invocation count (should be ~12 per hour)
- Lambda errors
- Lambda duration (should be < 10 seconds)
- Number of articles published per day

## Timezone Handling

All times are stored and processed in **UTC**. The frontend datetime picker will use the user's local timezone, but the backend converts everything to UTC.

**Example:**
- User in EST (UTC-5) schedules article for "Dec 25, 2024 10:00 AM EST"
- Stored in database as: "2024-12-25T15:00:00Z" (UTC)
- Scheduler checks against UTC time
- Published at exactly 10:00 AM EST / 3:00 PM UTC

## Cost Estimate

- Lambda invocations: ~8,640 per month (every 5 minutes)
- Free tier: 1 million requests/month
- **Cost: $0** (well within free tier)

## Troubleshooting

### Article Not Publishing
1. Check CloudWatch Logs for errors
2. Verify `scheduled_publish` format is ISO 8601
3. Ensure status is exactly 'scheduled' (case-sensitive)
4. Check Lambda has DynamoDB permissions

### Notifications Not Sending
1. Verify `notifications_api` Lambda exists
2. Check `email_subscribers` table has active subscribers
3. Review CloudWatch Logs for notification errors

### Scheduler Not Running
1. Check EventBridge rule is ENABLED
2. Verify Lambda has permission from EventBridge
3. Check Lambda execution role has necessary permissions

## Future Enhancements

Potential improvements:
- [ ] Support for recurring scheduled posts
- [ ] Bulk scheduling interface
- [ ] Preview scheduled content calendar
- [ ] Timezone selection in UI
- [ ] Schedule content unpublishing (auto-archive)
- [ ] Schedule content updates (not just publishing)
- [ ] Slack/Discord notifications when content publishes
- [ ] Analytics on scheduled vs immediate publishing

## Related Files

- `scheduled-publisher/lambda_function.py` - Scheduler Lambda code
- `deploy-scheduled-publisher.ps1` - Deployment script
- `news_api/index.py` - News API with scheduling logic
- `create-news.html` - Frontend with scheduling UI
- `edit-news.html` - Edit interface with scheduling

## Support

For issues or questions:
1. Check CloudWatch Logs first
2. Review this documentation
3. Test with manual Lambda invocation
4. Check AWS console for EventBridge rule status
