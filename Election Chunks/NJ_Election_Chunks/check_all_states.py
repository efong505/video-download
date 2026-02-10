import boto3
from collections import Counter

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# Get all races
races = races_table.scan()['Items']
race_states = Counter([r.get('state', 'Unknown') for r in races])

# Get all candidates
candidates = candidates_table.scan()['Items']
candidate_states = Counter([c.get('state', 'Unknown') for c in candidates])

print("RACES BY STATE:")
for state, count in sorted(race_states.items()):
    print(f"  {state}: {count} races")
print(f"\nTOTAL RACES: {len(races)}")

print("\n" + "="*50)
print("\nCANDIDATES BY STATE:")
for state, count in sorted(candidate_states.items()):
    print(f"  {state}: {count} candidates")
print(f"\nTOTAL CANDIDATES: {len(candidates)}")
