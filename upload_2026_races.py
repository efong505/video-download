import boto3, csv, uuid
from datetime import datetime

db = boto3.resource('dynamodb')
table = db.Table('races')

with open('add_2026_races.csv', encoding='utf-8') as f:
    for race in csv.DictReader(f):
        item = {
            'race_id': str(uuid.uuid4()),
            'state': race['state'],
            'office': race['office'],
            'election_date': race['election_date'],
            'race_type': race['race_type'],
            'description': race['description'],
            'created_at': datetime.utcnow().isoformat(),
            'created_by': 'super@admin.com'
        }
        table.put_item(Item=item)
        print(f"OK: {race['state']} - {race['office']} ({race['election_date']})")

print("\n2026 races added!")
