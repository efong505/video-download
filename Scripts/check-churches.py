import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')

API_URL = 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/resources'

print("Fetching all resources...")
response = requests.get(f"{API_URL}?action=list")
all_resources = response.json()

# Filter for church resources
churches = [r for r in all_resources if r.get('category') and any('Church' in str(c) or 'church' in str(c).lower() for c in (r['category'] if isinstance(r['category'], list) else [r['category']]))]

print(f"\nTotal church resources: {len(churches)}")

if churches:
    print("\nChurch resources:")
    for r in churches:
        print(f"\n  Name: {r.get('name')}")
        print(f"  Category: {r.get('category')}")
        print(f"  Subcategory: {r.get('subcategory')}")
