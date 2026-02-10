import boto3
from collections import defaultdict

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

print("Removing duplicate races...")
races_response = races_table.scan()
races = races_response['Items']

race_groups = defaultdict(list)
for race in races:
    key = f"{race.get('state', '')}|{race.get('office', '')}|{race.get('election_date', '')}"
    race_groups[key].append(race)

duplicates = {k: v for k, v in race_groups.items() if len(v) > 1}

races_deleted = 0
for key, dupes in duplicates.items():
    # Keep first, delete rest
    to_delete = dupes[1:]
    for race in to_delete:
        races_table.delete_item(Key={'race_id': race['race_id']})
        races_deleted += 1
        print(f"Deleted race: {race['race_id']} ({race.get('state')} - {race.get('office')})")

print(f"\nDeleted {races_deleted} duplicate races")

print("\n" + "="*60)
print("Removing duplicate candidates...")
candidates_response = candidates_table.scan()
candidates = candidates_response['Items']

candidate_groups = defaultdict(list)
for candidate in candidates:
    key = f"{candidate.get('name', '')}|{candidate.get('state', '')}|{candidate.get('office_sought', '')}"
    candidate_groups[key].append(candidate)

candidate_duplicates = {k: v for k, v in candidate_groups.items() if len(v) > 1}

candidates_deleted = 0
for key, dupes in candidate_duplicates.items():
    # Keep first, delete rest
    to_delete = dupes[1:]
    for candidate in to_delete:
        candidates_table.delete_item(Key={'candidate_id': candidate['candidate_id']})
        candidates_deleted += 1
        print(f"Deleted candidate: {candidate['candidate_id']} ({candidate.get('name')} - {candidate.get('state')})")

print(f"\nDeleted {candidates_deleted} duplicate candidates")

print("\n" + "="*60)
print("Final counts:")
races_response = races_table.scan()
candidates_response = candidates_table.scan()
print(f"Total races: {len(races_response['Items'])}")
print(f"Total candidates: {len(candidates_response['Items'])}")

# Michigan specific count
michigan_races = [r for r in races_response['Items'] if r.get('state') == 'Michigan']
print(f"Michigan races: {len(michigan_races)}")
