import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Pennsylvania 2026 Races
races = [
    # Federal Races
    {"state": "Pennsylvania", "office": "U.S. Senate", "election_date": "2026-11-03", "race_type": "general", "description": "Pennsylvania U.S. Senate seat"},
    {"state": "Pennsylvania", "office": "U.S. House District 1", "election_date": "2026-11-03", "race_type": "general", "description": "Philadelphia area"},
    {"state": "Pennsylvania", "office": "U.S. House District 2", "election_date": "2026-11-03", "race_type": "general", "description": "Philadelphia"},
    {"state": "Pennsylvania", "office": "U.S. House District 3", "election_date": "2026-11-03", "race_type": "general", "description": "Harrisburg area"},
    {"state": "Pennsylvania", "office": "U.S. House District 4", "election_date": "2026-11-03", "race_type": "general", "description": "Chester County"},
    {"state": "Pennsylvania", "office": "U.S. House District 5", "election_date": "2026-11-03", "race_type": "general", "description": "Northeastern PA"},
    {"state": "Pennsylvania", "office": "U.S. House District 6", "election_date": "2026-11-03", "race_type": "general", "description": "Reading area"},
    {"state": "Pennsylvania", "office": "U.S. House District 7", "election_date": "2026-11-03", "race_type": "general", "description": "Lehigh Valley"},
    {"state": "Pennsylvania", "office": "U.S. House District 8", "election_date": "2026-11-03", "race_type": "general", "description": "Scranton area"},
    {"state": "Pennsylvania", "office": "U.S. House District 9", "election_date": "2026-11-03", "race_type": "general", "description": "Central PA"},
    {"state": "Pennsylvania", "office": "U.S. House District 10", "election_date": "2026-11-03", "race_type": "general", "description": "Harrisburg"},
    {"state": "Pennsylvania", "office": "U.S. House District 11", "election_date": "2026-11-03", "race_type": "general", "description": "Wilkes-Barre area"},
    {"state": "Pennsylvania", "office": "U.S. House District 12", "election_date": "2026-11-03", "race_type": "general", "description": "York area"},
    {"state": "Pennsylvania", "office": "U.S. House District 13", "election_date": "2026-11-03", "race_type": "general", "description": "Montgomery County"},
    {"state": "Pennsylvania", "office": "U.S. House District 14", "election_date": "2026-11-03", "race_type": "general", "description": "Pittsburgh area"},
    {"state": "Pennsylvania", "office": "U.S. House District 15", "election_date": "2026-11-03", "race_type": "general", "description": "Allentown area"},
    {"state": "Pennsylvania", "office": "U.S. House District 16", "election_date": "2026-11-03", "race_type": "general", "description": "Lancaster area"},
    {"state": "Pennsylvania", "office": "U.S. House District 17", "election_date": "2026-11-03", "race_type": "general", "description": "Western PA"},
    
    # Statewide Races
    {"state": "Pennsylvania", "office": "Governor", "election_date": "2026-11-03", "race_type": "general", "description": "Pennsylvania Governor"},
    {"state": "Pennsylvania", "office": "Lieutenant Governor", "election_date": "2026-11-03", "race_type": "general", "description": "Pennsylvania Lieutenant Governor"},
    {"state": "Pennsylvania", "office": "Attorney General", "election_date": "2026-11-03", "race_type": "general", "description": "Pennsylvania Attorney General"},
    {"state": "Pennsylvania", "office": "Auditor General", "election_date": "2026-11-03", "race_type": "general", "description": "Pennsylvania Auditor General"},
    {"state": "Pennsylvania", "office": "State Treasurer", "election_date": "2026-11-03", "race_type": "general", "description": "Pennsylvania State Treasurer"},
]

# Pennsylvania Key Candidates (sample - will need full list)
candidates = [
    # U.S. Senate
    {"name": "Bob Casey Jr.", "state": "Pennsylvania", "office": "U.S. Senate", "party": "Democrat", "bio": "Incumbent U.S. Senator since 2007", "faith_statement": "", "website": "", "positions": {}, "endorsements": []},
    
    # Governor Race
    {"name": "Josh Shapiro", "state": "Pennsylvania", "office": "Governor", "party": "Democrat", "bio": "Current Pennsylvania Governor", "faith_statement": "", "website": "", "positions": {}, "endorsements": []},
]

