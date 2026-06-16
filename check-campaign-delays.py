import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

campaigns_table = dynamodb.Table('user-email-campaigns')
response = campaigns_table.query(
    KeyConditionExpression='user_id = :uid',
    FilterExpression='campaign_group = :cg',
    ExpressionAttributeValues={
        ':uid': PLATFORM_OWNER_ID,
        ':cg': 'general-newsletter-sequence'
    }
)

campaigns = sorted(response['Items'], key=lambda x: x.get('sequence_number', 0))

print("\n=== General Newsletter Sequence Campaigns ===")
for c in campaigns:
    print(f"\nStep {c.get('sequence_number')}: {c.get('campaign_name', 'N/A')}")
    print(f"  Campaign ID: {c['campaign_id'][:8]}...")
    print(f"  Subject: {c.get('subject', 'N/A')}")
    print(f"  Delay Days: {c.get('delay_days', 'NOT SET')}")
    print(f"  Delay Hours: {c.get('delay_hours', 'NOT SET')}")
