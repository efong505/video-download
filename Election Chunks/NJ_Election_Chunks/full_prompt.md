```
Where [STATE NAME] equals, New Jersey, create complete 2025-2026 election data for [STATE NAME] including races, candidates, and comprehensive voter guide.

**IMPORTANT: Include BOTH 2025 AND 2026 elections. Many states have municipal, school board, and local elections in 2025 (odd-year elections). DO NOT skip 2025 races.**

**DELIVERABLES:**

1. **Python Upload Script** (complete, ready to run)
2. **Races Array** (all major 2025-2026 races)
3. **Candidates Array** (major candidates with full profiles)
4. **Comprehensive Summary** (20,000+ character markdown guide)

---

## PART 1: PYTHON UPLOAD SCRIPT

Create a complete Python script named `upload_[state]_data.py` with this structure:

```python
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# [STATE NAME] Races
races = [
    # YOUR RACES HERE
]

# [STATE NAME] Candidates  
candidates = [
    # YOUR CANDIDATES HERE
]

# [STATE NAME] Summary
summary = {
    "state": "[STATE NAME]",
    "title": "[STATE NAME] 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """[YOUR COMPREHENSIVE SUMMARY HERE]""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing [STATE NAME] races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': '[STATE NAME]'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} [STATE NAME] races...")
race_ids = {}
for race in races:
    office = race['office']
    if office in existing_race_map:
        race_id = existing_race_map[office]
        race['race_id'] = race_id
        race['updated_at'] = datetime.now().isoformat()
        races_table.put_item(Item=race)
        print(f"  Updated: {office}")
    else:
        race_id = str(uuid.uuid4())
        race['race_id'] = race_id
        race['created_at'] = datetime.now().isoformat()
        race['created_by'] = 'system'
        races_table.put_item(Item=race)
        print(f"  Created: {office}")
    race_ids[office] = race_id
print(f"\n[SUCCESS] Processed {len(races)} races")

print(f"\nChecking for existing [STATE NAME] candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': '[STATE NAME]'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} [STATE NAME] candidates...")
for candidate in candidates:
    name = candidate['name']
    office = candidate['office']
    key = (name, office)
    if office in race_ids:
        candidate['race_id'] = race_ids[office]
    else:
        candidate['race_id'] = ''
    if key in existing_candidate_map:
        candidate_id = existing_candidate_map[key]
        candidate['candidate_id'] = candidate_id
        candidate['updated_at'] = datetime.now().isoformat()
        candidate['status'] = 'active'
        candidates_table.put_item(Item=candidate)
        print(f"  Updated: {name} - {office}")
    else:
        candidate_id = str(uuid.uuid4())
        candidate['candidate_id'] = candidate_id
        candidate['created_at'] = datetime.now().isoformat()
        candidate['created_by'] = 'system'
        candidate['status'] = 'active'
        candidates_table.put_item(Item=candidate)
        print(f"  Created: {name} - {office}")
print(f"\n[SUCCESS] Processed {len(candidates)} candidates")

print("\nProcessing [STATE NAME] summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': '[STATE NAME]'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] [STATE NAME] data upload complete!")
```

---

## PART 2: RACES ARRAY

**COMPREHENSIVE COVERAGE REQUIRED**

Research and create races for [STATE NAME] 2025-2026:

**CRITICAL INSTRUCTIONS:**
- Include elections from BOTH 2025 and 2026
- Include ALL races in the categories below, not just "major" or "competitive" ones
- School boards, municipal races, and some state positions have 2025 elections - DO NOT skip them
- **TARGET RACE COUNT:**
  - Large states (CA, TX, FL, NY, PA, OH, IL, NJ, etc.): 50-100+ races
  - Medium states (VA, NC, GA, MI, WA, AZ, etc.): 30-60 races
  - Small states (WY, VT, DE, AK, MT, ND, SD, etc.): 15-35 races
- Include both contested AND uncontested races where incumbents are running
- DO NOT filter down to only "key" races - include everything available for the state

**Federal Races (INCLUDE ALL):**
- U.S. Senate (if up in 2026) - include ALL candidates
- U.S. House - **EVERY SINGLE DISTRICT** (e.g., NJ has 12 districts - include all 12)

**Statewide Races:**
- Governor (if up in 2026)
- Lieutenant Governor
- Attorney General
- Secretary of State
- State Treasurer
- Comptroller/Controller
- State Auditor
- Commissioner of Agriculture
- Commissioner of Insurance
- Land Commissioner (if applicable)
- Superintendent of Public Instruction
- Other statewide offices

**State Legislature (INCLUDE MANY):**
- State Senate - include at least 10-20 competitive/notable districts
- State House/Assembly - include at least 20-30 competitive/notable districts
- DO NOT limit to only 2-3 districts - include comprehensive coverage

**County-Level Races:**
- County Commissioners/Supervisors
- Sheriff
- District Attorney/Prosecutor
- County Clerk
- County Treasurer

**Municipal Races (if applicable):**
- Major city mayors
- Key city council races

**School Board Races (REQUIRED - DO NOT SKIP - OFTEN IN 2025):**
- State Board of Education (if elected)
- **ALL major city school boards** - include at least 10-20 school board races
- Include ALL contested school board seats with district numbers
- Example: Newark, Jersey City, Paterson, Camden, Trenton, Elizabeth, Edison, Woodbridge, etc.
- For each major district, include multiple seat races (e.g., "Newark Board of Education At-Large Seat 1", "Seat 2", etc.)
- Example format: "Albuquerque School Board District 3", "Santa Fe School Board District 5"
- School boards are CRITICAL for parental rights and education policy
- **NOTE: Most school board elections are in 2025 (odd-year), NOT 2026**
- **MINIMUM: 15-20 school board races across the state**

**Judicial Races (if applicable):**
- State Supreme Court (election or retention)
- Court of Appeals
- District Court judges (major districts)

**Special Districts (if major/contested):**
- Water/Irrigation Districts (Western states)
- Hospital Districts
- Regional Transit Authorities
- Public Service/Corporation Commission

**Ballot Measures (if applicable):**
- Constitutional amendments affecting religious liberty, life, family values
- Education funding/school choice initiatives
- Tax/spending measures

**Format each race as:**
```python
{
    "state": "[STATE NAME]",
    "office": "[Office Title]",
    "election_date": "2026-11-03",  # or actual date
    "race_type": "general",
    "description": "[Brief description of race significance]"
}
```

**SCHOOL BOARD RACE EXAMPLES (REQUIRED FORMAT - 2025 ELECTIONS):**
```python
# ALBUQUERQUE SCHOOL BOARD 2025 - ALL FOUR DISTRICTS REQUIRED:
{
    "state": "New Mexico",
    "office": "Albuquerque School Board District 3",
    "election_date": "2025-11-04",
    "race_type": "general",
    "description": "Critical race for parental rights and curriculum control - Danielle Gonzales (incumbent) vs challengers"
},
{
    "state": "New Mexico",
    "office": "Albuquerque School Board District 5",
    "election_date": "2025-11-04",
    "race_type": "general",
    "description": "Open seat - Joshua S. Martinez vs Brian Kevin Laurent Jr."
},
{
    "state": "New Mexico",
    "office": "Albuquerque School Board District 6",
    "election_date": "2025-11-04",
    "race_type": "general",
    "description": "Open seat - David Adam Ams vs Margaret S. Warigia Bowman"
},
{
    "state": "New Mexico",
    "office": "Albuquerque School Board District 7",
    "election_date": "2025-11-04",
    "race_type": "general",
    "description": "Courtney Jackson (incumbent) vs Kristin Renee Wood-Hegner"
}
```

---

## PART 3: CANDIDATES ARRAY

Research and create candidate profiles for [STATE NAME]:

**For EACH major candidate, include:**

```python
{
    "name": "[Full Name]",
    "state": "[STATE NAME]",
    "office": "[Office - must match race office exactly]",
    "party": "[Republican/Democrat/Independent/Libertarian]",
    "status": "active",  # Use "dropped_out" if candidate withdrew from race
    "bio": "[Detailed 200-300 word biography including: background, career, family, accomplishments, current position. If dropped out, add '(DROPPED OUT - [Date])' at the start]",
    "faith_statement": "[Actual faith statement from candidate OR 'No publicly disclosed faith statement']",
    "website": "[https://candidatewebsite.com OR '' if no website - DO NOT use 'Not available' or 'N/A']",
    "positions": {
        "ABORTION": "[Detailed position: pro-life with specifics OR pro-choice with specifics]",
        "EDUCATION": "[School choice stance, parental rights position]",
        "RELIGIOUS-FREEDOM": "[Specific stance on religious liberty]",
        "GUNS": "[2nd Amendment position with specifics]",
        "TAXES": "[Tax policy position]",
        "IMMIGRATION": "[Border security/immigration stance]",
        "FAMILY-VALUES": "[Traditional marriage, parental rights, gender ideology stance]",
        "ELECTION-INTEGRITY": "[Voter ID, election security position]"
    },
    "endorsements": ["[Organization 1]", "[Organization 2]", "[Organization 3]"]
}
```

**CRITICAL REQUIREMENTS:**
- Research REAL candidates currently running or likely to run
- **INCLUDE dropped-out candidates** - mark their status as "dropped_out" in the candidate record
- For dropped-out candidates, add "(DROPPED OUT - [Date])" to their bio
- Find ACTUAL faith statements from interviews, websites, speeches
- Include REAL endorsements from organizations
- Provide DETAILED positions, not generic statements
- Cover at least 2-3 major candidates per top race
- **SCHOOL BOARDS ARE MANDATORY** - Include ALL contested school board races with district numbers and candidate names

**COMPLETENESS REQUIREMENT:**
- **WRITE OUT EVERY SINGLE CANDIDATE** - do not abbreviate, summarize, or use placeholders
- **CANDIDATE TARGET (2-3 per race):**
  - Large states: 100-200+ candidates
  - Medium states: 60-120 candidates
  - Small states: 30-70 candidates
- Each candidate must have ALL fields filled: name, state, office, party, status, bio, faith_statement, website, positions (all 8), endorsements
- **NO shortcuts like "# Add more here" or "for brevity" - write the complete data**
- **DO NOT filter to only "major" or "competitive" races - provide comprehensive coverage for the state size**

---

## PART 4: COMPREHENSIVE SUMMARY

Create 20,000-25,000 character markdown guide with this EXACT structure:

```markdown
# [STATE NAME] 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** [NUMBER from your races array]
**Total Candidates Profiled:** [NUMBER from your candidates array]
**Election Dates:**
- [DATE] ([ELECTION TYPE])
- [DATE] ([ELECTION TYPE])

---

## 🔴 [STATE NAME] POLITICAL LANDSCAPE

### **The [State Nickname]**

[STATE NAME] is a **[POLITICAL CHARACTERIZATION]**:
- **[Category]:** [Detailed state-specific description]
- **[Category]:** [Detailed state-specific description]
- **Urban-Rural Divide:** [Specific cities and counties]
- **[Unique State Factor]:** [Details]

### **Why [STATE NAME] Matters**

[STATE NAME] is **CRITICAL/WINNABLE** for Christian conservatives:
- ✅ **Pro-Life Leadership:** [State-specific abortion laws, restrictions, challenges]
- ✅ **Second Amendment:** [State gun rights status]
- ✅ **School Choice:** [State education freedom programs]
- ✅ **Religious Liberty:** [State protections and threats]
- ✅ **Family Values:** [State marriage/parental rights status]
- ✅ **[Additional Strength]:** [Details]

---

## 🔴 [YEAR] [RACE CATEGORY]

### **[Specific Race Name]** - [Date]

**Context:** [Why this race matters - 2-3 sentences with specific impact]

**[Candidate Name] ([Party])** - [Title]

**Faith Statement:** "[Actual statement OR 'No publicly disclosed faith statement']"

**Background:**
- [Specific background detail]
- [Career accomplishment]
- [Family/personal detail]

**Christian Conservative Analysis:**
- **Pro-Life:** [Specific record with votes/statements]
- **Religious Liberty:** [Specific stance with examples]
- **Education/Parental Rights:** [Specific position]
- **Family Values:** [Biblical alignment assessment]
- **Overall Assessment:** [X/10 rating with explanation]

**Key Positions:**
- **ABORTION:** [Detailed position]
- **EDUCATION:** [Detailed position]
- **RELIGIOUS FREEDOM:** [Detailed position]
- **GUNS:** [Detailed position]
- **TAXES:** [Detailed position]
- **[State-Specific Issue]:** [Position]

**Endorsements:** [List with organizations]

**Website:** [URL]

[REPEAT FOR EACH MAJOR CANDIDATE]

**Why It Matters:** [Single powerful sentence]

---

[REPEAT RACE STRUCTURE FOR ALL MAJOR RACES]

---

## 🎯 KEY ISSUES FOR [STATE NAME] CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- [State-specific pro-life laws and status]
- [Pregnancy resource centers in state]
- [Parental consent laws]
- [State funding issues]
- [Recent victories or challenges]

**Progressive Position:**
- [State-specific threats]
- [Abortion expansion efforts]
- [Funding battles]

**Christian Conservative Action:**
- [Specific state organizations to join]
- [Specific state legislation to support]
- [Specific volunteer opportunities]
- [Voting guidance]

### **School Choice & Parental Rights**

**Conservative Position:**
- [State's current school choice programs with details]
- [Parental rights laws]
- [CRT/gender ideology bans]
- [Homeschool freedom status]
- [Recent wins]

**Progressive Position:**
- [Teachers union control]
- [DEI mandates]
- [Threats to choice]

**Christian Conservative Action:**
- [Run for state school boards]
- [Support state legislation]
- [Join state organizations]

[CONTINUE FOR ALL 8 KEY ISSUES WITH STATE-SPECIFIC DETAILS]

---

## 📅 CRITICAL DATES

**[YEAR] Election Calendar:**
- **[Date]** - Voter registration deadline
- **[Date]** - Early voting begins
- **[Date]** - Primary Election
- **[Date]** - General Election

**Voter Registration:** [State-specific website]

---

## 🗳️ CHURCH MOBILIZATION STRATEGY

### **What Pastors Can Do (501c3 Compliant):**

✅ **Endorse candidates from pulpit** (IRS now permits pastoral endorsements)
✅ **Distribute non-partisan voter guides** (iVoterGuide, Christian Voter Guide)
✅ **Host candidate forums** (invite all candidates)
✅ **Preach on biblical citizenship** (Romans 13, Proverbs 29:2)
✅ **Voter registration drives** after services
✅ **Encourage early voting** and provide transportation
✅ **Prayer emphasis** for elections and candidates

❌ **Cannot donate church funds** to campaigns (personal donations allowed)

### **What Church Members Can Do:**

✅ **Volunteer for campaigns** (door-knocking, phone banking)
✅ **Donate to candidates** who align with biblical values
✅ **Host house parties** for conservative candidates
✅ **Share on social media** with #[State]FaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR [STATE NAME] CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - [State] coverage
- **[State] Right to Life** - Pro-life ratings
- **[State] Family Policy Council** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **[State] Secretary of State**: [website]
- **County Election Offices**: [how to find]
- **Early Voting Locations**: [how to find]

### **Conservative Organizations:**
- **[State] Right to Life**: [website]
- **[State] Family Alliance**: [website]
- **[State] Gun Rights Organization**: [website]
- **[State] School Choice Organization**: [website]
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR [STATE NAME] CHRISTIANS

**[YEAR] Elections Matter:**
- [Specific race] determines [specific outcome]
- [Specific race] affects [specific policy]
- [Specific race] impacts [specific community]
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ [State-specific positive outcome]
✅ [State-specific positive outcome]
✅ [State-specific positive outcome]

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ [State-specific negative outcome]
❌ [State-specific negative outcome]
❌ [State-specific negative outcome]

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- [Specific candidate names] and their families
- [State] Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in [State]
- Revival and awakening in [State]
- God's will in [State] elections

**Scripture for [STATE NAME] Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** [Month Year]
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute [STATE NAME] coverage, email contact@ekewaka.com

**[STATE NAME] CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**
```

---

**CRITICAL FORMATTING REQUIREMENTS:**
1. Use `**bold**` for all labels, candidate names, key terms
2. Include ALL emojis in section headers (📊, 🔴, 🎯, 📅, 🗳️, 📞, 🔥, 🙏)
3. Use `---` horizontal dividers between major sections
4. Use ✅ for positive points, ❌ for negative points
5. Italicize all scripture quotes with *asterisks*
6. Total length: 15,000-25,000 characters
7. Include specific candidate names, races, and details from my database
8. Provide detailed Christian conservative analysis for each major candidate
9. Address all 8 key focus areas with state-specific details
10. Include faith statements for candidates where available

**RESEARCH REQUIREMENTS:**
- Research actual candidates running in [STATE] 2025-2026
- Find real faith statements, voting records, endorsements
- Include specific state laws, policies, and political context
- Provide accurate election dates and voter registration info
- List real state organizations and resources with websites
- Give specific, actionable guidance for [STATE] Christian voters
---

## OUTPUT FORMAT

**CRITICAL: DO NOT ABBREVIATE OR SUMMARIZE**

Provide the complete Python script with:
1. **FULL races array** - every single race entry written out completely
2. **FULL candidates array** - every single candidate entry written out completely
3. **FULL summary content** - complete 20,000+ character markdown guide

**ABSOLUTELY FORBIDDEN:**
- ❌ "# Add more candidates here..."
- ❌ "# ... (abbreviated for brevity)"
- ❌ "# Assume 50 total"
- ❌ Any comments suggesting incomplete data
- ❌ Placeholder text like "[more entries]"

**REQUIRED:**
- ✅ Write out EVERY race completely
- ✅ Write out EVERY candidate completely
- ✅ Include ALL fields for each entry
- ✅ Make the script immediately runnable without edits

The script must be **production-ready** and **complete** - no abbreviations, no placeholders, no "for brevity" shortcuts.

Ready to run: `python upload_[state]_data.py`

---

**NOW CREATE COMPLETE DATA FOR: [STATE NAME]**

**FINAL REMINDER BEFORE YOU START:**

1. **DO NOT ABBREVIATE** - Write every race and every candidate in full
2. **NO PLACEHOLDERS** - No "# Add more here" or "for brevity" comments
3. **PRODUCTION READY** - The script must run immediately without any edits
4. **COUNT ACCURATELY** - The summary numbers must match the actual array lengths
5. **COMPLETE FIELDS** - Every candidate needs all 8 position fields filled out
6. **COMPREHENSIVE COVERAGE** - Aim for 50-100+ races and 100-200+ candidates
7. **DO NOT FILTER** - Include ALL federal races, many state legislative races, all major school boards
8. **NO "MAJOR ONLY" FILTERING** - Do not limit to only "competitive" or "key" races

If you find yourself wanting to write "for brevity" or "add more here", STOP and write out the complete data instead.

If you find yourself thinking "I'll just include the major races", STOP and include comprehensive coverage instead.

**TARGET BASED ON STATE SIZE:**
- Large states: 50-100+ races, 100-200+ candidates
- Medium states: 30-60 races, 60-120 candidates  
- Small states: 15-35 races, 30-70 candidates

**CRITICAL VERIFICATION BEFORE SUBMITTING:**

**STEP 1: COUNT YOUR ARRAYS**
- Manually count every item in your races array from first { to last }
- Manually count every item in your candidates array from first { to last }
- Write down: "I have X races and Y candidates"

**STEP 2: UPDATE SUMMARY WITH EXACT COUNTS**
- In the summary content, find the line: **Total Races Documented:** 
- Replace with the EXACT number from your races array count
- Find the line: **Total Candidates Profiled:**
- Replace with the EXACT number from your candidates array count

**STEP 3: DOUBLE-CHECK**
- Count the races array again to verify
- Count the candidates array again to verify
- Verify the summary numbers match your counts EXACTLY
- DO NOT use estimated numbers like "100+" or "50-60" - use EXACT counts
- DO NOT guess or approximate - count every single item

**Example:**
If you count 23 items in races array, write: "Total Races Documented: 23"
If you count 45 items in candidates array, write: "Total Candidates Profiled: 45"

**IMPORTANT NOTES:**
- This script should contain ALL races and candidates for the state, not just new additions
- If updating existing state data, include BOTH existing AND new races/candidates in the arrays
- The upload script will handle duplicates automatically - just include everything
- Summary counts should reflect the TOTAL after upload, not just what's new
```

---

