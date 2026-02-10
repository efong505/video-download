import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')

response = races_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'Michigan'}
)

print(f"Michigan races found: {len(response['Items'])}\n")
for race in response['Items']:
    print(f"{race['race_id']}: {race.get('office')} - {race.get('district', 'N/A')}")
