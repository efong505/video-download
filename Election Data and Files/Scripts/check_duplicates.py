import boto3
from collections import defaultdict

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

print("Checking for duplicate races...")
races_response = races_table.scan()
races = races_response['Items']

# Group by state + office + election_date
race_groups = defaultdict(list)
for race in races:
    key = f"{race.get('state', '')}|{race.get('office', '')}|{race.get('election_date', '')}"
    race_groups[key].append(race)

duplicates = {k: v for k, v in race_groups.items() if len(v) > 1}

if duplicates:
    print(f"\nFound {len(duplicates)} duplicate race groups:")
    for key, dupes in duplicates.items():
        state, office, date = key.split('|')
        print(f"\n{state} - {office} ({date}):")
        for race in dupes:
            print(f"  race_id: {race['race_id']}")
else:
    print("No duplicate races found")

print("\n" + "="*60)
print("Checking for duplicate candidates...")
candidates_response = candidates_table.scan()
candidates = candidates_response['Items']

# Group by name + state + office
candidate_groups = defaultdict(list)
for candidate in candidates:
    key = f"{candidate.get('name', '')}|{candidate.get('state', '')}|{candidate.get('office_sought', '')}"
    candidate_groups[key].append(candidate)

candidate_duplicates = {k: v for k, v in candidate_groups.items() if len(v) > 1}

if candidate_duplicates:
    print(f"\nFound {len(candidate_duplicates)} duplicate candidate groups:")
    for key, dupes in candidate_duplicates.items():
        name, state, office = key.split('|')
        print(f"\n{name} - {state} {office}:")
        for candidate in dupes:
            print(f"  candidate_id: {candidate['candidate_id']}")
else:
    print("No duplicate candidates found")

# Count by state
print("\n" + "="*60)
print("Race counts by state:")
state_counts = defaultdict(int)
for race in races:
    state_counts[race.get('state', 'Unknown')] += 1

for state in sorted(state_counts.keys()):
    print(f"{state}: {state_counts[state]} races")

print(f"\nTotal races: {len(races)}")
print(f"Total candidates: {len(candidates)}")
