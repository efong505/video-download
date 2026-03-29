import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

# Check the new email marketing subscribers table
subscribers_table = dynamodb.Table('user-email-subscribers')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Query all subscribers for platform owner
response = subscribers_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
)

subscribers = response['Items']

# Find ekewaka@gmail.com
ekewaka_subs = [s for s in subscribers if s.get('subscriber_email') == 'ekewaka@gmail.com']

if ekewaka_subs:
    print("✅ Found ekewaka@gmail.com in user-email-subscribers table:")
    print("-" * 80)
    for sub in ekewaka_subs:
        for key, value in sorted(sub.items()):
            print(f"   {key}: {value}")
else:
    print("❌ ekewaka@gmail.com NOT found in user-email-subscribers table")
    print(f"\n📋 Total subscribers in new system: {len(subscribers)}")
    print("\nShowing all subscriber emails:")
    for sub in sorted(subscribers, key=lambda x: x.get('subscriber_email', '')):
        print(f"   - {sub.get('subscriber_email')}")
