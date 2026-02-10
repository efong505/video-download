import boto3
import csv
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
candidates_table = dynamodb.Table('candidates')
races_table = dynamodb.Table('races')

def get_all_races():
    response = races_table.scan(FilterExpression='#state = :state', 
                                ExpressionAttributeNames={'#state': 'state'},
                                ExpressionAttributeValues={':state': 'Florida'})
    return response.get('Items', [])

def upload_candidates():
    all_races = get_all_races()
    print(f"Found {len(all_races)} Florida races")
    
    with open('Election Data and Files/CSV files/florida_candidates.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            candidate_id = str(uuid.uuid4())
            
            # Auto-match race by state + office
            matching_race = next((r for r in all_races if r['office'] == row['office']), None)
            race_id = matching_race['race_id'] if matching_race else ''
            
            # Parse positions
            positions = {}
            if row['positions']:
                for pos in row['positions'].split(';'):
                    if ':' in pos:
                        key, value = pos.split(':', 1)
                        positions[key.strip()] = value.strip()
            
            # Parse endorsements
            endorsements = [e.strip() for e in row['endorsements'].split(';') if e.strip()] if row['endorsements'] else []
            
            candidates_table.put_item(Item={
                'candidate_id': candidate_id,
                'race_id': race_id,
                'name': row['name'],
                'state': row['state'],
                'office': row['office'],
                'party': row['party'],
                'bio': row['bio'],
                'website': row['website'],
                'faith_statement': row['faith_statement'],
                'positions': positions,
                'endorsements': endorsements,
                'created_at': datetime.utcnow().isoformat()
            })
            count += 1
            print(f"Uploaded: {row['name']} - {row['office']} ({row['party']}) - Race ID: {race_id[:8] if race_id else 'NONE'}")
        
        print(f"\nTotal candidates uploaded: {count}")

if __name__ == '__main__':
    print("Uploading Florida candidates...\n")
    upload_candidates()
    print("\n✓ Florida candidates upload complete!")
