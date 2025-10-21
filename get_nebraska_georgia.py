import boto3
import json

db = boto3.resource('dynamodb')
races_table = db.Table('races')
candidates_table = db.Table('candidates')

for state in ['Nebraska', 'Georgia']:
    races = races_table.scan(FilterExpression='#s=:s',ExpressionAttributeNames={'#s':'state'},ExpressionAttributeValues={':s':state})['Items']
    candidates = candidates_table.scan(FilterExpression='#s=:s',ExpressionAttributeNames={'#s':'state'},ExpressionAttributeValues={':s':state})['Items']
    
    print(f"\n{state}: {len(races)} races, {len(candidates)} candidates")
    print("Races:")
    for r in races:
        print(f"  {r['office']} - {r['race_id'][:8]}")
    
    print("Candidates:")
    for c in candidates:
        print(f"  {c['name']} - {c['office']}")
    
    with open(f'{state.lower()}_races.json', 'w') as f:
        json.dump(races, f, indent=2, default=str)
