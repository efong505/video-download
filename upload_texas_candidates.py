import boto3
import csv
import uuid
import json
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
candidates_table = dynamodb.Table('candidates')

with open('texas_races.json', 'r') as f:
    races = json.load(f)

race_lookup = {}
for race in races:
    office = race['office']
    if office not in race_lookup:
        race_lookup[office] = []
    race_lookup[office].append(race['race_id'])

def parse_positions(positions_str):
    if not positions_str:
        return {}
    positions = {}
    for item in positions_str.split(';'):
        if ':' in item:
            key, value = item.split(':', 1)
            positions[key.strip()] = value.strip()
    return positions

def parse_endorsements(endorsements_str):
    if not endorsements_str:
        return []
    return [e.strip() for e in endorsements_str.split(';')]

with open('texas_candidates_additional.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    candidates = list(reader)

print(f"Found {len(candidates)} candidates to upload\n")

uploaded = 0

for candidate in candidates:
    office = candidate['office']
    race_ids = race_lookup.get(office, [])
    
    if not race_ids:
        print(f"WARNING: No race found for {office}")
        continue
    
    race_id = race_ids[0]
    
    item = {
        'candidate_id': str(uuid.uuid4()),
        'name': candidate['name'],
        'state': candidate['state'],
        'office': office,
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
        'voting_record_url': '',
        'race_id': race_id
    }
    
    try:
        candidates_table.put_item(Item=item)
        print(f"OK: {candidate['name']} ({candidate['party']}) - {office}")
        uploaded += 1
    except Exception as e:
        print(f"FAIL: {candidate['name']} - {str(e)}")

print(f"\n{'='*60}")
print(f"Upload Complete! Successfully uploaded: {uploaded}")
print(f"{'='*60}")
