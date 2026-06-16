import boto3
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')
enrollments_table = dynamodb.Table('user-email-drip-enrollments')
events_table = dynamodb.Table('user-email-events')
campaigns_table = dynamodb.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'
email = 'hawaiianintucson@gmail.com'

print(f"\n=== Checking enrollments for {email} ===")
response = enrollments_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
)

general_enrollments = [e for e in response['Items'] if e.get('campaign_group') == 'general-newsletter-sequence']
print(f"\nFound {len(general_enrollments)} general-newsletter-sequence enrollments")
for e in general_enrollments:
    if e.get('subscriber_email') == email:
        print(f"\nEnrollment ID: {e['enrollment_id']}")
        print(f"Status: {e.get('status')}")
        print(f"Current Step: {e.get('current_step')}")
        print(f"Last Sent: {e.get('last_sent_date', 'Never')}")
        print(f"Created: {e.get('created_at')}")

print(f"\n=== Checking recent events for {email} ===")
events_response = events_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID},
    ScanIndexForward=False,
    Limit=50
)

hawaiian_events = [ev for ev in events_response['Items'] if email in ev.get('recipient_email', '')]
print(f"\nFound {len(hawaiian_events)} events for {email}")
for ev in hawaiian_events[-5:]:  # Last 5
    ts = datetime.fromtimestamp(int(ev.get('timestamp', 0)))
    print(f"{ts} - {ev.get('event_type')} - Campaign: {ev.get('campaign_id', 'N/A')[:8]}")

print(f"\n=== Checking general-newsletter-sequence campaigns ===")
campaigns_response = campaigns_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
)

general_campaigns = [c for c in campaigns_response['Items'] if c.get('campaign_group') == 'general-newsletter-sequence']
print(f"\nFound {len(general_campaigns)} campaigns in group")
for c in sorted(general_campaigns, key=lambda x: x.get('sequence_number', 0)):
    print(f"Step {c.get('sequence_number')}: {c['campaign_id'][:8]}... - {c.get('subject', 'No subject')}")
