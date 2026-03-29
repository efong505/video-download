import boto3
from datetime import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

# Check subscribers table
subscribers_table = dynamodb.Table('user-email-subscribers')
enrollments_table = dynamodb.Table('user-email-drip-enrollments')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Get all subscribers
response = subscribers_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
)

subscribers = response['Items']

# Find ekewaka@gmail.com
ekewaka_sub = [s for s in subscribers if s.get('subscriber_email') == 'ekewaka@gmail.com']

if ekewaka_sub:
    print("✅ Subscription found in database:")
    sub = ekewaka_sub[0]
    for key, value in sorted(sub.items()):
        print(f"   {key}: {value}")
    
    # Check enrollments
    print("\n📧 Checking enrollments...")
    enroll_response = enrollments_table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
    )
    
    ekewaka_enrollments = [e for e in enroll_response['Items'] if e.get('subscriber_email') == 'ekewaka@gmail.com']
    
    if ekewaka_enrollments:
        print(f"   Found {len(ekewaka_enrollments)} enrollment(s):")
        for enroll in ekewaka_enrollments:
            print(f"   - Campaign Group: {enroll.get('campaign_group')}")
            print(f"     Status: {enroll.get('status')}")
            print(f"     Step: {enroll.get('current_step')}/{enroll.get('total_steps')}")
    else:
        print("   ❌ No enrollments found")
else:
    print("❌ Subscription NOT found in database")
    print("\nShowing last 5 subscribers:")
    for sub in subscribers[:5]:
        email = sub.get('subscriber_email')
        subscribed_at = sub.get('subscribed_at', 'N/A')
        print(f"   - {email} (subscribed: {subscribed_at})")
