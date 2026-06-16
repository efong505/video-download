import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

# Delete incorrect Governor entries for Moody/Patronis
print("Deleting incorrect entries...")
candidates_table.delete_item(Key={'candidate_id': 'ashley-moody-fl-gov-2026'})
candidates_table.delete_item(Key={'candidate_id': 'jimmy-patronis-fl-gov-2026'})
print("  Deleted Moody/Patronis as Governor candidates")

# Add correct statewide incumbents
print("\nAdding correct Florida 2026 statewide candidates...")
candidates = [
    {'candidate_id': 'ashley-moody-fl-ag-2026', 'name': 'Ashley Moody', 'office': 'Attorney General', 'party': 'Republican', 'race_id': '136c72ca-25b9-4109-8317-f121aed28521', 'state': 'Florida', 'incumbent': True, 'notes': 'Strong conservative record'},
    {'candidate_id': 'jimmy-patronis-fl-cfo-2026', 'name': 'Jimmy Patronis', 'office': 'Chief Financial Officer', 'party': 'Republican', 'race_id': '813e7c39-8ae6-4cbf-8f3d-ae76cd61b3c9', 'state': 'Florida', 'incumbent': True, 'notes': 'Fiscal conservative'},
    {'candidate_id': 'wilton-simpson-fl-ag-2026', 'name': 'Wilton Simpson', 'office': 'Commissioner of Agriculture', 'party': 'Republican', 'race_id': '50d0dccf-4d43-4ab2-b6b3-2dd58b95edca', 'state': 'Florida', 'incumbent': True, 'notes': 'Strong agricultural advocate'},
]

for candidate in candidates:
    candidates_table.put_item(Item=candidate)
    print(f"  Added: {candidate['name']} - {candidate['office']}")

print("\nFlorida 2026 statewide candidates corrected!")
