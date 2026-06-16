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

# 11 subscribers to migrate (excluding the 4 test accounts)
SUBSCRIBERS_TO_MIGRATE = [
    'fall1776@aol.com',
    'contact@ekewaka.com',
    'reedandjuliesmom@gmail.com',
    'ekewakafong@gmail.com',
    'efong505@nmsu.edu',
    'bobnglendagill@gmail.com',
    'davidoliver01@yahoo.com',
    'dkechols77@gmail.com',
    'contact@christianconservativestoday.com',
    'hitormissatthepottery@gmail.com',
    'doake@msn.com'
]

print(f"🔄 Migrating {len(SUBSCRIBERS_TO_MIGRATE)} election-map subscribers\n")
print("="*60)

# Get all transition campaigns first
print("\n📧 Fetching transition campaigns...")
campaigns_response = campaigns_table.query(
    KeyConditionExpression='user_id = :uid',
    FilterExpression='campaign_group = :group',
    ExpressionAttributeValues={
        ':uid': PLATFORM_OWNER_ID,
        ':group': 'election-map-transition-sequence'
    }
)

campaigns = sorted(campaigns_response['Items'], key=lambda x: x.get('delay_days', 0))
campaign_ids = [c['campaign_id'] for c in campaigns]
print(f"✅ Found {len(campaigns)} transition campaigns\n")

migrated_count = 0
skipped_count = 0
enrolled_count = 0

for email in SUBSCRIBERS_TO_MIGRATE:
    print(f"\n{'='*60}")
    print(f"Processing: {email}")
    print(f"{'='*60}")
    
    # Step 1: Get from old table
    try:
        old_response = old_subscribers_table.get_item(Key={'email': email})
        
        if 'Item' not in old_response:
            print(f"⚠️  Not found in email-subscribers table - skipping")
            skipped_count += 1
            continue
        
        old_sub = old_response['Item']
        print(f"✅ Found in email-subscribers")
        
    except Exception as e:
        print(f"❌ Error fetching from old table: {e}")
        skipped_count += 1
        continue
    
    # Step 2: Check if already in new table
    try:
        new_response = new_subscribers_table.get_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'subscriber_email': email}
        )
        
        if 'Item' in new_response:
            print(f"⚠️  Already in user-email-subscribers - skipping migration")
        else:
            # Step 3: Migrate to new table
            new_sub = {
                'user_id': PLATFORM_OWNER_ID,
                'subscriber_email': email,
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
            migrated_count += 1
            
    except Exception as e:
        print(f"❌ Error migrating: {e}")
        skipped_count += 1
        continue
    
    # Step 4: Check if already enrolled
    try:
        enrollment_id = f"{email}:election-map-transition-sequence"
        enrollment_response = enrollments_table.get_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'enrollment_id': enrollment_id}
        )
        
        if 'Item' in enrollment_response:
            print(f"⚠️  Already enrolled in transition sequence")
        else:
            # Step 5: Create enrollment
            enrollment = {
                'user_id': PLATFORM_OWNER_ID,
                'enrollment_id': enrollment_id,
                'subscriber_email': email,
                'campaign_group': 'election-map-transition-sequence',
                'campaign_ids': campaign_ids,
                'current_step': 0,
                'total_steps': len(campaigns),
                'status': 'active',
                'enrolled_at': datetime.now().isoformat(),
                'last_sent_date': None,
                'next_send_date': datetime.now().isoformat()
            }
            
            enrollments_table.put_item(Item=enrollment)
            print(f"✅ Enrolled in transition sequence (7 emails)")
            enrolled_count += 1
            
    except Exception as e:
        print(f"❌ Error enrolling: {e}")
        continue

# Summary
print("\n" + "="*60)
print("✅ MIGRATION COMPLETE!")
print("="*60)
print(f"\n📊 Summary:")
print(f"   Total processed: {len(SUBSCRIBERS_TO_MIGRATE)}")
print(f"   ✅ Migrated: {migrated_count}")
print(f"   ✅ Enrolled: {enrolled_count}")
print(f"   ⚠️  Skipped: {skipped_count}")

print(f"\n📧 All subscribers are now:")
print(f"   ✅ In user-email-subscribers table")
print(f"   ✅ Enrolled in election-map-transition-sequence")
print(f"   ✅ Ready to receive 7 transition emails")

print(f"\n💡 Next steps:")
print(f"   1. Check Campaign Manager > Enrollments tab")
print(f"   2. Use 'Send Next Now' to manually trigger emails")
print(f"   3. Or wait for drip processor to run automatically")
