import requests
import json
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_BASE = 'https://olmcyxwc1a.execute-api.us-east-1.amazonaws.com/prod/user-email'

print("📊 Testing API response timestamps...")
print("="*80)

response = requests.get(f"{API_BASE}?action=get_recent_events&limit=20")
data = response.json()

events = data.get('events', [])
print(f"\n✅ API returned {len(events)} events\n")

print("First 20 events with raw timestamp values:")
print("="*80)
for i, e in enumerate(events[:20]):
    timestamp = e.get('timestamp')
    timestamp_type = type(timestamp).__name__
    event_type = e.get('event_type', 'unknown')
    email = e.get('subscriber_email', e.get('email', 'unknown'))[:30]
    campaign_id = e.get('campaign_id', 'unknown')[:20]
    
    # Try to parse the timestamp
    try:
        if isinstance(timestamp, (int, float)):
            date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        else:
            date_str = f"Can't parse ({timestamp_type})"
    except:
        date_str = "Parse error"
    
    print(f"{i+1:2}. TS={timestamp} ({timestamp_type:5}) | {date_str} | {event_type:10} | {email}")
