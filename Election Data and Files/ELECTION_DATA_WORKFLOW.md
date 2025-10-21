# Election Data Management Workflow

## 📋 Overview

This document outlines the complete process for managing election data across election cycles, including gathering races, tracking candidates, and creating voter guides.

---

## 🔄 ANNUAL ELECTION CYCLE WORKFLOW

### Phase 1: Planning (January - March)

**1. Identify Election Year Races**
- Research which states have elections in upcoming cycle
- Determine race types: Governor, Senate, House, State Legislature, Municipal
- Create master list of all races by state

**2. Set Up Database Structure**
```
For each new election cycle:
- Keep existing DynamoDB tables (races, candidates, state-summaries)
- Add new races with proper election_date fields
- Archive previous cycle data if needed
```

**3. Create Race Import Template**
```csv
state,office,election_date,race_type,description
Texas,Governor,2026-11-03,general,Texas Gubernatorial Race
Texas,U.S. Senate,2026-11-03,general,Ted Cruz re-election
```

---

### Phase 2: Data Collection (April - August)

**1. Gather Race Information**

**Sources:**
- Ballotpedia.org - Comprehensive election database
- State Secretary of State websites
- Local election boards
- News sources (Politico, RealClearPolitics)

**Script to Import Races:**
```python
# Use: import_races.py
import boto3, csv, uuid
from datetime import datetime

db = boto3.resource('dynamodb')
table = db.Table('races')

with open('races_2028.csv', encoding='utf-8') as f:
    for race in csv.DictReader(f):
        table.put_item(Item={
            'race_id': str(uuid.uuid4()),
            'state': race['state'],
            'office': race['office'],
            'election_date': race['election_date'],
            'race_type': race['race_type'],
            'description': race['description'],
            'created_at': datetime.utcnow().isoformat(),
            'created_by': 'admin@system.com'
        })
```

**2. Track Candidate Announcements**

**Monitoring System:**
- Set up Google Alerts for "[State] [Office] candidate announces"
- Follow state political news sites
- Monitor candidate filing deadlines
- Track FEC filings for federal races

**Candidate Tracking Spreadsheet:**
```
State | Office | Candidate Name | Party | Announced Date | Website | Status
Texas | Governor | Greg Abbott | R | 2025-01-15 | url | Confirmed
```

---

### Phase 3: Candidate Research (Ongoing)

**1. Research Each Candidate**

**Information to Gather:**
- Full name and party affiliation
- Campaign website
- Bio (background, experience, key accomplishments)
- Faith statement (public statements about faith)
- Policy positions (abortion, guns, education, etc.)
- Endorsements (organizations, leaders)

**Research Sources:**
- Candidate websites
- iVoterGuide.org
- Project Vote Smart
- News articles and interviews
- Social media (Twitter/X, Facebook)
- Church affiliations (if public)

**2. Create Candidate Import CSV**
```csv
name,state,office,party,bio,website,faith_statement,positions,endorsements
Greg Abbott,Texas,Governor,Republican,Incumbent Governor...,url,Catholic faith...,abortion:pro-life;guns:strong,Texas Right to Life;NRA
```

**3. Import Candidates Script**
```python
# Use: import_candidates.py
# Links candidates to races via race_id
# See upload_2026_candidates.py for full example
```

---

### Phase 4: Candidate Updates (As Races Develop)

**1. Update Existing Candidates**

**When to Update:**
- Candidate drops out → Change status to 'withdrawn'
- New endorsements → Add to endorsements list
- Policy changes → Update positions
- New information → Enhance bio

**Update Script:**
```python
# update_candidate.py
import boto3

db = boto3.resource('dynamodb')
table = db.Table('candidates')

# Update candidate by name and state
response = table.scan(
    FilterExpression='#name = :name AND #state = :state',
    ExpressionAttributeNames={'#name': 'name', '#state': 'state'},
    ExpressionAttributeValues={':name': 'John Doe', ':state': 'Texas'}
)

if response['Items']:
    candidate = response['Items'][0]
    table.update_item(
        Key={'candidate_id': candidate['candidate_id']},
        UpdateExpression='SET #status = :status, updated_at = :time',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={
            ':status': 'withdrawn',
            ':time': datetime.utcnow().isoformat()
        }
    )
```

**2. Add New Candidates**

**When Candidates Announce:**
- Create new CSV row with candidate info
- Run import script to add to database
- Automatically links to race via state + office matching

---

### Phase 5: Voter Guide Creation (June - October)

**1. Generate State Summaries**

**Template Structure:**
```markdown
# [State] [Year] Elections - Complete Christian Conservatives Today Guide

## Database Summary
- Total Races
- Total Candidates
- Election Dates

## Political Landscape
- State overview
- Why it matters for conservatives

## Top Priority Races
- Governor
- U.S. Senate
- U.S. House
- State Legislature
- Local races

## Key Issues
- Life & Family
- Education & Parental Rights
- Religious Liberty
- Crime & Safety
- Economy

## Voter Strategy
- Priority races
- How to support
- Church mobilization

## Resources
- Voter guides
- Election info
- Conservative organizations

## Prayer Points
```

