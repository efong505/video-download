"""
Template for uploading state election data to DynamoDB with duplicate checking

FEATURES:
- Checks for existing races/candidates before uploading
- Updates existing items instead of creating duplicates
- Uses (name, office) as unique key for candidates
- Uses (state, office) as unique key for races
"""

import boto3
from datetime import datetime
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# [STATE NAME] Races
races = [
    # YOUR RACES HERE
]

# [STATE NAME] Candidates  
candidates = [
    # YOUR CANDIDATES HERE
]

# [STATE NAME] Summary
summary = {
    "state": "[STATE NAME]",
    "title": "[STATE NAME] 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """[YOUR COMPREHENSIVE SUMMARY HERE]""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# Check existing races for this state
print(f"Checking for existing [STATE NAME] races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': '[STATE NAME]'}
)['Items']

existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

# Upload or update races
print(f"\nProcessing {len(races)} [STATE NAME] races...")
race_ids = {}
for race in races:
    office = race['office']
    
    if office in existing_race_map:
        # Race exists - update it
        race_id = existing_race_map[office]
        race['race_id'] = race_id
        race['updated_at'] = datetime.now().isoformat()
        races_table.put_item(Item=race)
        print(f"  Updated: {office}")
    else:
        # New race - create it
        race_id = str(uuid.uuid4())
        race['race_id'] = race_id
        race['created_at'] = datetime.now().isoformat()
        race['created_by'] = 'system'
        races_table.put_item(Item=race)
        print(f"  Created: {office}")
    
    race_ids[office] = race_id

print(f"\n[SUCCESS] Processed {len(races)} races")

# Check existing candidates for this state
print(f"\nChecking for existing [STATE NAME] candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': '[STATE NAME]'}
)['Items']

existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

# Upload or update candidates
print(f"\nProcessing {len(candidates)} [STATE NAME] candidates...")
for candidate in candidates:
    name = candidate['name']
    office = candidate['office']
    key = (name, office)
    
    # Link to race
    if office in race_ids:
        candidate['race_id'] = race_ids[office]
    else:
        candidate['race_id'] = ''
    
    if key in existing_candidate_map:
        # Candidate exists - update it
        candidate_id = existing_candidate_map[key]
        candidate['candidate_id'] = candidate_id
        candidate['updated_at'] = datetime.now().isoformat()
        candidate['status'] = 'active'
        candidates_table.put_item(Item=candidate)
        print(f"  Updated: {name} - {office}")
    else:
        # New candidate - create it
        candidate_id = str(uuid.uuid4())
        candidate['candidate_id'] = candidate_id
        candidate['created_at'] = datetime.now().isoformat()
        candidate['created_by'] = 'system'
        candidate['status'] = 'active'
        candidates_table.put_item(Item=candidate)
        print(f"  Created: {name} - {office}")

print(f"\n[SUCCESS] Processed {len(candidates)} candidates")

# Upload or update summary
print("\nProcessing [STATE NAME] summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': '[STATE NAME]'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")

summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")

print("\n[SUCCESS] [STATE NAME] data upload complete!")
