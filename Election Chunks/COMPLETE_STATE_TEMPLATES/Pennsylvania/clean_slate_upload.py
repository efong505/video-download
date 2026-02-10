import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

print("=" * 60)
print("CLEAN SLATE: Deleting ALL Pennsylvania data")
print("=" * 60)

# Delete all Pennsylvania races
print("\n1. Deleting Pennsylvania races...")
races_response = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Pennsylvania'}
)
races = races_response['Items']
for race in races:
    races_table.delete_item(Key={'race_id': race['race_id']})
print(f"   Deleted {len(races)} races")

# Delete all Pennsylvania candidates
print("\n2. Deleting Pennsylvania candidates...")
candidates_response = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Pennsylvania'}
)
candidates = candidates_response['Items']
for candidate in candidates:
    candidates_table.delete_item(Key={'candidate_id': candidate['candidate_id']})
print(f"   Deleted {len(candidates)} candidates")

# Delete Pennsylvania summary
print("\n3. Deleting Pennsylvania summary...")
try:
    summaries_table.delete_item(Key={'state': 'Pennsylvania'})
    print("   Deleted summary")
except:
    print("   No summary found")

print("\n" + "=" * 60)
print("CLEAN SLATE COMPLETE - Now uploading fresh data")
print("=" * 60)

# Now run the upload script
import subprocess
result = subprocess.run(['python', 'upload_pennysylvania_data.py'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("ERRORS:", result.stderr)
