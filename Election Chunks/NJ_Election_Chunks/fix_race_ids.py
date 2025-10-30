import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# Get all NJ races
races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'New Jersey'}
)['Items']

# Create race lookup by office name
race_map = {r['office']: r['race_id'] for r in races}

# Get all NJ candidates
candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'New Jersey'}
)['Items']

print(f"Found {len(races)} races and {len(candidates)} candidates\n")

fixed = 0
orphaned = []

for candidate in candidates:
    office = candidate['office']
    current_race_id = candidate.get('race_id', '')
    
    if office in race_map:
        correct_race_id = race_map[office]
        if current_race_id != correct_race_id:
            candidate['race_id'] = correct_race_id
            candidates_table.put_item(Item=candidate)
            print(f"Fixed: {candidate['name']} -> {office}")
            fixed += 1
    else:
        orphaned.append(f"{candidate['name']} - {office}")

print(f"\n{fixed} candidates fixed")
if orphaned:
    print(f"\n{len(orphaned)} orphaned candidates (no matching race):")
    for o in orphaned[:10]:
        print(f"  {o}")
