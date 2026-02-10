"""
Generate COMPLETE template system for all 50 states.
Creates CHUNK_1, CHUNK_2A-2T, CHUNK_5A-5D for each state.
Based on New Jersey's detailed structure.
"""

STATES = {
    "Alabama": {"districts": 7, "senate_year": 2026, "gov_year": 2026},
    "Alaska": {"districts": 1, "senate_year": None, "gov_year": 2026},
    "Arizona": {"districts": 9, "senate_year": None, "gov_year": 2026},
    "Arkansas": {"districts": 4, "senate_year": None, "gov_year": 2026},
    "California": {"districts": 52, "senate_year": None, "gov_year": 2026},
    "Colorado": {"districts": 8, "senate_year": None, "gov_year": 2026},
    "Connecticut": {"districts": 5, "senate_year": None, "gov_year": 2026},
    "Delaware": {"districts": 1, "senate_year": 2026, "gov_year": None},
    "Florida": {"districts": 28, "senate_year": None, "gov_year": 2026},
    "Georgia": {"districts": 14, "senate_year": 2026, "gov_year": 2026},
    "Hawaii": {"districts": 2, "senate_year": None, "gov_year": 2026},
    "Idaho": {"districts": 2, "senate_year": 2026, "gov_year": 2026},
    "Illinois": {"districts": 17, "senate_year": None, "gov_year": 2026},
    "Indiana": {"districts": 9, "senate_year": None, "gov_year": 2026},
    "Iowa": {"districts": 4, "senate_year": 2026, "gov_year": 2026},
    "Kansas": {"districts": 4, "senate_year": 2026, "gov_year": 2026},
    "Kentucky": {"districts": 6, "senate_year": None, "gov_year": 2027},
    "Louisiana": {"districts": 6, "senate_year": 2026, "gov_year": 2027},
    "Maine": {"districts": 2, "senate_year": 2026, "gov_year": 2026},
    "Maryland": {"districts": 8, "senate_year": None, "gov_year": 2026},
    "Massachusetts": {"districts": 9, "senate_year": None, "gov_year": 2026},
    "Michigan": {"districts": 13, "senate_year": 2026, "gov_year": 2026},
    "Minnesota": {"districts": 8, "senate_year": 2026, "gov_year": 2026},
    "Mississippi": {"districts": 4, "senate_year": 2026, "gov_year": 2027},
    "Missouri": {"districts": 8, "senate_year": None, "gov_year": 2026},
    "Montana": {"districts": 2, "senate_year": None, "gov_year": 2026},
    "Nebraska": {"districts": 3, "senate_year": 2026, "gov_year": 2026},
    "Nevada": {"districts": 4, "senate_year": None, "gov_year": 2026},
    "New Hampshire": {"districts": 2, "senate_year": 2026, "gov_year": 2026},
    "New Jersey": {"districts": 12, "senate_year": 2026, "gov_year": 2025},
    "New Mexico": {"districts": 3, "senate_year": 2026, "gov_year": 2026},
    "New York": {"districts": 26, "senate_year": None, "gov_year": 2026},
    "North Carolina": {"districts": 14, "senate_year": 2026, "gov_year": 2026},
    "North Dakota": {"districts": 1, "senate_year": None, "gov_year": 2026},
    "Ohio": {"districts": 15, "senate_year": None, "gov_year": 2026},
    "Oklahoma": {"districts": 5, "senate_year": 2026, "gov_year": 2026},
    "Oregon": {"districts": 6, "senate_year": 2026, "gov_year": 2026},
    "Pennsylvania": {"districts": 17, "senate_year": None, "gov_year": 2026},
    "Rhode Island": {"districts": 2, "senate_year": 2026, "gov_year": 2026},
    "South Carolina": {"districts": 7, "senate_year": 2026, "gov_year": 2026},
    "South Dakota": {"districts": 1, "senate_year": 2026, "gov_year": 2026},
    "Tennessee": {"districts": 9, "senate_year": None, "gov_year": 2026},
    "Texas": {"districts": 38, "senate_year": None, "gov_year": 2026},
    "Utah": {"districts": 4, "senate_year": None, "gov_year": 2026},
    "Vermont": {"districts": 1, "senate_year": None, "gov_year": 2026},
    "Virginia": {"districts": 11, "senate_year": 2026, "gov_year": 2025},
    "Washington": {"districts": 10, "senate_year": None, "gov_year": 2026},
    "West Virginia": {"districts": 2, "senate_year": 2026, "gov_year": 2026},
    "Wisconsin": {"districts": 8, "senate_year": None, "gov_year": 2026},
    "Wyoming": {"districts": 1, "senate_year": 2026, "gov_year": 2026}
}

