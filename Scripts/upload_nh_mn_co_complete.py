import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# NEW HAMPSHIRE
nh_races = [
    {'race_id': str(uuid.uuid4()), 'state': 'New Hampshire', 'office': 'U.S. Senate', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-09-08', 'incumbent': 'Jeanne Shaheen', 'incumbent_party': 'Democrat', 'incumbent_running': False, 'rating': 'Toss-up'},
    {'race_id': str(uuid.uuid4()), 'state': 'New Hampshire', 'office': 'Governor', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-09-08', 'incumbent': 'Kelly Ayotte', 'incumbent_party': 'Republican', 'incumbent_running': True, 'rating': 'Lean Republican'}
]

nh_candidates = [
    # Senate - Democrat
    {'candidate_id': str(uuid.uuid4()), 'name': 'Chris Pappas', 'party': 'Democrat', 'office': 'U.S. Senate', 'state': 'New Hampshire', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Karishma Manzur', 'party': 'Democrat', 'office': 'U.S. Senate', 'state': 'New Hampshire', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Jared Sullivan', 'party': 'Democrat', 'office': 'U.S. Senate', 'state': 'New Hampshire', 'incumbent': False, 'election_date': '2026-11-03'},
    # Senate - Republican
    {'candidate_id': str(uuid.uuid4()), 'name': 'John Sununu', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'New Hampshire', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Scott Brown', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'New Hampshire', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Dan Innis', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'New Hampshire', 'incumbent': False, 'election_date': '2026-11-03'},
    # Governor - Republican
    {'candidate_id': str(uuid.uuid4()), 'name': 'Kelly Ayotte', 'party': 'Republican', 'office': 'Governor', 'state': 'New Hampshire', 'incumbent': True, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Corey Lewandowski', 'party': 'Republican', 'office': 'Governor', 'state': 'New Hampshire', 'incumbent': False, 'election_date': '2026-11-03'},
    # Governor - Democrat
    {'candidate_id': str(uuid.uuid4()), 'name': 'Jon Kiper', 'party': 'Democrat', 'office': 'Governor', 'state': 'New Hampshire', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Tom Sherman', 'party': 'Democrat', 'office': 'Governor', 'state': 'New Hampshire', 'incumbent': False, 'election_date': '2026-11-03'}
]

# MINNESOTA
mn_races = [
    {'race_id': str(uuid.uuid4()), 'state': 'Minnesota', 'office': 'U.S. Senate', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-08-11', 'incumbent': 'Tina Smith', 'incumbent_party': 'Democrat', 'incumbent_running': False, 'rating': 'Likely Democrat'},
    {'race_id': str(uuid.uuid4()), 'state': 'Minnesota', 'office': 'Governor', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-08-11', 'incumbent': 'Tim Walz', 'incumbent_party': 'Democrat', 'incumbent_running': True, 'rating': 'Lean Democrat'}
]

mn_candidates = [
    # Senate - Democrat
    {'candidate_id': str(uuid.uuid4()), 'name': 'Peggy Flanagan', 'party': 'Democrat', 'office': 'U.S. Senate', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Angie Craig', 'party': 'Democrat', 'office': 'U.S. Senate', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Melisa Lopez Franzen', 'party': 'Democrat', 'office': 'U.S. Senate', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Melvin Carter', 'party': 'Democrat', 'office': 'U.S. Senate', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Dave Wellstone', 'party': 'Democrat', 'office': 'U.S. Senate', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    # Senate - Republican
    {'candidate_id': str(uuid.uuid4()), 'name': 'Royce White', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Tom Weiler', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Ray Petersen', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Julia Coleman', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Lisa Demuth', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Zach Duckworth', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Tom Emmer', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Pete Stauber', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    # Governor - Democrat
    {'candidate_id': str(uuid.uuid4()), 'name': 'Tim Walz', 'party': 'Democrat', 'office': 'Governor', 'state': 'Minnesota', 'incumbent': True, 'election_date': '2026-11-03'},
    # Governor - Republican
    {'candidate_id': str(uuid.uuid4()), 'name': 'Scott Jensen', 'party': 'Republican', 'office': 'Governor', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Kendall Qualls', 'party': 'Republican', 'office': 'Governor', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Jeff Johnson', 'party': 'Republican', 'office': 'Governor', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Chris Madel', 'party': 'Republican', 'office': 'Governor', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Jim Nash', 'party': 'Republican', 'office': 'Governor', 'state': 'Minnesota', 'incumbent': False, 'election_date': '2026-11-03'}
]

# COLORADO
co_races = [
    {'race_id': str(uuid.uuid4()), 'state': 'Colorado', 'office': 'U.S. Senate', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-06-30', 'incumbent': 'John Hickenlooper', 'incumbent_party': 'Democrat', 'incumbent_running': True, 'rating': 'Likely Democrat'},
    {'race_id': str(uuid.uuid4()), 'state': 'Colorado', 'office': 'Governor', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-06-30', 'incumbent': 'Jared Polis', 'incumbent_party': 'Democrat', 'incumbent_running': False, 'rating': 'Lean Democrat'}
]

co_candidates = [
    # Senate - Democrat
    {'candidate_id': str(uuid.uuid4()), 'name': 'John Hickenlooper', 'party': 'Democrat', 'office': 'U.S. Senate', 'state': 'Colorado', 'incumbent': True, 'election_date': '2026-11-03'},
    # Senate - Republican
    {'candidate_id': str(uuid.uuid4()), 'name': 'Janak Joshi', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Colorado', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Heidi Ganahl', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Colorado', 'incumbent': False, 'election_date': '2026-11-03'},
    # Governor - Democrat
    {'candidate_id': str(uuid.uuid4()), 'name': 'Michael Bennet', 'party': 'Democrat', 'office': 'Governor', 'state': 'Colorado', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Phil Weiser', 'party': 'Democrat', 'office': 'Governor', 'state': 'Colorado', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Jason Crow', 'party': 'Democrat', 'office': 'Governor', 'state': 'Colorado', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Mike Johnston', 'party': 'Democrat', 'office': 'Governor', 'state': 'Colorado', 'incumbent': False, 'election_date': '2026-11-03'},
    # Governor - Republican
    {'candidate_id': str(uuid.uuid4()), 'name': 'Barbara Kirkmeyer', 'party': 'Republican', 'office': 'Governor', 'state': 'Colorado', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Greg Lopez', 'party': 'Republican', 'office': 'Governor', 'state': 'Colorado', 'incumbent': False, 'election_date': '2026-11-03'}
]

print("Uploading New Hampshire races and candidates...")
for race in nh_races:
    races_table.put_item(Item=race)
    print(f"  Added race: {race['office']}")

for candidate in nh_candidates:
    candidates_table.put_item(Item=candidate)
    print(f"  Added candidate: {candidate['name']} ({candidate['party']}) - {candidate['office']}")

print("\nUploading Minnesota races and candidates...")
for race in mn_races:
    races_table.put_item(Item=race)
    print(f"  Added race: {race['office']}")

for candidate in mn_candidates:
    candidates_table.put_item(Item=candidate)
    print(f"  Added candidate: {candidate['name']} ({candidate['party']}) - {candidate['office']}")

print("\nUploading Colorado races and candidates...")
for race in co_races:
    races_table.put_item(Item=race)
    print(f"  Added race: {race['office']}")

for candidate in co_candidates:
    candidates_table.put_item(Item=candidate)
    print(f"  Added candidate: {candidate['name']} ({candidate['party']}) - {candidate['office']}")

print("\n" + "="*60)
print("UPLOAD COMPLETE")
print("="*60)
print(f"New Hampshire: {len(nh_races)} races, {len(nh_candidates)} candidates")
print(f"Minnesota: {len(mn_races)} races, {len(mn_candidates)} candidates")
print(f"Colorado: {len(co_races)} races, {len(co_candidates)} candidates")
print(f"TOTAL: {len(nh_races) + len(mn_races) + len(co_races)} races, {len(nh_candidates) + len(mn_candidates) + len(co_candidates)} candidates")
