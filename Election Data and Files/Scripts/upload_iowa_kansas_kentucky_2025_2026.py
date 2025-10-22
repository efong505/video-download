import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# IOWA
print("=== IOWA ===")
print("Checking for existing Iowa races...")
existing_races = races_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Iowa'})
existing_race_ids = {r['race_id'] for r in existing_races['Items']}
print(f"Found {len(existing_race_ids)} existing Iowa races")

iowa_races = [
    {"race_id": "IA-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Open Seat", "importance": "CRITICAL - Open seat opportunity"},
    {"race_id": "IA-01-2026", "office": "U.S. Representative", "district": "1", "status": "Competitive", "importance": "Hold - Miller-Meeks seat"},
    {"race_id": "IA-02-2026", "office": "U.S. Representative", "district": "2", "status": "Competitive", "importance": "Hold"},
    {"race_id": "IA-03-2026", "office": "U.S. Representative", "district": "3", "status": "Competitive", "importance": "Hold - Nunn seat"},
    {"race_id": "IA-04-2026", "office": "U.S. Representative", "district": "4", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "IA-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Open Seat", "importance": "CRITICAL - Reynolds term-limited"},
    {"race_id": "IA-AG-2026", "office": "Attorney General", "district": "Statewide", "status": "Competitive", "importance": "High"},
    {"race_id": "IA-SOS-2026", "office": "Secretary of State", "district": "Statewide", "status": "Competitive", "importance": "High - Election integrity"}
]

