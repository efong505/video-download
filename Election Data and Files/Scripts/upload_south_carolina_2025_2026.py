import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

print("Checking for existing South Carolina races...")
existing_races = races_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'South Carolina'})
existing_race_ids = {r['race_id'] for r in existing_races['Items']}
print(f"Found {len(existing_race_ids)} existing South Carolina races")

races = [
    {"race_id": "SC-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Safe Republican", "importance": "CRITICAL - Must hold for Senate control"},
    {"race_id": "SC-01-2026", "office": "U.S. Representative", "district": "1", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "SC-02-2026", "office": "U.S. Representative", "district": "2", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "SC-03-2026", "office": "U.S. Representative", "district": "3", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "SC-04-2026", "office": "U.S. Representative", "district": "4", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "SC-05-2026", "office": "U.S. Representative", "district": "5", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "SC-06-2026", "office": "U.S. Representative", "district": "6", "status": "Safe Democrat", "importance": "Low"},
    {"race_id": "SC-07-2026", "office": "U.S. Representative", "district": "7", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "SC-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Safe Republican", "importance": "High"},
    {"race_id": "SC-AG-2026", "office": "Attorney General", "district": "Statewide", "importance": "High"}
]

print("\nUploading South Carolina races...")
uploaded = 0
skipped = 0
for race in races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']} (already exists)")
        skipped += 1
        continue
    
    races_table.put_item(Item={
        "race_id": race["race_id"],
        "state": "South Carolina",
        "race_type": "Senate" if "SEN" in race["race_id"] else "House" if "-0" in race["race_id"] else "Statewide",
        "office": race["office"],
        "district": race["district"],
        "election_date": "2026-11-03",
        "status": race.get("status", "Competitive"),
        "importance": race["importance"],
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    })
    print(f"+ {race['race_id']}")
    uploaded += 1

print(f"\nUploaded {uploaded} new races, skipped {skipped} existing")

print("\nChecking for existing South Carolina candidates...")
existing_candidates = candidates_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'South Carolina'})
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}
print(f"Found {len(existing_candidate_keys)} existing South Carolina candidates")

candidates = [
    {
        "candidate_id": "lindsey-graham-sc-sen-2026",
        "name": "Lindsey Graham",
        "race_id": "SC-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Republican",
        "incumbent": True,
        "background": "U.S. Senator since 2003, former U.S. Representative, Air Force veteran, strong conservative",
        "positions": {
            "abortion": "Pro-life - supports federal protections",
            "education": "School choice, parental rights",
            "religious_freedom": "Strong defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, pro-business"
        },
        "endorsements": ["SC GOP", "NRA", "SC Citizens for Life"],
        "website": "lgraham.senate.gov",
        "christian_conservative_rating": "STRONG - Proven conservative"
    },
    {
        "candidate_id": "henry-mcmaster-sc-gov-2026",
        "name": "Henry McMaster",
        "race_id": "SC-GOV-2026",
        "office_sought": "Governor",
        "party": "Republican",
        "incumbent": True,
        "background": "Governor since 2017, former Lt. Governor, Attorney General, strong conservative record",
        "positions": {
            "abortion": "Pro-life - signed pro-life legislation",
            "education": "School choice expansion, parental rights",
            "religious_freedom": "Defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, pro-business, jobs"
        },
        "endorsements": ["SC GOP", "NRA", "SC Citizens for Life"],
        "website": "henrymcmaster.com",
        "christian_conservative_rating": "STRONG - Conservative governor"
    },
    {
        "candidate_id": "nancy-mace-sc-01-2026",
        "name": "Nancy Mace",
        "race_id": "SC-01-2026",
        "office_sought": "U.S. Representative",
        "party": "Republican",
        "incumbent": True,
        "background": "U.S. Representative since 2021, businesswoman, first woman to graduate from The Citadel",
        "positions": {
            "abortion": "Pro-life with exceptions",
            "education": "School choice, parental rights",
            "religious_freedom": "Defender of religious liberty",
            "guns": "A-rating from NRA",
            "immigration": "Secure border",
            "economy": "Lower taxes, pro-business"
        },
        "endorsements": ["SC GOP", "NRA"],
        "website": "nancymace.com",
        "christian_conservative_rating": "STRONG - Conservative voting"
    },
    {
        "candidate_id": "joe-wilson-sc-02-2026",
        "name": "Joe Wilson",
        "race_id": "SC-02-2026",
        "office_sought": "U.S. Representative",
        "party": "Republican",
        "incumbent": True,
        "background": "U.S. Representative since 2001, Army Reserve veteran, strong conservative",
        "positions": {
            "abortion": "Pro-life - 100% pro-life voting",
            "education": "School choice, parental rights",
            "religious_freedom": "Strong defender",
            "guns": "A-rating from NRA",
            "immigration": "Secure border",
            "economy": "Lower taxes, fiscal conservative"
        },
        "endorsements": ["SC GOP", "NRA", "SC Citizens for Life"],
        "website": "joewilson.house.gov",
        "christian_conservative_rating": "STRONG - Conservative record"
    }
]

print("\nUploading South Carolina candidates...")
uploaded_cand = 0
skipped_cand = 0
for candidate in candidates:
    key = f"{candidate['name']}|{candidate['office_sought']}"
    if key in existing_candidate_keys:
        print(f"SKIP: {candidate['name']} (already exists)")
        skipped_cand += 1
        continue
    
    candidates_table.put_item(Item={
        "candidate_id": candidate["candidate_id"],
        "name": candidate["name"],
        "race_id": candidate["race_id"],
        "state": "South Carolina",
        "party": candidate["party"],
        "incumbent": candidate["incumbent"],
        "office_sought": candidate["office_sought"],
        "background": candidate["background"],
        "positions": candidate["positions"],
        "endorsements": candidate["endorsements"],
        "website": candidate["website"],
        "christian_conservative_rating": candidate["christian_conservative_rating"],
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    })
    print(f"+ {candidate['name']} - {candidate['party']}")
    uploaded_cand += 1

print(f"\nUploaded {uploaded_cand} new candidates, skipped {skipped_cand} existing")
print("\nSouth Carolina 2025-2026 races and candidates upload complete!")
