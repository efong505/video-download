import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# SOUTH DAKOTA
print("=== SOUTH DAKOTA ===")
sd_races = [
    {"race_id": "SD-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Safe Republican", "importance": "CRITICAL - Must hold Rounds seat"},
    {"race_id": "SD-AL-2026", "office": "U.S. Representative", "district": "At-Large", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "SD-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Safe Republican", "importance": "High"}
]

for race in sd_races:
    races_table.put_item(Item={"race_id": race["race_id"], "state": "South Dakota", "race_type": "Senate" if "SEN" in race["race_id"] else "House" if "AL" in race["race_id"] else "Statewide", "office": race["office"], "district": race["district"], "election_date": "2026-11-03", "status": race["status"], "importance": race["importance"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {race['race_id']}")

sd_candidates = [
    {"candidate_id": "mike-rounds-sd-sen-2026", "name": "Mike Rounds", "race_id": "SD-SEN-2026", "office_sought": "U.S. Senator", "party": "Republican", "incumbent": True, "background": "U.S. Senator since 2015, former Governor, businessman", "positions": {"abortion": "Pro-life - 100% pro-life voting", "education": "School choice, parental rights", "religious_freedom": "Strong defender", "guns": "A-rating from NRA", "immigration": "Secure border", "economy": "Lower taxes, fiscal conservative"}, "endorsements": ["South Dakota GOP", "NRA", "SD Right to Life"], "website": "rounds.senate.gov", "christian_conservative_rating": "STRONG - Conservative senator"},
    {"candidate_id": "kristi-noem-sd-gov-2026", "name": "Kristi Noem", "race_id": "SD-GOV-2026", "office_sought": "Governor", "party": "Republican", "incumbent": True, "background": "Governor since 2019, former U.S. Representative, strong conservative", "positions": {"abortion": "Pro-life - signed pro-life legislation", "education": "School choice, parental rights", "religious_freedom": "Strong defender", "guns": "A-rating from NRA", "immigration": "Secure border", "economy": "Lower taxes, pro-business"}, "endorsements": ["South Dakota GOP", "NRA", "SD Right to Life"], "website": "kristinoem.com", "christian_conservative_rating": "STRONG - Conservative governor"}
]

for candidate in sd_candidates:
    candidates_table.put_item(Item={"candidate_id": candidate["candidate_id"], "name": candidate["name"], "race_id": candidate["race_id"], "state": "South Dakota", "party": candidate["party"], "incumbent": candidate["incumbent"], "office_sought": candidate["office_sought"], "background": candidate["background"], "positions": candidate["positions"], "endorsements": candidate["endorsements"], "website": candidate["website"], "christian_conservative_rating": candidate["christian_conservative_rating"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {candidate['name']}")

# WYOMING
print("\n=== WYOMING ===")
wy_races = [
    {"race_id": "WY-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Safe Republican", "importance": "CRITICAL - Must hold Barrasso seat"},
    {"race_id": "WY-AL-2026", "office": "U.S. Representative", "district": "At-Large", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "WY-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Safe Republican", "importance": "High"}
]

for race in wy_races:
    races_table.put_item(Item={"race_id": race["race_id"], "state": "Wyoming", "race_type": "Senate" if "SEN" in race["race_id"] else "House" if "AL" in race["race_id"] else "Statewide", "office": race["office"], "district": race["district"], "election_date": "2026-11-03", "status": race["status"], "importance": race["importance"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {race['race_id']}")

wy_candidates = [
    {"candidate_id": "john-barrasso-wy-sen-2026", "name": "John Barrasso", "race_id": "WY-SEN-2026", "office_sought": "U.S. Senator", "party": "Republican", "incumbent": True, "background": "U.S. Senator since 2007, physician, Senate Republican leadership", "positions": {"abortion": "Pro-life - 100% pro-life voting", "education": "School choice, parental rights", "religious_freedom": "Strong defender", "guns": "A-rating from NRA", "immigration": "Secure border", "economy": "Energy jobs, lower taxes"}, "endorsements": ["Wyoming GOP", "NRA", "Wyoming Right to Life"], "website": "barrasso.senate.gov", "christian_conservative_rating": "STRONG - Conservative leader"},
    {"candidate_id": "mark-gordon-wy-gov-2026", "name": "Mark Gordon", "race_id": "WY-GOV-2026", "office_sought": "Governor", "party": "Republican", "incumbent": True, "background": "Governor since 2019, rancher, businessman", "positions": {"abortion": "Pro-life", "education": "School choice, parental rights", "religious_freedom": "Defender", "guns": "A-rating from NRA", "immigration": "Secure border", "economy": "Energy jobs, pro-business"}, "endorsements": ["Wyoming GOP", "NRA"], "website": "markgordon.com", "christian_conservative_rating": "STRONG - Conservative governor"}
]

for candidate in wy_candidates:
    candidates_table.put_item(Item={"candidate_id": candidate["candidate_id"], "name": candidate["name"], "race_id": candidate["race_id"], "state": "Wyoming", "party": candidate["party"], "incumbent": candidate["incumbent"], "office_sought": candidate["office_sought"], "background": candidate["background"], "positions": candidate["positions"], "endorsements": candidate["endorsements"], "website": candidate["website"], "christian_conservative_rating": candidate["christian_conservative_rating"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {candidate['name']}")

# MAINE
print("\n=== MAINE ===")
me_races = [
    {"race_id": "ME-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Competitive", "importance": "CRITICAL - MUST HOLD Collins seat"},
    {"race_id": "ME-01-2026", "office": "U.S. Representative", "district": "1", "status": "Safe Democrat", "importance": "Low"},
    {"race_id": "ME-02-2026", "office": "U.S. Representative", "district": "2", "status": "Competitive", "importance": "Pickup opportunity"},
    {"race_id": "ME-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Competitive", "importance": "High - Flip opportunity"}
]

for race in me_races:
    races_table.put_item(Item={"race_id": race["race_id"], "state": "Maine", "race_type": "Senate" if "SEN" in race["race_id"] else "House" if "-0" in race["race_id"] else "Statewide", "office": race["office"], "district": race["district"], "election_date": "2026-11-03", "status": race["status"], "importance": race["importance"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {race['race_id']}")

me_candidates = [
    {"candidate_id": "susan-collins-me-sen-2026", "name": "Susan Collins", "race_id": "ME-SEN-2026", "office_sought": "U.S. Senator", "party": "Republican", "incumbent": True, "background": "U.S. Senator since 1997, moderate Republican, critical hold", "positions": {"abortion": "Pro-choice with restrictions", "education": "Moderate positions", "religious_freedom": "Defender", "guns": "Moderate on 2nd Amendment", "immigration": "Moderate", "economy": "Fiscal moderate"}, "endorsements": ["Maine GOP"], "website": "collins.senate.gov", "christian_conservative_rating": "MODERATE - Critical hold for majority"}
]

for candidate in me_candidates:
    candidates_table.put_item(Item={"candidate_id": candidate["candidate_id"], "name": candidate["name"], "race_id": candidate["race_id"], "state": "Maine", "party": candidate["party"], "incumbent": candidate["incumbent"], "office_sought": candidate["office_sought"], "background": candidate["background"], "positions": candidate["positions"], "endorsements": candidate["endorsements"], "website": candidate["website"], "christian_conservative_rating": candidate["christian_conservative_rating"], "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    print(f"+ {candidate['name']}")

print("\n[SUCCESS] South Dakota, Wyoming, Maine 2025-2026 upload complete!")
