import sys
import requests
import time

sys.stdout.reconfigure(encoding='utf-8')

API_URL = 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/resources'

print("Fetching all resources...")
response = requests.get(f"{API_URL}?action=list")
all_resources = response.json()

# Filter for pro-life resources
prolife = [r for r in all_resources if r.get('category') and any('Pro-Life' in str(c) for c in (r['category'] if isinstance(r['category'], list) else [r['category']]))]

print(f"Found {len(prolife)} pro-life resources to delete\n")

deleted = 0
failed = 0

for resource in prolife:
    resource_id = resource.get('id') or resource.get('resource_id')
    if not resource_id:
        continue
    
    try:
        response = requests.delete(f"{API_URL}?action=delete&resource_id={resource_id}")
        if response.status_code == 200:
            deleted += 1
            if deleted % 50 == 0:
                print(f"Deleted {deleted}/{len(prolife)}...")
        else:
            failed += 1
            print(f"❌ Failed to delete {resource_id}")
        time.sleep(0.1)
    except Exception as e:
        failed += 1
        print(f"❌ Error deleting {resource_id}: {e}")

print(f"\n✅ Deletion complete!")
print(f"Deleted: {deleted} | Failed: {failed}")
