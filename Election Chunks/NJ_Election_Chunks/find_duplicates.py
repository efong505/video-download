import boto3
from collections import Counter

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

# Get all NJ candidates
candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'New Jersey'}
)['Items']

print(f"Total NJ candidates: {len(candidates)}\n")

# Check for duplicate names
names = Counter([c['name'] for c in candidates])
duplicates = {name: count for name, count in names.items() if count > 1}

if duplicates:
    print("DUPLICATE NAMES:")
    for name, count in sorted(duplicates.items()):
        print(f"  {name}: {count} times")
        # Show offices for this name
        offices = [c['office'] for c in candidates if c['name'] == name]
        for office in offices:
            print(f"    - {office}")
else:
    print("No duplicate names found")

print(f"\nUnique candidates: {len(names)}")
