import boto3
import json

dynamodb = boto3.resource('dynamodb')
races_table = dynamodb.Table('races')

response = races_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'Texas'}
)

races = response['Items']
print(f"Found {len(races)} Texas races\n")

for race in races:
    print(f"{race['office']} ({race['race_type']}) - {race['election_date']}")
    print(f"  race_id: {race['race_id']}\n")

with open('texas_races.json', 'w') as f:
    json.dump(races, f, indent=2, default=str)
