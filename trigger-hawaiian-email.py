import boto3
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
sqs = session.client('sqs', region_name='us-east-1')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'
email = 'hawaiianintucson@gmail.com'

# Get first campaign in general-newsletter-sequence
campaigns_table = dynamodb.Table('user-email-campaigns')
response = campaigns_table.query(
    KeyConditionExpression='user_id = :uid',
    FilterExpression='campaign_group = :cg AND sequence_number = :seq',
    ExpressionAttributeValues={
        ':uid': PLATFORM_OWNER_ID,
        ':cg': 'general-newsletter-sequence',
        ':seq': 1
    }
)

if not response['Items']:
    print("❌ No campaign found for sequence #1 in general-newsletter-sequence")
    sys.exit(1)

campaign = response['Items'][0]
print(f"✅ Found campaign: {campaign['campaign_id'][:8]}... - {campaign.get('subject')}")

# Send to SQS
message = {
    'user_id': PLATFORM_OWNER_ID,
    'campaign_id': campaign['campaign_id'],
    'recipients': [email],
    'drip_sequence': True
}

sqs.send_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/371751795928/email-sending-queue',
    MessageBody=json.dumps(message)
)

print(f"✅ Email queued for {email}")
print(f"   Campaign: {campaign.get('campaign_name', 'N/A')}")
print(f"   Subject: {campaign.get('subject', 'N/A')}")