import os

# CHUNK 1 Template
CHUNK1_TEMPLATE = """# CHUNK 1: {STATE} RACES ARRAY ONLY

## TASK: Provide ONLY the races array for {state} 2025-2026

**DO NOT provide:**
- NO Candidates array
- NO Summary  
- NO Upload script
- NO Explanatory text

**DO provide:**
- Complete Python array named `races`
- EXACT race count (verify at end)
- Every race: state, office, election_date, race_type, description
- Base ALL data on real sources (Ballotpedia, state.gov)
- Cite sources in descriptions

## FORMAT:

```python
races = [
    {{
        "state": "{state}",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent [Name] seeks re-election... (source: Ballotpedia)"
    }},
    # CONTINUE FOR ALL RACES
]
```

**START OUTPUT NOW - RACES ARRAY ONLY**
"""

# CHUNK 2 Template (for each 10-candidate chunk)
CHUNK2_TEMPLATE = """# CHUNK 2{letter}: {STATE} CANDIDATES {start}-{end}

## TASK: Provide UP TO 10 candidates ({start}-{end})

**CRITICAL: Write ALL candidates COMPLETELY. If you write "..." or "[continue]" or abbreviate ANY candidate, you have FAILED.**

**IMPORTANT:** If fewer than 10 viable candidates exist for this range, provide only the real candidates you can find. DO NOT invent fake candidates.

**DO NOT provide:**
- ❌ Races array
- ❌ Summary
- ❌ Other candidate ranges
- ❌ Any explanatory text

**DO provide:**
- ✅ Up to 10 complete candidates (or fewer if that's all that exist)
- ✅ Each: name, state, office, party, status, bio (200-300 words), faith_statement, website, positions (ALL 8), endorsements

## FORMAT:

```python
candidates = [
    {{
        "name": "Full Legal Name",
        "state": "{state}",
        "office": "Exact Office Name (e.g., U.S. Senate, U.S. House District 1, Governor)",
        "party": "Democrat/Republican/Independent/Libertarian/Green",
        "status": "active",
        "bio": "[200-300 words from Ballotpedia/{state}.gov - include background, career, education, family, accomplishments, voting record. Cite source.]",
        "faith_statement": "[Actual public statement about faith/religion OR 'No publicly disclosed faith statement']",
        "website": "https://realcampaignwebsite.com",
        "positions": {{
            "ABORTION": "[Detailed position with specifics - pro-life/pro-choice, exceptions, legislation supported]",
            "EDUCATION": "[Detailed position with specifics - school choice, vouchers, curriculum, funding]",
            "RELIGIOUS-FREEDOM": "[Detailed position with specifics - religious liberty protections, conscience rights]",
            "GUNS": "[Detailed position with specifics - 2nd Amendment stance, gun control measures]",
            "TAXES": "[Detailed position with specifics - tax rates, cuts/increases, economic policy]",
            "IMMIGRATION": "[Detailed position with specifics - border security, legal immigration, enforcement]",
            "FAMILY-VALUES": "[Detailed position with specifics - marriage, parental rights, gender issues]",
            "ELECTION-INTEGRITY": "[Detailed position with specifics - voter ID, election security, ballot measures]"
        }},
        "endorsements": ["Organization 1", "Organization 2", "Organization 3"]
    }},
    # WRITE REMAINING CANDIDATES (up to 9 more) EXACTLY LIKE ABOVE - COMPLETE ALL FIELDS
]
```

## VERIFICATION:
At end, write:
```
CANDIDATES {start}-{end} COMPLETE
Total provided: [ACTUAL NUMBER]
```

**START OUTPUT NOW - WRITE ALL AVAILABLE CANDIDATES COMPLETELY**
"""

