import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# Find the race_id for U.S. House District 7
print("Finding U.S. House District 7 race...")
response = races_table.scan(
    FilterExpression='#st = :state AND office = :office',
    ExpressionAttributeNames={'#st': 'state'},
    ExpressionAttributeValues={
        ':state': 'Pennsylvania',
        ':office': 'U.S. House District 7'
    }
)

if not response['Items']:
    print("ERROR: U.S. House District 7 race not found!")
    exit(1)

race = response['Items'][0]
race_id = race['race_id']
print(f"Found race_id: {race_id}")

# Find the two candidates
print("\nFinding candidates...")
response = candidates_table.scan(
    FilterExpression='#st = :state AND office = :office',
    ExpressionAttributeNames={'#st': 'state'},
    ExpressionAttributeValues={
        ':state': 'Pennsylvania',
        ':office': 'U.S. House District 7'
    }
)

candidates = response['Items']
print(f"Found {len(candidates)} candidates for U.S. House District 7")

# Update candidates that are missing race_id
updated = 0
for candidate in candidates:
    if not candidate.get('race_id'):
        print(f"\nUpdating {candidate['name']} ({candidate['party']})...")
        candidates_table.update_item(
            Key={'candidate_id': candidate['candidate_id']},
            UpdateExpression='SET race_id = :race_id',
            ExpressionAttributeValues={':race_id': race_id}
        )
        updated += 1
        print(f"  Added race_id: {race_id}")

print(f"\nUpdated {updated} candidates")
print("Candidates should now appear in the main race section, not 'Other Candidates'")
