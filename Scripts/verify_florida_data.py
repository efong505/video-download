import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

print("=== FLORIDA 2026 VERIFICATION ===\n")

# Check statewide races
races_response = races_table.scan(FilterExpression=Attr('state').eq('Florida'))
statewide = [r for r in races_response['Items'] if 'House' not in r.get('office', '') and 'Senate' not in r.get('office', '')]

print("STATEWIDE RACES:")
for race in sorted(statewide, key=lambda x: x.get('office', '')):
    print(f"  {race.get('office', 'N/A')}")

# Check statewide candidates
candidates_response = candidates_table.scan(FilterExpression=Attr('state').eq('Florida'))
statewide_candidates = [c for c in candidates_response['Items'] if 'House' not in c.get('office', '') and 'Senate' not in c.get('office', '')]

print(f"\nSTATEWIDE CANDIDATES ({len(statewide_candidates)} total):")
for candidate in sorted(statewide_candidates, key=lambda x: (x.get('office', ''), x.get('name', ''))):
    print(f"  {candidate.get('name', 'N/A')} ({candidate.get('party', 'N/A')}) - {candidate.get('office', 'N/A')}")

print("\n=== REQUIRED PER YOUR DATA ===")
print("Governor: OPEN SEAT (DeSantis term-limited)")
print("Attorney General: Ashley Moody (R)")
print("CFO: Jimmy Patronis (R)")
print("Agriculture Commissioner: Wilton Simpson (R)")
print("NO Senate race in 2026")

print("\n=== MISSING? ===")
required = {
    'Ashley Moody': 'Attorney General',
    'Jimmy Patronis': 'Chief Financial Officer',
    'Wilton Simpson': 'Commissioner of Agriculture'
}

for name, office in required.items():
    found = any(c.get('name') == name for c in statewide_candidates)
    if not found:
        print(f"  MISSING: {name} - {office}")
