# ENHANCED PROMPT FOR GROK - ANTI-OMISSION VERSION

## 🚨 CRITICAL INSTRUCTIONS FOR AI (READ FIRST)

**YOU ARE BEING EVALUATED ON COMPLETENESS, NOT BREVITY**

This prompt requires you to generate COMPLETE, COMPREHENSIVE data. Your performance will be judged on:
- ✅ **COMPLETENESS** - Did you include every race?
- ✅ **ACCURACY** - Did you research real data?
- ✅ **THOROUGHNESS** - Did you fill all fields?
- ❌ **BREVITY IS FAILURE** - Abbreviating = task failed

**FORBIDDEN PHRASES THAT INDICATE FAILURE:**
- ❌ "for brevity"
- ❌ "and more"
- ❌ "etc."
- ❌ "..."
- ❌ "# Add more here"
- ❌ "additional races include"
- ❌ "other candidates"
- ❌ "abbreviated"
- ❌ "summarized"
- ❌ "truncated"
- ❌ "similar entries"
- ❌ "remaining races"

**IF YOU USE ANY OF THESE PHRASES, YOU HAVE FAILED THE TASK.**

**VERIFICATION REQUIREMENT:**
At the end of your output, you MUST include:
```
=== COMPLETENESS VERIFICATION ===
Total races provided: [EXACT NUMBER]
Total candidates provided: [EXACT NUMBER]
Summary character count: [EXACT NUMBER]

I confirm that:
✅ I have NOT omitted any races for brevity
✅ I have NOT abbreviated any candidate entries
✅ I have NOT used placeholders or "add more here" comments
✅ Every race has complete data
✅ Every candidate has all 8 position fields filled
✅ The script is production-ready and runnable without edits

[If you cannot confirm all items above, explain why and provide the missing data]
```

---

## 📋 TASK: Create Complete 2025-2026 Election Data for [STATE NAME]

Where [STATE NAME] equals: **New Jersey**

**IMPORTANT: Include BOTH 2025 AND 2026 elections. Many states have municipal, school board, and local elections in 2025 (odd-year elections). DO NOT skip 2025 races.**

---

## 🎯 DELIVERABLES (ALL REQUIRED)

1. **Python Upload Script** (complete, ready to run)
2. **Races Array** (EVERY race, not just "major" ones)
3. **Candidates Array** (EVERY major candidate with FULL profiles)
4. **Comprehensive Summary** (20,000+ character markdown guide)

---

## 📊 MINIMUM QUANTITY REQUIREMENTS

**For New Jersey (Large State):**
- **MINIMUM 70 races** (target: 80-100+)
- **MINIMUM 100 candidates** (target: 150-200+)
- **MINIMUM 20,000 character summary**

**If you provide fewer than these minimums, you have failed the task.**

**Breakdown Required:**
- ✅ 1 U.S. Senate race
- ✅ ALL 12 U.S. House districts (not 2-3, ALL 12)
- ✅ At least 12 State Senate districts
- ✅ At least 12 State Assembly districts
- ✅ At least 20 school board races (CRITICAL - DO NOT SKIP)
- ✅ At least 6 municipal races (mayors)
- ✅ At least 10 county races (executives, sheriffs)
- ✅ Additional races to reach 70+ total

---

## PART 1: PYTHON UPLOAD SCRIPT

Create a complete Python script named `upload_new_jersey_data.py` with this structure:

```python
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# New Jersey Races
races = [
    # YOUR RACES HERE - WRITE OUT EVERY SINGLE ONE
    # DO NOT use "# Add more here" or "for brevity"
    # MINIMUM 70 races required
]

# New Jersey Candidates  
candidates = [
    # YOUR CANDIDATES HERE - WRITE OUT EVERY SINGLE ONE
    # DO NOT use "# Add more here" or "for brevity"
    # MINIMUM 100 candidates required
]

# New Jersey Summary
summary = {
    "state": "New Jersey",
    "title": "New Jersey 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """[YOUR COMPREHENSIVE SUMMARY HERE - MINIMUM 20,000 CHARACTERS]""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing New Jersey races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'New Jersey'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} New Jersey races...")
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

print(f"\nChecking for existing New Jersey candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'New Jersey'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} New Jersey candidates...")
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

print("\nProcessing New Jersey summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'New Jersey'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] New Jersey data upload complete!")
```

---

