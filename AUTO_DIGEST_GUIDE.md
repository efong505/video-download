# Auto-Digest Newsletter System

## Overview
Automated weekly newsletter that compiles top content from your platform and sends to all subscribers.

## What It Does
- Runs weekly (configurable schedule)
- Pulls top 3 articles (by views)
- Pulls latest 3 news items
- Pulls top 3 prayer requests (by prayer count)
- Pulls next 3 upcoming events
- Generates professional HTML email
- Automatically sends to all active subscribers

## Components

### Lambda Function: digest_generator
- **Location**: `digest_generator/index.py`
- **Runtime**: Python 3.12
- **Timeout**: 60 seconds
- **Memory**: 256 MB
- **Trigger**: Manual or CloudWatch Events (weekly)

### How It Works
1. Scans DynamoDB tables for content from last 7 days
2. Sorts and filters top content
3. Generates HTML using professional template
4. Creates newsletter via newsletter_api
5. Automatically sends to all subscribers

## Manual Testing
```bash
# Test the digest generator
aws lambda invoke --function-name digest_generator response.json
cat response.json
```

## Schedule Weekly Digest (Optional)

### Option 1: CloudWatch Events (Recommended)
```bash
# Create rule for every Monday at 8 AM EST
aws events put-rule --name weekly-digest --schedule-expression "cron(0 13 ? * MON *)"

# Add Lambda as target
aws events put-targets --rule weekly-digest --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:371751795928:function:digest_generator"

# Grant permission
aws lambda add-permission --function-name digest_generator --statement-id weekly-digest --action lambda:InvokeFunction --principal events.amazonaws.com --source-arn arn:aws:events:us-east-1:371751795928:rule/weekly-digest
```

### Option 2: Manual Trigger from Admin Panel
Add button to admin-newsletters.html:
```html
<button onclick="generateDigest()">Generate Weekly Digest Now</button>

<script>
function generateDigest() {
    // Call digest_generator Lambda via API Gateway or direct invoke
    alert('Generating weekly digest...');
}
</script>
```

## Professional Email Templates

### 5 Templates Created
1. **Modern Gradient** - Purple gradient header, clean layout
2. **Classic Newsletter** - Traditional with sidebar style
3. **Patriotic Theme** - Red, white, blue design
4. **Minimalist Clean** - Simple, elegant white space
5. **Bold Impact** - Eye-catching large typography

### Using Templates
1. Go to admin-newsletters.html
2. Click Templates tab
3. Click "Use Template" on any template
4. Edit content as needed
5. Save and send

### Template Features
- Mobile-responsive (max-width: 600px)
- Inline CSS (email-safe)
- Professional typography
- Color-coded sections
- Unsubscribe link placeholder
- Brand consistency

## Customization

### Change Digest Schedule
Edit CloudWatch Events rule schedule expression:
- Daily: `cron(0 13 * * ? *)`
- Weekly Monday: `cron(0 13 ? * MON *)`
- Bi-weekly: `cron(0 13 ? * MON/2 *)`
- Monthly: `cron(0 13 1 * ? *)`

### Change Content Selection
Edit `digest_generator/index.py`:
```python
# Change number of items
top_articles = articles[:5]  # Show 5 instead of 3

# Change sorting
articles.sort(key=lambda x: x.get('created_at', ''), reverse=True)  # Sort by date instead of views

# Change time range
week_ago = (datetime.utcnow() - timedelta(days=14)).isoformat()  # Last 2 weeks instead of 1
```

### Customize HTML Template
Edit `generate_digest_html()` function in `digest_generator/index.py`

## Monitoring

### Check Digest Logs
```bash
aws logs tail /aws/lambda/digest_generator --follow
```

### View Sent Digests
1. Go to admin-newsletters.html
2. Filter by "auto-digest" creator
3. View recipient count and status

## Cost Estimate
- Lambda execution: ~$0.0001 per digest
- SES emails: $0.10 per 1,000 emails
- **Total**: ~$0.10 per week for 1,000 subscribers

## Troubleshooting

### No Content in Digest
- Check if articles/news/prayers/events exist in DynamoDB
- Verify status fields are correct (published, approved, upcoming)
- Check date ranges (content must be from last 7 days)

### Digest Not Sending
- Check Lambda logs for errors
- Verify SES permissions on lambda-execution-role
- Ensure newsletter_api is working
- Check subscriber count (need at least 1 active subscriber)

### Template Not Loading
- Verify template exists in newsletter_templates table
- Check template_id is correct
- Ensure HTML is valid and email-safe (inline CSS only)
