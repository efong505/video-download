import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')

states = ['North Carolina', 'Georgia', 'Virginia']

for state in states:
    print(f"\n{state}:")
    response = races_table.scan(FilterExpression='#st = :state', 
                                ExpressionAttributeNames={'#st': 'state'},
                                ExpressionAttributeValues={':state': state})
    for race in response['Items']:
        print(f"  - {race['office']} ({race['race_type']}) - {race['election_date']}")
