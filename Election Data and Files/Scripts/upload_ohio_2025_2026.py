import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Ohio 2025-2026 Races
races = [
    # 2026 Federal Races
    {"state": "Ohio", "office": "U.S. Senate", "election_date": "2026-11-03", "race_type": "general", "description": "Ohio U.S. Senate - Sherrod Brown seat"},
    {"state": "Ohio", "office": "U.S. House District 1", "election_date": "2026-11-03", "race_type": "general", "description": "Cincinnati area"},
    {"state": "Ohio", "office": "U.S. House District 2", "election_date": "2026-11-03", "race_type": "general", "description": "Southern Ohio"},
    {"state": "Ohio", "office": "U.S. House District 3", "election_date": "2026-11-03", "race_type": "general", "description": "Columbus area"},
    {"state": "Ohio", "office": "U.S. House District 4", "election_date": "2026-11-03", "race_type": "general", "description": "Western Ohio"},
    {"state": "Ohio", "office": "U.S. House District 5", "election_date": "2026-11-03", "race_type": "general", "description": "Northwestern Ohio"},
    {"state": "Ohio", "office": "U.S. House District 6", "election_date": "2026-11-03", "race_type": "general", "description": "Eastern Ohio"},
    {"state": "Ohio", "office": "U.S. House District 7", "election_date": "2026-11-03", "race_type": "general", "description": "Central Ohio"},
    {"state": "Ohio", "office": "U.S. House District 8", "election_date": "2026-11-03", "race_type": "general", "description": "Southwestern Ohio"},
    {"state": "Ohio", "office": "U.S. House District 9", "election_date": "2026-11-03", "race_type": "general", "description": "Toledo area"},
    {"state": "Ohio", "office": "U.S. House District 10", "election_date": "2026-11-03", "race_type": "general", "description": "Columbus suburbs"},
    {"state": "Ohio", "office": "U.S. House District 11", "election_date": "2026-11-03", "race_type": "general", "description": "Cleveland area"},
    {"state": "Ohio", "office": "U.S. House District 12", "election_date": "2026-11-03", "race_type": "general", "description": "Central Ohio"},
    {"state": "Ohio", "office": "U.S. House District 13", "election_date": "2026-11-03", "race_type": "general", "description": "Akron area"},
    {"state": "Ohio", "office": "U.S. House District 14", "election_date": "2026-11-03", "race_type": "general", "description": "Northeastern Ohio"},
    {"state": "Ohio", "office": "U.S. House District 15", "election_date": "2026-11-03", "race_type": "general", "description": "Columbus suburbs"},
    
    # 2026 Statewide Races
    {"state": "Ohio", "office": "Governor", "election_date": "2026-11-03", "race_type": "general", "description": "Ohio Governor - Open seat"},
    {"state": "Ohio", "office": "Lieutenant Governor", "election_date": "2026-11-03", "race_type": "general", "description": "Ohio Lieutenant Governor"},
    {"state": "Ohio", "office": "Attorney General", "election_date": "2026-11-03", "race_type": "general", "description": "Ohio Attorney General"},
    {"state": "Ohio", "office": "Secretary of State", "election_date": "2026-11-03", "race_type": "general", "description": "Ohio Secretary of State"},
    {"state": "Ohio", "office": "State Auditor", "election_date": "2026-11-03", "race_type": "general", "description": "Ohio State Auditor"},
    {"state": "Ohio", "office": "State Treasurer", "election_date": "2026-11-03", "race_type": "general", "description": "Ohio State Treasurer"},
]

# Ohio Key Candidates
candidates = [
    # U.S. Senate
    {
        "name": "Sherrod Brown",
        "state": "Ohio",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "Incumbent U.S. Senator since 2007, seeking fourth term. Liberal Democrat with progressive voting record. Vulnerable in increasingly Republican Ohio.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://sherrodbrown.com",
        "positions": {
            "ABORTION": "pro-choice",
            "GUNS": "gun-control",
            "TAXES": "raise-taxes",
            "IMMIGRATION": "open-borders",
            "RELIGIOUS-FREEDOM": "mixed",
            "EDUCATION": "oppose-school-choice"
        },
        "endorsements": ["Planned Parenthood", "NARAL", "Teachers Unions"]
    },
    {
        "name": "Bernie Moreno",
        "state": "Ohio",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Conservative businessman, luxury car dealer, blockchain entrepreneur. Strong Trump supporter. Pro-life, pro-2nd Amendment champion.",
        "faith_statement": "Christian conservative who speaks openly about faith guiding business and political decisions",
        "website": "https://berniemoreno.com",
        "positions": {
            "ABORTION": "pro-life-100-percent",
            "GUNS": "strong-support",
            "TAXES": "lower-taxes",
            "IMMIGRATION": "secure-border",
            "RELIGIOUS-FREEDOM": "strong-support",
            "EDUCATION": "school-choice"
        },
        "endorsements": ["President Trump", "Ohio Right to Life", "NRA"]
    },
    
    # Governor Race
    {
        "name": "Jon Husted",
        "state": "Ohio",
        "office": "Governor",
        "party": "Republican",
        "bio": "Current Lieutenant Governor, former Ohio Secretary of State and State Senator. Conservative leader with executive experience.",
        "faith_statement": "Christian conservative, active in church community",
        "website": "https://jonhusted.com",
        "positions": {
            "ABORTION": "pro-life",
            "GUNS": "strong-support",
            "TAXES": "lower-taxes",
            "RELIGIOUS-FREEDOM": "strong-support",
            "EDUCATION": "school-choice",
            "ECONOMY": "pro-business"
        },
        "endorsements": ["Ohio GOP establishment", "Business community"]
    },
    {
        "name": "Dave Yost",
        "state": "Ohio",
        "office": "Governor",
        "party": "Republican",
        "bio": "Current Ohio Attorney General, former State Auditor. Strong conservative record defending pro-life laws and religious liberty.",
        "faith_statement": "Christian conservative, defender of religious freedom",
        "website": "https://daveyost.com",
        "positions": {
            "ABORTION": "pro-life-defender",
            "GUNS": "strong-support",
            "RELIGIOUS-FREEDOM": "strong-defender",
            "EDUCATION": "school-choice",
            "LAW-ENFORCEMENT": "strong-support"
        },
        "endorsements": ["Ohio Right to Life", "Law enforcement"]
    },
]

print(f"Uploading {len(races)} Ohio races...")
race_ids = {}
for race in races:
    import uuid
    race_id = str(uuid.uuid4())
    race['race_id'] = race_id
    race['created_at'] = datetime.utcnow().isoformat()
    race['created_by'] = 'system'
    races_table.put_item(Item=race)
    race_ids[race['office']] = race_id
    print(f"  Added: {race['office']}")

print(f"\n[SUCCESS] Uploaded {len(races)} races")

print(f"\nUploading {len(candidates)} Ohio candidates...")
for candidate in candidates:
    import uuid
    candidate['candidate_id'] = str(uuid.uuid4())
    if candidate['office'] in race_ids:
        candidate['race_id'] = race_ids[candidate['office']]
    else:
        candidate['race_id'] = ''
    candidate['created_at'] = datetime.utcnow().isoformat()
    candidate['created_by'] = 'system'
    candidate['status'] = 'active'
    candidate['voting_record_url'] = ''
    candidate['photo_url'] = ''
    candidates_table.put_item(Item=candidate)
    print(f"  Added: {candidate['name']} - {candidate['office']}")

print(f"\n[SUCCESS] Uploaded {len(candidates)} candidates")
print("\nNote: Summary will be uploaded separately due to size")
