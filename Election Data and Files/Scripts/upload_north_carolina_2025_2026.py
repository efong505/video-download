import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# Check for existing North Carolina races
print("Checking for existing North Carolina races...")
existing_races = races_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'North Carolina'}
)
existing_race_ids = {r['race_id'] for r in existing_races['Items']}
print(f"Found {len(existing_race_ids)} existing North Carolina races")

races = [
    {"race_id": "NC-SEN-2026", "office": "U.S. Senator", "district": "Statewide", "status": "Competitive", "importance": "CRITICAL - Senate control"},
    {"race_id": "NC-01-2026", "office": "U.S. Representative", "district": "1", "status": "Safe Democrat", "importance": "Monitor"},
    {"race_id": "NC-02-2026", "office": "U.S. Representative", "district": "2", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "NC-03-2026", "office": "U.S. Representative", "district": "3", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "NC-04-2026", "office": "U.S. Representative", "district": "4", "status": "Safe Democrat", "importance": "Monitor"},
    {"race_id": "NC-05-2026", "office": "U.S. Representative", "district": "5", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "NC-06-2026", "office": "U.S. Representative", "district": "6", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "NC-07-2026", "office": "U.S. Representative", "district": "7", "status": "Competitive", "importance": "High - Must hold"},
    {"race_id": "NC-08-2026", "office": "U.S. Representative", "district": "8", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "NC-09-2026", "office": "U.S. Representative", "district": "9", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "NC-10-2026", "office": "U.S. Representative", "district": "10", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "NC-11-2026", "office": "U.S. Representative", "district": "11", "status": "Safe Republican", "importance": "Hold"},
    {"race_id": "NC-12-2026", "office": "U.S. Representative", "district": "12", "status": "Safe Democrat", "importance": "Monitor"},
    {"race_id": "NC-13-2026", "office": "U.S. Representative", "district": "13", "status": "Competitive", "importance": "High - Flip opportunity"},
    {"race_id": "NC-14-2026", "office": "U.S. Representative", "district": "14", "status": "Competitive", "importance": "High - Flip opportunity"},
    {"race_id": "NC-GOV-2026", "office": "Governor", "district": "Statewide", "status": "Competitive", "importance": "CRITICAL - Open seat"},
    {"race_id": "NC-AG-2026", "office": "Attorney General", "district": "Statewide", "status": "Competitive", "importance": "High - Law enforcement"},
    {"race_id": "NC-SOS-2026", "office": "Secretary of State", "district": "Statewide", "status": "Competitive", "importance": "High - Election integrity"}
]

print("\nUploading North Carolina races...")
uploaded = 0
skipped = 0
for race in races:
    if race['race_id'] in existing_race_ids:
        print(f"SKIP: {race['race_id']} (already exists)")
        skipped += 1
        continue
    
    races_table.put_item(Item={
        "race_id": race["race_id"],
        "state": "North Carolina",
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

# Check for existing North Carolina candidates
print("\nChecking for existing North Carolina candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#state = :state',
    ExpressionAttributeNames={'#state': 'state'},
    ExpressionAttributeValues={':state': 'North Carolina'}
)
existing_candidate_keys = {f"{c['name']}|{c.get('office_sought', '')}" for c in existing_candidates['Items']}
print(f"Found {len(existing_candidate_keys)} existing North Carolina candidates")

candidates = [
    {
        "candidate_id": "jeff-jackson-nc-sen-2026",
        "name": "Jeff Jackson",
        "race_id": "NC-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Democrat",
        "incumbent": False,
        "background": "U.S. Representative NC-14, Army National Guard veteran, progressive voting record",
        "positions": {
            "abortion": "Pro-choice - supports abortion expansion",
            "education": "Opposes school choice expansion",
            "religious_freedom": "Weak on religious liberty",
            "guns": "F-rating from NRA, gun control advocate",
            "immigration": "Supports pathway to citizenship",
            "economy": "Supports Biden spending agenda"
        },
        "endorsements": ["Progressive groups", "Labor unions"],
        "website": "jeffjacksonnc.com",
        "christian_conservative_rating": "FAILS - Liberal voting record"
    },
    {
        "candidate_id": "mark-robinson-nc-sen-2026",
        "name": "Mark Robinson",
        "race_id": "NC-SEN-2026",
        "office_sought": "U.S. Senator",
        "party": "Republican",
        "incumbent": False,
        "background": "Lieutenant Governor of North Carolina, conservative firebrand, strong Christian faith",
        "positions": {
            "abortion": "Pro-life - will vote to protect unborn",
            "education": "School choice champion, parental rights",
            "religious_freedom": "Strong defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment champion",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, pro-growth policies"
        },
        "endorsements": ["President Trump (expected)", "North Carolina Right to Life (expected)", "NRA (expected)"],
        "website": "markrobinsonnc.com",
        "christian_conservative_rating": "STRONG - Bold Christian conservative"
    },
    {
        "candidate_id": "josh-stein-nc-gov-2026",
        "name": "Josh Stein",
        "race_id": "NC-GOV-2026",
        "office_sought": "Governor",
        "party": "Democrat",
        "incumbent": False,
        "background": "Attorney General since 2017, progressive policies, weak on crime",
        "positions": {
            "abortion": "Pro-choice - supports abortion expansion",
            "education": "Opposes school choice expansion",
            "religious_freedom": "Weak on religious liberty",
            "guns": "Supports gun control measures",
            "immigration": "Weak on border enforcement",
            "economy": "Higher taxes and spending"
        },
        "endorsements": ["Teachers unions", "Planned Parenthood", "Progressive groups"],
        "website": "joshstein.org",
        "christian_conservative_rating": "FAILS - Progressive record"
    },
    {
        "candidate_id": "dan-forest-nc-gov-2026",
        "name": "Dan Forest",
        "race_id": "NC-GOV-2026",
        "office_sought": "Governor",
        "party": "Republican",
        "incumbent": False,
        "background": "Former Lieutenant Governor (2013-2021), architect, strong Christian conservative",
        "positions": {
            "abortion": "Pro-life - will sign pro-life legislation",
            "education": "School choice expansion, parental rights",
            "religious_freedom": "Defender of religious liberty",
            "guns": "A-rating from NRA, 2nd Amendment",
            "immigration": "Secure border, enforce laws",
            "economy": "Lower taxes, cut regulations"
        },
        "endorsements": ["North Carolina Right to Life (expected)", "Conservative groups"],
        "website": "danforest.com",
        "christian_conservative_rating": "STRONG - Proven conservative leader"
    }
]

print("\nUploading North Carolina candidates...")
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
        "state": "North Carolina",
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
print("\nNorth Carolina 2025-2026 races and candidates upload complete!")
