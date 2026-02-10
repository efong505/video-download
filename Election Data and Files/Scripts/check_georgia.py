import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races = dynamodb.Table('races')
candidates = dynamodb.Table('candidates')
summaries = dynamodb.Table('state-summaries')

r = races.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Georgia'})
c = candidates.scan(FilterExpression='#st = :state', ExpressionAttributeNames={'#st': 'state'}, ExpressionAttributeValues={':state': 'Georgia'})
s = summaries.get_item(Key={'state': 'Georgia'})

print(f'Georgia - Races: {len(r["Items"])}, Candidates: {len(c["Items"])}')
print(f'Summary: {"YES" if "Item" in s else "NO"}')
if "Item" in s:
    print(f'Summary length: {len(s["Item"]["content"])} characters')

print('\nRace IDs:')
for race in sorted(r['Items'], key=lambda x: x.get('race_id', '')):
    print(f'  {race.get("race_id", "NO ID")} - {race.get("office", "NO OFFICE")}')
