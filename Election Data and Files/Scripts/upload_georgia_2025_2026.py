import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

print("Checking for existing Georgia races...")
existing_races = races_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'Georgia'}
)
existing_race_ids = {r['race_id'] for r in existing_races['Items']}
print(f"Found {len(existing_race_ids)} existing Georgia races")

races = [
    {"race_id": "GA-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Competitive", "importance": "CRITICAL - Senate control"},
    {"race_id": "GA-01-2026", "office": "U.S. Representative", "district": "1", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "GA-02-2026", "office": "U.S. Representative", "district": "2", "status": "Safe Democrat", "importance": "Monitor"},
    {"race_id": "GA-03-2026", "office": "U.S. Representative", "district": "3", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "GA-04-2026", "office": "U.S. Representative", "district": "4", "status": "Safe Democrat", "importance": "Monitor"},
    {"race_id": "GA-05-2026", "office": "U.S. Representative", "district": "5", "status": "Safe Democrat", "importance": "Monitor"},
    {"race_id": "GA-06-2026", "office": "U.S. Representative", "district": "6", "status": "Competitive", "importance": "High - Must hold"},
    {"race_id": "GA-07-2026", "office": "U.S. Representative", "district": "7", "status": "Competitive", "importance": "High - Flip opportunity"},
    {"race_id": "GA-08-2026", "office": "U.S. Representative", "district": "8", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "GA-09-2026", "office": "U.S. Representative", "district": "9", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "GA-10-2026", "office": "U.S. Representative", "district": "10", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "GA-11-2026", "office": "U.S. Representative", "district": "11", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "GA-12-2026", "office": "U.S. Representative", "district": "12", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "GA-13-2026", "office": "U.S. Representative", "district": "13", "status": "Safe Democrat", "importance": "Monitor"},
    {"race_id": "GA-14-2026", "office": "U.S. Representative", "district": "14", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "GA-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Competitive", "importance": "CRITICAL - Open seat"},
    {"race_id": "GA-LTGOV-2026", "office": "Lieutenant Governor", "district": "Statewide", "status": "Competitive", "importance": "High"},
    {"race_id": "GA-AG-2026", "office": "Attorney General", "district": "Statewide", "status": "Competitive", "importance": "High"},
    {"race_id": "GA-SOS-2026", "office": "Secretary of State", "district": "Statewide", "status": "Competitive", "importance": "CRITICAL - Election integrity"}
]

print("\nUploading Georgia races...")
uploaded = 0
skipped = 0
for race in races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']} (already exists)")
        skipped += 1
        continue
    
    races_table.put_item(Item={
        "race_id": race["race_id"],
        "state": "Georgia",
        "race_type": "Senate" if "SEN" in race["race_id"] else "House" if "-0" in race["race_id"] or "-1" in race["race_id"] else "Statewide",
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

print("\nChecking for existing Georgia candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'Georgia'}
)
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}
print(f"Found {len(existing_candidate_keys)} existing Georgia candidates")

candidates = [
    {
        "candidate_id": "jon-ossoff-ga-sen-2026",
        "name": "Jon Ossoff",
        "race_id": "GA-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Democrat",
        "incumbent": True,
        "background": "U.S. Senator since 2021, documentary filmmaker, progressive voting record",
        "positions": {
            "abortion": "Pro-choice - supports abortion expansion",
            "education": "Opposes school choice expansion",
            "religious_freedom": "Weak on religious liberty",
            "guns": "F-rating from NRA, gun control advocate",
            "immigration": "Supports pathway to citizenship",
            "economy": "Supports Biden spending agenda"
        },
        "endorsements": ["Progressive groups", "Labor unions"],
        "website": "electjon.com",
        "christian_conservative_rating": "FAILS - Liberal voting record"
    },
    {
        "candidate_id": "herschel-walker-ga-sen-2026",
        "name": "Herschel Walker",
        "race_id": "GA-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Republican",
        "incumbent": False,
        "background": "Former NFL star, Heisman Trophy winner, businessman, 2022 Senate candidate",
        "positions": {
            "abortion": "Pro-life - will vote to protect unborn",
            "education": "School choice champion, parental rights",
            "religious_freedom": "Strong defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment champion",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, pro-growth policies"
        },
        "endorsements": ["President Trump (expected)", "Georgia Right to Life (expected)", "NRA (expected)"],
        "website": "teamherschel.com",
        "christian_conservative_rating": "STRONG - Conservative values"
    },
    {
        "candidate_id": "stacey-abrams-ga-gov-2026",
        "name": "Stacey Abrams",
        "race_id": "GA-GOV-2026",
        "office_sought": "Governor",
        "party": "Democrat",
        "incumbent": False,
        "background": "Former State House Minority Leader, 2018 and 2022 gubernatorial candidate, voting rights activist",
        "positions": {
            "abortion": "Pro-choice - supports abortion expansion",
            "education": "Opposes school choice expansion",
            "religious_freedom": "Weak on religious liberty",
            "guns": "Supports gun control measures",
            "immigration": "Supports pathway to citizenship",
            "economy": "Higher taxes and spending"
        },
        "endorsements": ["Progressive groups", "Planned Parenthood"],
        "website": "staceyabrams.com",
        "christian_conservative_rating": "FAILS - Progressive record"
    },
    {
        "candidate_id": "brian-kemp-ga-gov-2026",
        "name": "Brian Kemp",
        "race_id": "GA-GOV-2026",
        "office_sought": "Governor",
        "party": "Republican",
        "incumbent": True,
        "background": "Governor since 2019, former Secretary of State, strong conservative record",
        "positions": {
            "abortion": "Pro-life - signed heartbeat bill",
            "education": "School choice expansion, parental rights",
            "religious_freedom": "Defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, pro-business"
        },
        "endorsements": ["Georgia Right to Life", "NRA", "Georgia GOP"],
        "website": "briankemp.com",
        "christian_conservative_rating": "STRONG - Proven conservative leader"
    }
]

print("\nUploading Georgia candidates...")
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
        "state": "Georgia",
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
print("\nGeorgia 2025-2026 races and candidates upload complete!")