# Pennsylvania Summary
summary = {
    "state": "Pennsylvania",
    "title": "Pennsylvania 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Pennsylvania 2025-2026 Election Guide

## Overview
Pennsylvania stands as one of America's most critical battleground states, where Christian conservative values meet the challenges of modern governance. With 13 million residents and a rich heritage of faith-based communities, the Keystone State's 2026 elections will shape the future of religious freedom, family values, and constitutional principles.

## Key Races

### Federal Elections
**U.S. Senate (2026)**
- Incumbent: Bob Casey Jr. (D)
- Critical race for Senate control
- Key issues: Religious freedom, life, family values

**U.S. House - All 17 Districts**
Pennsylvania's congressional delegation plays a vital role in national policy affecting Christian values and conservative principles.

### Statewide Offices
**Governor (2026)**
- Current: Josh Shapiro (D)
- Open or contested seat
- Executive authority over religious freedom, education, life issues

**Lieutenant Governor, Attorney General, Auditor General, State Treasurer**
These offices significantly impact state policy on family values, religious liberty, and fiscal responsibility.

## Christian Conservative Priorities

### Life and Family
- **Pro-Life Protections**: Pennsylvania's abortion laws and protections for the unborn
- **Parental Rights**: Education freedom and parental authority in schools
- **Marriage and Family**: Traditional marriage and family structure support

### Religious Freedom
- **Church Liberty**: Protection from government overreach
- **Conscience Rights**: Healthcare worker and business owner protections
- **School Choice**: Educational freedom including Christian schools

### Constitutional Values
- **Second Amendment**: Gun rights and self-defense
- **Free Speech**: Protection of Christian expression in public square
- **Limited Government**: Reducing government interference in faith and family

## Biblical Perspective
*"Righteousness exalts a nation, but sin condemns any people."* - Proverbs 14:34

Pennsylvania's elections are not merely political contests but spiritual battles for the soul of our commonwealth. Christian conservatives must engage with biblical wisdom, prayerful discernment, and active participation.

## Prayer Points
1. **Wisdom for Voters**: That Pennsylvania Christians would vote according to biblical principles
2. **Godly Leadership**: For candidates who fear the Lord and uphold righteousness
3. **Protection of Life**: For strong pro-life leadership at all levels
4. **Religious Freedom**: For continued liberty to worship and live out our faith
5. **Family Values**: For leaders who will protect marriage and parental rights

## Action Steps
1. **Register to Vote**: Ensure your voter registration is current
2. **Research Candidates**: Use Christian voter guides and scorecards
3. **Pray Regularly**: Intercede for Pennsylvania's elections and leaders
4. **Volunteer**: Support godly candidates with time and resources
5. **Vote**: Exercise your civic duty on Election Day

## Important Dates
- **Voter Registration Deadline**: 15 days before election
- **Early Voting**: Check county election office for dates
- **Election Day**: November 3, 2026

## Resources
- **Pennsylvania Family Institute**: Christian policy organization
- **Pennsylvania Pro-Life Federation**: Life advocacy
- **iVoterGuide Pennsylvania**: Biblical worldview candidate ratings
- **Family Research Council Action**: Federal candidate scorecards

## Conclusion
Pennsylvania's 2026 elections represent a pivotal moment for Christian conservatives. Our participation is not optional but a biblical mandate to be salt and light in our society. Let us engage with wisdom, vote with conviction, and trust God for His purposes in our state.

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - Proverbs 29:2

---
**Last Updated**: January 2025
**Source**: Christian Conservatives Today Election Coverage
**Contact**: For questions or to contribute state coverage, email contact@ekewaka.com
""",
    "last_updated": datetime.utcnow().isoformat(),
    "updated_by": "system"
}

print("Uploading Pennsylvania races...")
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

print(f"\nUploaded {len(races)} races")

print("\nUploading Pennsylvania candidates...")
for candidate in candidates:
    import uuid
    candidate['candidate_id'] = str(uuid.uuid4())
    # Auto-match to race
    if candidate['office'] in race_ids:
        candidate['race_id'] = race_ids[candidate['office']]
    else:
        candidate['race_id'] = ''
    candidate['created_at'] = datetime.utcnow().isoformat()
    candidate['created_by'] = 'system'
    candidate['status'] = 'active'
    candidate['voting_record_url'] = ''
    candidates_table.put_item(Item=candidate)
    print(f"  Added: {candidate['name']} - {candidate['office']}")

print(f"\nUploaded {len(candidates)} candidates")

print("\nUploading Pennsylvania summary...")
summaries_table.put_item(Item=summary)
print("  Summary uploaded successfully")

print("\n[SUCCESS] Pennsylvania data upload complete!")
print(f"   Races: {len(races)}")
print(f"   Candidates: {len(candidates)}")
print(f"   Summary: Uploaded")
