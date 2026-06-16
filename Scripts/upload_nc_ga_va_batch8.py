import boto3
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# Check for existing races to prevent duplicates
def race_exists(state, office, election_date):
    response = races_table.scan(
        FilterExpression='#s = :state AND office = :office AND election_date = :date',
        ExpressionAttributeNames={'#s': 'state'},
        ExpressionAttributeValues={':state': state, ':office': office, ':date': election_date}
    )
    return len(response['Items']) > 0

# NORTH CAROLINA 2026
nc_races = [
    {'race_id': str(uuid.uuid4()), 'state': 'North Carolina', 'office': 'U.S. Senate', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-03-03', 'incumbent': 'Thom Tillis', 'incumbent_party': 'Republican', 'incumbent_running': False, 'rating': 'Toss-up'},
    {'race_id': str(uuid.uuid4()), 'state': 'North Carolina', 'office': 'NC Supreme Court', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-03-03', 'incumbent': 'Anita Earls', 'incumbent_party': 'Democrat', 'incumbent_running': True, 'rating': 'Competitive'}
]

nc_candidates = [
    # Senate - Democrat
    {'candidate_id': str(uuid.uuid4()), 'name': 'Roy Cooper', 'party': 'Democrat', 'office': 'U.S. Senate', 'state': 'North Carolina', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'Former two-term Governor (2017-2025) and Attorney General; led hurricane recovery and Medicaid expansion'},
    # Senate - Republican
    {'candidate_id': str(uuid.uuid4()), 'name': 'Michael Whatley', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'North Carolina', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'Former RNC Chair and NCGOP chair; Trump-aligned party leader'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Don Brown', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'North Carolina', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'Attorney, former Navy JAG and federal prosecutor; conservative author'},
    # Supreme Court
    {'candidate_id': str(uuid.uuid4()), 'name': 'Anita Earls', 'party': 'Democrat', 'office': 'NC Supreme Court', 'state': 'North Carolina', 'incumbent': True, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Sarah Stevens', 'party': 'Republican', 'office': 'NC Supreme Court', 'state': 'North Carolina', 'incumbent': False, 'election_date': '2026-11-03'}
]

# GEORGIA 2026
ga_races = [
    {'race_id': str(uuid.uuid4()), 'state': 'Georgia', 'office': 'U.S. Senate', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-05-19', 'incumbent': 'Jon Ossoff', 'incumbent_party': 'Democrat', 'incumbent_running': True, 'rating': 'Toss-up'},
    {'race_id': str(uuid.uuid4()), 'state': 'Georgia', 'office': 'Governor', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-05-19', 'incumbent': 'Brian Kemp', 'incumbent_party': 'Republican', 'incumbent_running': False, 'rating': 'Lean Republican'},
    {'race_id': str(uuid.uuid4()), 'state': 'Georgia', 'office': 'Lieutenant Governor', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-05-19', 'incumbent': 'Burt Jones', 'incumbent_party': 'Republican', 'incumbent_running': False, 'rating': 'Competitive'},
    {'race_id': str(uuid.uuid4()), 'state': 'Georgia', 'office': 'Attorney General', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-05-19', 'incumbent': 'Chris Carr', 'incumbent_party': 'Republican', 'incumbent_running': False, 'rating': 'Competitive'},
    {'race_id': str(uuid.uuid4()), 'state': 'Georgia', 'office': 'Secretary of State', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-05-19', 'incumbent': 'Brad Raffensperger', 'incumbent_party': 'Republican', 'incumbent_running': True, 'rating': 'Competitive'}
]

ga_candidates = [
    # Senate - Democrat
    {'candidate_id': str(uuid.uuid4()), 'name': 'Jon Ossoff', 'party': 'Democrat', 'office': 'U.S. Senate', 'state': 'Georgia', 'incumbent': True, 'election_date': '2026-11-03', 'bio': 'U.S. Senator since 2021; investigative media executive; close Warnock ally'},
    # Senate - Republican
    {'candidate_id': str(uuid.uuid4()), 'name': 'Buddy Carter', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'U.S. Representative GA-01 since 2015; pro-life, strong 2A, border enforcement'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Mike Collins', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'U.S. Representative GA-10 since 2023; America First, pro-2A, hardline immigration'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Reagan Box', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Derek Dooley', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03'},
    # Governor - Democrat
    {'candidate_id': str(uuid.uuid4()), 'name': 'Keisha Lance Bottoms', 'party': 'Democrat', 'office': 'Governor', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'Former Atlanta Mayor and White House public engagement director; abortion rights, gun safety advocate'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Jason Esteves', 'party': 'Democrat', 'office': 'Governor', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'State Senator, former Atlanta Board of Education chair'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Michael Thurmond', 'party': 'Democrat', 'office': 'Governor', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'Former DeKalb CEO and Labor Commissioner'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Geoff Duncan', 'party': 'Democrat', 'office': 'Governor', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'Former GOP Lt. Governor, now running as Democrat'},
    # Governor - Republican
    {'candidate_id': str(uuid.uuid4()), 'name': 'Chris Carr', 'party': 'Republican', 'office': 'Governor', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'Attorney General since 2016; anti-crime agenda, supports Trump border initiatives'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Burt Jones', 'party': 'Republican', 'office': 'Governor', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'Lieutenant Governor since 2023; Trump-aligned'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Brad Raffensperger', 'party': 'Republican', 'office': 'Governor', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'Secretary of State; election integrity focus'},
    # Lt. Governor - Democrat
    {'candidate_id': str(uuid.uuid4()), 'name': 'Josh McLaurin', 'party': 'Democrat', 'office': 'Lieutenant Governor', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'State Senator, former State Representative; voting rights and reproductive freedom advocate'},
    # Lt. Governor - Republican
    {'candidate_id': str(uuid.uuid4()), 'name': 'Steve Gooch', 'party': 'Republican', 'office': 'Lieutenant Governor', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03'},
    # Attorney General - Democrat
    {'candidate_id': str(uuid.uuid4()), 'name': 'Tanya Miller', 'party': 'Democrat', 'office': 'Attorney General', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03'},
    # Attorney General - Republican
    {'candidate_id': str(uuid.uuid4()), 'name': 'Bill Cowsert', 'party': 'Republican', 'office': 'Attorney General', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'State Senator; tough-on-crime, conservative legal agenda'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Brian Strickland', 'party': 'Republican', 'office': 'Attorney General', 'state': 'Georgia', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'State Senator; conservative legal agenda'}
]

# VIRGINIA 2026
va_races = [
    {'race_id': str(uuid.uuid4()), 'state': 'Virginia', 'office': 'U.S. Senate', 'race_type': 'general', 'election_date': '2026-11-03', 'primary_date': '2026-06-16', 'incumbent': 'Mark Warner', 'incumbent_party': 'Democrat', 'incumbent_running': True, 'rating': 'Safe Democrat'}
]

va_candidates = [
    # Senate - Democrat
    {'candidate_id': str(uuid.uuid4()), 'name': 'Mark Warner', 'party': 'Democrat', 'office': 'U.S. Senate', 'state': 'Virginia', 'incumbent': True, 'election_date': '2026-11-03', 'bio': 'U.S. Senator, former Governor; centrist Democrat running for 4th term'},
    # Senate - Republican
    {'candidate_id': str(uuid.uuid4()), 'name': 'Bryce Reeves', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Virginia', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'Virginia State Senator; conservative platform'},
    {'candidate_id': str(uuid.uuid4()), 'name': 'Kim Farington', 'party': 'Republican', 'office': 'U.S. Senate', 'state': 'Virginia', 'incumbent': False, 'election_date': '2026-11-03', 'bio': 'Accountant'}
]

print("Uploading North Carolina races and candidates...")
for race in nc_races:
    if not race_exists(race['state'], race['office'], race['election_date']):
        races_table.put_item(Item=race)
        print(f"  Added race: {race['office']}")
    else:
        print(f"  Skipped duplicate: {race['office']}")

for candidate in nc_candidates:
    candidates_table.put_item(Item=candidate)
    print(f"  Added candidate: {candidate['name']} ({candidate['party']}) - {candidate['office']}")

print("\nUploading Georgia races and candidates...")
for race in ga_races:
    if not race_exists(race['state'], race['office'], race['election_date']):
        races_table.put_item(Item=race)
        print(f"  Added race: {race['office']}")
    else:
        print(f"  Skipped duplicate: {race['office']}")

for candidate in ga_candidates:
    candidates_table.put_item(Item=candidate)
    print(f"  Added candidate: {candidate['name']} ({candidate['party']}) - {candidate['office']}")

print("\nUploading Virginia races and candidates...")
for race in va_races:
    if not race_exists(race['state'], race['office'], race['election_date']):
        races_table.put_item(Item=race)
        print(f"  Added race: {race['office']}")
    else:
        print(f"  Skipped duplicate: {race['office']}")

for candidate in va_candidates:
    candidates_table.put_item(Item=candidate)
    print(f"  Added candidate: {candidate['name']} ({candidate['party']}) - {candidate['office']}")

print("\n" + "="*60)
print("UPLOAD COMPLETE - BATCH 8")
print("="*60)
print(f"North Carolina: {len(nc_races)} races, {len(nc_candidates)} candidates")
print(f"Georgia: {len(ga_races)} races, {len(ga_candidates)} candidates")
print(f"Virginia: {len(va_races)} races, {len(va_candidates)} candidates")
print(f"TOTAL: {len(nc_races) + len(ga_races) + len(va_races)} races, {len(nc_candidates) + len(ga_candidates) + len(va_candidates)} candidates")
