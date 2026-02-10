import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

print("Checking for existing West Virginia races...")
existing_races = races_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'West Virginia'}
)
existing_race_ids = {r['race_id'] for r in existing_races['Items']}
print(f"Found {len(existing_race_ids)} existing West Virginia races")

races = [
    {"race_id": "WV-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Safe Republican", "importance": "CRITICAL - Guaranteed pickup, Manchin retiring"},
    {"race_id": "WV-01-2026", "office": "U.S. Representative", "district": "1", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "WV-02-2026", "office": "U.S. Representative", "district": "2", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "WV-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Safe Republican", "importance": "High"},
    {"race_id": "WV-AG-2026", "office": "Attorney General", "district": "Statewide", "importance": "High"},
    {"race_id": "WV-SOS-2026", "office": "Secretary of State", "district": "Statewide", "importance": "High - Election integrity"}
]

print("\nUploading West Virginia races...")
uploaded = 0
skipped = 0
for race in races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']} (already exists)")
        skipped += 1
        continue
    
    races_table.put_item(Item={
        "race_id": race["race_id"],
        "state": "West Virginia",
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

print("\nChecking for existing West Virginia candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'West Virginia'}
)
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}
print(f"Found {len(existing_candidate_keys)} existing West Virginia candidates")

candidates = [
    {
        "candidate_id": "patrick-morrisey-wv-sen-2026",
        "name": "Patrick Morrisey",
        "race_id": "WV-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Republican",
        "incumbent": False,
        "background": "West Virginia Attorney General since 2013, led lawsuits against Biden overreach, strong conservative record",
        "positions": {
            "abortion": "Pro-life - defended WV pro-life laws",
            "education": "School choice champion, parental rights",
            "religious_freedom": "Strong defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment champion",
            "immigration": "Secure border, sued Biden admin over border",
            "economy": "Lower taxes, pro-coal, energy independence"
        },
        "endorsements": ["President Trump (expected)", "WV GOP", "NRA"],
        "website": "morriseyforwv.com",
        "christian_conservative_rating": "STRONG - Proven conservative fighter"
    },
    {
        "candidate_id": "jim-justice-wv-gov-2026",
        "name": "Jim Justice",
        "race_id": "WV-GOV-2026",
        "office_sought": "Governor",
        "party": "Republican",
        "incumbent": True,
        "background": "Governor since 2017, businessman, switched from Democrat to Republican in 2017, Trump ally",
        "positions": {
            "abortion": "Pro-life - signed pro-life legislation",
            "education": "School choice expansion, teacher pay raises",
            "religious_freedom": "Defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, pro-coal, pro-business"
        },
        "endorsements": ["President Trump", "WV GOP", "NRA"],
        "website": "jimjustice.com",
        "christian_conservative_rating": "STRONG - Conservative governor"
    },
    {
        "candidate_id": "carol-miller-wv-03-2026",
        "name": "Carol Miller",
        "race_id": "WV-03-2026",
        "office_sought": "U.S. Representative",
        "party": "Republican",
        "incumbent": True,
        "background": "U.S. Representative since 2019, businesswoman, state legislator, strong conservative",
        "positions": {
            "abortion": "Pro-life - 100% pro-life voting record",
            "education": "School choice, parental rights",
            "religious_freedom": "Strong defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, pro-coal, energy jobs"
        },
        "endorsements": ["President Trump", "NRA", "WV Right to Life"],
        "website": "carolmillerforcongress.com",
        "christian_conservative_rating": "STRONG - Conservative voting record"
    },
    {
        "candidate_id": "alex-mooney-wv-02-2026",
        "name": "Alex Mooney",
        "race_id": "WV-02-2026",
        "office_sought": "U.S. Representative",
        "party": "Republican",
        "incumbent": True,
        "background": "U.S. Representative since 2015, former Maryland state senator, strong conservative",
        "positions": {
            "abortion": "Pro-life - 100% pro-life voting record",
            "education": "School choice champion, parental rights",
            "religious_freedom": "Strong defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, pro-coal, fiscal conservative"
        },
        "endorsements": ["President Trump", "NRA", "WV Right to Life"],
        "website": "alexmoonyforcongress.com",
        "christian_conservative_rating": "STRONG - Conservative voting record"
    }
]

print("\nUploading West Virginia candidates...")
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
        "state": "West Virginia",
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
print("\nWest Virginia 2025-2026 races and candidates upload complete!")
