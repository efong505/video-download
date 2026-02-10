# Single State Complete Data Generation Prompt

Use this prompt to generate races, candidates, AND comprehensive summary for ONE state at a time.

---

## MASTER PROMPT (Copy and replace [STATE NAME])

```
Create complete 2025-2026 election data for [STATE NAME] including races, candidates, and comprehensive voter guide.

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

# Upload code (standard)
print(f"Uploading {len(races)} [STATE NAME] races...")
race_ids = {}
for race in races:
    import uuid
    race_id = str(uuid.uuid4())
    race['race_id'] = race_id
    race['created_at'] = datetime.now().isoformat()
    race['created_by'] = 'system'
    races_table.put_item(Item=race)
    race_ids[race['office']] = race_id
    print(f"  Added: {race['office']}")

print(f"\\n[SUCCESS] Uploaded {len(races)} races")

print(f"\\nUploading {len(candidates)} [STATE NAME] candidates...")
for candidate in candidates:
    import uuid
    candidate['candidate_id'] = str(uuid.uuid4())
    if candidate['office'] in race_ids:
        candidate['race_id'] = race_ids[candidate['office']]
    else:
        candidate['race_id'] = ''
    candidate['created_at'] = datetime.now().isoformat()
    candidate['created_by'] = 'system'
    candidate['status'] = 'active'
    candidates_table.put_item(Item=candidate)
    print(f"  Added: {candidate['name']} - {candidate['office']}")

print(f"\\n[SUCCESS] Uploaded {len(candidates)} candidates")

print("\\nUploading [STATE NAME] summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")

print("\\n[SUCCESS] [STATE NAME] data upload complete!")
```

---

## PART 2: RACES ARRAY

Research and create races for [STATE NAME] 2025-2026:

**Federal Races:**
- U.S. Senate (if up in 2026)
- U.S. House (all districts)

**Statewide Races:**
- Governor (if up in 2026)
- Lieutenant Governor
- Attorney General
- Secretary of State
- State Treasurer
- Other statewide offices

**Municipal Races (if applicable):**
- Major city mayors
- Key city council races

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
    "bio": "[Detailed 200-300 word biography including: background, career, family, accomplishments, current position]",
    "faith_statement": "[Actual faith statement from candidate OR 'No publicly disclosed faith statement']",
    "website": "[https://candidatewebsite.com OR '']",
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
- Find ACTUAL faith statements from interviews, websites, speeches
- Include REAL endorsements from organizations
- Provide DETAILED positions, not generic statements
- Cover at least 2-3 major candidates per top race

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

## CRITICAL REQUIREMENTS

**Research Quality:**
- Use REAL candidates currently running or announced
- Find ACTUAL faith statements from sources
- Include REAL endorsements from organizations
- Provide state-specific laws, policies, and context
- Include accurate election dates

**Formatting:**
- Use `**bold**` for all labels and key terms
- Include ALL emojis in headers
- Use `---` dividers between sections
- Italicize scripture quotes
- 20,000-25,000 character total length

**Content Depth:**
- Detailed candidate profiles (not generic)
- State-specific issue analysis (not national talking points)
- Real organizations with websites
- Specific action items for voters

---

## OUTPUT FORMAT

Provide the complete Python script with:
1. Races array populated with [STATE NAME] races
2. Candidates array populated with [STATE NAME] candidates
3. Summary content with full 20,000+ char markdown guide

Ready to run: `python upload_[state]_data.py`

---

**NOW CREATE COMPLETE DATA FOR: [STATE NAME]**
```

---

## USAGE INSTRUCTIONS

1. Copy the entire MASTER PROMPT above
2. Replace every instance of `[STATE NAME]` with your target state
3. Submit to AI (Claude, ChatGPT, etc.)
4. Receive complete Python upload script
5. Save as `upload_[state]_data.py`
6. Run: `python upload_[state]_data.py`
7. Repeat for next state

---

## PRIORITY ORDER (17 remaining states)

**High Priority (have some data in database):**
1. California
2. Arizona

**Medium Priority:**
3. Minnesota
4. Colorado
5. Maine
6. Rhode Island
7. New Jersey
8. Delaware
9. Kansas
10. Iowa
11. Kentucky
12. Nevada

**Low Priority:**
13. Oklahoma
14. Louisiana
15. Tennessee
16. South Dakota
17. Wyoming
