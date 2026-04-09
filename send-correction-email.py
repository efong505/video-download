import boto3
import os
import json
import uuid
from datetime import datetime

os.environ['AWS_PROFILE'] = 'ekewaka'

db = boto3.resource('dynamodb', region_name='us-east-1')
sqs = boto3.client('sqs', region_name='us-east-1')

events_table = db.Table('user-email-events')
campaigns_table = db.Table('user-email-campaigns')
subscribers_table = db.Table('user-email-subscribers')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Step 1: Get all unique emails that have opened any email
print("Finding all subscribers who have opened emails...")
response = events_table.query(
    KeyConditionExpression='user_id = :uid',
    FilterExpression='event_type = :et',
    ExpressionAttributeValues={
        ':uid': PLATFORM_OWNER_ID,
        ':et': 'opened'
    }
)

openers = set()
for item in response['Items']:
    email = item.get('subscriber_email')
    if email:
        openers.add(email)

# Handle pagination
while 'LastEvaluatedKey' in response:
    response = events_table.query(
        KeyConditionExpression='user_id = :uid',
        FilterExpression='event_type = :et',
        ExpressionAttributeValues={
            ':uid': PLATFORM_OWNER_ID,
            ':et': 'opened'
        },
        ExclusiveStartKey=response['LastEvaluatedKey']
    )
    for item in response['Items']:
        email = item.get('subscriber_email')
        if email:
            openers.add(email)

print(f"Found {len(openers)} unique subscribers who have opened emails")

# Step 2: Filter to only active subscribers
print("Filtering to active subscribers...")
active_recipients = []
for email in openers:
    try:
        sub_response = subscribers_table.get_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'subscriber_email': email}
        )
        if 'Item' in sub_response:
            sub = sub_response['Item']
            if sub.get('status') == 'active':
                active_recipients.append(email)
    except:
        pass

print(f"Found {len(active_recipients)} active subscribers")

if len(active_recipients) == 0:
    print("No active recipients found. Exiting.")
    exit()

# Step 3: Create the correction campaign
campaign_id = str(uuid.uuid4())
subject = "Quick correction - Reply email address"

html_content = """<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
<p>Hey {{first_name}},</p>

<p>Quick heads up:</p>

<p>If you tried to reply to any of my recent emails, you might have gotten a bounce.</p>

<p>The reply-to address was set incorrectly to <code>super@admin.com</code> (a test account).</p>

<p><strong>The correct email is:</strong><br>
<a href="mailto:contact@christianconservativestoday.com">contact@christianconservativestoday.com</a></p>

<p>This has been fixed going forward, but if you tried to reach out and didn't hear back, that's why.</p>

<p>Feel free to reply to this email — it'll come straight to me.</p>

<p>Thanks for your patience!</p>

<p>— Ed</p>

<hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

<p style="font-size: 12px; color: #999;">
Christian Conservatives Today<br>
<a href="{{unsubscribe_link}}" style="color: #999;">Unsubscribe</a>
</p>
</div>"""

print(f"\nCreating campaign: {subject}")
campaigns_table.put_item(Item={
    'user_id': PLATFORM_OWNER_ID,
    'campaign_id': campaign_id,
    'campaign_name': 'Email Correction - Reply Address',
    'subject': subject,
    'html_content': html_content,
    'status': 'draft',
    'created_at': datetime.now().isoformat(),
    'updated_at': datetime.now().isoformat()
})

print(f"Campaign created: {campaign_id}")

# Step 4: Send to SQS queue
print(f"\nSending to {len(active_recipients)} recipients via SQS...")
sqs.send_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/371751795928/email-sending-queue',
    MessageBody=json.dumps({
        'user_id': PLATFORM_OWNER_ID,
        'campaign_id': campaign_id,
        'recipients': active_recipients
    })
)

print("Message sent to SQS queue!")
print(f"\nSummary:")
print(f"  Campaign ID: {campaign_id}")
print(f"  Recipients: {len(active_recipients)}")
print(f"  Subject: {subject}")
print("\nEmails will be sent by the email-sender Lambda within a few minutes.")
