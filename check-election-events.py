import boto3
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
events_table = dynamodb.Table('user-email-events')
campaigns_table = dynamodb.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Get all election-map campaigns
print("📧 Fetching election-map campaigns...")
campaigns_response = campaigns_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
)

election_campaigns = [c for c in campaigns_response['Items'] 
                     if c.get('campaign_group') == 'election-map-transition-sequence']

print(f"\n✅ Found {len(election_campaigns)} election-map campaigns:")
for c in election_campaigns:
    print(f"  - {c['campaign_name']} ({c['campaign_id'][:8]}...)")

# Check events for each campaign
print("\n📊 Checking events for each campaign...")
for campaign in election_campaigns:
    campaign_id = campaign['campaign_id']
    campaign_name = campaign['campaign_name']
    
    # Query events by campaign_id using GSI
    try:
        events_response = events_table.query(
            IndexName='campaign-index',
            KeyConditionExpression='campaign_id = :cid',
            ExpressionAttributeValues={':cid': campaign_id}
        )
        
        events = events_response['Items']
        
        if events:
            print(f"\n✅ {campaign_name}: {len(events)} events")
            event_types = {}
            for e in events:
                event_type = e.get('event_type', 'unknown')
                event_types[event_type] = event_types.get(event_type, 0) + 1
            
            for event_type, count in event_types.items():
                print(f"   - {event_type}: {count}")
        else:
            print(f"\n❌ {campaign_name}: NO EVENTS FOUND")
            
    except Exception as e:
        print(f"\n❌ Error querying events for {campaign_name}: {e}")

# Also check by user_id to see all events
print("\n\n📊 Checking ALL events for platform owner...")
all_events_response = events_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID},
    ScanIndexForward=False,
    Limit=20
)

print(f"\n✅ Found {len(all_events_response['Items'])} recent events (showing last 20):")
for event in all_events_response['Items']:
    event_type = event.get('event_type', 'unknown')
    email = event.get('subscriber_email', event.get('email', 'unknown'))
    campaign_id = event.get('campaign_id', 'unknown')[:8]
    timestamp = int(event.get('timestamp', 0)) if event.get('timestamp') else 0
    date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'unknown'
    
    print(f"  - {date_str} | {event_type:10} | {email:30} | campaign: {campaign_id}...")