# CHUNK 5A-5D Templates
CHUNK5A_TEMPLATE = """# CHUNK 5A: {STATE} SUMMARY - PART 1

## TASK: Generate FIRST HALF of summary only

**This chunk covers:**
1. Database Summary + Political Landscape (2,000 words)
2. 2026 Federal Races ({federal_words:,} words)
3. 2025 State Races ({state_words:,} words)
4. 2025 School Board Races (3,000 words)
5. 2025 Municipal Races (2,000 words)

**TOTAL FOR PART 1: {total_words:,} words minimum**

## CRITICAL ANTI-ABBREVIATION RULES:

### ABSOLUTELY FORBIDDEN:
- NO "[REPEAT FOR Districts...]"
- NO "[Full format]"
- NO "[Continue...]"
- NO "etc." or "..."
- NO "D" or "R" abbreviations

### ABSOLUTELY REQUIRED:
- Write EVERY House district completely
- Write EVERY school board completely
- Full paragraphs, no shortcuts
- Spell out "Democrat" and "Republican"

## OUTPUT FORMAT:

```markdown
# {state} 2025-2026 Elections - Complete Christian Conservatives Today Guide

## Database Summary

**Total Races Documented:** [NUMBER]
**Total Candidates Profiled:** [NUMBER]
**Election Dates:**
- November 4, 2025 (State/Local)
- November 3, 2026 (Federal)

---

## {STATE} POLITICAL LANDSCAPE

[Write 5-7 full paragraphs. MINIMUM 2,000 words]

---

[FEDERAL RACES - FULL FORMAT FOR EACH]

---

[STATE RACES - FULL FORMAT FOR EACH]

---

[SCHOOL BOARD RACES - FULL FORMAT FOR EACH]

---

[MUNICIPAL RACES - FULL FORMAT FOR EACH]

---

**END OF PART 1**
```

Generate Part 1 now with NO abbreviations.
"""

CHUNK5B_TEMPLATE = """# CHUNK 5B: {STATE} SUMMARY - PART 2

## TASK: Generate SECOND HALF of summary only

**This chunk covers:**
6. County Elections (2,000 words)
7. Key Issues for Christian Conservatives (4,000 words)
8. Church Mobilization Strategy (2,000 words)
9. Critical Dates & Resources (1,500 words)
10. Bottom Line & Prayer Points (2,000 words)

**TOTAL FOR PART 2: 11,500+ words minimum**

## CRITICAL ANTI-ABBREVIATION RULES:

### ABSOLUTELY FORBIDDEN:
- NO "[Continue...]"
- NO "etc." or "..."
- NO abbreviations

### ABSOLUTELY REQUIRED:
- Write ALL 8 key issues completely
- Full prose, no shortcuts
- Complete scripture quotes

## OUTPUT FORMAT:

```markdown
## COUNTY ELECTIONS

[Full paragraphs on county races]

---

## KEY ISSUES FOR {STATE} CHRISTIAN CONSERVATIVES

### Life & Family
[3-4 paragraphs conservative position]
[2-3 paragraphs progressive position]
[2-3 paragraphs action steps]
[Scripture quotes]

### School Choice & Parental Rights
[FULL FORMAT]

### Religious Liberty
[FULL FORMAT]

### Second Amendment Rights
[FULL FORMAT]

### Family Values & Marriage
[FULL FORMAT]

### Election Integrity
[FULL FORMAT]

### Taxes & Economic Freedom
[FULL FORMAT]

### Crime & Public Safety
[FULL FORMAT]

---

## CHURCH MOBILIZATION STRATEGY

[Full paragraphs on what pastors can do]
[Full paragraphs on what members can do]

---

## CRITICAL DATES

[Full paragraphs explaining each date]

---

## RESOURCES

[Full paragraphs on each resource]

---

## BOTTOM LINE

[Full paragraphs on what's at stake]

---

## PRAYER POINTS

[Full paragraphs with scripture]

---

**END OF PART 2**
```

Generate Part 2 now with NO abbreviations.
"""

