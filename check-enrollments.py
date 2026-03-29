import boto3
import sys
from datetime import datetime
from decimal import Decimal

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
enrollments_table = dynamodb.Table('user-email-drip-enrollments')
campaigns_table = dynamodb.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Get all enrollments
print("📧 Fetching all drip enrollments...")
enrollments_response = enrollments_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
)

enrollments = enrollments_response['Items']
print(f"\n✅ Found {len(enrollments)} total enrollments")

# Filter for election-map enrollments
election_enrollments = [e for e in enrollments 
                       if e.get('campaign_group') == 'election-map-transition-sequence']

print(f"✅ Found {len(election_enrollments)} election-map enrollments\n")

# Group by email
by_email = {}
for e in election_enrollments:
    email = e.get('subscriber_email', 'unknown')
    if email not in by_email:
        by_email[email] = []
    by_email[email].append(e)

# Display status for each subscriber
for email, enrollments_list in sorted(by_email.items()):
    print(f"\n📧 {email}")
    for enrollment in enrollments_list:
        status = enrollment.get('status', 'unknown')
        current_step = int(enrollment.get('current_step', 0)) if enrollment.get('current_step') else 0
        total_steps = int(enrollment.get('total_steps', 0)) if enrollment.get('total_steps') else 0
        last_sent = enrollment.get('last_sent_at', 'never')
        next_send = enrollment.get('next_send_at', 'unknown')
        
        # Convert timestamps to readable dates
        if last_sent != 'never' and isinstance(last_sent, (int, Decimal)):
            last_sent = datetime.fromtimestamp(int(last_sent)).strftime('%Y-%m-%d %H:%M:%S')
        if next_send != 'unknown' and isinstance(next_send, (int, Decimal)):
            next_send = datetime.fromtimestamp(int(next_send)).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"  Status: {status} | Step: {current_step}/{total_steps} | Last: {last_sent} | Next: {next_send}")

# Check if any are stuck
print("\n\n🔍 Checking for stuck enrollments...")
now = datetime.now().timestamp()
stuck = []
for enrollment in election_enrollments:
    status = enrollment.get('status')
    next_send = enrollment.get('next_send_at')
    
    if status == 'active' and next_send and isinstance(next_send, (int, Decimal)):
        next_send_ts = int(next_send)
        if next_send_ts < now:
            email = enrollment.get('subscriber_email')
            current_step = int(enrollment.get('current_step', 0)) if enrollment.get('current_step') else 0
            days_overdue = (now - next_send_ts) / 86400
            stuck.append((email, current_step, days_overdue))

if stuck:
    print(f"\n❌ Found {len(stuck)} stuck enrollments (next_send_at is in the past):")
    for email, step, days in stuck:
        print(f"  - {email}: Step {step}, {days:.1f} days overdue")
else:
    print("\n✅ No stuck enrollments found")
