import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

# Get existing Alaska candidates
response = candidates_table.scan(FilterExpression=Attr('state').eq('Alaska'))
existing = {c['candidate_id'] for c in response['Items']}

# Correct 2026 Alaska candidates
candidates = [
    # Senate
    {'candidate_id': 'dan-sullivan-ak-sen-2026', 'name': 'Dan Sullivan', 'office': 'U.S. Senator', 'party': 'Republican', 'race_id': 'AK-SEN-2026', 'state': 'Alaska', 'incumbent': True},
    {'candidate_id': 'christopher-miklos-ak-sen-2026', 'name': 'Christopher Miklos', 'office': 'U.S. Senator', 'party': 'Republican', 'race_id': 'AK-SEN-2026', 'state': 'Alaska'},
    {'candidate_id': 'ann-diener-ak-sen-2026', 'name': 'Ann Diener', 'office': 'U.S. Senator', 'party': 'Democrat', 'race_id': 'AK-SEN-2026', 'state': 'Alaska'},
    
    # Governor - OPEN SEAT (Dunleavy term-limited)
    {'candidate_id': 'nancy-dahlstrom-ak-gov-2026', 'name': 'Nancy Dahlstrom', 'office': 'Governor', 'party': 'Republican', 'race_id': 'AK-GOV-2026', 'state': 'Alaska', 'notes': 'Lt. Governor'},
    {'candidate_id': 'treg-taylor-ak-gov-2026', 'name': 'Treg Taylor', 'office': 'Governor', 'party': 'Republican', 'race_id': 'AK-GOV-2026', 'state': 'Alaska', 'notes': 'Former Attorney General'},
    {'candidate_id': 'bernadette-wilson-ak-gov-2026', 'name': 'Bernadette Wilson', 'office': 'Governor', 'party': 'Republican', 'race_id': 'AK-GOV-2026', 'state': 'Alaska'},
    {'candidate_id': 'edna-devries-ak-gov-2026', 'name': 'Edna DeVries', 'office': 'Governor', 'party': 'Republican', 'race_id': 'AK-GOV-2026', 'state': 'Alaska'},
    {'candidate_id': 'dave-bronson-ak-gov-2026', 'name': 'Dave Bronson', 'office': 'Governor', 'party': 'Republican', 'race_id': 'AK-GOV-2026', 'state': 'Alaska'},
    {'candidate_id': 'shelley-hughes-ak-gov-2026', 'name': 'Shelley Hughes', 'office': 'Governor', 'party': 'Republican', 'race_id': 'AK-GOV-2026', 'state': 'Alaska'},
    {'candidate_id': 'adam-crum-ak-gov-2026', 'name': 'Adam Crum', 'office': 'Governor', 'party': 'Republican', 'race_id': 'AK-GOV-2026', 'state': 'Alaska'},
    {'candidate_id': 'james-parkin-ak-gov-2026', 'name': 'James Parkin', 'office': 'Governor', 'party': 'Republican', 'race_id': 'AK-GOV-2026', 'state': 'Alaska'},
    {'candidate_id': 'tom-begich-ak-gov-2026', 'name': 'Tom Begich', 'office': 'Governor', 'party': 'Democrat', 'race_id': 'AK-GOV-2026', 'state': 'Alaska', 'notes': 'Former State Senator'},
    
    # House
    {'candidate_id': 'nick-begich-ak-al-2026', 'name': 'Nick Begich III', 'office': 'U.S. Representative At-Large', 'party': 'Republican', 'race_id': 'AK-AL-2026', 'state': 'Alaska', 'incumbent': True},
    {'candidate_id': 'john-brendan-williams-ak-al-2026', 'name': 'John Brendan Williams', 'office': 'U.S. Representative At-Large', 'party': 'Democrat', 'race_id': 'AK-AL-2026', 'state': 'Alaska'},
    {'candidate_id': 'matt-schultz-ak-al-2026', 'name': 'Matt Schultz', 'office': 'U.S. Representative At-Large', 'party': 'Democrat', 'race_id': 'AK-AL-2026', 'state': 'Alaska', 'notes': 'Pastor'},
]

added = 0
for candidate in candidates:
    if candidate['candidate_id'] not in existing:
        candidates_table.put_item(Item=candidate)
        print(f"Added: {candidate['name']} ({candidate['party']}) - {candidate['office']}")
        added += 1
    else:
        print(f"Exists: {candidate['name']}")

print(f"\nAdded {added} new Alaska candidates")
