import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

state = 'Nebraska'

print(f"Deleting all {state} data...")

# Delete races
print(f"\nDeleting {state} races...")
races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': state}
)['Items']
print(f"Found {len(races)} races to delete")
for race in races:
    races_table.delete_item(Key={'race_id': race['race_id']})
    print(f"  Deleted: {race['office']}")
print(f"[SUCCESS] Deleted {len(races)} races")

# Delete candidates
print(f"\nDeleting {state} candidates...")
candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': state}
)['Items']
print(f"Found {len(candidates)} candidates to delete")
for candidate in candidates:
    candidates_table.delete_item(Key={'candidate_id': candidate['candidate_id']})
    print(f"  Deleted: {candidate['name']} - {candidate.get('office', 'N/A')}")
print(f"[SUCCESS] Deleted {len(candidates)} candidates")

# Delete summary
print(f"\nDeleting {state} summary...")
try:
    summaries_table.delete_item(Key={'state': state})
    print(f"[SUCCESS] Deleted {state} summary")
except:
    print(f"No summary found for {state}")

print(f"\n[SUCCESS] All {state} data deleted!")
