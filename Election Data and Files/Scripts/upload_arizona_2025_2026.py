import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# Check for existing Arizona races
print("Checking for existing Arizona races...")
existing_races = races_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'Arizona'}
)
existing_race_ids = {r['race_id'] for r in existing_races['Items']}
print(f"Found {len(existing_race_ids)} existing Arizona races")

races = [
    {"race_id": "AZ-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Competitive", "importance": "High - Senate control"},
    {"race_id": "AZ-01-2026", "office": "U.S. Representative", "district": "1", "status": "Competitive", "importance": "High - Flip opportunity"},
    {"race_id": "AZ-02-2026", "office": "U.S. Representative", "district": "2", "status": "Competitive", "importance": "High - Flip opportunity"},
    {"race_id": "AZ-03-2026", "office": "U.S. Representative", "district": "3", "status": "Safe Democrat", "importance": "Monitor"},
    {"race_id": "AZ-04-2026", "office": "U.S. Representative", "district": "4", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "AZ-05-2026", "office": "U.S. Representative", "district": "5", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "AZ-06-2026", "office": "U.S. Representative", "district": "6", "status": "Competitive", "importance": "High - Must hold"},
    {"race_id": "AZ-07-2026", "office": "U.S. Representative", "district": "7", "status": "Safe Democrat", "importance": "Monitor"},
    {"race_id": "AZ-08-2026", "office": "U.S. Representative", "district": "8", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "AZ-09-2026", "office": "U.S. Representative", "district": "9", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "AZ-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Competitive", "importance": "High - Open seat"},
    {"race_id": "AZ-AG-2026", "office": "Attorney General", "district": "Statewide", "status": "Competitive", "importance": "High - Election integrity"},
    {"race_id": "AZ-SOS-2026", "office": "Secretary of State", "district": "Statewide", "status": "Competitive", "importance": "CRITICAL - Election integrity"}
]

print("\nUploading Arizona races...")
uploaded = 0
skipped = 0
for race in races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']} (already exists)")
        skipped += 1
        continue
    
    races_table.put_item(Item={
        "race_id": race["race_id"],
        "state": "Arizona",
        "race_type": "Senate" if "SEN" in race["race_id"] else "House" if "-0" in race["race_id"] else "Statewide",
        "office": race["office"],
        "district": race["district"],
        "election_date": "2026-11-03",
        "status": race["status"],
        "importance": race["importance"],
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    })
    print(f"+ {race['race_id']}")
    uploaded += 1

print(f"\nUploaded {uploaded} new races, skipped {skipped} existing")

# Check for existing Arizona candidates
print("\nChecking for existing Arizona candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'Arizona'}
)
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}
print(f"Found {len(existing_candidate_keys)} existing Arizona candidates")

candidates = [
    {
        "candidate_id": "ruben-gallego-az-sen-2026",
        "name": "Ruben Gallego",
        "race_id": "AZ-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Democrat",
        "incumbent": False,
        "background": "U.S. Representative AZ-3, Marine Corps veteran, progressive voting record",
        "positions": {
            "abortion": "Pro-choice - supports abortion expansion",
            "education": "Opposes school choice expansion",
            "religious_freedom": "Weak on religious liberty",
            "guns": "F-rating from NRA, gun control advocate",
            "immigration": "Supports pathway to citizenship, weak border",
            "economy": "Supports Biden spending agenda"
        },
        "endorsements": ["Progressive groups", "Labor unions"],
        "website": "rubengallego.com",
        "christian_conservative_rating": "FAILS - Liberal voting record"
    },
    {
        "candidate_id": "kari-lake-az-sen-2026",
        "name": "Kari Lake",
        "race_id": "AZ-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Republican",
        "incumbent": False,
        "background": "Former news anchor, 2022 gubernatorial candidate, America First conservative",
        "positions": {
            "abortion": "Pro-life - will vote to protect unborn",
            "education": "School choice champion, parental rights",
            "religious_freedom": "Strong defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment defender",
            "immigration": "Secure border, finish the wall",
            "economy": "Lower taxes, pro-growth policies"
        },
        "endorsements": ["President Trump", "Arizona Right to Life (expected)", "NRA (expected)"],
        "website": "karilake.com",
        "christian_conservative_rating": "STRONG - America First conservative"
    },
    {
        "candidate_id": "katie-hobbs-az-gov-2026",
        "name": "Katie Hobbs",
        "race_id": "AZ-GOV-2026",
        "office_sought": "Governor",
        "party": "Democrat",
        "incumbent": True,
        "background": "Governor since 2023, former Secretary of State, progressive policies",
        "positions": {
            "abortion": "Pro-choice - supports abortion expansion",
            "education": "Opposes school choice expansion",
            "religious_freedom": "Weak on religious liberty",
            "guns": "Supports gun control measures",
            "immigration": "Opposes border wall, weak enforcement",
            "economy": "Higher taxes and spending"
        },
        "endorsements": ["Teachers unions", "Planned Parenthood", "Progressive groups"],
        "website": "katiehobbs.com",
        "christian_conservative_rating": "FAILS - Progressive record"
    },
    {
        "candidate_id": "karrin-taylor-robson-az-gov-2026",
        "name": "Karrin Taylor Robson",
        "race_id": "AZ-GOV-2026",
        "office_sought": "Governor",
        "party": "Republican",
        "incumbent": False,
        "background": "Businesswoman, real estate developer, 2022 GOP primary candidate, conservative leader",
        "positions": {
            "abortion": "Pro-life - will sign pro-life legislation",
            "education": "School choice expansion, parental rights",
            "religious_freedom": "Defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment",
            "immigration": "Secure border, finish the wall",
            "economy": "Lower taxes, cut regulations"
        },
        "endorsements": ["Arizona Chamber of Commerce", "Business community"],
        "website": "karrintaylorrobson.com",
        "christian_conservative_rating": "STRONG - Conservative values"
    }
]

print("\nUploading Arizona candidates...")
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
        "state": "Arizona",
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
print("\nArizona 2025-2026 races and candidates upload complete!")
