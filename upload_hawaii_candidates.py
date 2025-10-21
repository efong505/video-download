import boto3
import csv
import uuid
import json
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
candidates_table = dynamodb.Table('candidates')

# Load races from file
with open('hawaii_races.json', 'r') as f:
    races = json.load(f)

# Create race lookup by office
race_lookup = {}
for race in races:
    office = race['office']
    if office not in race_lookup:
        race_lookup[office] = race['race_id']

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

print("Reading Hawaii candidates CSV...")
with open('hawaii_candidates_additional.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    candidates = list(reader)

print(f"Found {len(candidates)} candidates to upload\n")

uploaded = 0
skipped = 0
no_race = 0

for candidate in candidates:
    candidate_id = str(uuid.uuid4())
    
    office = candidate['office']
    race_id = race_lookup.get(office)
    
    if not race_id:
        print(f"WARNING: No race found: {candidate['name']} - {office}")
        no_race += 1
    
    item = {
        'candidate_id': candidate_id,
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
        'voting_record_url': ''
    }
    
    if race_id:
        item['race_id'] = race_id
    
    try:
        candidates_table.put_item(Item=item)
        race_status = f"[race_id: {race_id[:8]}...]" if race_id else "[no race_id]"
        print(f"OK: {candidate['name']} ({candidate['party']}) - {office} {race_status}")
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
