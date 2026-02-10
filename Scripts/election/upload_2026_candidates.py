import boto3, csv, uuid, json
from datetime import datetime

db = boto3.resource('dynamodb')
candidates_table = db.Table('candidates')
races_table = db.Table('races')

# Get all 2026 races
all_races = races_table.scan()['Items']
races_2026 = [r for r in all_races if '2026' in r.get('election_date','')]
race_lookup = {f"{r['state']}|{r['office']}": r['race_id'] for r in races_2026}

def parse_positions(s):
    if not s: return {}
    return {k.strip():v.strip() for item in s.split(';') if ':' in item for k,v in [item.split(':',1)]}

def parse_endorsements(s):
    return [e.strip() for e in s.split(';')] if s else []

with open('candidates_2026_races.csv', encoding='utf-8') as f:
    for c in csv.DictReader(f):
        key = f"{c['state']}|{c['office']}"
        race_id = race_lookup.get(key, '')
        
        item = {
            'candidate_id': str(uuid.uuid4()),
            'name': c['name'],
            'state': c['state'],
            'office': c['office'],
            'party': c['party'],
            'bio': c['bio'],
            'website': c['website'],
            'faith_statement': c['faith_statement'],
            'positions': parse_positions(c['positions']),
            'endorsements': parse_endorsements(c['endorsements']),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'created_by': 'super@admin.com',
            'status': 'active',
            'photo_url': '',
            'voting_record_url': '',
            'race_id': race_id
        }
        candidates_table.put_item(Item=item)
        print(f"OK: {c['name']} ({c['state']}) - {c['office']}")

print("\n2026 candidates uploaded!")