## PART 2: RACES ARRAY - COMPREHENSIVE COVERAGE REQUIRED

**🚨 CRITICAL: You must research and provide REAL election data from official sources.**

**Research Sources (USE THESE):**
- Ballotpedia.org - Search "New Jersey elections 2025" and "New Jersey elections 2026"
- NJ.gov/state/elections - Official New Jersey election information
- County clerk websites for local races
- School district websites for board elections
- News articles about 2025-2026 NJ elections

**MANDATORY RACE CATEGORIES:**

### Federal Races (2026) - INCLUDE ALL

**U.S. Senate:**
- Research: Is Cory Booker up for re-election in 2026? (Verify on Ballotpedia)
- Include the race with actual election date

**U.S. House - ALL 12 DISTRICTS (NOT NEGOTIABLE):**
You MUST include ALL of these:
1. U.S. House District 1
2. U.S. House District 2
3. U.S. House District 3
4. U.S. House District 4
5. U.S. House District 5
6. U.S. House District 6
7. U.S. House District 7
8. U.S. House District 8
9. U.S. House District 9
10. U.S. House District 10
11. U.S. House District 11
12. U.S. House District 12

**For each district, research:**
- Current incumbent name
- District geography (which counties/cities)
- Competitive status
- 2024 election results

### State Legislature (2025) - INCLUDE MANY

**New Jersey has 40 State Senate districts and 80 State Assembly seats (2 per district).**

**MINIMUM REQUIREMENT: Include at least 15 State Senate districts and 15 State Assembly districts**

**Priority Districts to Research:**
- Competitive/swing districts
- Districts with open seats
- Districts with notable incumbents
- Mix of urban, suburban, and rural districts

**Research on Ballotpedia:**
- "New Jersey State Senate elections 2025"
- "New Jersey General Assembly elections 2025"
- Look for competitive races, open seats, notable candidates

### School Board Races (2025) - MINIMUM 20 REQUIRED

**🚨 THIS IS CRITICAL - DO NOT SKIP SCHOOL BOARDS**

**New Jersey school board elections are typically in November 2025.**

**MANDATORY: Research and include school board races for these cities:**
1. Newark Board of Education (multiple seats)
2. Jersey City Board of Education (multiple seats)
3. Paterson Board of Education (multiple seats)
4. Elizabeth Board of Education (multiple seats)
5. Edison Board of Education (multiple seats)
6. Woodbridge Board of Education (multiple seats)
7. Camden Board of Education (multiple seats)
8. Trenton Board of Education (multiple seats)
9. Clifton Board of Education (multiple seats)
10. Passaic Board of Education (multiple seats)
11. Union City Board of Education (multiple seats)
12. Bayonne Board of Education (multiple seats)
13. East Orange Board of Education (multiple seats)
14. Vineland Board of Education (multiple seats)
15. New Brunswick Board of Education (multiple seats)

**For EACH district, research:**
- How many seats are up in 2025?
- Are they at-large or district-based?
- What is the election date?
- Check district website or county clerk

**MINIMUM: 20 school board seat races (not just 20 districts, but 20 individual seat races)**

### Municipal Races (2025) - INCLUDE MAJOR CITIES

**New Jersey municipal elections vary by municipality - some in May, some in November.**

**MANDATORY: Research mayoral races for:**
1. Newark (research: when is next election?)
2. Jersey City (research: when is next election?)
3. Paterson (research: when is next election?)
4. Elizabeth (research: when is next election?)
5. Trenton (research: when is next election?)
6. Camden (research: when is next election?)
7. Clifton (research: when is next election?)
8. Passaic (research: when is next election?)

**Research each city:**
- Election date (May or November 2025?)
- Current mayor and term status
- Announced candidates

### County Races (2025) - INCLUDE MAJOR COUNTIES

**New Jersey has 21 counties. County elections are typically in November 2025.**

**MANDATORY: Include races for these counties:**
1. Bergen County (Executive/Commissioners)
2. Essex County (Executive/Commissioners)
3. Hudson County (Executive/Commissioners)
4. Middlesex County (Commissioners)
5. Monmouth County (Commissioners)
6. Morris County (Commissioners)
7. Ocean County (Commissioners)
8. Passaic County (Commissioners)
9. Union County (Commissioners)
10. Camden County (Commissioners)

**Sheriff Races - INCLUDE AT LEAST 10:**
Research which counties have sheriff elections in 2025.

