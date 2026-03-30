import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')

API_URL = 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/resources'

print("Fetching all resources...")
response = requests.get(f"{API_URL}?action=list")
all_resources = response.json()

print(f"\nTotal resources: {len(all_resources)}")

# Filter for pro-life resources
prolife = [r for r in all_resources if r.get('category') and any('Pro-Life' in str(c) or 'pro-life' in str(c).lower() for c in (r['category'] if isinstance(r['category'], list) else [r['category']]))]

print(f"Pro-life resources: {len(prolife)}")

if prolife:
    print("\nFirst 3 pro-life resources:")
    for r in prolife[:3]:
        print(f"\n  Name: {r.get('name')}")
        print(f"  Category: {r.get('category')}")
        print(f"  Subcategory: {r.get('subcategory')}")
        print(f"  State: {r.get('state')}")
        print(f"  City: {r.get('city')}")
