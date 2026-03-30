import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')

API_URL = 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/resources'

print("Fetching all resources...")
response = requests.get(f"{API_URL}?action=list")
all_resources = response.json()

# Filter for Albuquerque
albuquerque = [r for r in all_resources if r.get('city') and 'albuquerque' in r.get('city', '').lower()]

print(f"\nAlbuquerque resources: {len(albuquerque)}")

if albuquerque:
    for r in albuquerque:
        print(f"\n  Name: {r.get('name')}")
        print(f"  Subcategory: {r.get('subcategory')}")
        print(f"  State: {r.get('state')}")
        print(f"  City: {r.get('city')}")
else:
    print("\nNo Albuquerque resources found!")
    
# Check New Mexico
print("\n\n--- New Mexico resources ---")
nm = [r for r in all_resources if r.get('state') == 'New Mexico']
print(f"New Mexico resources: {len(nm)}")
for r in nm:
    print(f"  {r.get('city')} - {r.get('name')}")
