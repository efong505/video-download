import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

print("Checking for existing Nevada races...")
existing_races = races_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'Nevada'}
)
existing_race_ids = {r['race_id'] for r in existing_races['Items']}
print(f"Found {len(existing_race_ids)} existing Nevada races")

races = [
    {"race_id": "NV-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Competitive - CRITICAL", "importance": "CRITICAL - Senate control"},
    {"race_id": "NV-01-2026", "office": "U.S. Representative", "district": "1", "status": "Competitive", "importance": "High - Flip opportunity"},
    {"race_id": "NV-02-2026", "office": "U.S. Representative", "district": "2", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "NV-03-2026", "office": "U.S. Representative", "district": "3", "status": "Competitive", "importance": "High - Flip opportunity"},
    {"race_id": "NV-04-2026", "office": "U.S. Representative", "district": "4", "status": "Competitive", "importance": "High - Must hold"},
    {"race_id": "NV-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Competitive", "importance": "High"},
    {"race_id": "NV-AG-2026", "office": "Attorney General", "district": "Statewide", "status": "Competitive", "importance": "High"},
    {"race_id": "NV-SOS-2026", "office": "Secretary of State", "district": "Statewide", "status": "Competitive", "importance": "CRITICAL - Election integrity"}
]

print("\nUploading Nevada races...")
uploaded = 0
skipped = 0
for race in races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']} (already exists)")
        skipped += 1
        continue
    
    races_table.put_item(Item={
        "race_id": race["race_id"],
        "state": "Nevada",
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

print("\nChecking for existing Nevada candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'Nevada'}
)
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}
print(f"Found {len(existing_candidate_keys)} existing Nevada candidates")

candidates = [
    {
        "candidate_id": "jacky-rosen-nv-sen-2026",
        "name": "Jacky Rosen",
        "race_id": "NV-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Democrat",
        "incumbent": True,
        "background": "U.S. Senator since 2019, former U.S. Representative, moderate image but liberal voting record",
        "positions": {
            "abortion": "Pro-choice - supports abortion expansion",
            "education": "Opposes school choice expansion",
            "religious_freedom": "Weak on religious liberty",
            "guns": "F-rating from NRA, gun control advocate",
            "immigration": "Weak on border security",
            "economy": "Supports Biden spending agenda"
        },
        "endorsements": ["EMILY's List", "Planned Parenthood", "Progressive groups"],
        "website": "rosenfornevada.com",
        "christian_conservative_rating": "FAILS - Liberal voting record"
    },
    {
        "candidate_id": "sam-brown-nv-sen-2026",
        "name": "Sam Brown",
        "race_id": "NV-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Republican",
        "incumbent": False,
        "background": "Army veteran, Purple Heart recipient, businessman, 2022 Senate candidate, conservative leader",
        "positions": {
            "abortion": "Pro-life - will vote to protect unborn",
            "education": "School choice champion, parental rights",
            "religious_freedom": "Strong defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment defender",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, pro-growth policies"
        },
        "endorsements": ["Nevada GOP", "Veterans groups", "Conservative organizations"],
        "website": "sambrown.com",
        "christian_conservative_rating": "STRONG - Conservative veteran"
    },
    {
        "candidate_id": "steve-sisolak-nv-gov-2026",
        "name": "Steve Sisolak",
        "race_id": "NV-GOV-2026",
        "office_sought": "Governor",
        "party": "Democrat",
        "incumbent": False,
        "background": "Former Governor (2019-2023), lost 2022 re-election, progressive policies",
        "positions": {
            "abortion": "Pro-choice - supports abortion expansion",
            "education": "Opposes school choice expansion",
            "religious_freedom": "Weak on religious liberty",
            "guns": "Supports gun control measures",
            "immigration": "Weak on enforcement",
            "economy": "Higher taxes and spending"
        },
        "endorsements": ["Teachers unions", "Progressive groups"],
        "website": "sisolak.com",
        "christian_conservative_rating": "FAILS - Progressive record"
    },
    {
        "candidate_id": "joe-lombardo-nv-gov-2026",
        "name": "Joe Lombardo",
        "race_id": "NV-GOV-2026",
        "office_sought": "Governor",
        "party": "Republican",
        "incumbent": True,
        "background": "Governor since 2023, former Clark County Sheriff, law enforcement background, conservative leader",
        "positions": {
            "abortion": "Pro-life - will sign pro-life legislation",
            "education": "School choice expansion, parental rights",
            "religious_freedom": "Defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment",
            "immigration": "Secure border, support law enforcement",
            "economy": "Lower taxes, cut regulations"
        },
        "endorsements": ["Nevada GOP", "Law enforcement", "Business community"],
        "website": "joelombardo.com",
        "christian_conservative_rating": "STRONG - Law enforcement conservative"
    }
]

print("\nUploading Nevada candidates...")
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
        "state": "Nevada",
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
print("\nNevada 2025-2026 races and candidates upload complete!")
