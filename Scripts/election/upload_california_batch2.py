import boto3, csv, uuid, json
from datetime import datetime

db = boto3.resource('dynamodb')
candidates_table = db.Table('candidates')
races_table = db.Table('races')

# Get all California races
ca_races = races_table.scan(FilterExpression='#s=:s',ExpressionAttributeNames={'#s':'state'},ExpressionAttributeValues={':s':'California'})['Items']
race_lookup = {r['office']:r['race_id'] for r in ca_races}

def parse_positions(s):
    if not s: return {}
    return {k.strip():v.strip() for item in s.split(';') if ':' in item for k,v in [item.split(':',1)]}

def parse_endorsements(s):
    return [e.strip() for e in s.split(';')] if s else []

with open('california_candidates_batch2.csv', encoding='utf-8') as f:
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
        print(f"OK: {c['name']} - {c['office']}")

print(f"\nUpload complete!")
