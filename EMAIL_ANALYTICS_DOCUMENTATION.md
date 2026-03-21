# Comprehensive Email Analytics System - Documentation

## Overview
A complete email tracking and analytics system for ChristianConservativesToday.com that tracks every aspect of email engagement including sends, deliveries, opens, clicks, bounces, complaints, and more.

## Architecture

### 1. SES Configuration Set
- **Name**: `email-tracking-config`
- **Purpose**: Enables SES to send events to SNS
- **Events Tracked**: send, reject, bounce, complaint, delivery, open, click

### 2. SNS Topic
- **Name**: `ses-email-events`
- **ARN**: `arn:aws:sns:us-east-1:371751795928:ses-email-events`
- **Purpose**: Receives SES events and triggers Lambda processor

### 3. Lambda Functions

#### ses-event-processor
- **Purpose**: Processes SES events from SNS and stores analytics
- **Trigger**: SNS topic subscription
- **Tables Updated**:
  - `email-events` - Raw event log
  - `email-campaign-stats` - Aggregated campaign metrics
  - `email-subscriber-stats` - Aggregated subscriber metrics
  - `user-email-subscribers` - Updates subscriber status (bounced/complained)

#### manual-email-sender (Updated)
- **New Features**:
  - Adds tracking pixel to all emails
  - Uses SES configuration set
  - Tags emails with campaign_id and recipient
  - Enables full event tracking

### 4. DynamoDB Tables

#### email-events (Existing)
- **Key**: event_id (String), timestamp (Number)
- **Attributes**: email, event_type, campaign_id, date, metadata
- **Purpose**: Raw event log for all email interactions

#### email-campaign-stats (New)
- **Key**: campaign_id (String)
- **Attributes**: 
  - sent_count, delivered_count, open_count, click_count
  - bounce_count, complaint_count, reject_count
  - last_updated
- **Purpose**: Aggregated statistics per campaign

#### email-subscriber-stats (New)
- **Key**: subscriber_email (String)
- **Attributes**:
  - emails_sent, emails_delivered, opens, clicks
  - bounces, complaints
  - last_activity
- **Purpose**: Aggregated statistics per subscriber

### 5. Frontend Dashboards

#### advanced-email-analytics.html
- **URL**: https://christianconservativestoday.com/advanced-email-analytics.html
- **Features**:
  - Overview stats with delivery/open/click/bounce/complaint rates
  - Performance charts (line chart over time)
  - Engagement funnel (bar chart)
  - Campaign performance table
  - Subscriber engagement table
  - Recent events log (last 100 events)
  - Auto-refresh every 60 seconds
  - Tabbed interface

#### email-analytics.html (Existing)
- **Purpose**: Basic drip campaign analytics
- **Features**: Enrollment tracking, manual email sending

#### campaign-manager.html
- **Purpose**: Create/edit/delete email campaigns
- **Features**: Full CRUD for drip sequences

## Event Types Tracked

### 1. Send
- Email accepted by SES for sending
- Increments: sent_count

### 2. Delivery
- Email successfully delivered to recipient's mail server
- Increments: delivered_count

### 3. Open
- Recipient opened the email (tracking pixel loaded)
- Increments: open_count
- Captures: user_agent, ip_address

### 4. Click
- Recipient clicked a tracked link
- Increments: click_count
- Captures: link URL, user_agent, ip_address

### 5. Bounce
- Email bounced (hard or soft)
- Increments: bounce_count
- Types:
  - **Permanent (Hard)**: Invalid email, marks subscriber as bounced
  - **Transient (Soft)**: Temporary issue (mailbox full, etc.)
- Captures: bounce_type, bounce_subtype, diagnostic_code

### 6. Complaint
- Recipient marked email as spam
- Increments: complaint_count
- Marks subscriber as complained
- Captures: complaint_type

### 7. Reject
- SES rejected email before sending (invalid recipient, etc.)
- Increments: reject_count
- Captures: reason

## Key Metrics

### Campaign Metrics
- **Delivery Rate**: (delivered / sent) × 100
- **Open Rate**: (opens / delivered) × 100
- **Click-Through Rate (CTR)**: (clicks / opens) × 100
- **Bounce Rate**: (bounces / sent) × 100
- **Complaint Rate**: (complaints / delivered) × 100

### Subscriber Status
- **Active**: Normal subscriber, no issues
- **Bounced**: Hard bounce received, no longer receiving emails
- **Complained**: Marked email as spam, no longer receiving emails
- **Inactive**: Received 3+ emails but never opened

## API Endpoints

All endpoints use base URL: `https://niexv1rw75.execute-api.us-east-1.amazonaws.com/subscribe`

### Analytics Endpoints

#### GET ?action=get_analytics_overview
Returns overall statistics across all campaigns
```json
{
  "stats": {
    "total_sent": 150,
    "total_delivered": 145,
    "total_opens": 45,
    "total_clicks": 12,
    "total_bounces": 3,
    "total_complaints": 1
  }
}
```

#### GET ?action=get_campaign_analytics
Returns per-campaign statistics
```json
{
  "campaigns": [
    {
      "campaign_id": "uuid",
      "campaign_name": "Welcome Email 1",
      "sent_count": 50,
      "delivered_count": 48,
      "open_count": 15,
      "click_count": 4,
      "bounce_count": 1,
      "complaint_count": 0
    }
  ]
}
```

