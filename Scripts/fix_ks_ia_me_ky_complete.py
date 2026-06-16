import boto3
from boto3.dynamodb.conditions import Attr
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

print("=== FIXING KANSAS, IOWA, MAINE, KENTUCKY ===\n")

# 1. FIX KANSAS - Remove Laura Kelly, add correct candidates
print("1. KANSAS - Removing Laura Kelly, adding correct OPEN SEAT candidates...")
candidates_response = candidates_table.scan(FilterExpression=Attr('state').eq('Kansas'))
for c in candidates_response['Items']:
    if c.get('name') == 'Laura Kelly':
        candidates_table.delete_item(Key={'candidate_id': c['candidate_id']})
        print("  Deleted Laura Kelly (term-limited, not running)")

# Add Kansas Governor candidates
ks_candidates = [
    {'candidate_id': 'jeff-colyer-ks-gov-2026', 'name': 'Jeff Colyer', 'office': 'Governor', 'party': 'Republican', 'race_id': 'KS-GOV-2026', 'state': 'Kansas', 'notes': 'Former Governor'},
    {'candidate_id': 'ty-masterson-ks-gov-2026', 'name': 'Ty Masterson', 'office': 'Governor', 'party': 'Republican', 'race_id': 'KS-GOV-2026', 'state': 'Kansas', 'notes': 'Senate President'},
    {'candidate_id': 'ethan-corson-ks-gov-2026', 'name': 'Ethan Corson', 'office': 'Governor', 'party': 'Democrat', 'race_id': 'KS-GOV-2026', 'state': 'Kansas', 'notes': 'State Senator'},
    {'candidate_id': 'cindy-holscher-ks-gov-2026', 'name': 'Cindy Holscher', 'office': 'Governor', 'party': 'Democrat', 'race_id': 'KS-GOV-2026', 'state': 'Kansas', 'notes': 'State Senator'},
]

for c in ks_candidates:
    candidates_table.put_item(Item=c)
    print(f"  Added: {c['name']} ({c['party']})")

# 2. FIX IOWA - Add missing Democratic candidates
print("\n2. IOWA - Adding missing Democratic candidates...")
ia_candidates = [
    {'candidate_id': 'rob-sand-ia-gov-2026', 'name': 'Rob Sand', 'office': 'Governor', 'party': 'Democrat', 'race_id': 'IA-GOV-2026', 'state': 'Iowa', 'notes': 'State Auditor'},
    {'candidate_id': 'julie-stauch-ia-gov-2026', 'name': 'Julie Stauch', 'office': 'Governor', 'party': 'Democrat', 'race_id': 'IA-GOV-2026', 'state': 'Iowa'},
]

for c in ia_candidates:
    candidates_table.put_item(Item=c)
    print(f"  Added: {c['name']} ({c['party']})")

# 3. FIX MAINE - Add Janet Mills as Senate candidate
print("\n3. MAINE - Adding Governor Janet Mills as Senate challenger...")
me_candidate = {
    'candidate_id': 'janet-mills-me-sen-2026',
    'name': 'Janet Mills',
    'office': 'U.S. Senator',
    'party': 'Democrat',
    'race_id': 'ME-SEN-2026',
    'state': 'Maine',
    'notes': 'Governor, announced October 14, 2025 - Race now Toss-up'
}
candidates_table.put_item(Item=me_candidate)
print(f"  Added: Janet Mills (D) - Governor challenging Collins")

# 4. FIX KENTUCKY - Remove Amy McGrath, add declared Democrats
print("\n4. KENTUCKY - Removing Amy McGrath, adding declared Democratic candidates...")
candidates_response = candidates_table.scan(FilterExpression=Attr('state').eq('Kentucky'))
for c in candidates_response['Items']:
    if c.get('name') == 'Amy McGrath':
        candidates_table.delete_item(Key={'candidate_id': c['candidate_id']})
        print("  Deleted Amy McGrath (not declared)")

ky_candidates = [
    {'candidate_id': 'logan-forsythe-ky-sen-2026', 'name': 'Logan Forsythe', 'office': 'U.S. Senator', 'party': 'Democrat', 'race_id': 'KY-SEN-2026', 'state': 'Kentucky'},
    {'candidate_id': 'pamela-stevenson-ky-sen-2026', 'name': 'Pamela Stevenson', 'office': 'U.S. Senator', 'party': 'Democrat', 'race_id': 'KY-SEN-2026', 'state': 'Kentucky'},
    {'candidate_id': 'joel-willett-ky-sen-2026', 'name': 'Joel Willett', 'office': 'U.S. Senator', 'party': 'Democrat', 'race_id': 'KY-SEN-2026', 'state': 'Kentucky'},
]

for c in ky_candidates:
    candidates_table.put_item(Item=c)
    print(f"  Added: {c['name']} ({c['party']})")

print("\n=== CANDIDATE DATA CORRECTIONS COMPLETE ===")
print("\nNext: Run upload summaries script to create voter guides")
