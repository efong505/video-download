import boto3
import sys

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

# Get state from command line or prompt
if len(sys.argv) > 1:
    state = sys.argv[1]
else:
    state = input("Enter state name: ").strip()

print(f"Fixing orphaned candidates for {state}...")

# Get all candidates for the state
candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': state}
)['Items']

# Find candidates with empty or missing race_id
orphaned = [c for c in candidates if not c.get('race_id') or c.get('race_id') == '']

print(f"\nFound {len(orphaned)} orphaned candidates:")
for c in orphaned:
    print(f"  - {c['name']} ({c['office']})")

if len(orphaned) == 0:
    print("\nNo orphaned candidates found!")
else:
    print(f"\nTo fix these, you need to:")
    print(f"1. Verify the office names match races exactly")
    print(f"2. Run smart_fix_race_ids.py to auto-match")
    print(f"3. Or manually update race_id for each candidate")
