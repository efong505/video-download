import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# Check for existing Wisconsin races
print("Checking for existing Wisconsin races...")
existing_races = races_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'Wisconsin'}
)
existing_race_ids = {r['race_id'] for r in existing_races['Items']}
print(f"Found {len(existing_race_ids)} existing Wisconsin races")

races = [
    {"race_id": "WI-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Competitive - CRITICAL PICKUP", "importance": "CRITICAL - Senate control"},
    {"race_id": "WI-01-2026", "office": "U.S. Representative", "district": "1", "status": "Competitive", "importance": "High"},
    {"race_id": "WI-02-2026", "office": "U.S. Representative", "district": "2", "status": "Safe Democrat", "importance": "Monitor"},
    {"race_id": "WI-03-2026", "office": "U.S. Representative", "district": "3", "status": "Competitive", "importance": "High"},
    {"race_id": "WI-04-2026", "office": "U.S. Representative", "district": "4", "status": "Safe Democrat", "importance": "Monitor"},
    {"race_id": "WI-05-2026", "office": "U.S. Representative", "district": "5", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "WI-06-2026", "office": "U.S. Representative", "district": "6", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "WI-07-2026", "office": "U.S. Representative", "district": "7", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "WI-08-2026", "office": "U.S. Representative", "district": "8", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "WI-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Competitive", "importance": "High"},
    {"race_id": "WI-AG-2026", "office": "Attorney General", "district": "Statewide", "status": "Competitive", "importance": "High"},
    {"race_id": "WI-SOS-2026", "office": "Secretary of State", "district": "Statewide", "status": "Competitive", "importance": "High - Election integrity"}
]

print("\nUploading Wisconsin races...")
uploaded = 0
skipped = 0
for race in races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']} (already exists)")
        skipped += 1
        continue
    
    races_table.put_item(Item={
        "race_id": race["race_id"],
        "state": "Wisconsin",
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

# Check for existing Wisconsin candidates
print("\nChecking for existing Wisconsin candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'Wisconsin'}
)
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}
print(f"Found {len(existing_candidate_keys)} existing Wisconsin candidates")

candidates = [
    {
        "candidate_id": "tammy-baldwin-wi-sen-2026",
        "name": "Tammy Baldwin",
        "race_id": "WI-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Democrat",
        "incumbent": True,
        "background": "U.S. Senator since 2013, first openly gay senator, liberal voting record",
        "positions": {
            "abortion": "Pro-choice - supports abortion expansion",
            "education": "Opposes school choice, supports teachers unions",
            "religious_freedom": "Weak record on religious liberty",
            "guns": "F-rating from NRA, gun control advocate",
            "immigration": "Supports pathway to citizenship, weak border",
            "economy": "Supports Biden spending agenda"
        },
        "endorsements": ["Planned Parenthood", "EMILY's List", "Progressive groups"],
        "website": "tammybaldwin.com",
        "christian_conservative_rating": "FAILS - Liberal voting record"
    },
    {
        "candidate_id": "eric-hovde-wi-sen-2026",
        "name": "Eric Hovde",
        "race_id": "WI-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Republican",
        "incumbent": False,
        "background": "Businessman, CEO of Sunwest Bank, 2012 Senate candidate, conservative outsider",
        "positions": {
            "abortion": "Pro-life - will vote to protect unborn",
            "education": "School choice champion, parental rights",
            "religious_freedom": "Strong defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment defender",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, pro-growth policies"
        },
        "endorsements": ["Wisconsin Right to Life (expected)", "NRA (expected)", "Wisconsin GOP"],
        "website": "hovdeforwisconsin.com",
        "christian_conservative_rating": "STRONG - Conservative businessman"
    },
    {
        "candidate_id": "tony-evers-wi-gov-2026",
        "name": "Tony Evers",
        "race_id": "WI-GOV-2026",
        "office_sought": "Governor",
        "party": "Democrat",
        "incumbent": True,
        "background": "Governor since 2019, former State Superintendent, progressive policies",
        "positions": {
            "abortion": "Pro-choice - vetoed pro-life legislation",
            "education": "Opposes school choice expansion",
            "religious_freedom": "Weak on religious liberty",
            "guns": "Supports gun control measures",
            "immigration": "Opposes immigration enforcement",
            "economy": "Higher taxes and spending"
        },
        "endorsements": ["Teachers unions", "Planned Parenthood", "Progressive groups"],
        "website": "tonyevers.com",
        "christian_conservative_rating": "FAILS - Progressive record"
    },
    {
        "candidate_id": "tim-michels-wi-gov-2026",
        "name": "Tim Michels",
        "race_id": "WI-GOV-2026",
        "office_sought": "Governor",
        "party": "Republican",
        "incumbent": False,
        "background": "Businessman, Army veteran, 2022 GOP nominee, conservative leader",
        "positions": {
            "abortion": "Pro-life - will sign pro-life legislation",
            "education": "School choice expansion, parental rights",
            "religious_freedom": "Defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment",
            "immigration": "Secure border, oppose sanctuary cities",
            "economy": "Lower taxes, cut regulations"
        },
        "endorsements": ["Wisconsin Right to Life", "NRA", "President Trump (2022)"],
        "website": "timforwisconsin.com",
        "christian_conservative_rating": "STRONG - Conservative values"
    }
]

print("\nUploading Wisconsin candidates...")
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
        "state": "Wisconsin",
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
print("\nWisconsin 2025-2026 races and candidates upload complete!")
