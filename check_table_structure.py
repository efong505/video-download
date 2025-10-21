import boto3
import json

dynamodb = boto3.resource('dynamodb')

# Check races table structure
races_table = dynamodb.Table('races')
races_response = races_table.scan(Limit=3)

print("=" * 80)
print("RACES TABLE STRUCTURE (Sample)")
print("=" * 80)
for race in races_response['Items']:
    print(json.dumps(race, indent=2, default=str))
    print("-" * 80)

# Check candidates table structure
candidates_table = dynamodb.Table('candidates')
candidates_response = candidates_table.scan(Limit=3)

print("\n" + "=" * 80)
print("CANDIDATES TABLE STRUCTURE (Sample)")
print("=" * 80)
for candidate in candidates_response['Items']:
    print(json.dumps(candidate, indent=2, default=str))
    print("-" * 80)

# Check if candidates reference race_id
print("\n" + "=" * 80)
print("CHECKING FOR RACE_ID REFERENCES")
print("=" * 80)

all_candidates = candidates_table.scan()['Items']
candidates_with_race_id = [c for c in all_candidates if 'race_id' in c]

print(f"Total candidates: {len(all_candidates)}")
print(f"Candidates with race_id: {len(candidates_with_race_id)}")

if candidates_with_race_id:
    print("\nSample candidate with race_id:")
    print(json.dumps(candidates_with_race_id[0], indent=2, default=str))
