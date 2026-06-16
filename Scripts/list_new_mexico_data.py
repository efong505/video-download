import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# Get New Mexico races
races_response = races_table.scan(FilterExpression='#s = :state',
                                  ExpressionAttributeNames={'#s': 'state'},
                                  ExpressionAttributeValues={':state': 'New Mexico'})
races = races_response['Items']

# Get New Mexico candidates
candidates_response = candidates_table.scan(FilterExpression='#s = :state',
                                           ExpressionAttributeNames={'#s': 'state'},
                                           ExpressionAttributeValues={':state': 'New Mexico'})
candidates = candidates_response['Items']

print(f"NEW MEXICO DATABASE:\n")
print(f"Total Races: {len(races)}")
print(f"Total Candidates: {len(candidates)}\n")

print("RACES:")
for race in sorted(races, key=lambda x: x.get('office', '')):
    print(f"  - {race.get('office', 'N/A')} - {race.get('district', '')} (ID: {race.get('race_id', 'N/A')[:8]}...)")

print(f"\nCANDIDATES:")
for cand in sorted(candidates, key=lambda x: x.get('name', '')):
    race = next((r for r in races if r.get('race_id') == cand.get('race_id')), {})
    race_name = f"{race.get('office', 'Unknown')} {race.get('district', '')}".strip()
    print(f"  - {cand.get('name')} ({cand.get('party', 'N/A')}) - {race_name}")
