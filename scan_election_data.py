import boto3
import json
from collections import defaultdict

dynamodb = boto3.resource('dynamodb')

# Scan races table
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

print("=" * 80)
print("SCANNING RACES TABLE")
print("=" * 80)

races_response = races_table.scan()
races = races_response['Items']

# Group by state
races_by_state = defaultdict(list)
for race in races:
    state = race.get('state', 'Unknown')
    races_by_state[state].append(race)

print(f"\nTotal Races: {len(races)}")
print(f"States with Races: {len(races_by_state)}")
print("\nRaces by State:")
for state in sorted(races_by_state.keys()):
    print(f"\n{state}: {len(races_by_state[state])} races")
    for race in sorted(races_by_state[state], key=lambda x: x.get('office', '')):
        office = race.get('office', 'N/A')
        date = race.get('election_date', 'N/A')
        race_type = race.get('race_type', 'N/A')
        print(f"  - {office} ({race_type}) - {date}")

print("\n" + "=" * 80)
print("SCANNING CANDIDATES TABLE")
print("=" * 80)

candidates_response = candidates_table.scan()
candidates = candidates_response['Items']

# Group by state
candidates_by_state = defaultdict(list)
for candidate in candidates:
    state = candidate.get('state', 'Unknown')
    candidates_by_state[state].append(candidate)

print(f"\nTotal Candidates: {len(candidates)}")
print(f"States with Candidates: {len(candidates_by_state)}")
print("\nCandidates by State:")
for state in sorted(candidates_by_state.keys()):
    print(f"\n{state}: {len(candidates_by_state[state])} candidates")
    for candidate in sorted(candidates_by_state[state], key=lambda x: x.get('name', '')):
        name = candidate.get('name', 'N/A')
        office = candidate.get('office', 'N/A')
        party = candidate.get('party', 'N/A')
        print(f"  - {name} ({party}) - {office}")

print("\n" + "=" * 80)
print("GAP ANALYSIS")
print("=" * 80)

# Find races without candidates
print("\nRaces Missing Candidates:")
for state in sorted(races_by_state.keys()):
    state_races = races_by_state[state]
    state_candidates = candidates_by_state.get(state, [])
    
    # Get offices with candidates
    offices_with_candidates = set(c.get('office', '') for c in state_candidates)
    
    # Find races without candidates
    missing = []
    for race in state_races:
        office = race.get('office', '')
        if office not in offices_with_candidates:
            missing.append(race)
    
    if missing:
        print(f"\n{state}:")
        for race in missing:
            print(f"  - {race.get('office', 'N/A')} ({race.get('election_date', 'N/A')})")

# Export to JSON for further processing
output = {
    'races': races,
    'candidates': candidates,
    'races_by_state': {k: v for k, v in races_by_state.items()},
    'candidates_by_state': {k: v for k, v in candidates_by_state.items()}
}

with open('election_data_scan.json', 'w') as f:
    json.dump(output, f, indent=2, default=str)

print("\n" + "=" * 80)
print("Data exported to: election_data_scan.json")
print("=" * 80)
