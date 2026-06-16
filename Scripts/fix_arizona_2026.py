import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# 1. DELETE incorrect Senate race
print("Deleting incorrect AZ-SEN-2026 race...")
races_table.delete_item(Key={'race_id': 'AZ-SEN-2026'})

# 2. DELETE 2024 candidates
print("Deleting 2024 candidates...")
candidates_response = candidates_table.scan(FilterExpression=Attr('state').eq('Arizona'))
for candidate in candidates_response['Items']:
    if candidate.get('race_id') == 'AZ-SEN-2026':
        candidates_table.delete_item(Key={'candidate_id': candidate['candidate_id']})
        print(f"  Deleted: {candidate.get('name')}")

# 3. ADD missing state races
print("\nAdding missing state races...")
new_races = [
    {'race_id': 'AZ-TREAS-2026', 'state': 'Arizona', 'office': 'State Treasurer', 'election_date': '2026-11-03', 'race_type': 'Statewide', 'status': 'OPEN SEAT'},
    {'race_id': 'AZ-SUPT-2026', 'state': 'Arizona', 'office': 'Superintendent of Public Instruction', 'election_date': '2026-11-03', 'race_type': 'Statewide'},
]

for race in new_races:
    races_table.put_item(Item=race)
    print(f"  Added: {race['race_id']}")

# 4. ADD correct 2026 candidates
print("\nAdding correct 2026 candidates...")
new_candidates = [
    # Governor
    {'candidate_id': 'katie-hobbs-az-gov-2026', 'name': 'Katie Hobbs', 'office': 'Governor', 'party': 'Democrat', 'race_id': 'AZ-GOV-2026', 'state': 'Arizona', 'incumbent': True},
    {'candidate_id': 'andy-biggs-az-gov-2026', 'name': 'Andy Biggs', 'office': 'Governor', 'party': 'Republican', 'race_id': 'AZ-GOV-2026', 'state': 'Arizona', 'notes': 'U.S. Representative'},
    {'candidate_id': 'david-schweikert-az-gov-2026', 'name': 'David Schweikert', 'office': 'Governor', 'party': 'Republican', 'race_id': 'AZ-GOV-2026', 'state': 'Arizona', 'notes': 'U.S. Representative'},
    {'candidate_id': 'karrin-taylor-robson-az-gov-2026', 'name': 'Karrin Taylor Robson', 'office': 'Governor', 'party': 'Republican', 'race_id': 'AZ-GOV-2026', 'state': 'Arizona', 'notes': 'Former Regent'},
    
    # Secretary of State
    {'candidate_id': 'adrian-fontes-az-sos-2026', 'name': 'Adrian Fontes', 'office': 'Secretary of State', 'party': 'Democrat', 'race_id': 'AZ-SOS-2026', 'state': 'Arizona', 'incumbent': True},
    
    # Attorney General
    {'candidate_id': 'kris-mayes-az-ag-2026', 'name': 'Kris Mayes', 'office': 'Attorney General', 'party': 'Democrat', 'race_id': 'AZ-AG-2026', 'state': 'Arizona', 'incumbent': True},
    
    # Superintendent
    {'candidate_id': 'tom-horne-az-supt-2026', 'name': 'Tom Horne', 'office': 'Superintendent of Public Instruction', 'party': 'Republican', 'race_id': 'AZ-SUPT-2026', 'state': 'Arizona', 'incumbent': True},
    {'candidate_id': 'kimberly-yee-az-supt-2026', 'name': 'Kimberly Yee', 'office': 'Superintendent of Public Instruction', 'party': 'Republican', 'race_id': 'AZ-SUPT-2026', 'state': 'Arizona', 'notes': 'State Treasurer (term-limited)'},
]

for candidate in new_candidates:
    candidates_table.put_item(Item=candidate)
    print(f"  Added: {candidate['name']} ({candidate['party']}) - {candidate['office']}")

print("\nArizona 2026 data corrected!")
