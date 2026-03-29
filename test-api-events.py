import requests
import json
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_BASE = 'https://olmcyxwc1a.execute-api.us-east-1.amazonaws.com/prod/user-email'

print("📊 Testing get_recent_events API endpoint...")
print("="*80)

response = requests.get(f"{API_BASE}?action=get_recent_events&limit=100")
data = response.json()

events = data.get('events', [])
print(f"\n✅ API returned {len(events)} events\n")

# Sort by timestamp
events.sort(key=lambda x: x.get('timestamp', 0), reverse=True)

# Show first 20
print("First 20 events (most recent):")
print("="*80)
for i, e in enumerate(events[:20]):
    timestamp = e.get('timestamp', 0)
    date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'unknown'
    event_type = e.get('event_type', 'unknown')
    email = e.get('subscriber_email', e.get('email', 'unknown'))
    campaign_id = e.get('campaign_id', 'unknown')[:20]
    
    print(f"{i+1:2}. {date_str} | {event_type:10} | {email:30} | {campaign_id}")

# Check for election-map events
print("\n" + "="*80)
print("Checking for ALL election-map events in the 100 returned...")
print("="*80)

# Known election-map campaign ID
election_campaign_id = '40aee2fb-951b-4563-9034-a043da9a9e05'
election_events = [e for e in events if e.get('campaign_id') == election_campaign_id]

print(f"\n✅ Found {len(election_events)} events for Transition #1 (40aee2fb...) in the 100 returned")
if election_events:
    print("\nAll election-map events:")
    for e in election_events:
        timestamp = e.get('timestamp', 0)
        date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'unknown'
        event_type = e.get('event_type', 'unknown')
        email = e.get('subscriber_email', e.get('email', 'unknown'))
        print(f"  - {date_str} | {event_type:10} | {email}")
