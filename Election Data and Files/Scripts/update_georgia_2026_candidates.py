import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

print("Checking existing Georgia candidates...")
existing = candidates_table.scan(FilterExpression='#st = :state', ExpressionAttributeNames={'#st': 'state'}, ExpressionAttributeValues={':state': 'Georgia'})
existing_keys = {f"{c.get('name', '')}|{c.get('race_id', '')}" for c in existing['Items']}
print(f"Found {len(existing_keys)} existing candidates\n")

new_candidates = [
    # SENATE - Republican Challengers
    {"candidate_id": "buddy-carter-ga-sen-2026", "name": "Buddy Carter", "race_id": "GA-SEN-2026", "office_sought": "U.S. Senator", "party": "Republican", "incumbent": False, "background": "U.S. Representative from Georgia's 1st District", "positions": {"abortion": "Pro-life", "education": "School choice", "religious_freedom": "Defender", "guns": "A-rating NRA", "immigration": "Secure border", "economy": "Lower taxes"}, "endorsements": ["TBD"], "website": "buddycarter.com", "christian_conservative_rating": "STRONG"},
    {"candidate_id": "mike-collins-ga-sen-2026", "name": "Mike Collins", "race_id": "GA-SEN-2026", "office_sought": "U.S. Senator", "party": "Republican", "incumbent": False, "background": "U.S. Representative from Georgia's 10th District", "positions": {"abortion": "Pro-life", "education": "School choice", "religious_freedom": "Defender", "guns": "A-rating NRA", "immigration": "Secure border", "economy": "Lower taxes"}, "endorsements": ["TBD"], "website": "mikecollins.com", "christian_conservative_rating": "STRONG"},
    {"candidate_id": "derek-dooley-ga-sen-2026", "name": "Derek Dooley", "race_id": "GA-SEN-2026", "office_sought": "U.S. Senator", "party": "Republican", "incumbent": False, "background": "Former football coach", "positions": {"abortion": "Pro-life", "education": "School choice", "religious_freedom": "Defender", "guns": "2nd Amendment", "immigration": "Secure border", "economy": "Pro-business"}, "endorsements": ["TBD"], "website": "TBD", "christian_conservative_rating": "STRONG"},
    
    # GOVERNOR - Democrats
    {"candidate_id": "keisha-lance-bottoms-ga-gov-2026", "name": "Keisha Lance Bottoms", "race_id": "GA-GOV-2026", "office_sought": "Governor", "party": "Democrat", "incumbent": False, "background": "Former Atlanta Mayor", "positions": {"abortion": "Pro-choice", "education": "Opposes school choice", "religious_freedom": "Moderate", "guns": "Gun control", "immigration": "Pathway to citizenship", "economy": "Higher spending"}, "endorsements": ["TBD"], "website": "TBD", "christian_conservative_rating": "FAILS"},
    {"candidate_id": "jason-esteves-ga-gov-2026", "name": "Jason Esteves", "race_id": "GA-GOV-2026", "office_sought": "Governor", "party": "Democrat", "incumbent": False, "background": "Former Atlanta school board chair and state senator", "positions": {"abortion": "Pro-choice", "education": "Opposes school choice", "religious_freedom": "Moderate", "guns": "Gun control", "immigration": "Pathway to citizenship", "economy": "Higher spending"}, "endorsements": ["TBD"], "website": "TBD", "christian_conservative_rating": "FAILS"},
    {"candidate_id": "derrick-jackson-ga-gov-2026", "name": "Derrick Jackson", "race_id": "GA-GOV-2026", "office_sought": "Governor", "party": "Democrat", "incumbent": False, "background": "State Representative from Tyrone", "positions": {"abortion": "Pro-choice", "education": "Opposes school choice", "religious_freedom": "Moderate", "guns": "Gun control", "immigration": "Pathway to citizenship", "economy": "Higher spending"}, "endorsements": ["TBD"], "website": "TBD", "christian_conservative_rating": "FAILS"},
    
    # GOVERNOR - Republicans
    {"candidate_id": "chris-carr-ga-gov-2026", "name": "Chris Carr", "race_id": "GA-GOV-2026", "office_sought": "Governor", "party": "Republican", "incumbent": False, "background": "Attorney General", "positions": {"abortion": "Pro-life", "education": "School choice", "religious_freedom": "Strong defender", "guns": "A-rating NRA", "immigration": "Secure border", "economy": "Lower taxes"}, "endorsements": ["TBD"], "website": "chriscarr.com", "christian_conservative_rating": "STRONG"},
    {"candidate_id": "burt-jones-ga-gov-2026", "name": "Burt Jones", "race_id": "GA-GOV-2026", "office_sought": "Governor", "party": "Republican", "incumbent": False, "background": "Lieutenant Governor", "positions": {"abortion": "Pro-life", "education": "School choice", "religious_freedom": "Strong defender", "guns": "A-rating NRA", "immigration": "Secure border", "economy": "Lower taxes"}, "endorsements": ["TBD"], "website": "burtjones.com", "christian_conservative_rating": "STRONG"},
    
    # HOUSE DISTRICT 7
    {"candidate_id": "lucy-mcbath-ga-07-2026", "name": "Lucy McBath", "race_id": "GA-07-2026", "office_sought": "U.S. Representative", "party": "Democrat", "incumbent": True, "background": "U.S. Representative since 2019, gun control advocate", "positions": {"abortion": "Pro-choice", "education": "Opposes school choice", "religious_freedom": "Moderate", "guns": "Gun control advocate", "immigration": "Pathway to citizenship", "economy": "Higher spending"}, "endorsements": ["TBD"], "website": "lucymcbath.com", "christian_conservative_rating": "FAILS"},
    
    # HOUSE DISTRICT 6 - Additional candidates
    {"candidate_id": "justin-pinker-ga-06-2026", "name": "Justin Pinker", "race_id": "GA-06-2026", "office_sought": "U.S. Representative", "party": "Republican", "incumbent": False, "background": "Republican challenger", "positions": {"abortion": "Pro-life", "education": "School choice", "religious_freedom": "Defender", "guns": "2nd Amendment", "immigration": "Secure border", "economy": "Lower taxes"}, "endorsements": ["TBD"], "website": "TBD", "christian_conservative_rating": "STRONG"},
    {"candidate_id": "chris-capparell-ga-06-2026", "name": "Chris Capparell", "race_id": "GA-06-2026", "office_sought": "U.S. Representative", "party": "Democrat", "incumbent": False, "background": "Democrat challenger", "positions": {"abortion": "Pro-choice", "education": "Opposes school choice", "religious_freedom": "Moderate", "guns": "Gun control", "immigration": "Pathway to citizenship", "economy": "Higher spending"}, "endorsements": ["TBD"], "website": "TBD", "christian_conservative_rating": "FAILS"},
    {"candidate_id": "sonya-halpern-ga-06-2026", "name": "Sonya Halpern", "race_id": "GA-06-2026", "office_sought": "U.S. Representative", "party": "Democrat", "incumbent": False, "background": "Democrat challenger", "positions": {"abortion": "Pro-choice", "education": "Opposes school choice", "religious_freedom": "Moderate", "guns": "Gun control", "immigration": "Pathway to citizenship", "economy": "Higher spending"}, "endorsements": ["TBD"], "website": "TBD", "christian_conservative_rating": "FAILS"},
]

uploaded = 0
skipped = 0
for candidate in new_candidates:
    key = f"{candidate['name']}|{candidate['race_id']}"
    if key in existing_keys:
        print(f"SKIP: {candidate['name']} (already exists)")
        skipped += 1
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
    print(f"+ {candidate['name']} ({candidate['party']}) - {candidate['office_sought']}")
    uploaded += 1

print(f"\n[SUCCESS] Uploaded {uploaded} new candidates, skipped {skipped} existing")
print(f"Total Georgia candidates now: {len(existing['Items']) + uploaded}")
