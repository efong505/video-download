import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
campaigns_table = dynamodb.Table('user-email-campaigns')
events_table = dynamodb.Table('user-email-events')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Get Transition #1 campaign
campaigns_response = campaigns_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
)

transition_1 = None
for c in campaigns_response['Items']:
    if c.get('campaign_name') == 'Transition #1 - Welcome Back':
        transition_1 = c
        break

if transition_1:
    print(f"✅ Found Transition #1 campaign:")
    print(f"   Campaign ID: {transition_1['campaign_id']}")
    print(f"   Campaign Name: {transition_1.get('campaign_name')}")
    print(f"   Campaign Group: {transition_1.get('campaign_group')}")
    
    # Get events for this campaign
    events_response = events_table.query(
        IndexName='campaign-index',
        KeyConditionExpression='campaign_id = :cid',
        ExpressionAttributeValues={':cid': transition_1['campaign_id']}
    )
    
    events = events_response['Items']
    print(f"\n✅ Found {len(events)} events for this campaign:")
    for e in events:
        event_type = e.get('event_type')
        email = e.get('subscriber_email', 'unknown')
        print(f"   - {event_type:10} | {email}")
else:
    print("❌ Transition #1 campaign not found")

# Also check what campaign IDs are in recent events
print("\n" + "="*60)
print("Checking recent events...")
print("="*60)

all_events_response = events_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID},
    ScanIndexForward=False,
    Limit=50
)

# Group by campaign_id
by_campaign = {}
for e in all_events_response['Items']:
    cid = e.get('campaign_id', 'unknown')
    if cid not in by_campaign:
        by_campaign[cid] = 0
    by_campaign[cid] += 1

print(f"\n✅ Found {len(by_campaign)} unique campaign IDs in recent events:")
for cid, count in sorted(by_campaign.items(), key=lambda x: x[1], reverse=True):
    # Try to find campaign name
    try:
        camp = campaigns_table.get_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'campaign_id': cid}
        ).get('Item')
        name = camp.get('campaign_name', camp.get('title', 'Unknown')) if camp else 'Not found in campaigns table'
    except:
        name = 'Error fetching'
    
    print(f"   {cid[:20]:20} | {count:3} events | {name}")
