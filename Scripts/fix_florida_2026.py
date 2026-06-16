import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# 1. DELETE Senate race
print("Deleting incorrect FL Senate race...")
races_table.delete_item(Key={'race_id': 'f1ae4667-a8fb-48de-91bc-b235f4911eb9'})

# 2. DELETE Rick Scott (2024 candidate)
print("Deleting Rick Scott (2024 candidate)...")
candidates_response = candidates_table.scan(FilterExpression=Attr('state').eq('Florida'))
for candidate in candidates_response['Items']:
    if candidate.get('name') == 'Rick Scott':
        candidates_table.delete_item(Key={'candidate_id': candidate['candidate_id']})
        print(f"  Deleted: Rick Scott")

# 3. ADD Governor candidates
print("\nAdding Florida 2026 Governor candidates...")
gov_candidates = [
    {'candidate_id': 'ashley-moody-fl-gov-2026', 'name': 'Ashley Moody', 'office': 'Governor', 'party': 'Republican', 'race_id': 'ca3c0fc3-7e7f-44ae-9949-5e522966c22a', 'state': 'Florida', 'notes': 'Attorney General'},
    {'candidate_id': 'jimmy-patronis-fl-gov-2026', 'name': 'Jimmy Patronis', 'office': 'Governor', 'party': 'Republican', 'race_id': 'ca3c0fc3-7e7f-44ae-9949-5e522966c22a', 'state': 'Florida', 'notes': 'CFO'},
]

for candidate in gov_candidates:
    candidates_table.put_item(Item=candidate)
    print(f"  Added: {candidate['name']} ({candidate['party']})")

print("\nFlorida 2026 data corrected!")