def calculate_words(districts):
    if districts >= 20:  # Large states
        return 8000, 4000, 17000
    elif districts >= 10:  # Medium states
        return 6000, 3000, 14000
    else:  # Small states
        return 4000, 2000, 11000

def calculate_candidate_chunks(districts):
    """Determine MAXIMUM number of candidate chunks based on state size"""
    if districts >= 20:  # Large states: UP TO 200 candidates
        return 20
    elif districts >= 10:  # Medium states: UP TO 150 candidates
        return 15
    else:  # Small states: UP TO 100 candidates
        return 10

# Generate all templates
output_dir = "COMPLETE_STATE_TEMPLATES"
os.makedirs(output_dir, exist_ok=True)

for state, config in STATES.items():
    state_dir = f"{output_dir}/{state.replace(' ', '_')}"
    os.makedirs(state_dir, exist_ok=True)
    
    # CHUNK 1
    with open(f"{state_dir}/CHUNK_1_RACES.md", 'w', encoding='utf-8') as f:
        f.write(CHUNK1_TEMPLATE.format(STATE=state.upper(), state=state))
    
    # CHUNK 2A-2X (scaled by state size)
    num_chunks = calculate_candidate_chunks(config['districts'])
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T']
    for i in range(num_chunks):
        letter = letters[i]
        start = i * 10 + 1
        end = start + 9
        with open(f"{state_dir}/CHUNK_2{letter}_CANDIDATES_{start}-{end}.md", 'w', encoding='utf-8') as f:
            f.write(CHUNK2_TEMPLATE.format(
                letter=letter, STATE=state.upper(), state=state, start=start, end=end
            ))
    
    # CHUNK 5A-5D
    federal_words, state_words, total_words = calculate_words(config['districts'])
    
    with open(f"{state_dir}/CHUNK_5A_SUMMARY_PART1.md", 'w', encoding='utf-8') as f:
        f.write(CHUNK5A_TEMPLATE.format(
            STATE=state.upper(), state=state,
            federal_words=federal_words, state_words=state_words, total_words=total_words
        ))
    
    with open(f"{state_dir}/CHUNK_5B_SUMMARY_PART2.md", 'w', encoding='utf-8') as f:
        f.write(CHUNK5B_TEMPLATE.format(STATE=state.upper(), state=state))
    
    # 5C and 5D would be similar to 5B (continuation of summary)
    with open(f"{state_dir}/CHUNK_5C_SUMMARY_PART3.md", 'w', encoding='utf-8') as f:
        f.write(f"# CHUNK 5C: {state.upper()} SUMMARY - PART 3\n\n[Continuation of summary - similar structure to Part 2]")
    
    with open(f"{state_dir}/CHUNK_5D_SUMMARY_PART4.md", 'w', encoding='utf-8') as f:
        f.write(f"# CHUNK 5D: {state.upper()} SUMMARY - PART 4\n\n[Final section of summary]")
    
    num_chunks = calculate_candidate_chunks(config['districts'])
    total_candidates = num_chunks * 10
    total_files = 1 + num_chunks + 4
    print(f"Generated: {state} ({total_files} files, {total_candidates} candidates)")

print(f"\nGenerated complete template system for {len(STATES)} states")
print(f"Location: {output_dir}/")
print("\nState sizing:")
print("  - Large (20+ districts): 1 race + 20 candidate chunks (200 candidates) + 4 summary = 25 files")
print("  - Medium (10-19 districts): 1 race + 15 candidate chunks (150 candidates) + 4 summary = 20 files")
print("  - Small (<10 districts): 1 race + 10 candidate chunks (100 candidates) + 4 summary = 15 files")