**Format each race as:**
```python
{
    "state": "New Jersey",
    "office": "[Exact Office Title]",
    "election_date": "YYYY-MM-DD",  # Research actual date
    "race_type": "general",  # or "primary"
    "description": "[Brief description of race significance]"
}
```

**EXAMPLE (DO NOT COPY - RESEARCH REAL DATA):**
```python
{
    "state": "New Jersey",
    "office": "U.S. House District 7",
    "election_date": "2026-11-03",
    "race_type": "general",
    "description": "Competitive suburban district - Tom Kean Jr. (R) incumbent vs Democratic challenger"
},
```

---

## PART 3: CANDIDATES ARRAY - FULL PROFILES REQUIRED

**🚨 CRITICAL: Research REAL candidates currently running or likely to run.**

**Research Sources:**
- Ballotpedia candidate pages
- Candidate official websites
- News articles about candidates
- FEC filings for federal candidates
- State election commission filings

**For EACH major candidate, provide:**

```python
{
    "name": "[Full Legal Name]",
    "state": "New Jersey",
    "office": "[Office - must match race office exactly]",
    "party": "[Republican/Democrat/Independent/Libertarian]",
    "incumbent": True,  # or False
    "bio": "[Detailed 200-300 word biography]",
    "positions": "[Detailed positions on key issues]",
    "faith_statement": "[Actual faith statement OR 'No publicly disclosed faith statement']",
    "website": "[https://candidatewebsite.com OR '']",
    "endorsements": "[List of endorsing organizations]",
    "priority": "high"  # or "medium" or "low"
}
```

**MINIMUM CANDIDATES REQUIRED:**
- U.S. Senate: At least 2 candidates (incumbent + main challenger)
- U.S. House: At least 2 candidates per competitive district (minimum 10 total)
- State Legislature: At least 1-2 candidates per included district (minimum 20 total)
- School Boards: At least 1 candidate per race (minimum 20 total)
- Municipal: At least 1-2 candidates per mayoral race (minimum 10 total)
- County: At least 1 candidate per race (minimum 10 total)

**TOTAL MINIMUM: 100 candidates**

**Research Tips:**
- For incumbents: Check their official government website
- For challengers: Search "[name] for [office] New Jersey"
- For faith statements: Search "[name] faith" or "[name] Christian" or check interviews
- For positions: Check candidate websites, voter guides, news interviews

---

## PART 4: COMPREHENSIVE SUMMARY (20,000+ CHARACTERS)

**🚨 CRITICAL: This must be a COMPLETE voter guide, not a summary.**

**Required Sections (ALL MANDATORY):**

1. **Executive Summary** (500 words)
   - Why New Jersey matters
   - Key dates
   - Priority races

2. **2026 Federal Races** (3,000 words)
   - U.S. Senate race (detailed analysis)
   - All 12 U.S. House races (at least paragraph each)
   - Candidate profiles with positions

3. **2025 State Legislative Races** (2,000 words)
   - Why state legislature matters
   - Key competitive districts
   - Issues at stake

4. **2025 School Board Elections** (2,000 words)
   - Why school boards are critical
   - Major district races
   - Parental rights issues
   - How to research candidates

5. **2025 Municipal Elections** (1,500 words)
   - Major mayoral races
   - Why local elections matter
   - Key issues

6. **2025 County Elections** (1,500 words)
   - County executive/commissioner races
   - Sheriff races
   - County-level issues

7. **Key Issues for NJ Christian Conservatives** (3,000 words)
   - Abortion and life issues
   - Parental rights and education
   - Religious liberty
   - Family values
   - Second Amendment
   - Election integrity
   - Taxes and economy
   - Crime and public safety

8. **Church Mobilization Strategy** (1,500 words)
   - What pastors can do (501c3 compliant)
   - What church members can do
   - Voter registration drives
   - Get out the vote

9. **Critical Dates and Deadlines** (500 words)
   - Voter registration deadlines
   - Early voting dates
   - Election days
   - How to vote

10. **Prayer Points for New Jersey** (1,000 words)
    - Specific candidates to pray for
    - Issues to pray about
    - Scripture for elections

11. **Resources** (500 words)
    - Voter guide organizations
    - Pro-life organizations
    - Religious liberty groups
    - Election information

12. **Action Steps** (1,000 words)
    - Immediate actions
    - Spring 2025 actions
    - Fall 2025 actions
    - 2026 actions

