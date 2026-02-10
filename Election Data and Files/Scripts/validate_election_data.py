"""
Validate election data quality
Checks for races without candidates, missing info, etc.
"""
import boto3
from collections import defaultdict

db = boto3.resource('dynamodb')
races_table = db.Table('races')
candidates_table = db.Table('candidates')

print("Validating Election Data...\n")

# Get all data
races = races_table.scan()['Items']
candidates = candidates_table.scan()['Items']

# Group by state
races_by_state = defaultdict(list)
candidates_by_state = defaultdict(list)

for race in races:
    races_by_state[race['state']].append(race)

for candidate in candidates:
    candidates_by_state[candidate['state']].append(candidate)

# Check 1: Races without candidates
print("=" * 60)
print("RACES WITHOUT CANDIDATES")
print("=" * 60)
missing_candidates = []
for state in sorted(races_by_state.keys()):
    state_races = races_by_state[state]
    state_candidates = candidates_by_state.get(state, [])
    offices_with_candidates = set(c['office'] for c in state_candidates)
    
    for race in state_races:
        if race['office'] not in offices_with_candidates:
            missing_candidates.append(f"{state}: {race['office']} ({race['election_date']})")

if missing_candidates:
    for item in missing_candidates[:20]:
        print(f"  {item}")
    if len(missing_candidates) > 20:
        print(f"  ... and {len(missing_candidates) - 20} more")
else:
    print("  All races have candidates!")

# Check 2: Candidates without race_id
print("\n" + "=" * 60)
print("CANDIDATES WITHOUT RACE_ID")
print("=" * 60)
no_race_id = [c for c in candidates if not c.get('race_id')]
if no_race_id:
    for c in no_race_id[:10]:
        print(f"  {c['name']} ({c['state']}) - {c['office']}")
    if len(no_race_id) > 10:
        print(f"  ... and {len(no_race_id) - 10} more")
else:
    print("  All candidates have race_id!")

# Check 3: Missing information
print("\n" + "=" * 60)
print("CANDIDATES WITH MISSING INFO")
print("=" * 60)
missing_info = []
for c in candidates:
    issues = []
    if not c.get('bio') or len(c['bio']) < 50:
        issues.append('bio')
    if not c.get('website') or c['website'] == 'Not available':
        issues.append('website')
    if not c.get('faith_statement'):
        issues.append('faith_statement')
    if not c.get('positions') or len(c['positions']) == 0:
        issues.append('positions')
    
    if issues:
        missing_info.append(f"{c['name']} ({c['state']}): {', '.join(issues)}")

if missing_info:
    for item in missing_info[:15]:
        print(f"  {item}")
    if len(missing_info) > 15:
        print(f"  ... and {len(missing_info) - 15} more")
else:
    print("  All candidates have complete info!")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total Races: {len(races)}")
print(f"Total Candidates: {len(candidates)}")
print(f"States with Races: {len(races_by_state)}")
print(f"Races without Candidates: {len(missing_candidates)}")
print(f"Candidates without race_id: {len(no_race_id)}")
print(f"Candidates with missing info: {len(missing_info)}")
