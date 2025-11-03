import boto3
from collections import defaultdict

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

print("Scanning Pennsylvania candidates...")
response = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Pennsylvania'}
)

candidates = response['Items']
print(f"Found {len(candidates)} total candidates\n")

# Group by name+office to find duplicates
groups = defaultdict(list)
for c in candidates:
    key = (c.get('name', ''), c.get('office', ''))
    groups[key].append(c)

# Find and remove duplicates
duplicates_removed = 0
for (name, office), items in groups.items():
    if len(items) > 1:
        print(f"DUPLICATE: {name} - {office} ({len(items)} copies)")
        # Keep the first one, delete the rest
        for item in items[1:]:
            candidates_table.delete_item(Key={'candidate_id': item['candidate_id']})
            print(f"  Deleted: {item['candidate_id']}")
            duplicates_removed += 1

print(f"\n[SUCCESS] Removed {duplicates_removed} duplicate candidates")
print(f"Remaining: {len(candidates) - duplicates_removed} unique candidates")
