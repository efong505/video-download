import boto3
import json

dynamodb = boto3.resource('dynamodb')
races_table = dynamodb.Table('races')

response = races_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'Hawaii'}
)

races = response['Items']
print(f"Found {len(races)} Hawaii races\n")

# Group by office
by_office = {}
for race in races:
    office = race['office']
    if office not in by_office:
        by_office[office] = []
    by_office[office].append(race)

for office in sorted(by_office.keys()):
    print(f"\n{office}:")
    for race in by_office[office]:
        print(f"  race_id: {race['race_id']}")
        print(f"  date: {race['election_date']}")
        print(f"  type: {race['race_type']}")

# Save to file
with open('hawaii_races.json', 'w') as f:
    json.dump(races, f, indent=2, default=str)