**2. Upload Summaries**
```python
# upload_summary.py
import boto3, uuid
from datetime import datetime

db = boto3.resource('dynamodb')
table = db.Table('state-summaries')

with open('state_summary.md', encoding='utf-8') as f:
    content = f.read()

table.put_item(Item={
    'state': 'Texas',
    'title': 'Texas 2026 Elections - Complete Christian Conservatives Today Guide',
    'election_year': '2026',
    'content': content,
    'created_at': datetime.utcnow().isoformat(),
    'updated_at': datetime.utcnow().isoformat(),
    'created_by': 'admin@system.com',
    'status': 'published'
})
```

---

## 🔧 AUTOMATION TOOLS

### 1. Race Import Automation

**Script: `bulk_import_races.py`**
```python
# Imports all races from CSV for new election cycle
# Validates data before import
# Checks for duplicates
# Logs all imports
```

### 2. Candidate Tracking System

**Script: `candidate_tracker.py`**
```python
# Monitors candidate announcements
# Sends alerts when new candidates file
# Tracks filing deadlines by state
# Generates weekly reports
```

### 3. Data Quality Checker

**Script: `validate_election_data.py`**
```python
# Checks for races without candidates
# Identifies missing information
# Validates date formats
# Ensures race_id links are correct
```

### 4. Summary Generator Helper

**Script: `generate_summary_template.py`**
```python
# Creates summary template for each state
# Pre-fills with race and candidate data
# Leaves sections for manual content
# Formats in markdown
```

---

## 📊 MONITORING & MAINTENANCE

### Weekly Tasks
- [ ] Check for new candidate announcements
- [ ] Update candidate statuses (if any drop out)
- [ ] Add new endorsements
- [ ] Review news for policy changes

### Monthly Tasks
- [ ] Run data quality checker
- [ ] Update summaries with new information
- [ ] Verify all race dates are correct
- [ ] Check for new races added

### Pre-Election Tasks (2 months before)
- [ ] Final candidate verification
- [ ] Update all summaries
- [ ] Verify all links work
- [ ] Check endorsement accuracy
- [ ] Final data quality check

---

## 📁 FILE ORGANIZATION

```
Election Data and Files/
├── CSV files/
│   ├── races_2026.csv
│   ├── races_2028.csv
│   ├── candidates_2026.csv
│   ├── candidates_2028.csv
│   └── archived/
│       ├── races_2024.csv
│       └── candidates_2024.csv
├── Voter Guides_Summaries/
│   ├── 2026/
│   │   ├── texas_summary_guide.md
│   │   ├── california_summary_guide.md
│   │   └── ...
│   └── 2028/
│       └── (future summaries)
├── Scripts/
│   ├── import_races.py
│   ├── import_candidates.py
│   ├── update_candidate.py
│   ├── upload_summary.py
│   ├── validate_election_data.py
│   └── generate_summary_template.py
└── Documentation/
    ├── ELECTION_DATA_WORKFLOW.md (this file)
    └── API_DOCUMENTATION.md
```

---

## 🔄 REPLICATION FOR NEXT CYCLE

### Step-by-Step Process for 2028 Elections:

**1. January 2027: Planning**
```bash
# Create new CSV templates
cp races_2026.csv races_2028.csv
# Clear old data, keep structure
```

**2. February-March 2027: Research**
- Identify all 2028 races (Governor, Senate, House)
- Create master race list
- Import to database

**3. April-December 2027: Candidate Tracking**
- Monitor candidate announcements
- Research each candidate
- Import as they announce
- Update continuously

**4. January-October 2028: Voter Guides**
- Create state summaries
- Update with latest info
- Publish to database

**5. November 2028: Election Day**
- Final updates
- Post-election: Archive data

---

## 🤖 FUTURE AUTOMATION IDEAS

### Advanced Features:
1. **API Integration**
   - Connect to Ballotpedia API
   - Auto-import race data
   - Real-time candidate updates

2. **Web Scraping**
   - Monitor candidate websites
   - Track policy changes
   - Alert on new endorsements

3. **AI-Assisted Research**
   - Use AI to summarize candidate bios
   - Generate initial policy summaries
   - Draft summary templates

4. **Notification System**
   - Email alerts for new candidates
   - Slack/Discord notifications
   - Weekly digest reports

5. **Dashboard**
   - Visual progress tracker
   - Data completeness metrics
   - State-by-state status

---

## 📞 SUPPORT & RESOURCES

### Key Websites:
- **Ballotpedia.org** - Comprehensive election database
- **iVoterGuide.org** - Christian voter guides
- **FEC.gov** - Federal candidate filings
- **State SOS websites** - Official election info

### Contact for Updates:
- Monitor state political news sites
- Follow conservative organizations
- Join state GOP email lists
- Connect with local campaign offices

---

## ✅ CHECKLIST FOR NEW ELECTION CYCLE

- [ ] Research all races for cycle
- [ ] Create races CSV
- [ ] Import races to database
- [ ] Set up candidate tracking
- [ ] Monitor announcements
- [ ] Research candidates as they announce
- [ ] Import candidates to database
- [ ] Link candidates to races
- [ ] Create state summaries
- [ ] Upload summaries to database
- [ ] Update continuously until election
- [ ] Archive after election

---

**This workflow ensures comprehensive, accurate, and up-to-date election data for every cycle!**
