import boto3
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

candidates = [
    # Rhode Island Governor - Known candidates
    {'candidate_id': str(uuid.uuid4()), 'name': 'Dan McKee', 'party': 'Democrat', 'office': 'Governor', 'state': 'Rhode Island', 'incumbent': True, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Helena Foulkes', 'party': 'Democrat', 'office': 'Governor', 'state': 'Rhode Island', 'incumbent': False, 'election_date': '2026-11-03'}
]

print("Adding known candidates...")
for candidate in candidates:
    candidates_table.put_item(Item=candidate)
    print(f"  Added: {candidate['name']} ({candidate['party']}) - {candidate['state']} {candidate['office']}")

print("\n" + "="*60)
print("CANDIDATES ADDED")
print("="*60)
print(f"Total: {len(candidates)} candidates")
print("\nNOTE: Senate candidates for DE, NJ, RI not yet declared - will be noted in summaries")
