"""
Combine Pennsylvania election data chunks into single upload script.

USAGE:
1. Run each CHUNK file through Grok AI
2. Save Grok's output to text files:
   - chunk1_output.txt (races array)
   - chunk2a_output.txt through chunk2t_output.txt (candidates 1-200, 10 per file)
   - chunk5a_output.txt through chunk5d_output.txt (summary parts 1-4)
3. Run: python combine_p_chunks.py
"""

import os

def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(filepath):
        print(f"WARNING: {filename} not found - skipping")
        return ""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

print("Reading chunk outputs...")

# Read races
races_content = read_file('chunk1_output.txt')

# Read candidates (combine all 20 parts - 10 candidates each)
candidates_parts = []
for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't']:
    content = read_file(f'chunk2{letter}_output.txt')
    if content:
        candidates_parts.append(content.strip())

# Read summary (combine all 4 parts)
summary_part1 = read_file('chunk5a_output.txt')
summary_part2 = read_file('chunk5b_output.txt')
summary_part3 = read_file('chunk5c_output.txt')
summary_part4 = read_file('chunk5d_output.txt')

# Combine summary
full_summary = summary_part1 + "\n\n" + summary_part2 + "\n\n" + summary_part3 + "\n\n" + summary_part4

# Create final script (build without f-string to avoid backslash issues)
script_template = '''import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Pennsylvania Races
{{RACES_CONTENT}}

# Pennsylvania Candidates
candidates = [
{{CANDIDATES_CONTENT}}
]

# Pennsylvania Summary
summary = {
    "state": "Pennsylvania",
    "title": "Pennsylvania 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """{{SUMMARY_CONTENT}}""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Pennsylvania races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Pennsylvania'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Pennsylvania races...")
race_ids = {}
for race in races:
    office = race['office']
    if office in existing_race_map:
        race_id = existing_race_map[office]
        race['race_id'] = race_id
        race['updated_at'] = datetime.now().isoformat()
        races_table.put_item(Item=race)
        print(f"  Updated: {office}")
    else:
        race_id = str(uuid.uuid4())
        race['race_id'] = race_id
        race['created_at'] = datetime.now().isoformat()
        race['created_by'] = 'system'
        races_table.put_item(Item=race)
        print(f"  Created: {office}")
    race_ids[office] = race_id
print(f"\n[SUCCESS] Processed {len(races)} races")

print(f"\nChecking for existing Pennsylvania candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Pennsylvania'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Pennsylvania candidates...")
for candidate in candidates:
    name = candidate['name']
    office = candidate['office']
    key = (name, office)
    if office in race_ids:
        candidate['race_id'] = race_ids[office]
    else:
        candidate['race_id'] = ''
    if key in existing_candidate_map:
        candidate_id = existing_candidate_map[key]
        candidate['candidate_id'] = candidate_id
        candidate['updated_at'] = datetime.now().isoformat()
        candidate['status'] = 'active'
        candidates_table.put_item(Item=candidate)
        print(f"  Updated: {name} - {office}")
    else:
        candidate_id = str(uuid.uuid4())
        candidate['candidate_id'] = candidate_id
        candidate['created_at'] = datetime.now().isoformat()
        candidate['created_by'] = 'system'
        candidate['status'] = 'active'
        candidates_table.put_item(Item=candidate)
        print(f"  Created: {name} - {office}")
print(f"\n[SUCCESS] Processed {len(candidates)} candidates")

print("\nProcessing Pennsylvania summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Pennsylvania'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Pennsylvania data upload complete!")
'''

# Replace placeholders
final_script = script_template.replace('{{RACES_CONTENT}}', races_content)
final_script = final_script.replace('{{CANDIDATES_CONTENT}}', ',\n'.join(candidates_parts))
final_script = final_script.replace('{{SUMMARY_CONTENT}}', full_summary)

# Write final script
output_file = os.path.join(os.path.dirname(__file__), 'upload_p_data.py')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(final_script)

print(f"\nSUCCESS! Created: {output_file}")
print(f"\nNext steps:")
print(f"1. Review the file")
print(f"2. Run: python upload_p_data.py")
