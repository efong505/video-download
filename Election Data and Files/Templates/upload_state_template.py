"""
Template for uploading state election data to DynamoDB

INSTRUCTIONS:
1. Copy this file and rename to: upload_[state_name]_data.py
2. Replace all [PLACEHOLDERS] with actual data
3. Follow the formatting rules in FORMATTING_RULES.md
4. Use state_summary_template.md for content structure
5. Run: python upload_[state_name]_data.py

IMPORTANT:
- Use [SUCCESS] instead of emoji in print statements (Windows compatibility)
- Match candidate race_id to race race_id for proper linking
- Use markdown formatting with **bold** and proper headers
- Include all emojis in content string
"""

import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# [STATE NAME] Races
races = [
    # Federal Races
    {
        "state": "[STATE NAME]",
        "office": "U.S. Senate",
        "election_date": "[YYYY-MM-DD]",
        "race_type": "general",
        "description": "[Brief description]"
    },
    {
        "state": "[STATE NAME]",
        "office": "U.S. House District [NUMBER]",
        "election_date": "[YYYY-MM-DD]",
        "race_type": "general",
        "description": "[Brief description]"
    },
    # Add more House districts as needed
    
    # Statewide Races
    {
        "state": "[STATE NAME]",
        "office": "Governor",
        "election_date": "[YYYY-MM-DD]",
        "race_type": "general",
        "description": "[Brief description]"
    },
    {
        "state": "[STATE NAME]",
        "office": "Lieutenant Governor",
        "election_date": "[YYYY-MM-DD]",
        "race_type": "general",
        "description": "[Brief description]"
    },
    # Add more statewide offices as needed
    
    # Municipal Races (if applicable)
    {
        "state": "[STATE NAME]",
        "office": "[City] Mayor",
        "election_date": "[YYYY-MM-DD]",
        "race_type": "general",
        "description": "[Brief description]"
    },
    # Add more municipal races as needed
]

# [STATE NAME] Candidates
candidates = [
    # Example Senate Candidate
    {
        "name": "[Candidate Full Name]",
        "state": "[STATE NAME]",
        "office": "U.S. Senate",
        "party": "[Republican/Democrat/Independent/Libertarian/Green/Constitution/Other]",
        "bio": "[Detailed biography]",
        "faith_statement": "[Faith statement or 'No publicly disclosed faith statement']",
        "website": "[https://website.com]",
        "positions": {
            "ABORTION": "[pro-life/pro-choice/etc]",
            "GUNS": "[strong-support/gun-safety/etc]",
            "TAXES": "[lower/raise/etc]",
            "IMMIGRATION": "[secure-border/comprehensive-reform/etc]",
            "RELIGIOUS-FREEDOM": "[strong-support/etc]",
            "EDUCATION": "[school-choice/parental-rights/etc]"
        },
        "endorsements": ["[Organization 1]", "[Organization 2]"]
    },
    # Add more candidates as needed
]

# [STATE NAME] Summary
summary = {
    "state": "[STATE NAME]",
    "title": "[STATE NAME] 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# [STATE NAME] 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** [NUMBER] races across [STATE NAME]
**Total Candidates Profiled:** [NUMBER] major candidates
**Election Dates:**
- [DATE] ([ELECTION TYPE])

---

## 🔴 [STATE NAME] POLITICAL LANDSCAPE

### **The [State Nickname]**

[STATE NAME] is a **[POLITICAL CHARACTERIZATION]**:

- **[Category]:** [Description]
- **[Category]:** [Description]
- **[Category]:** [Description]
- **[Category]:** [Description]
- **[Category]:** [Description]

### **Why [STATE NAME] Matters**

[STATE NAME] is **[WINNABLE/CRITICAL]** for Christian conservatives:

- ✅ **[Strength 1]:** [Explanation]
- ✅ **[Strength 2]:** [Explanation]
- ✅ **[Strength 3]:** [Explanation]
- ✅ **[Strength 4]:** [Explanation]
- ✅ **[Strength 5]:** [Explanation]
- ✅ **[Strength 6]:** [Explanation]

---

## 🔴 [YEAR] [RACE CATEGORY]

### **[Race Name]** - [Date]

**Context:** [Brief description]

**[Candidate Name] ([Party])** - [Title]
- [Point 1]
- [Point 2]
- [Point 3]

**Why It Matters:** [Explanation]

---

## 🎯 KEY ISSUES FOR CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- [Position]

**Progressive Position:**
- [Position]

**Christian Conservative Action:**
- [Action]

[Continue with all key issues sections]

---

## 📅 CRITICAL DATES

**[YEAR] Election Calendar:**
- **[Date]** - [Event]

---

## 🗳️ CHURCH MOBILIZATION STRATEGY

### **What Pastors Can Do (501c3 Compliant):**

✅ **Endorse candidates from pulpit** (IRS now permits pastoral endorsements)
✅ **Distribute non-partisan voter guides**
✅ **Host candidate forums**
✅ **Preach on biblical citizenship**
✅ **Voter registration drives**
✅ **Encourage early voting**
✅ **Prayer emphasis** for elections

❌ **Cannot donate church funds** to campaigns (personal donations allowed)

### **What Church Members Can Do:**

✅ **Volunteer for campaigns**
✅ **Donate to candidates**
✅ **Host house parties**
✅ **Share on social media**
✅ **Pray daily** for elections
✅ **Vote early** and bring friends

---

## 📞 RESOURCES FOR [STATE NAME] CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **[Organization]** - [Description]

### **Election Information:**
- **[State] Secretary of State**: [website]

### **Conservative Organizations:**
- **[Organization]** - [Description]

---

## 🔥 BOTTOM LINE FOR [STATE NAME] CHRISTIANS

**[YEAR] Elections Matter:**
- [Point]

**If Conservatives Win:**

✅ [Outcome]

**If Progressives Win:**

❌ [Outcome]

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- [Prayer point]

*"[Scripture]"* - [Reference]

---

**Last Updated:** [Month Year]
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute [STATE NAME] coverage, email contact@ekewaka.com

**[STATE NAME] CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "last_updated": datetime.utcnow().isoformat(),
    "updated_by": "system"
}

# Upload races
print(f"Uploading {len(races)} [STATE NAME] races...")
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

# Upload candidates
print(f"\nUploading {len(candidates)} [STATE NAME] candidates...")
for candidate in candidates:
    import uuid
    candidate['candidate_id'] = str(uuid.uuid4())
    # Auto-match to race by office
    if candidate['office'] in race_ids:
        candidate['race_id'] = race_ids[candidate['office']]
    else:
        candidate['race_id'] = ''
    candidate['created_at'] = datetime.utcnow().isoformat()
    candidate['created_by'] = 'system'
    candidate['status'] = 'active'
    candidate['voting_record_url'] = candidate.get('voting_record_url', '')
    candidate['photo_url'] = candidate.get('photo_url', '')
    candidates_table.put_item(Item=candidate)
    print(f"  Added: {candidate['name']} - {candidate['office']}")

print(f"\n[SUCCESS] Uploaded {len(candidates)} candidates")

# Upload summary
print("\nUploading [STATE NAME] summary...")
summaries_table.put_item(Item=summary)
print("  Summary uploaded successfully")

print("\n[SUCCESS] [STATE NAME] data upload complete!")
print(f"   Races: {len(races)}")
print(f"   Candidates: {len(candidates)}")
print(f"   Summary: Uploaded")
