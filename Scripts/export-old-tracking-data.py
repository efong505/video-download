import requests
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

API_BASE = 'https://niexv1rw75.execute-api.us-east-1.amazonaws.com/subscribe'

print("Exporting data from niexv1rw75 API...")

# Export recent events
print("\n1. Fetching recent events...")
response = requests.get(f"{API_BASE}?action=get_recent_events&limit=1000")
events_data = response.json()
print(f"   ✓ Found {len(events_data.get('events', []))} events")

# Export campaign analytics
print("\n2. Fetching campaign analytics...")
response = requests.get(f"{API_BASE}?action=get_campaign_analytics")
campaign_data = response.json()
print(f"   ✓ Found {len(campaign_data.get('campaigns', []))} campaigns")

# Export analytics overview
print("\n3. Fetching analytics overview...")
response = requests.get(f"{API_BASE}?action=get_analytics_overview")
overview_data = response.json()
print(f"   ✓ Overview data retrieved")

# Export subscriber list
print("\n4. Fetching subscribers...")
response = requests.get(f"{API_BASE}?action=get_subscribers")
subscriber_data = response.json()
print(f"   ✓ Found {len(subscriber_data.get('subscribers', []))} subscribers")

# Save to file
export_data = {
    'events': events_data.get('events', []),
    'campaigns': campaign_data.get('campaigns', []),
    'overview': overview_data,
    'subscribers': subscriber_data.get('subscribers', [])
}

with open('niexv1rw75_export.json', 'w', encoding='utf-8') as f:
    json.dump(export_data, f, indent=2)

print(f"\n✓ Data exported to niexv1rw75_export.json")
print(f"  - {len(export_data['events'])} events")
print(f"  - {len(export_data['campaigns'])} campaigns")
print(f"  - {len(export_data['subscribers'])} subscribers")
