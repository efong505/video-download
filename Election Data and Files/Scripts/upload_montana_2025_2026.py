import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

print("Checking for existing Montana races...")
existing_races = races_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'Montana'}
)
existing_race_ids = {r['race_id'] for r in existing_races['Items']}
print(f"Found {len(existing_race_ids)} existing Montana races")

races = [
    {"race_id": "MT-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Competitive", "importance": "CRITICAL - Top Senate pickup"},
    {"race_id": "MT-01-2026", "office": "U.S. Representative", "district": "1", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "MT-02-2026", "office": "U.S. Representative", "district": "2", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "MT-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Competitive", "importance": "High"},
    {"race_id": "MT-AG-2026", "office": "Attorney General", "district": "Statewide", "status": "Competitive", "importance": "High"},
    {"race_id": "MT-SOS-2026", "office": "Secretary of State", "district": "Statewide", "status": "Competitive", "importance": "High - Election integrity"}
]

print("\nUploading Montana races...")
uploaded = 0
skipped = 0
for race in races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']} (already exists)")
        skipped += 1
        continue
    
    races_table.put_item(Item={
        "race_id": race["race_id"],
        "state": "Montana",
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

print("\nChecking for existing Montana candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'Montana'}
)
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}
print(f"Found {len(existing_candidate_keys)} existing Montana candidates")

candidates = [
    {
        "candidate_id": "jon-tester-mt-sen-2026",
        "name": "Jon Tester",
        "race_id": "MT-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Democrat",
        "incumbent": True,
        "background": "U.S. Senator since 2007, farmer, moderate image but liberal voting record",
        "positions": {
            "abortion": "Pro-choice - supports abortion expansion",
            "education": "Opposes school choice expansion",
            "religious_freedom": "Weak on religious liberty",
            "guns": "Mixed record - claims support but votes for gun control",
            "immigration": "Weak on border security",
            "economy": "Supports Biden spending agenda"
        },
        "endorsements": ["Labor unions", "Progressive groups"],
        "website": "jontester.com",
        "christian_conservative_rating": "FAILS - Liberal voting record in Trump state"
    },
    {
        "candidate_id": "tim-sheehy-mt-sen-2026",
        "name": "Tim Sheehy",
        "race_id": "MT-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Republican",
        "incumbent": False,
        "background": "Navy SEAL veteran, businessman, aerial firefighting company founder",
        "positions": {
            "abortion": "Pro-life - will vote to protect unborn",
            "education": "School choice champion, parental rights",
            "religious_freedom": "Strong defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment champion",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, pro-growth policies"
        },
        "endorsements": ["President Trump", "Montana GOP", "NRA (expected)"],
        "website": "timsheehy.com",
        "christian_conservative_rating": "STRONG - Conservative veteran"
    },
    {
        "candidate_id": "greg-gianforte-mt-gov-2026",
        "name": "Greg Gianforte",
        "race_id": "MT-GOV-2026",
        "office_sought": "Governor",
        "party": "Republican",
        "incumbent": True,
        "background": "Governor since 2021, businessman, tech entrepreneur, strong conservative",
        "positions": {
            "abortion": "Pro-life - signed pro-life legislation",
            "education": "School choice expansion, parental rights",
            "religious_freedom": "Defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, pro-business"
        },
        "endorsements": ["Montana Right to Life", "NRA", "Montana GOP"],
        "website": "greggianforte.com",
        "christian_conservative_rating": "STRONG - Proven conservative leader"
    },
    {
        "candidate_id": "ryan-busse-mt-gov-2026",
        "name": "Ryan Busse",
        "race_id": "MT-GOV-2026",
        "office_sought": "Governor",
        "party": "Democrat",
        "incumbent": False,
        "background": "Former firearms executive turned gun control advocate, progressive",
        "positions": {
            "abortion": "Pro-choice - supports abortion expansion",
            "education": "Opposes school choice expansion",
            "religious_freedom": "Weak on religious liberty",
            "guns": "Gun control advocate despite industry background",
            "immigration": "Weak on border enforcement",
            "economy": "Higher taxes and spending"
        },
        "endorsements": ["Progressive groups", "Gun control organizations"],
        "website": "ryanbusse.com",
        "christian_conservative_rating": "FAILS - Progressive record"
    }
]

print("\nUploading Montana candidates...")
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
        "state": "Montana",
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
print("\nMontana 2025-2026 races and candidates upload complete!")
