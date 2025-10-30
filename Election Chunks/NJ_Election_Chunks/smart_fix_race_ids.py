import boto3
import re

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

races = races_table.scan(FilterExpression='#s = :state', ExpressionAttributeNames={'#s': 'state'}, ExpressionAttributeValues={':state': 'New Jersey'})['Items']
candidates = candidates_table.scan(FilterExpression='#s = :state', ExpressionAttributeNames={'#s': 'state'}, ExpressionAttributeValues={':state': 'New Jersey'})['Items']

race_map = {r['office']: r['race_id'] for r in races}

def normalize_office(office):
    # Convert "Board of Education At-Large Seat X" to "School Board Seat X"
    office = office.replace('Board of Education At-Large', 'School Board')
    office = office.replace('Board of Education Ward', 'School Board')
    office = office.replace('Board of Education', 'School Board')
    # Remove extra spaces
    office = re.sub(r'\s+', ' ', office).strip()
    return office

fixed = 0
for candidate in candidates:
    office = candidate['office']
    normalized = normalize_office(office)
    
    if normalized in race_map:
        correct_race_id = race_map[normalized]
        if candidate.get('race_id') != correct_race_id:
            candidate['race_id'] = correct_race_id
            candidates_table.put_item(Item=candidate)
            print(f"Fixed: {candidate['name']}")
            print(f"  {office} -> {normalized}")
            fixed += 1

print(f"\n{fixed} candidates fixed")