**TOTAL TARGET: 20,000-25,000 characters**

**Use this structure with proper markdown formatting, emojis, and bold text as shown in original prompt.**

---

## 🚨 OUTPUT FORMAT - ANTI-ABBREVIATION REQUIREMENTS

**YOU MUST PROVIDE:**

1. **Complete Python script** with:
   - FULL races array (every race written out)
   - FULL candidates array (every candidate written out)
   - FULL summary content (complete 20,000+ char guide)

2. **NO abbreviations, NO placeholders, NO "for brevity" comments**

3. **Production-ready code** that runs immediately without edits

**ABSOLUTELY FORBIDDEN:**
- ❌ "# Add more candidates here..."
- ❌ "# ... (abbreviated for brevity)"
- ❌ "# Assume 50 total"
- ❌ Any comments suggesting incomplete data
- ❌ Placeholder text like "[more entries]"
- ❌ "etc."
- ❌ "..."
- ❌ "and more"
- ❌ "additional races"
- ❌ "similar entries"

**REQUIRED:**
- ✅ Write out EVERY race completely
- ✅ Write out EVERY candidate completely
- ✅ Include ALL fields for each entry
- ✅ Make the script immediately runnable

---

## ✅ VERIFICATION CHECKLIST (COMPLETE BEFORE SUBMITTING)

**Before you submit your response, verify:**

1. **Count Verification:**
   - [ ] I have counted my races array: _____ races (minimum 70)
   - [ ] I have counted my candidates array: _____ candidates (minimum 100)
   - [ ] I have counted my summary characters: _____ chars (minimum 20,000)

2. **Completeness Verification:**
   - [ ] I included ALL 12 U.S. House districts (not just 2-3)
   - [ ] I included at least 20 school board races
   - [ ] I included at least 15 state legislature races
   - [ ] I included at least 6 municipal races
   - [ ] I included at least 10 county races

3. **Quality Verification:**
   - [ ] Every candidate has all required fields filled
   - [ ] Every race has complete information
   - [ ] I researched real candidates and real data
   - [ ] I did NOT use placeholder text or "TBD" excessively
   - [ ] I did NOT abbreviate or use "for brevity"

4. **Code Verification:**
   - [ ] The Python script is syntactically correct
   - [ ] The arrays are properly formatted
   - [ ] The script would run without errors
   - [ ] No comments like "# Add more here"

**If you cannot check ALL boxes above, DO NOT SUBMIT. Go back and complete the missing items.**

---

## 📤 FINAL SUBMISSION FORMAT

**Provide your output in this exact format:**

```
=== NEW JERSEY 2025-2026 ELECTION DATA ===

[Complete Python script here - all code from import statements through final print]

=== COMPLETENESS VERIFICATION ===
Total races provided: [EXACT NUMBER]
Total candidates provided: [EXACT NUMBER]
Summary character count: [EXACT NUMBER]

Breakdown:
- Federal races: [NUMBER]
- State legislature races: [NUMBER]
- School board races: [NUMBER]
- Municipal races: [NUMBER]
- County races: [NUMBER]

I confirm that:
✅ I have NOT omitted any races for brevity
✅ I have NOT abbreviated any candidate entries
✅ I have NOT used placeholders or "add more here" comments
✅ Every race has complete data
✅ Every candidate has all required fields
✅ The script is production-ready and runnable without edits
✅ I researched real candidates and real election data
✅ I met all minimum quantity requirements

Research sources used:
- [List sources you actually used]

=== END VERIFICATION ===
```

---

## 🎯 FINAL REMINDERS

1. **COMPLETENESS > BREVITY** - Your goal is comprehensive data, not concise data
2. **RESEARCH REQUIRED** - Use Ballotpedia, NJ.gov, news sources
3. **NO ABBREVIATIONS** - Write everything out in full
4. **VERIFY COUNTS** - Count your arrays before submitting
5. **PRODUCTION READY** - Script must run without edits

**If you find yourself wanting to abbreviate, STOP and write it out completely instead.**

**If you're unsure about data, RESEARCH IT before including it.**

**If you can't meet the minimums, EXPLAIN WHY rather than submitting incomplete data.**

---

**NOW CREATE COMPLETE DATA FOR NEW JERSEY**

**Remember: You are being evaluated on COMPLETENESS, not brevity. Take the time to do it right.**
