import boto3
import csv
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
candidates_table = dynamodb.Table('candidates')
races_table = dynamodb.Table('races')

def parse_positions(positions_str):
    """Convert positions string to dict"""
    if not positions_str:
        return {}
    positions = {}
    for item in positions_str.split(';'):
        if ':' in item:
            key, value = item.split(':', 1)
            positions[key.strip()] = value.strip()
    return positions

def parse_endorsements(endorsements_str):
    """Convert endorsements string to list"""
    if not endorsements_str:
        return []
    return [e.strip() for e in endorsements_str.split(';')]

def find_race_id(state, office):
    """Find race_id by matching state and office"""
    try:
        response = races_table.scan(
            FilterExpression='#state = :state AND #office = :office',
            ExpressionAttributeNames={'#state': 'state', '#office': 'office'},
            ExpressionAttributeValues={':state': state, ':office': office}
        )
        if response['Items']:
            return response['Items'][0]['race_id']
    except Exception as e:
        print(f"  Warning: Could not find race for {office} in {state}: {e}")
    return None

print("Loading Virginia races from database...")
virginia_races = races_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'Virginia'}
)['Items']

print(f"Found {len(virginia_races)} Virginia races in database")
for race in virginia_races:
    print(f"  - {race['office']} ({race['race_type']}) - {race['election_date']}")

print("\nReading Virginia candidates CSV...")
with open('virginia_candidates_2025.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    candidates = list(reader)

print(f"Found {len(candidates)} candidates to upload\n")

uploaded = 0
skipped = 0
no_race = 0

for candidate in candidates:
    candidate_id = str(uuid.uuid4())
    
    # Find matching race_id
    race_id = find_race_id(candidate['state'], candidate['office'])
    
    if not race_id:
        print(f"WARNING: No race found: {candidate['name']} - {candidate['office']}")
        no_race += 1
        # Still upload but without race_id
    
    item = {
        'candidate_id': candidate_id,
        'name': candidate['name'],
        'state': candidate['state'],
        'office': candidate['office'],
        'party': candidate['party'],
        'bio': candidate['bio'],
        'website': candidate['website'],
        'faith_statement': candidate['faith_statement'],
        'positions': parse_positions(candidate['positions']),
        'endorsements': parse_endorsements(candidate['endorsements']),
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
        'created_by': 'super@admin.com',
        'status': 'active',
        'photo_url': '',
        'voting_record_url': ''
    }
    
    if race_id:
        item['race_id'] = race_id
    
    try:
        candidates_table.put_item(Item=item)
        race_status = f"[race_id: {race_id[:8]}...]" if race_id else "[no race_id]"
        print(f"OK Uploaded: {candidate['name']} ({candidate['party']}) - {candidate['office']} {race_status}")
        uploaded += 1
    except Exception as e:
        print(f"FAIL: {candidate['name']} - {str(e)}")
        skipped += 1

print(f"\n{'='*60}")
print(f"Upload Complete!")
print(f"Successfully uploaded: {uploaded}")
print(f"Without race_id: {no_race}")
print(f"Failed: {skipped}")
print(f"{'='*60}")
