import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# LOUISIANA
print("=== LOUISIANA ===")
existing_races = races_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Louisiana'})
existing_race_ids = {r['race_id'] for r in existing_races['Items']}

la_races = [
    {"race_id": "LA-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Safe Republican", "importance": "CRITICAL - Must hold Kennedy seat"},
    {"race_id": "LA-01-2026", "office": "U.S. Representative", "district": "1", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "LA-02-2026", "office": "U.S. Representative", "district": "2", "status": "Safe Democrat", "importance": "Low"},
    {"race_id": "LA-03-2026", "office": "U.S. Representative", "district": "3", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "LA-04-2026", "office": "U.S. Representative", "district": "4", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "LA-05-2026", "office": "U.S. Representative", "district": "5", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "LA-06-2026", "office": "U.S. Representative", "district": "6", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "LA-GOV-2027", "office": "Governor", "district": "Statewide", "status": "Competitive", "importance": "High - 2027 election"}
]

uploaded = 0
for race in la_races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']}")
        continue
    races_table.put_item(Item={"race_id": race["race_id"], "state": "Louisiana", "race_type": "Senate" if "SEN" in race["race_id"] else "House" if "-0" in race["race_id"] else "Statewide", "office": race["office"], "district": race["district"], "election_date": "2027-10-14" if "2027" in race["race_id"] else "2026-11-03", "status": race["status"], "importance": race["importance"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {race['race_id']}")
    uploaded += 1
print(f"Uploaded {uploaded} new races\n")

existing_candidates = candidates_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Louisiana'})
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}

la_candidates = [
    {"candidate_id": "john-kennedy-la-sen-2026", "name": "John Kennedy", "race_id": "LA-SEN-2026", "office_sought": "U.S. Senator", "party": "Republican", "incumbent": True, "background": "U.S. Senator since 2017, former State Treasurer, strong conservative", "positions": {"abortion": "Pro-life - 100% pro-life voting", "education": "School choice, parental rights", "religious_freedom": "Strong defender", "guns": "A-rating from NRA", "immigration": "Secure border", "economy": "Lower taxes, fiscal conservative"}, "endorsements": ["Louisiana GOP", "NRA", "Louisiana Right to Life"], "website": "kennedy.senate.gov", "christian_conservative_rating": "STRONG - Conservative senator"}
]

uploaded_cand = 0
for candidate in la_candidates:
    key = f"{candidate['name']}|{candidate['office_sought']}"
    if key in existing_candidate_keys:
        print(f"SKIP: {candidate['name']}")
        continue
    candidates_table.put_item(Item={"candidate_id": candidate["candidate_id"], "name": candidate["name"], "race_id": candidate["race_id"], "state": "Louisiana", "party": candidate["party"], "incumbent": candidate["incumbent"], "office_sought": candidate["office_sought"], "background": candidate["background"], "positions": candidate["positions"], "endorsements": candidate["endorsements"], "website": candidate["website"], "christian_conservative_rating": candidate["christian_conservative_rating"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {candidate['name']}")
    uploaded_cand += 1
print(f"Uploaded {uploaded_cand} new candidates\n")

# TENNESSEE
print("=== TENNESSEE ===")
existing_races = races_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Tennessee'})
existing_race_ids = {r['race_id'] for r in existing_races['Items']}

tn_races = [
    {"race_id": "TN-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Safe Republican", "importance": "CRITICAL - Must hold Hagerty seat"},
    {"race_id": "TN-01-2026", "office": "U.S. Representative", "district": "1", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "TN-02-2026", "office": "U.S. Representative", "district": "2", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "TN-03-2026", "office": "U.S. Representative", "district": "3", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "TN-04-2026", "office": "U.S. Representative", "district": "4", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "TN-05-2026", "office": "U.S. Representative", "district": "5", "status": "Safe Democrat", "importance": "Low"},
    {"race_id": "TN-06-2026", "office": "U.S. Representative", "district": "6", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "TN-07-2026", "office": "U.S. Representative", "district": "7", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "TN-08-2026", "office": "U.S. Representative", "district": "8", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "TN-09-2026", "office": "U.S. Representative", "district": "9", "status": "Safe Democrat", "importance": "Low"}
]

uploaded = 0
for race in tn_races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']}")
        continue
    races_table.put_item(Item={"race_id": race["race_id"], "state": "Tennessee", "race_type": "Senate" if "SEN" in race["race_id"] else "House", "office": race["office"], "district": race["district"], "election_date": "2026-11-03", "status": race["status"], "importance": race["importance"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {race['race_id']}")
    uploaded += 1
print(f"Uploaded {uploaded} new races\n")

existing_candidates = candidates_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Tennessee'})
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}

tn_candidates = [
    {"candidate_id": "bill-hagerty-tn-sen-2026", "name": "Bill Hagerty", "race_id": "TN-SEN-2026", "office_sought": "U.S. Senator", "party": "Republican", "incumbent": True, "background": "U.S. Senator since 2021, former Ambassador to Japan, businessman", "positions": {"abortion": "Pro-life - 100% pro-life voting", "education": "School choice, parental rights", "religious_freedom": "Strong defender", "guns": "A-rating from NRA", "immigration": "Secure border", "economy": "Lower taxes, pro-business"}, "endorsements": ["Tennessee GOP", "NRA", "Tennessee Right to Life"], "website": "hagerty.senate.gov", "christian_conservative_rating": "STRONG - Conservative senator"}
]

uploaded_cand = 0
for candidate in tn_candidates:
    key = f"{candidate['name']}|{candidate['office_sought']}"
    if key in existing_candidate_keys:
        print(f"SKIP: {candidate['name']}")
        continue
    candidates_table.put_item(Item={"candidate_id": candidate["candidate_id"], "name": candidate["name"], "race_id": candidate["race_id"], "state": "Tennessee", "party": candidate["party"], "incumbent": candidate["incumbent"], "office_sought": candidate["office_sought"], "background": candidate["background"], "positions": candidate["positions"], "endorsements": candidate["endorsements"], "website": candidate["website"], "christian_conservative_rating": candidate["christian_conservative_rating"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {candidate['name']}")
    uploaded_cand += 1
print(f"Uploaded {uploaded_cand} new candidates\n")

# OKLAHOMA
print("=== OKLAHOMA ===")
existing_races = races_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Oklahoma'})
existing_race_ids = {r['race_id'] for r in existing_races['Items']}

ok_races = [
    {"race_id": "OK-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Safe Republican", "importance": "CRITICAL - Must hold Lankford seat"},
    {"race_id": "OK-01-2026", "office": "U.S. Representative", "district": "1", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "OK-02-2026", "office": "U.S. Representative", "district": "2", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "OK-03-2026", "office": "U.S. Representative", "district": "3", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "OK-04-2026", "office": "U.S. Representative", "district": "4", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "OK-05-2026", "office": "U.S. Representative", "district": "5", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "OK-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Safe Republican", "importance": "High"}
]

uploaded = 0
for race in ok_races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']}")
        continue
    races_table.put_item(Item={"race_id": race["race_id"], "state": "Oklahoma", "race_type": "Senate" if "SEN" in race["race_id"] else "House" if "-0" in race["race_id"] else "Statewide", "office": race["office"], "district": race["district"], "election_date": "2026-11-03", "status": race["status"], "importance": race["importance"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {race['race_id']}")
    uploaded += 1
print(f"Uploaded {uploaded} new races\n")

existing_candidates = candidates_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Oklahoma'})
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}

ok_candidates = [
    {"candidate_id": "james-lankford-ok-sen-2026", "name": "James Lankford", "race_id": "OK-SEN-2026", "office_sought": "U.S. Senator", "party": "Republican", "incumbent": True, "background": "U.S. Senator since 2015, former U.S. Representative, former Baptist youth minister", "positions": {"abortion": "Pro-life - 100% pro-life voting", "education": "School choice, parental rights", "religious_freedom": "Strong defender, former minister", "guns": "A-rating from NRA", "immigration": "Secure border", "economy": "Lower taxes, fiscal conservative"}, "endorsements": ["Oklahoma GOP", "NRA", "Oklahomans for Life"], "website": "lankford.senate.gov", "christian_conservative_rating": "STRONG - Former minister, conservative"},
    {"candidate_id": "kevin-stitt-ok-gov-2026", "name": "Kevin Stitt", "race_id": "OK-GOV-2026", "office_sought": "Governor", "party": "Republican", "incumbent": True, "background": "Governor since 2019, businessman, strong conservative", "positions": {"abortion": "Pro-life - signed pro-life legislation", "education": "School choice champion", "religious_freedom": "Strong defender", "guns": "A-rating from NRA", "immigration": "Secure border", "economy": "Lower taxes, pro-business"}, "endorsements": ["Oklahoma GOP", "NRA", "Oklahomans for Life"], "website": "kevinstitt.com", "christian_conservative_rating": "STRONG - Conservative governor"}
]

uploaded_cand = 0
for candidate in ok_candidates:
    key = f"{candidate['name']}|{candidate['office_sought']}"
    if key in existing_candidate_keys:
        print(f"SKIP: {candidate['name']}")
        continue
    candidates_table.put_item(Item={"candidate_id": candidate["candidate_id"], "name": candidate["name"], "race_id": candidate["race_id"], "state": "Oklahoma", "party": candidate["party"], "incumbent": candidate["incumbent"], "office_sought": candidate["office_sought"], "background": candidate["background"], "positions": candidate["positions"], "endorsements": candidate["endorsements"], "website": candidate["website"], "christian_conservative_rating": candidate["christian_conservative_rating"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {candidate['name']}")
    uploaded_cand += 1
print(f"Uploaded {uploaded_cand} new candidates\n")

print("[SUCCESS] Louisiana, Tennessee, Oklahoma 2025-2026 upload complete!")
