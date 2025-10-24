# Email Subscription System - Usage Guide

Complete guide for managing your email subscribers, sending campaigns, and viewing analytics.

---

## Table of Contents
1. [Command-Line Tools](#command-line-tools)
2. [Web Dashboard](#web-dashboard)
3. [Common Tasks](#common-tasks)
4. [API Endpoints](#api-endpoints)

---

## Command-Line Tools

### 1. Subscriber Management (`manage_subscribers.py`)

Manage your subscriber list from the command line.

#### View All Subscribers
```bash
# View all active subscribers
python manage_subscribers.py list

# View unsubscribed users
python manage_subscribers.py list unsubscribed
```

#### Export Subscribers
```bash
# Export active subscribers to CSV
python manage_subscribers.py export subscribers.csv

# Export unsubscribed users
python manage_subscribers.py export unsubscribed.csv unsubscribed

# Export all subscribers (active and inactive)
python manage_subscribers.py export all_subscribers.csv all
```

#### Search for a Subscriber
```bash
python manage_subscribers.py search user@example.com
```

Output shows:
- Email address
- Status (active/unsubscribed)
- Subscription date
- Source (where they subscribed)
- Total opens and clicks
- Last activity date

#### Unsubscribe Someone
```bash
python manage_subscribers.py unsubscribe user@example.com
```

#### Resubscribe Someone
```bash
python manage_subscribers.py resubscribe user@example.com
```

#### View Statistics
```bash
python manage_subscribers.py stats
```

Shows:
- Total subscribers
- Active vs unsubscribed count
- Total opens and clicks
- Average engagement per subscriber

---

### 2. Email Analytics (`analytics_queries.py`)

View detailed email campaign performance.

#### View All Statistics
```bash
python analytics_queries.py
```

Shows:
- Total subscribers
- Campaign performance (by campaign_id)
- Top engaged subscribers
- Recent activity

#### View Specific Campaign
```bash
# Edit the script to filter by campaign_id
# Or query DynamoDB directly for specific campaigns
```

---

### 3. Send Newsletter (`send_newsletter.py`)

Send email campaigns to all active subscribers.

#### Send a Campaign
```bash
python send_newsletter.py
```

The script will:
1. Prompt for campaign details (subject, content)
2. Show preview
3. Ask for confirmation
4. Send to all active subscribers
5. Automatically add tracking pixels and links
6. Log all sends to database

**Important:** Edit the script to customize:
- Email subject
- Email content (HTML and plain text)
- Campaign ID

---

## Web Dashboard

### Setup

1. **Install Flask** (if not already installed):
```bash
pip install flask flask-cors boto3
```

2. **Start the API Server**:
```bash
python dashboard_api.py
```

The server will start on http://localhost:5000

3. **Open the Dashboard**:
```bash
# Open dashboard_simple.html in your browser
start dashboard_simple.html
```

Or use a simple HTTP server:
```bash
python -m http.server 8000
# Then visit: http://localhost:8000/dashboard_simple.html
```

### Dashboard Features

#### 📊 Overview Tab
- Total subscribers count
- Active vs unsubscribed
- Total opens and clicks
- Engagement rates
- Recent activity chart

#### 👥 Subscribers Tab
- View all subscribers in a table
- Search and filter
- Sort by date, opens, clicks
- Export to CSV
- Individual subscriber actions:
  - View details
  - Unsubscribe/Resubscribe
  - View activity history

#### 📧 Campaigns Tab
- View all sent campaigns
- Campaign performance metrics
- Open rates and click rates
- Send new campaign

#### 📈 Analytics Tab
- Engagement trends over time
- Top performing campaigns
- Subscriber growth chart
- Geographic distribution (if available)

---

## Common Tasks

### Task 1: Export Your Email List for Mailchimp/Other Service
```bash
python manage_subscribers.py export my_list.csv active
```

The CSV includes: Email, Status, Subscribed Date, Source, Opens, Clicks, Last Activity

### Task 2: Check Who Opened Your Last Email
```bash
python analytics_queries.py
```

Look for the campaign_id of your last email and see the open count.

### Task 3: Remove Inactive Subscribers
```bash
# First, identify inactive subscribers (0 opens, old subscription date)
python manage_subscribers.py list active

# Then unsubscribe them individually
python manage_subscribers.py unsubscribe inactive@example.com
```

### Task 4: Send a Newsletter
```bash
# Edit send_newsletter.py with your content
python send_newsletter.py
```

### Task 5: View Subscriber Details
```bash
python manage_subscribers.py search user@example.com
```

### Task 6: Get Total Subscriber Count
```bash
python manage_subscribers.py stats
```

### Task 7: Manually Add a Subscriber
Use the web dashboard or call the API directly:
```bash
curl -X POST https://niexv1rw75.execute-api.us-east-1.amazonaws.com/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"newuser@example.com"}'
```

---

## API Endpoints

Your email system has the following API endpoints:

### Subscribe
```
POST https://niexv1rw75.execute-api.us-east-1.amazonaws.com/subscribe
Body: {"email": "user@example.com"}
```

### Unsubscribe
```
GET https://niexv1rw75.execute-api.us-east-1.amazonaws.com/unsubscribe?email=user@example.com
```

### Track Email Open
```
GET https://niexv1rw75.execute-api.us-east-1.amazonaws.com/track/open/{tracking_id}
```

### Track Link Click
```
GET https://niexv1rw75.execute-api.us-east-1.amazonaws.com/track/click/{tracking_id}
```

---

## Database Structure

### email-subscribers Table
- **email** (Primary Key): Subscriber email address
- **status**: "active" or "unsubscribed"
- **subscribed_at**: ISO timestamp
- **unsubscribed_at**: ISO timestamp (if unsubscribed)
- **source**: Where they subscribed (e.g., "election-map")
- **total_opens**: Number of emails opened
- **total_clicks**: Number of links clicked
- **last_activity**: Last interaction timestamp

### email-events Table
- **event_id** (Primary Key): Unique event ID
- **timestamp** (Sort Key): Unix timestamp
- **email**: Subscriber email
- **event_type**: "subscribed", "opened", "clicked", "unsubscribed"
- **campaign_id**: Campaign identifier
- **date**: ISO timestamp
- **metadata**: Additional event data (JSON)

---

## Troubleshooting

### Subscribers Not Receiving Emails
1. Check SES sending limits: `aws ses get-send-quota --region us-east-1`
2. Verify email is in database: `python manage_subscribers.py search email@example.com`
3. Check CloudWatch logs: `aws logs tail /aws/lambda/email-subscription-handler --since 1h`
4. Verify SES email is verified: `aws ses get-identity-verification-attributes --identities contact@christianconservativestoday.com`

### Emails Going to Spam
- Set up SPF, DKIM, and DMARC records
- Use SES custom MAIL FROM domain
- Avoid spam trigger words
- Include unsubscribe link
- Maintain good engagement rates

### Export Not Working
```bash
# Check AWS credentials
aws sts get-caller-identity

# Test DynamoDB access
aws dynamodb scan --table-name email-subscribers --limit 1
```

### Dashboard Not Loading
1. Check API endpoint in dashboard.html matches your API Gateway URL
2. Verify CORS is enabled on API Gateway
3. Check browser console for errors

---

## Best Practices

1. **Regular Exports**: Export your list weekly as backup
2. **Clean Your List**: Remove inactive subscribers quarterly
3. **Monitor Engagement**: Check analytics after each campaign
4. **Test Emails**: Send test emails before campaigns
5. **Respect Unsubscribes**: Never re-add unsubscribed users
6. **Segment Your List**: Consider adding tags/categories for targeting
7. **Track Performance**: Monitor open rates (aim for >20%) and click rates (aim for >2%)

---

## Quick Reference

```bash
# Most common commands
python manage_subscribers.py stats                    # View overview
python manage_subscribers.py list                     # List all subscribers
python manage_subscribers.py export list.csv          # Export to CSV
python manage_subscribers.py search user@example.com  # Find subscriber
python send_newsletter.py                             # Send campaign
python analytics_queries.py                           # View analytics
```

---

## Support

For issues or questions:
1. Check CloudWatch logs for Lambda errors
2. Review setup_instructions.md for configuration
3. Check troubleshooting.md for common issues
4. Verify API Gateway routes are configured correctly
