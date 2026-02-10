import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')

missing_races = [
    {
        "state": "New Jersey",
        "office": "Perth Amboy School Board Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Perth Amboy Board of Education At-Large Seat 1"
    },
    {
        "state": "New Jersey",
        "office": "Perth Amboy School Board Seat 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Perth Amboy Board of Education At-Large Seat 2"
    },
    {
        "state": "New Jersey",
        "office": "Plainfield School Board Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Plainfield Board of Education At-Large Seat 1"
    },
    {
        "state": "New Jersey",
        "office": "Plainfield School Board Seat 2",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Plainfield Board of Education At-Large Seat 2"
    }
]

for race in missing_races:
    race['race_id'] = str(uuid.uuid4())
    race['created_at'] = datetime.now().isoformat()
    race['created_by'] = 'system'
    races_table.put_item(Item=race)
    print(f"Created: {race['office']}")

print("\nDone! Now run smart_fix_race_ids.py again")
