# AWS SES with Email Tracking Implementation

## Architecture with Tracking

```
Email Sent → Tracking Pixel (opens) → Lambda → DynamoDB
          → Tracking Links (clicks) → Lambda → DynamoDB
```

## What Gets Tracked

- ✅ Email opens (when recipient views email)
- ✅ Link clicks (which links were clicked)
- ✅ Delivery status (sent, bounced, complained)
- ✅ Timestamp for each event
- ✅ Per-subscriber analytics

## Implementation

### Step 1: Create Tracking Tables in DynamoDB

**Table 1: email-subscribers** (already created)
```
Partition Key: email (String)
```

**Table 2: email-events**
```
Partition Key: event_id (String)
Sort Key: timestamp (Number)
Attributes: email, event_type, campaign_id, metadata
```

### Step 2: Enhanced Lambda Function with Tracking

**File: lambda_email_subscription_tracking.py**

```python
import json
import boto3
import os
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name='us-east-1')
subscribers_table = dynamodb.Table('email-subscribers')
events_table = dynamodb.Table('email-events')

DOMAIN = 'https://christianconservativestoday.com'

def lambda_handler(event, context):
    path = event.get('path', '')
    
    # Handle email subscription
    if path == '/subscribe' or event.get('httpMethod') == 'POST':
        return handle_subscription(event)
    
    # Handle open tracking
    elif path.startswith('/track/open/'):
        return handle_open_tracking(event)
    
    # Handle click tracking
    elif path.startswith('/track/click/'):
        return handle_click_tracking(event)
    
    # Handle CORS preflight
    elif event.get('httpMethod') == 'OPTIONS':
        return cors_response(200, {'message': 'OK'})
    
    return cors_response(404, {'error': 'Not found'})

def handle_subscription(event):
    """Handle email subscription"""
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email', '').strip().lower()
        
        if not email or '@' not in email:
            return cors_response(400, {'error': 'Invalid email'})
        
        # Store subscriber
        subscribers_table.put_item(Item={
            'email': email,
            'status': 'active',
            'subscribed_at': datetime.now().isoformat(),
            'source': 'election-map',
            'total_opens': 0,
            'total_clicks': 0
        })
        
        # Send welcome email with tracking
        send_welcome_email(email)
        
        # Log subscription event
        log_event(email, 'subscribed', 'welcome-email')
        
        return cors_response(200, {
            'message': 'Subscription successful',
            'email': email
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return cors_response(500, {'error': 'Subscription failed'})

def handle_open_tracking(event):
    """Track email opens via 1x1 pixel"""
    try:
        # Extract tracking ID from path: /track/open/{tracking_id}
        tracking_id = event['path'].split('/')[-1]
        
        # Decode tracking ID to get email and campaign
        email, campaign_id = decode_tracking_id(tracking_id)
        
        # Log open event
        log_event(email, 'opened', campaign_id)
        
        # Update subscriber stats
        subscribers_table.update_item(
            Key={'email': email},
            UpdateExpression='SET total_opens = total_opens + :inc',
            ExpressionAttributeValues={':inc': 1}
        )
        
        # Return 1x1 transparent pixel
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/png',
                'Cache-Control': 'no-cache, no-store, must-revalidate'
            },
            'body': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==',
            'isBase64Encoded': True
        }
        
    except Exception as e:
        print(f"Open tracking error: {str(e)}")
        return {'statusCode': 200, 'body': ''}

def handle_click_tracking(event):
    """Track link clicks and redirect"""
    try:
        # Extract tracking ID from path: /track/click/{tracking_id}
        tracking_id = event['path'].split('/')[-1]
        
        # Decode to get email, campaign, and destination URL
        email, campaign_id, destination_url = decode_click_tracking_id(tracking_id)
        
        # Log click event
        log_event(email, 'clicked', campaign_id, {'url': destination_url})
        
        # Update subscriber stats
        subscribers_table.update_item(
            Key={'email': email},
            UpdateExpression='SET total_clicks = total_clicks + :inc',
            ExpressionAttributeValues={':inc': 1}
        )
        
        # Redirect to destination
        return {
            'statusCode': 302,
            'headers': {
                'Location': destination_url,
                'Cache-Control': 'no-cache'
            },
            'body': ''
        }
        
    except Exception as e:
        print(f"Click tracking error: {str(e)}")
        return {'statusCode': 302, 'headers': {'Location': DOMAIN}, 'body': ''}

def send_welcome_email(email):
    """Send welcome email with tracking"""
    campaign_id = 'welcome-email'
    
    # Generate tracking pixel URL
    tracking_id = encode_tracking_id(email, campaign_id)
    pixel_url = f"{DOMAIN}/track/open/{tracking_id}"
    
    # Generate tracked links
    election_map_link = create_tracked_link(
        email, 
        campaign_id, 
        f"{DOMAIN}/election-map.html"
    )
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #667eea;">Welcome to Christian Conservatives Today!</h2>
        <p>Thank you for subscribing to our election updates and voter guides.</p>
        <p>You'll receive:</p>
        <ul>
            <li>🗳️ Election updates and key dates</li>
            <li>📖 State-specific voter guides</li>
            <li>🎯 Pro-life, pro-family candidate information</li>
            <li>⛪ Church mobilization resources</li>
        </ul>
        <p style="margin-top: 30px;">
            <a href="{election_map_link}" 
               style="background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">
                View Election Map
            </a>
        </p>
        <hr style="margin: 30px 0; border: 1px solid #eee;">
        <p style="font-size: 12px; color: #666;">
            You're receiving this because you subscribed at christianconservativestoday.com<br>
            <a href="{DOMAIN}/unsubscribe?email={email}">Unsubscribe</a>
        </p>
        <img src="{pixel_url}" width="1" height="1" style="display:none;" alt="">
    </body>
    </html>
    """
    
    ses.send_email(
        Source='Christian Conservatives Today <contact@christianconservativestoday.com>',
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': 'Welcome to Christian Conservatives Today!'},
            'Body': {'Html': {'Data': html_body}}
        }
    )

def encode_tracking_id(email, campaign_id):
    """Encode email and campaign into tracking ID"""
    import base64
    data = f"{email}|{campaign_id}"
    return base64.urlsafe_b64encode(data.encode()).decode()

def decode_tracking_id(tracking_id):
    """Decode tracking ID to email and campaign"""
    import base64
    data = base64.urlsafe_b64decode(tracking_id.encode()).decode()
    email, campaign_id = data.split('|')
    return email, campaign_id

def create_tracked_link(email, campaign_id, destination_url):
    """Create tracked link for click tracking"""
    import base64
    data = f"{email}|{campaign_id}|{destination_url}"
    tracking_id = base64.urlsafe_b64encode(data.encode()).decode()
    return f"{DOMAIN}/track/click/{tracking_id}"

def decode_click_tracking_id(tracking_id):
    """Decode click tracking ID"""
    import base64
    data = base64.urlsafe_b64decode(tracking_id.encode()).decode()
    parts = data.split('|')
    return parts[0], parts[1], parts[2]

def log_event(email, event_type, campaign_id, metadata=None):
    """Log email event to DynamoDB"""
    event_id = str(uuid.uuid4())
    timestamp = int(datetime.now().timestamp())
    
    item = {
        'event_id': event_id,
        'timestamp': timestamp,
        'email': email,
        'event_type': event_type,
        'campaign_id': campaign_id
    }
    
    if metadata:
        item['metadata'] = metadata
    
    events_table.put_item(Item=item)

def cors_response(status_code, body):
    """Return CORS response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
```

