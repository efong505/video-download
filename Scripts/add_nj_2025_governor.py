import boto3
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# New Jersey 2025 Governor race
nj_2025_race = {
    'race_id': str(uuid.uuid4()), 
    'state': 'New Jersey', 
    'office': 'Governor', 
    'race_type': 'general', 
    'election_date': '2025-11-04', 
    'primary_date': '2025-06-03', 
    'incumbent': 'Phil Murphy', 
    'incumbent_party': 'Democrat', 
    'incumbent_running': False, 
    'rating': 'Toss-up'
}

nj_2025_candidates = [
    {'candidate_id': str(uuid.uuid4()), 'name': 'Mikie Sherrill', 'party': 'Democrat', 'office': 'Governor', 'state': 'New Jersey', 'incumbent': False, 'election_date': '2025-11-04'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Jack Ciattarelli', 'party': 'Republican', 'office': 'Governor', 'state': 'New Jersey', 'incumbent': False, 'election_date': '2025-11-04'}
]

print("Adding New Jersey 2025 Governor race...")
races_table.put_item(Item=nj_2025_race)
print(f"  Added race: Governor 2025 - Murphy term-limited")

print("\nAdding New Jersey 2025 Governor candidates...")
for candidate in nj_2025_candidates:
    candidates_table.put_item(Item=candidate)
    print(f"  Added: {candidate['name']} ({candidate['party']})")

print("\n" + "="*60)
print("NJ 2025 GOVERNOR RACE ADDED")
print("="*60)
print("1 race, 2 candidates added")
