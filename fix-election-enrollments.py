import boto3
import sys
from datetime import datetime, timedelta
from decimal import Decimal

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
enrollments_table = dynamodb.Table('user-email-drip-enrollments')
campaigns_table = dynamodb.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Get all election-map enrollments
print("📧 Fetching election-map enrollments...")
enrollments_response = enrollments_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
)

election_enrollments = [e for e in enrollments_response['Items'] 
                       if e.get('campaign_group') == 'election-map-transition-sequence']

print(f"✅ Found {len(election_enrollments)} election-map enrollments\n")

# Get all campaigns in the election-map group
campaigns_response = campaigns_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
)

election_campaigns = sorted(
    [c for c in campaigns_response['Items'] 
     if c.get('campaign_group') == 'election-map-transition-sequence'],
    key=lambda x: int(x.get('sequence_number', 0))
)

total_steps = len(election_campaigns)
print(f"📊 Total steps in sequence: {total_steps}\n")

# Display campaigns
for c in election_campaigns:
    seq = int(c.get('sequence_number', 0))
    name = c.get('campaign_name', 'Unknown')
    delay = int(c.get('delay_days', 0))
    print(f"  Step {seq}: {name} (delay: {delay} days)")

print("\n" + "="*60)
print("FIXING ENROLLMENTS")
print("="*60 + "\n")

# Fix each enrollment
for enrollment in election_enrollments:
    enrollment_id = enrollment['enrollment_id']
    email = enrollment.get('subscriber_email', 'unknown')
    current_step = int(enrollment.get('current_step', 0)) if enrollment.get('current_step') else 0
    
    print(f"\n📧 {email}")
    print(f"  Current: Step {current_step}/{total_steps}")
    
    # Email #1 was already sent, so current_step should be 1
    new_current_step = 1
    
    # Find the next email (Email #2)
    next_campaign = None
    for c in election_campaigns:
        if int(c.get('sequence_number', 0)) == new_current_step + 1:
            next_campaign = c
            break
    
    if next_campaign:
        # Calculate next_send_at based on Email #2's delay (2 days from now)
        delay_days = int(next_campaign.get('delay_days', 2))
        next_send_dt = datetime.now() + timedelta(days=delay_days)
        next_send_timestamp = int(next_send_dt.timestamp())
        
        print(f"  → Updating to: Step {new_current_step}/{total_steps}")
        print(f"  → Next email: {next_campaign.get('campaign_name')} (in {delay_days} days)")
        print(f"  → Next send: {next_send_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Update enrollment
        enrollments_table.update_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'enrollment_id': enrollment_id},
            UpdateExpression='SET current_step = :step, total_steps = :total, next_send_at = :next, last_sent_at = :last',
            ExpressionAttributeValues={
                ':step': new_current_step,
                ':total': total_steps,
                ':next': next_send_timestamp,
                ':last': int(datetime.now().timestamp())
            }
        )
        print("  ✅ Updated!")
    else:
        print(f"  ⚠️  No next email found (sequence complete)")

print("\n" + "="*60)
print("✅ ALL ENROLLMENTS FIXED!")
print("="*60)
