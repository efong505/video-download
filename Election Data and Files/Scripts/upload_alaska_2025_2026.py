import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

print("Checking for existing Alaska races...")
existing_races = races_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Alaska'})
existing_race_ids = {r['race_id'] for r in existing_races['Items']}
print(f"Found {len(existing_race_ids)} existing Alaska races")

races = [
    {"race_id": "AK-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Safe Republican", "importance": "CRITICAL - Must hold for Senate control"},
    {"race_id": "AK-AL-2026", "office": "U.S. Representative", "district": "At-Large", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "AK-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Competitive", "importance": "High"},
    {"race_id": "AK-LG-2026", "office": "Lieutenant Governor", "district": "Statewide", "importance": "High"}
]

print("\nUploading Alaska races...")
uploaded = 0
skipped = 0
for race in races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']} (already exists)")
        skipped += 1
        continue
    
    races_table.put_item(Item={
        "race_id": race["race_id"],
        "state": "Alaska",
        "race_type": "Senate" if "SEN" in race["race_id"] else "House" if "AL" in race["race_id"] else "Statewide",
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

print("\nChecking for existing Alaska candidates...")
existing_candidates = candidates_table.scan(FilterExpression='#state = :state', ExpressionAttributeNames={'#state': 'state'}, ExpressionAttributeValues={':state': 'Alaska'})
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}
print(f"Found {len(existing_candidate_keys)} existing Alaska candidates")

candidates = [
    {
        "candidate_id": "dan-sullivan-ak-sen-2026",
        "name": "Dan Sullivan",
        "race_id": "AK-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Republican",
        "incumbent": True,
        "background": "U.S. Senator since 2015, Marine Corps veteran, former Alaska Attorney General, strong conservative",
        "positions": {
            "abortion": "Pro-life - will vote to protect unborn",
            "education": "School choice, parental rights",
            "religious_freedom": "Strong defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment champion",
            "immigration": "Secure border, enforce laws",
            "economy": "Pro-energy, lower taxes, Alaska jobs"
        },
        "endorsements": ["Alaska GOP", "NRA", "Alaska Right to Life"],
        "website": "dansullivan.com",
        "christian_conservative_rating": "STRONG - Proven conservative"
    },
    {
        "candidate_id": "mike-dunleavy-ak-gov-2026",
        "name": "Mike Dunleavy",
        "race_id": "AK-GOV-2026",
        "office_sought": "Governor",
        "party": "Republican",
        "incumbent": True,
        "background": "Governor since 2018, former educator, strong conservative record",
        "positions": {
            "abortion": "Pro-life - signed pro-life legislation",
            "education": "School choice, parental rights",
            "religious_freedom": "Defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment",
            "immigration": "Secure border, enforce laws",
            "economy": "Pro-oil, pro-gas, Alaska jobs"
        },
        "endorsements": ["Alaska GOP", "NRA", "Alaska Right to Life"],
        "website": "dunleavy.com",
        "christian_conservative_rating": "STRONG - Conservative governor"
    },
    {
        "candidate_id": "nick-begich-ak-al-2026",
        "name": "Nick Begich III",
        "race_id": "AK-AL-2026",
        "office_sought": "U.S. Representative",
        "party": "Republican",
        "incumbent": True,
        "background": "U.S. Representative since 2023, businessman, strong conservative",
        "positions": {
            "abortion": "Pro-life - 100% pro-life voting",
            "education": "School choice, parental rights",
            "religious_freedom": "Strong defender",
            "guns": "A-rating from NRA",
            "immigration": "Secure border",
            "economy": "Pro-energy, Alaska jobs"
        },
        "endorsements": ["Alaska GOP", "NRA"],
        "website": "nickbegich.com",
        "christian_conservative_rating": "STRONG - Conservative voting"
    }
]

print("\nUploading Alaska candidates...")
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
        "state": "Alaska",
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
print("\nAlaska 2025-2026 races and candidates upload complete!")
