# AWS SES Email Subscription Implementation

## Architecture Overview

```
User Browser → API Gateway → Lambda Function → DynamoDB (store email)
                                              ↓
                                         AWS SES (send confirmation)
```

## Step 1: Verify Your Email Domain in SES

1. Go to AWS SES Console: https://console.aws.amazon.com/ses/
2. Click **Verified identities** → **Create identity**
3. Choose **Domain** and enter: `christianconservativestoday.com`
4. Enable **DKIM** (recommended)
5. Copy the DNS records provided
6. Add DNS records to your domain registrar:
   - CNAME records for DKIM
   - TXT record for domain verification
7. Wait for verification (can take up to 72 hours, usually < 1 hour)

**Alternative**: Verify just the email address:
- Choose **Email address** instead of domain
- Enter: `contact@christianconservativestoday.com`
- Click verification link in email AWS sends

## Step 2: Request Production Access (Important!)

By default, SES is in **sandbox mode** (can only send to verified emails).

1. In SES Console, click **Account dashboard**
2. Click **Request production access**
3. Fill out form:
   - **Use case**: Transactional emails (election updates, voter guides)
   - **Website URL**: https://christianconservativestoday.com
   - **Expected volume**: Start with 1,000/month
   - **Compliance**: Explain you have opt-in and unsubscribe
4. Usually approved within 24 hours

## Step 3: Create DynamoDB Table

```bash
# Table name: email-subscribers
# Partition key: email (String)
# No sort key needed
```

In AWS Console:
1. Go to DynamoDB → **Create table**
2. Table name: `email-subscribers`
3. Partition key: `email` (String)
4. Use default settings
5. Click **Create table**

## Step 4: Create Lambda Function

**File: lambda_email_subscription.py**

```python
import json
import boto3
import os
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name='us-east-1')
table = dynamodb.Table('email-subscribers')

def lambda_handler(event, context):
    # Handle CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return cors_response(200, {'message': 'OK'})
    
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email', '').strip().lower()
        
        if not email or '@' not in email:
            return cors_response(400, {'error': 'Invalid email address'})
        
        # Check if already subscribed
        response = table.get_item(Key={'email': email})
        if 'Item' in response:
            if response['Item'].get('status') == 'active':
                return cors_response(200, {'message': 'Already subscribed'})
        
        # Store in DynamoDB
        table.put_item(Item={
            'email': email,
            'status': 'pending',
            'subscribed_at': datetime.now().isoformat(),
            'source': 'election-map',
            'confirmed': False
        })
        
        # Send confirmation email
        send_confirmation_email(email)
        
        return cors_response(200, {
            'message': 'Subscription successful',
            'email': email
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return cors_response(500, {'error': 'Subscription failed'})

def send_confirmation_email(email):
    """Send confirmation email via SES"""
    subject = "Confirm Your Election Updates Subscription"
    
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
            <a href="https://christianconservativestoday.com/election-map.html" 
               style="background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">
                View Election Map
            </a>
        </p>
        <hr style="margin: 30px 0; border: 1px solid #eee;">
        <p style="font-size: 12px; color: #666;">
            You're receiving this because you subscribed at christianconservativestoday.com<br>
            <a href="https://christianconservativestoday.com/unsubscribe?email={email}">Unsubscribe</a>
        </p>
    </body>
    </html>
    """
    
    text_body = f"""
    Welcome to Christian Conservatives Today!
    
    Thank you for subscribing to our election updates and voter guides.
    
    You'll receive:
    - Election updates and key dates
    - State-specific voter guides
    - Pro-life, pro-family candidate information
    - Church mobilization resources
    
    View the election map: https://christianconservativestoday.com/election-map.html
    
    Unsubscribe: https://christianconservativestoday.com/unsubscribe?email={email}
    """
    
    ses.send_email(
        Source='Christian Conservatives Today <contact@christianconservativestoday.com>',
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {
                'Text': {'Data': text_body},
                'Html': {'Data': html_body}
            }
        }
    )

def cors_response(status_code, body):
    """Return response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
```

## Step 5: Deploy Lambda Function

1. Go to AWS Lambda Console
2. Click **Create function**
3. Name: `email-subscription-handler`
4. Runtime: **Python 3.12**
5. Click **Create function**
6. Paste the code above
7. Click **Deploy**

## Step 6: Add IAM Permissions to Lambda

1. In Lambda function, go to **Configuration** → **Permissions**
2. Click the role name
3. Click **Add permissions** → **Attach policies**
4. Add these policies:
   - `AmazonDynamoDBFullAccess`
   - `AmazonSESFullAccess`

## Step 7: Create API Gateway

1. Go to API Gateway Console
2. Click **Create API** → **HTTP API**
3. Click **Add integration** → **Lambda**
4. Select your Lambda function
5. API name: `email-subscription-api`
6. Click **Next** → **Next** → **Create**
7. Copy the **Invoke URL** (looks like: `https://abc123.execute-api.us-east-1.amazonaws.com`)

## Step 8: Update election-map.html

Replace the `subscribeEmail()` function:

```javascript
async function subscribeEmail() {
    const emailInput = document.getElementById('email-input');
    const email = emailInput.value.trim();

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        alert('Please enter a valid email address.');
        return;
    }

    try {
        const response = await fetch('YOUR_API_GATEWAY_URL', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email: email})
        });

        const data = await response.json();

        if (response.ok) {
            const banner = document.getElementById('email-capture-banner');
            banner.innerHTML = '<div class="text-center py-3">' +
                '<h5 class="text-success mb-2">✓ Thank You for Subscribing!</h5>' +
                '<p class="mb-0">Confirmation email sent to <strong>' + email + '</strong></p>' +
                '<small class="text-muted">Check your inbox (and spam folder) to confirm.</small>' +
                '</div>';
        } else {
            alert(data.error || 'Subscription failed. Please try again.');
        }
    } catch (error) {
        console.error('Subscription error:', error);
        alert('There was an error subscribing. Please try again.');
    }
}
```

## Step 9: Test the System

1. Visit your election map page
2. Enter a test email
3. Check DynamoDB table for the entry
4. Check email inbox for confirmation
5. Verify email appears with status='pending'

## Step 10: Create Unsubscribe Page (Optional)

Create `unsubscribe.html` to handle unsubscribe requests.

## Sending Newsletters

To send emails to all subscribers:

```python
import boto3

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name='us-east-1')
table = dynamodb.Table('email-subscribers')

# Get all active subscribers
response = table.scan(
    FilterExpression='#status = :status',
    ExpressionAttributeNames={'#status': 'status'},
    ExpressionAttributeValues={':status': 'active'}
)

subscribers = response['Items']

# Send email to each subscriber
for subscriber in subscribers:
    email = subscriber['email']
    
    ses.send_email(
        Source='contact@christianconservativestoday.com',
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': 'Your Election Update'},
            'Body': {
                'Html': {'Data': '<h1>Your newsletter content here</h1>'}
            }
        }
    )
    print(f"Sent to {email}")
```

## Cost Estimate

- **1,000 subscribers**: ~$0.00
- **10,000 emails/month**: ~$1.00
- **100,000 emails/month**: ~$10.00

## Summary

This gives you:
- ✅ Full control over subscriber data
- ✅ Unlimited subscribers
- ✅ Very low cost
- ✅ Professional confirmation emails
- ✅ Integration with your AWS infrastructure
- ✅ Ability to send custom newsletters