### Step 3: Create Analytics Dashboard Query

**Query to get campaign stats:**

```python
import boto3
from collections import defaultdict

dynamodb = boto3.resource('dynamodb')
events_table = dynamodb.Table('email-events')

def get_campaign_stats(campaign_id):
    """Get stats for a specific campaign"""
    response = events_table.scan(
        FilterExpression='campaign_id = :cid',
        ExpressionAttributeValues={':cid': campaign_id}
    )
    
    events = response['Items']
    
    stats = {
        'total_sent': 0,
        'total_opens': 0,
        'total_clicks': 0,
        'unique_opens': set(),
        'unique_clicks': set()
    }
    
    for event in events:
        email = event['email']
        event_type = event['event_type']
        
        if event_type == 'subscribed':
            stats['total_sent'] += 1
        elif event_type == 'opened':
            stats['total_opens'] += 1
            stats['unique_opens'].add(email)
        elif event_type == 'clicked':
            stats['total_clicks'] += 1
            stats['unique_clicks'].add(email)
    
    return {
        'campaign_id': campaign_id,
        'total_sent': stats['total_sent'],
        'total_opens': stats['total_opens'],
        'unique_opens': len(stats['unique_opens']),
        'total_clicks': stats['total_clicks'],
        'unique_clicks': len(stats['unique_clicks']),
        'open_rate': f"{(len(stats['unique_opens']) / max(stats['total_sent'], 1)) * 100:.1f}%",
        'click_rate': f"{(len(stats['unique_clicks']) / max(stats['total_sent'], 1)) * 100:.1f}%"
    }

# Example usage
print(get_campaign_stats('welcome-email'))
```

### Step 4: API Gateway Routes

Configure these routes in API Gateway:
- `POST /subscribe` → Lambda function
- `GET /track/open/{tracking_id}` → Lambda function
- `GET /track/click/{tracking_id}` → Lambda function

## What You Get

### **Email Analytics:**
- Total emails sent
- Open rate (% who opened)
- Click rate (% who clicked)
- Per-subscriber engagement
- Campaign performance comparison

### **Subscriber Insights:**
- Most engaged subscribers
- Inactive subscribers
- Best performing content
- Optimal send times

## Cost

Same as basic SES:
- $0.10 per 1,000 emails
- DynamoDB: ~$0.25 per million events (essentially free)
- No additional cost for tracking

## Comparison to Mailchimp

| Feature | AWS SES + Tracking | Mailchimp |
|---------|-------------------|-----------|
| Open tracking | ✅ Yes | ✅ Yes |
| Click tracking | ✅ Yes | ✅ Yes |
| Cost (10k emails) | $1.00 | $13/month |
| Dashboard | Build your own | Built-in |
| Setup time | 2-3 hours | 15 minutes |
| Control | Full | Limited |

## Next Steps

1. Deploy the enhanced Lambda function
2. Create the email-events DynamoDB table
3. Configure API Gateway routes
4. Test tracking with a sample email
5. Build analytics dashboard (optional)

Would you like me to help you deploy this?