uploaded = 0
skipped = 0
for race in iowa_races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']} (already exists)")
        skipped += 1
        continue
    races_table.put_item(Item={"race_id": race["race_id"], "state": "Iowa", "race_type": "Senate" if "SEN" in race["race_id"] else "House" if "-0" in race["race_id"] else "Statewide", "office": race["office"], "district": race["district"], "election_date": "2026-11-03", "status": race["status"], "importance": race["importance"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {race['race_id']}")
    uploaded += 1
print(f"Uploaded {uploaded} new races, skipped {skipped} existing\n")

print("Checking for existing Iowa candidates...")
existing_candidates = candidates_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Iowa'})
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}
print(f"Found {len(existing_candidate_keys)} existing Iowa candidates")

iowa_candidates = [
    {"candidate_id": "brad-sherman-ia-gov-2026", "name": "Brad Sherman", "race_id": "IA-GOV-2026", "office_sought": "Governor", "party": "Republican", "incumbent": False, "background": "Pastor, former state representative, seeking Republican nomination for open governor seat", "positions": {"abortion": "Pro-life - pastoral background", "education": "School choice, parental rights", "religious_freedom": "Strong defender as pastor", "guns": "2nd Amendment supporter", "immigration": "Secure border", "economy": "Conservative fiscal policy"}, "endorsements": ["TBD"], "website": "TBD", "christian_conservative_rating": "STRONG - Pastor and conservative"},
    {"candidate_id": "mariannette-miller-meeks-ia-01-2026", "name": "Mariannette Miller-Meeks", "race_id": "IA-01-2026", "office_sought": "U.S. Representative", "party": "Republican", "incumbent": True, "background": "U.S. Representative since 2021, physician, Army veteran, strong conservative", "positions": {"abortion": "Pro-life - medical background", "education": "School choice, parental rights", "religious_freedom": "Defender", "guns": "A-rating from NRA", "immigration": "Secure border", "economy": "Lower taxes, pro-business"}, "endorsements": ["Iowa GOP", "NRA"], "website": "millermeeks.house.gov", "christian_conservative_rating": "STRONG - Conservative voting"},
    {"candidate_id": "zach-nunn-ia-03-2026", "name": "Zach Nunn", "race_id": "IA-03-2026", "office_sought": "U.S. Representative", "party": "Republican", "incumbent": True, "background": "U.S. Representative since 2023, Air Force veteran, state senator, conservative", "positions": {"abortion": "Pro-life", "education": "School choice, parental rights", "religious_freedom": "Defender", "guns": "A-rating from NRA", "immigration": "Secure border", "economy": "Lower taxes, pro-business"}, "endorsements": ["Iowa GOP", "NRA"], "website": "nunn.house.gov", "christian_conservative_rating": "STRONG - Conservative voting"}
]

uploaded_cand = 0
skipped_cand = 0
for candidate in iowa_candidates:
    key = f"{candidate['name']}|{candidate['office_sought']}"
    if key in existing_candidate_keys:
        print(f"SKIP: {candidate['name']} (already exists)")
        skipped_cand += 1
        continue
    candidates_table.put_item(Item={"candidate_id": candidate["candidate_id"], "name": candidate["name"], "race_id": candidate["race_id"], "state": "Iowa", "party": candidate["party"], "incumbent": candidate["incumbent"], "office_sought": candidate["office_sought"], "background": candidate["background"], "positions": candidate["positions"], "endorsements": candidate["endorsements"], "website": candidate["website"], "christian_conservative_rating": candidate["christian_conservative_rating"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {candidate['name']} - {candidate['party']}")
    uploaded_cand += 1
print(f"Uploaded {uploaded_cand} new candidates, skipped {skipped_cand} existing\n")

# KANSAS
print("=== KANSAS ===")
print("Checking for existing Kansas races...")
existing_races = races_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Kansas'})
existing_race_ids = {r['race_id'] for r in existing_races['Items']}
print(f"Found {len(existing_race_ids)} existing Kansas races")

kansas_races = [
    {"race_id": "KS-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Safe Republican", "importance": "CRITICAL - Must hold Moran seat"},
    {"race_id": "KS-01-2026", "office": "U.S. Representative", "district": "1", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "KS-02-2026", "office": "U.S. Representative", "district": "2", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "KS-03-2026", "office": "U.S. Representative", "district": "3", "status": "Competitive", "importance": "Pickup opportunity"},
    {"race_id": "KS-04-2026", "office": "U.S. Representative", "district": "4", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "KS-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Competitive", "importance": "CRITICAL - Flip Kelly seat"},
    {"race_id": "KS-AG-2026", "office": "Attorney General", "district": "Statewide", "status": "Competitive", "importance": "High"},
    {"race_id": "KS-SOS-2026", "office": "Secretary of State", "district": "Statewide", "status": "Competitive", "importance": "High - Election integrity"}
]

uploaded = 0
skipped = 0
for race in kansas_races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']} (already exists)")
        skipped += 1
        continue
    races_table.put_item(Item={"race_id": race["race_id"], "state": "Kansas", "race_type": "Senate" if "SEN" in race["race_id"] else "House" if "-0" in race["race_id"] else "Statewide", "office": race["office"], "district": race["district"], "election_date": "2026-11-03", "status": race["status"], "importance": race["importance"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {race['race_id']}")
    uploaded += 1
print(f"Uploaded {uploaded} new races, skipped {skipped} existing\n")

print("Checking for existing Kansas candidates...")
existing_candidates = candidates_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Kansas'})
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}
print(f"Found {len(existing_candidate_keys)} existing Kansas candidates")

kansas_candidates = [
    {"candidate_id": "jerry-moran-ks-sen-2026", "name": "Jerry Moran", "race_id": "KS-SEN-2026", "office_sought": "U.S. Senator", "party": "Republican", "incumbent": True, "background": "U.S. Senator since 2011, former U.S. Representative, strong conservative", "positions": {"abortion": "Pro-life - 100% pro-life voting", "education": "School choice, parental rights", "religious_freedom": "Strong defender", "guns": "A-rating from NRA", "immigration": "Secure border", "economy": "Lower taxes, fiscal conservative"}, "endorsements": ["Kansas GOP", "NRA", "Kansans for Life"], "website": "moran.senate.gov", "christian_conservative_rating": "STRONG - Conservative senator"},
    {"candidate_id": "laura-kelly-ks-gov-2026", "name": "Laura Kelly", "race_id": "KS-GOV-2026", "office_sought": "Governor", "party": "Democrat", "incumbent": True, "background": "Governor since 2019, Democrat in Trump +15 state, extremely vulnerable", "positions": {"abortion": "Pro-choice - vetoed pro-life bills", "education": "Opposes school choice", "religious_freedom": "Weak record", "guns": "Supports gun control", "immigration": "Weak on border", "economy": "Higher spending"}, "endorsements": ["Kansas Democrats", "Teachers unions"], "website": "laurakelly.com", "christian_conservative_rating": "FAILS - Liberal in red state"}
]

uploaded_cand = 0
skipped_cand = 0
for candidate in kansas_candidates:
    key = f"{candidate['name']}|{candidate['office_sought']}"
    if key in existing_candidate_keys:
        print(f"SKIP: {candidate['name']} (already exists)")
        skipped_cand += 1
        continue
    candidates_table.put_item(Item={"candidate_id": candidate["candidate_id"], "name": candidate["name"], "race_id": candidate["race_id"], "state": "Kansas", "party": candidate["party"], "incumbent": candidate["incumbent"], "office_sought": candidate["office_sought"], "background": candidate["background"], "positions": candidate["positions"], "endorsements": candidate["endorsements"], "website": candidate["website"], "christian_conservative_rating": candidate["christian_conservative_rating"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {candidate['name']} - {candidate['party']}")
    uploaded_cand += 1
print(f"Uploaded {uploaded_cand} new candidates, skipped {skipped_cand} existing\n")

# KENTUCKY
print("=== KENTUCKY ===")
print("Checking for existing Kentucky races...")
existing_races = races_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Kentucky'})
existing_race_ids = {r['race_id'] for r in existing_races['Items']}
print(f"Found {len(existing_race_ids)} existing Kentucky races")

kentucky_races = [
    {"race_id": "KY-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Open Seat", "importance": "CRITICAL - McConnell retiring, must hold"},
    {"race_id": "KY-01-2026", "office": "U.S. Representative", "district": "1", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "KY-02-2026", "office": "U.S. Representative", "district": "2", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "KY-03-2026", "office": "U.S. Representative", "district": "3", "status": "Safe Democrat", "importance": "Low"},
    {"race_id": "KY-04-2026", "office": "U.S. Representative", "district": "4", "status": "Safe Republican", "importance": "Hold - Massie primary challenge"},
    {"race_id": "KY-05-2026", "office": "U.S. Representative", "district": "5", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "KY-06-2026", "office": "U.S. Representative", "district": "6", "status": "Safe Republican", "importance": "Hold"}
]

uploaded = 0
skipped = 0
for race in kentucky_races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']} (already exists)")
        skipped += 1
        continue
    races_table.put_item(Item={"race_id": race["race_id"], "state": "Kentucky", "race_type": "Senate" if "SEN" in race["race_id"] else "House" if "-0" in race["race_id"] else "Statewide", "office": race["office"], "district": race["district"], "election_date": "2026-11-03", "status": race["status"], "importance": race["importance"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {race['race_id']}")
    uploaded += 1
print(f"Uploaded {uploaded} new races, skipped {skipped} existing\n")

print("Checking for existing Kentucky candidates...")
existing_candidates = candidates_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Kentucky'})
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}
print(f"Found {len(existing_candidate_keys)} existing Kentucky candidates")

kentucky_candidates = [
    {"candidate_id": "daniel-cameron-ky-sen-2026", "name": "Daniel Cameron", "race_id": "KY-SEN-2026", "office_sought": "U.S. Senator", "party": "Republican", "incumbent": False, "background": "Former Kentucky Attorney General, strong conservative, potential Senate candidate", "positions": {"abortion": "Pro-life - defended KY pro-life laws as AG", "education": "School choice, parental rights", "religious_freedom": "Strong defender", "guns": "A-rating from NRA", "immigration": "Secure border", "economy": "Lower taxes, fiscal conservative"}, "endorsements": ["TBD"], "website": "TBD", "christian_conservative_rating": "STRONG - Conservative AG"},
    {"candidate_id": "amy-mcgrath-ky-sen-2026", "name": "Amy McGrath", "race_id": "KY-SEN-2026", "office_sought": "U.S. Senator", "party": "Democrat", "incumbent": False, "background": "Retired fighter pilot, former congressional candidate, moderate Democrat", "positions": {"abortion": "Pro-choice", "education": "Opposes school choice expansion", "religious_freedom": "Moderate", "guns": "Supports gun control", "immigration": "Pathway to citizenship", "economy": "Higher spending"}, "endorsements": ["Kentucky Democrats"], "website": "TBD", "christian_conservative_rating": "FAILS - Liberal record"},
    {"candidate_id": "thomas-massie-ky-04-2026", "name": "Thomas Massie", "race_id": "KY-04-2026", "office_sought": "U.S. Representative", "party": "Republican", "incumbent": True, "background": "U.S. Representative since 2012, libertarian-leaning conservative, faces primary challenge", "positions": {"abortion": "Pro-life", "education": "School choice, parental rights", "religious_freedom": "Defender", "guns": "A-rating from NRA", "immigration": "Secure border", "economy": "Lower taxes, fiscal conservative"}, "endorsements": ["NRA"], "website": "massie.house.gov", "christian_conservative_rating": "STRONG - Conservative voting"}
]

uploaded_cand = 0
skipped_cand = 0
for candidate in kentucky_candidates:
    key = f"{candidate['name']}|{candidate['office_sought']}"
    if key in existing_candidate_keys:
        print(f"SKIP: {candidate['name']} (already exists)")
        skipped_cand += 1
        continue
    candidates_table.put_item(Item={"candidate_id": candidate["candidate_id"], "name": candidate["name"], "race_id": candidate["race_id"], "state": "Kentucky", "party": candidate["party"], "incumbent": candidate["incumbent"], "office_sought": candidate["office_sought"], "background": candidate["background"], "positions": candidate["positions"], "endorsements": candidate["endorsements"], "website": candidate["website"], "christian_conservative_rating": candidate["christian_conservative_rating"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {candidate['name']} - {candidate['party']}")
    uploaded_cand += 1
print(f"Uploaded {uploaded_cand} new candidates, skipped {skipped_cand} existing\n")

print("[SUCCESS] Iowa, Kansas, and Kentucky 2025-2026 races and candidates upload complete!")
