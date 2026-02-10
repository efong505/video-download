import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

print("Scanning for Pennsylvania candidates...")
response = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Pennsylvania'}
)

candidates = response['Items']
print(f"Found {len(candidates)} Pennsylvania candidates")

print("\nDeleting all Pennsylvania candidates...")
for candidate in candidates:
    candidates_table.delete_item(Key={'candidate_id': candidate['candidate_id']})
    print(f"  Deleted: {candidate.get('name', 'Unknown')} - {candidate.get('office', 'Unknown')}")

print(f"\n[SUCCESS] Deleted {len(candidates)} Pennsylvania candidates")
print("Now run: python upload_pennysylvania_data.py")
