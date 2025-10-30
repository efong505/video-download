import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Delete all New Jersey races
print("Deleting New Jersey races...")
races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'New Jersey'}
)['Items']

for race in races:
    races_table.delete_item(Key={'race_id': race['race_id']})
    print(f"  Deleted race: {race['office']}")
print(f"Deleted {len(races)} races\n")

# Delete all New Jersey candidates
print("Deleting New Jersey candidates...")
candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'New Jersey'}
)['Items']

for candidate in candidates:
    candidates_table.delete_item(Key={'candidate_id': candidate['candidate_id']})
    print(f"  Deleted candidate: {candidate['name']}")
print(f"Deleted {len(candidates)} candidates\n")

# Delete New Jersey summary
print("Deleting New Jersey summary...")
try:
    summaries_table.delete_item(Key={'state': 'New Jersey'})
    print("Summary deleted\n")
except:
    print("No summary found\n")

print("All New Jersey data deleted!")
