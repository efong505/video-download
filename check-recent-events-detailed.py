import boto3
import sys
from datetime import datetime
from decimal import Decimal

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
events_table = dynamodb.Table('user-email-events')
campaigns_table = dynamodb.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Get all events and sort by timestamp
print("📊 Fetching ALL events for platform owner...")
all_events = []
response = events_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
)
all_events.extend(response['Items'])

while 'LastEvaluatedKey' in response:
    response = events_table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID},
        ExclusiveStartKey=response['LastEvaluatedKey']
    )
    all_events.extend(response['Items'])

print(f"✅ Found {len(all_events)} total events\n")

# Sort by timestamp descending
all_events.sort(key=lambda x: int(x.get('timestamp', 0)), reverse=True)

# Get campaign names
campaign_map = {}
campaigns_response = campaigns_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
)
for c in campaigns_response['Items']:
    campaign_map[c['campaign_id']] = c.get('campaign_name', c.get('title', 'Unknown'))

# Show last 100 events
print("="*100)
print("LAST 100 EVENTS (Most Recent First)")
print("="*100)
print(f"{'Date/Time':<20} | {'Event Type':<12} | {'Email':<35} | {'Campaign':<30}")
print("="*100)

for i, event in enumerate(all_events[:100]):
    timestamp = int(event.get('timestamp', 0))
    date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'unknown'
    event_type = event.get('event_type', 'unknown')
    email = event.get('subscriber_email', event.get('email', 'unknown'))
    campaign_id = event.get('campaign_id', 'unknown')
    campaign_name = campaign_map.get(campaign_id, campaign_id[:20])
    
    # Highlight election-map events
    marker = "🔴" if 'Transition' in campaign_name else "  "
    
    print(f"{marker} {date_str:<20} | {event_type:<12} | {email:<35} | {campaign_name:<30}")

# Count election-map events in last 100
election_events = [e for e in all_events[:100] if 'Transition' in campaign_map.get(e.get('campaign_id', ''), '')]
print("\n" + "="*100)
print(f"✅ Found {len(election_events)} election-map transition events in last 100 events")
print("="*100)

if election_events:
    print("\nElection-map events breakdown:")
    by_type = {}
    for e in election_events:
        et = e.get('event_type', 'unknown')
        by_type[et] = by_type.get(et, 0) + 1
    for et, count in by_type.items():
        print(f"  - {et}: {count}")
