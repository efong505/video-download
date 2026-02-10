import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races = dynamodb.Table('races')
candidates = dynamodb.Table('candidates')

for state in ['Iowa', 'Kansas', 'Kentucky']:
    r = races.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': state})
    c = candidates.scan(FilterExpression='#st = :state', ExpressionAttributeNames={'#st': 'state'}, ExpressionAttributeValues={':state': state})
    print(f'{state} - Races: {len(r["Items"])}, Candidates: {len(c["Items"])}')
