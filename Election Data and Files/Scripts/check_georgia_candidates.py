import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates = dynamodb.Table('candidates')

c = candidates.scan(FilterExpression='#st = :state', ExpressionAttributeNames={'#st': 'state'}, ExpressionAttributeValues={':state': 'Georgia'})

print(f'Total Georgia Candidates: {len(c["Items"])}\n')

for cand in sorted(c['Items'], key=lambda x: (x.get('race_id', ''), x.get('name', ''))):
    print(f"{cand.get('name', 'NO NAME')} ({cand.get('party', 'NO PARTY')})")
    print(f"  Race: {cand.get('race_id', 'NO RACE')}")
    print(f"  Office: {cand.get('office_sought', cand.get('office', 'NO OFFICE'))}")
    print()
