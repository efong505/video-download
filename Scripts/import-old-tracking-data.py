import boto3
import json
import sys
from decimal import Decimal
sys.stdout.reconfigure(encoding='utf-8')

dynamodb = boto3.Session(profile_name='ekewaka', region_name='us-east-1').resource('dynamodb')
events_table = dynamodb.Table('user-email-events')
campaigns_table = dynamodb.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

print("Loading exported data...")
with open('niexv1rw75_export.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"\nFound:")
print(f"  - {len(data['events'])} events")
print(f"  - {len(data['campaigns'])} campaigns")

# Import events
print("\n1. Importing events...")
imported_events = 0
skipped_events = 0

for event in data['events']:
    try:
        # Check if event already exists
        event_id = event.get('event_id')
        if not event_id:
            skipped_events += 1
            continue
            
        existing = events_table.get_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'event_id': event_id}
        )
        
        if 'Item' in existing:
            skipped_events += 1
            continue
        
        # Prepare item for DynamoDB
        item = {
            'user_id': PLATFORM_OWNER_ID,
            'event_id': event_id,
            'event_type': event.get('event_type', 'opened'),
            'campaign_id': event.get('campaign_id', ''),
            'subscriber_email': event.get('subscriber_email', event.get('email', '')),
            'timestamp': int(event.get('timestamp', 0)),
            'date': event.get('date', '')
        }
        
        # Add optional fields
        if 'url' in event:
            item['url'] = event['url']
        if 'ip_address' in event:
            item['ip_address'] = event['ip_address']
        
        events_table.put_item(Item=item)
        imported_events += 1
        
        if imported_events % 10 == 0:
            print(f"   Imported {imported_events} events...")
            
    except Exception as e:
        print(f"   Error importing event {event.get('event_id')}: {e}")
        skipped_events += 1

print(f"   ✓ Imported {imported_events} events, skipped {skipped_events}")

# Import campaigns
print("\n2. Importing campaigns...")
imported_campaigns = 0
skipped_campaigns = 0

for campaign in data['campaigns']:
    try:
        campaign_id = campaign.get('campaign_id')
        if not campaign_id:
            skipped_campaigns += 1
            continue
            
        # Check if campaign already exists
        existing = campaigns_table.get_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'campaign_id': campaign_id}
        )
        
        if 'Item' in existing:
            skipped_campaigns += 1
            continue
        
        # Prepare item
        item = {
            'user_id': PLATFORM_OWNER_ID,
            'campaign_id': campaign_id,
            'title': campaign.get('title', campaign.get('name', 'Imported Campaign')),
            'subject': campaign.get('subject', ''),
            'content': campaign.get('content', ''),
            'status': 'sent',
            'created_at': campaign.get('created_at', ''),
            'recipient_count': int(campaign.get('sent', 0)),
            'open_count': int(campaign.get('opens', 0)),
            'click_count': int(campaign.get('clicks', 0))
        }
        
        campaigns_table.put_item(Item=item)
        imported_campaigns += 1
        
    except Exception as e:
        print(f"   Error importing campaign {campaign.get('campaign_id')}: {e}")
        skipped_campaigns += 1

print(f"   ✓ Imported {imported_campaigns} campaigns, skipped {skipped_campaigns}")

print(f"\n✓ Import complete!")
print(f"  Total events: {imported_events}")
print(f"  Total campaigns: {imported_campaigns}")