#### GET ?action=get_subscriber_analytics
Returns per-subscriber statistics
```json
{
  "subscribers": [
    {
      "subscriber_email": "user@example.com",
      "emails_sent": 5,
      "emails_delivered": 5,
      "opens": 3,
      "clicks": 1,
      "bounces": 0,
      "complaints": 0,
      "last_activity": "2026-03-21T18:00:00"
    }
  ]
}
```

#### GET ?action=get_recent_events&limit=100
Returns recent email events
```json
{
  "events": [
    {
      "event_id": "uuid",
      "timestamp": 1711047600,
      "email": "user@example.com",
      "event_type": "opened",
      "campaign_id": "uuid",
      "date": "2026-03-21T18:00:00",
      "metadata": "{\"user_agent\":\"...\",\"ip_address\":\"...\"}"
    }
  ]
}
```

## How Tracking Works

### Email Sending Flow
1. **Email Created**: Campaign content with placeholders
2. **Tracking Pixel Added**: 1×1 transparent PNG added to HTML
3. **SES Tags Applied**: campaign_id and recipient tagged
4. **Configuration Set Used**: Enables SES event tracking
5. **Email Sent**: Via SES with all tracking enabled

### Event Processing Flow
1. **SES Event Occurs**: User opens email, clicks link, etc.
2. **SNS Notification**: SES sends event to SNS topic
3. **Lambda Triggered**: ses-event-processor receives event
4. **Event Logged**: Raw event stored in email-events table
5. **Stats Updated**: Aggregated stats updated in campaign-stats and subscriber-stats
6. **Subscriber Status**: Updated if bounce/complaint

### Tracking Pixel
- **URL Format**: `https://niexv1rw75.execute-api.us-east-1.amazonaws.com/track/open/{tracking_id}`
- **Tracking ID**: Base64 encoded `{email}|{campaign_id}`
- **Image**: 1×1 transparent PNG
- **Placement**: Before `</body>` tag in HTML emails

## Access Control

All analytics dashboards are **admin-only**:
- Must be logged in with role = 'admin' or 'super_user'
- Links only appear in admin dropdown menu
- Direct URL access requires authentication

## Testing

### Test Email Tracking
1. Send test email via email-analytics.html manual sender
2. Open email in your inbox
3. Check advanced-email-analytics.html for:
   - Sent count increment
   - Delivered count increment (within 1-2 minutes)
   - Open count increment (when you open email)
4. Check Recent Events tab for event log

### Test Bounce Handling
1. Send email to invalid address (e.g., bounce@simulator.amazonses.com)
2. Check for bounce event in Recent Events
3. Verify subscriber marked as bounced in subscriber-stats

### Test Complaint Handling
1. Send email to complaint@simulator.amazonses.com
2. Check for complaint event
3. Verify subscriber marked as complained

## Maintenance

### Monitor Lambda Logs
```bash
# SES Event Processor
aws logs tail /aws/lambda/ses-event-processor --follow --profile ekewaka --region us-east-1

# Manual Email Sender
aws logs tail /aws/lambda/manual-email-sender --follow --profile ekewaka --region us-east-1
```

### Check SES Sending Statistics
```bash
aws ses get-send-statistics --profile ekewaka --region us-east-1
```

### Query Campaign Stats
```bash
aws dynamodb scan --table-name email-campaign-stats --profile ekewaka --region us-east-1
```

### Query Subscriber Stats
```bash
aws dynamodb scan --table-name email-subscriber-stats --profile ekewaka --region us-east-1
```

## Future Enhancements

### Potential Additions
1. **Geographic Tracking**: Map opens/clicks by location
2. **Device/Client Detection**: Track email clients (Gmail, Outlook, etc.)
3. **A/B Testing**: Compare subject lines, content variations
4. **Unsubscribe Tracking**: Track unsubscribe reasons
5. **Email Heatmaps**: Visual click tracking
6. **Predictive Analytics**: ML-based engagement predictions
7. **Automated Segmentation**: Auto-segment based on engagement
8. **Real-time Alerts**: Notify on high bounce/complaint rates
9. **Export Reports**: PDF/CSV export of analytics
10. **Comparative Analysis**: Compare campaigns side-by-side

## Troubleshooting

### No Events Appearing
1. Check SES configuration set is applied to emails
2. Verify SNS topic subscription is active
3. Check Lambda has permissions to write to DynamoDB
4. Review Lambda logs for errors

### Tracking Pixel Not Working
1. Verify pixel URL is correct
2. Check API Gateway route exists for /track/open
3. Ensure tracking_id is properly encoded
4. Test pixel URL directly in browser

### Stats Not Updating
1. Check ses-event-processor Lambda is being triggered
2. Verify DynamoDB tables exist and are accessible
3. Review Lambda execution logs
4. Check for Decimal conversion errors

## Cost Considerations

### AWS Services Used
- **SES**: $0.10 per 1,000 emails
- **SNS**: $0.50 per 1 million notifications
- **Lambda**: Free tier covers most usage
- **DynamoDB**: Pay-per-request, minimal cost
- **API Gateway**: $3.50 per million requests

### Estimated Monthly Cost (1,000 emails/month)
- SES: $0.10
- SNS: ~$0.01
- Lambda: Free tier
- DynamoDB: ~$0.25
- **Total**: ~$0.36/month

## Support

For issues or questions:
- Check Lambda logs first
- Review DynamoDB tables for data
- Test with SES simulator addresses
- Contact: hawaiianintucson@gmail.com
