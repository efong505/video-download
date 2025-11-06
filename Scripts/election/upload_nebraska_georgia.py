import boto3, csv, uuid, json
from datetime import datetime

db = boto3.resource('dynamodb')
candidates_table = db.Table('candidates')

def parse_positions(s):
    if not s: return {}
    return {k.strip():v.strip() for item in s.split(';') if ':' in item for k,v in [item.split(':',1)]}

def parse_endorsements(s):
    return [e.strip() for e in s.split(';')] if s else []

files = [('Nebraska','nebraska_candidate_additional.csv'),('Georgia','georgia_candidates_additional.csv')]
for state, csvfile in files:
    with open(f'{state.lower()}_races.json') as f:
        races = json.load(f)
    race_lookup = {r['office']:r['race_id'] for r in races}
    
    with open(csvfile, encoding='utf-8') as f:
        for c in csv.DictReader(f):
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
                'race_id': race_lookup.get(c['office'],'')
            }
            candidates_table.put_item(Item=item)
            print(f"OK: {c['name']} ({state}) - {c['office']}")

print("\nUpload complete!")
