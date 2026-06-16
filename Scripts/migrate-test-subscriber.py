import boto3
import sys
import uuid
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')

old_subscribers_table = dynamodb.Table('email-subscribers')
new_subscribers_table = dynamodb.Table('user-email-subscribers')
enrollments_table = dynamodb.Table('user-email-drip-enrollments')
campaigns_table = dynamodb.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'
TEST_EMAIL = 'hawaiianintucson@gmail.com'

print(f"🔄 Migrating test subscriber: {TEST_EMAIL}\n")

# Step 1: Get subscriber from old table
print("Step 1: Fetching from email-subscribers table...")
old_response = old_subscribers_table.get_item(Key={'email': TEST_EMAIL})

if 'Item' not in old_response:
    print(f"❌ Email not found in email-subscribers table")
    sys.exit(1)

old_sub = old_response['Item']
print(f"✅ Found: {old_sub.get('email')} (source: {old_sub.get('source')})")

# Step 2: Check if already exists in new table
print("\nStep 2: Checking if already exists in user-email-subscribers...")
new_response = new_subscribers_table.get_item(
    Key={'user_id': PLATFORM_OWNER_ID, 'subscriber_email': TEST_EMAIL}
)

if 'Item' in new_response:
    print(f"⚠️  Already exists in user-email-subscribers (skipping migration)")
else:
    # Step 3: Migrate to new table
    print("\nStep 3: Migrating to user-email-subscribers...")
    new_sub = {
        'user_id': PLATFORM_OWNER_ID,
        'subscriber_email': TEST_EMAIL,
        'first_name': old_sub.get('first_name', ''),
        'last_name': old_sub.get('last_name', ''),
        'phone': old_sub.get('phone', ''),
        'status': 'active',
        'subscribed_at': old_sub.get('subscribed_at', datetime.now().isoformat()),
        'source': 'election-map-migration',
        'tags': ['election-map', 'transition-sequence']
    }
    
    new_subscribers_table.put_item(Item=new_sub)
    print(f"✅ Migrated to user-email-subscribers")

# Step 4: Get all transition campaigns
print("\nStep 4: Fetching transition campaigns...")
campaigns_response = campaigns_table.query(
    KeyConditionExpression='user_id = :uid',
    FilterExpression='campaign_group = :group',
    ExpressionAttributeValues={
        ':uid': PLATFORM_OWNER_ID,
        ':group': 'election-map-transition-sequence'
    }
)

campaigns = sorted(campaigns_response['Items'], key=lambda x: x.get('delay_days', 0))
print(f"✅ Found {len(campaigns)} transition campaigns")

for i, camp in enumerate(campaigns, 1):
    print(f"   {i}. {camp['campaign_name']} (Day {camp.get('delay_days', 0)})")

# Step 5: Check if already enrolled
print("\nStep 5: Checking existing enrollments...")
enrollment_id = f"{PLATFORM_OWNER_ID}:election-map-transition-sequence"
enrollment_response = enrollments_table.get_item(
    Key={'user_id': PLATFORM_OWNER_ID, 'enrollment_id': enrollment_id}
)

if 'Item' in enrollment_response:
    existing = enrollment_response['Item']
    print(f"⚠️  Already enrolled:")
    print(f"   Current step: {existing.get('current_step', 0)}/{existing.get('total_steps', 0)}")
    print(f"   Status: {existing.get('status', 'unknown')}")
    print(f"   Last sent: {existing.get('last_sent_date', 'never')}")
else:
    # Step 6: Create enrollment
    print("\nStep 6: Creating drip enrollment...")
    enrollment = {
        'user_id': PLATFORM_OWNER_ID,
        'enrollment_id': enrollment_id,
        'subscriber_email': TEST_EMAIL,
        'campaign_group': 'election-map-transition-sequence',
        'campaign_ids': [c['campaign_id'] for c in campaigns],
        'current_step': 0,
        'total_steps': len(campaigns),
        'status': 'active',
        'enrolled_at': datetime.now().isoformat(),
        'last_sent_date': None,
        'next_send_date': datetime.now().isoformat()
    }
    
    enrollments_table.put_item(Item=enrollment)
    print(f"✅ Enrolled in transition sequence")
    print(f"   Total emails: {len(campaigns)}")
    print(f"   Current step: 0 (ready to send first email)")
    print(f"   Next send: Immediately (Day 0)")

print("\n" + "="*60)
print("✅ MIGRATION COMPLETE!")
print("="*60)
print(f"\n📧 {TEST_EMAIL} is now:")
print(f"   ✅ In user-email-subscribers table")
print(f"   ✅ Enrolled in election-map-transition-sequence")
print(f"   ✅ Ready to receive 7 transition emails")
print(f"\n💡 Next step: Drip processor will send Email #1 on next run")
print(f"   (or use 'Send Next Now' in Campaign Manager)")
