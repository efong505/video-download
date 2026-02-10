import boto3
import re
import sys

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# Get state from command line or prompt
if len(sys.argv) > 1:
    state = sys.argv[1]
else:
    state = input("Enter state name: ").strip()

print(f"Smart-fixing race IDs for {state}...")

# Get all races and candidates for the state
races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': state}
)['Items']

candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': state}
)['Items']

# Create race map
race_map = {r['office']: r['race_id'] for r in races}

def normalize_office(office):
    """Normalize office names for matching"""
    # Common variations
    office = office.replace('Board of Education At-Large', 'School Board')
    office = office.replace('Board of Education Ward', 'School Board')
    office = office.replace('Board of Education', 'School Board')
    office = office.replace('Public Schools', 'School')
    # Remove extra spaces
    office = re.sub(r'\s+', ' ', office).strip()
    return office

fixed = 0
not_found = []

for candidate in candidates:
    office = candidate['office']
    
    # Try exact match first
    if office in race_map:
        correct_race_id = race_map[office]
        if candidate.get('race_id') != correct_race_id:
            candidate['race_id'] = correct_race_id
            candidates_table.put_item(Item=candidate)
            print(f"✓ Fixed: {candidate['name']} ({office})")
            fixed += 1
    else:
        # Try normalized match
        normalized = normalize_office(office)
        if normalized in race_map:
            correct_race_id = race_map[normalized]
            if candidate.get('race_id') != correct_race_id:
                candidate['race_id'] = correct_race_id
                candidates_table.put_item(Item=candidate)
                print(f"✓ Fixed (normalized): {candidate['name']}")
                print(f"  {office} -> {normalized}")
                fixed += 1
        else:
            # Still not found
            if not candidate.get('race_id') or candidate.get('race_id') == '':
                not_found.append(candidate)

print(f"\n[SUCCESS] {fixed} candidates fixed")

if len(not_found) > 0:
    print(f"\n[WARNING] {len(not_found)} candidates still orphaned:")
    for c in not_found:
        print(f"  - {c['name']} ({c['office']})")
    print("\nThese need manual review - office names don't match any races")
