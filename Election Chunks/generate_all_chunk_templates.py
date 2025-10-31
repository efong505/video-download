"""
Generate ALL chunk templates (1, 2A-2T, 5A-5D) for all 50 states.
Uses New Jersey's detailed structure for consistency.
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

def generate_chunk1(state, config):
    """Generate CHUNK_1_RACES template"""
    return f"""# CHUNK 1: {state.upper()} RACES ARRAY ONLY

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
- Base ALL data on real sources (state.gov, Ballotpedia)
- Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026)
- U.S. Senate (if applicable)
- U.S. House Districts 1-{config['districts']} (ALL {config['districts']})

### State (2025/2026)
- Governor (if applicable)
- Lieutenant Governor
- Other statewide offices

### State Legislature (2025)
- State Senate seats up for election
- State House/Assembly seats up for election

### School Boards (2025)
- Top 10-15 largest districts
- 3 seats each

### County (2025)
- Commissioners, Sheriffs, Prosecutors, Clerks

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

## VERIFICATION:
At end, provide:
```
TOTAL RACES: [NUMBER]
- Federal: [NUMBER]
- State: [NUMBER]
- Legislature: [NUMBER]
- School Boards: [NUMBER]
- County: [NUMBER]
```

**START OUTPUT NOW - RACES ARRAY ONLY**
"""

def generate_chunk2a(state, config):
    """Generate CHUNK_2A_CANDIDATES template"""
    return f"""# CHUNK 2A: {state.upper()} CANDIDATES 1-10

## TASK: Provide EXACTLY 10 candidates (1-10) - NO MORE, NO LESS

**CRITICAL: Write ALL 10 candidates COMPLETELY. If you write "..." or "[continue]" or abbreviate ANY candidate, you have FAILED.**

**DO NOT provide:**
- NO Races array
- NO Summary
- NO Candidates 11+
- NO Explanatory text

**DO provide:**
- Exactly 10 complete candidates
- Each: name, state, office, party, status, bio (200-300 words), faith_statement, website, positions (ALL 8), endorsements

## CANDIDATES 1-10:
Research real candidates from Ballotpedia, campaign websites, news coverage.

## FORMAT:

```python
candidates = [
    {{
        "name": "Full Legal Name",
        "state": "{state}",
        "office": "Exact Office Name",
        "party": "Democrat/Republican/Independent",
        "status": "active",
        "bio": "[200-300 words from Ballotpedia/official sources. Cite source.]",
        "faith_statement": "[Actual statement OR 'No publicly disclosed faith statement']",
        "website": "https://realwebsite.com",
        "positions": {{
            "ABORTION": "[Detailed position]",
            "EDUCATION": "[Detailed position]",
            "RELIGIOUS-FREEDOM": "[Detailed position]",
            "GUNS": "[Detailed position]",
            "TAXES": "[Detailed position]",
            "IMMIGRATION": "[Detailed position]",
            "FAMILY-VALUES": "[Detailed position]",
            "ELECTION-INTEGRITY": "[Detailed position]"
        }},
        "endorsements": ["Org 1", "Org 2", "Org 3"]
    }},
    # WRITE CANDIDATES 2-10 EXACTLY LIKE ABOVE
]
```

## VERIFICATION:
At end, write:
```
CANDIDATES 1-10 COMPLETE
Total: 10
```

**START OUTPUT NOW - WRITE ALL 10 CANDIDATES COMPLETELY**
"""

# Generate for all states
output_dir = "ALL_STATE_TEMPLATES"
os.makedirs(output_dir, exist_ok=True)

for state, config in STATES.items():
    state_dir = f"{output_dir}/{state.replace(' ', '_')}"
    os.makedirs(state_dir, exist_ok=True)
    
    # CHUNK 1
    with open(f"{state_dir}/CHUNK_1_RACES.md", 'w', encoding='utf-8') as f:
        f.write(generate_chunk1(state, config))
    
    # CHUNK 2A (only showing 2A, would need 2B-2T for full system)
    with open(f"{state_dir}/CHUNK_2A_CANDIDATES_1-10.md", 'w', encoding='utf-8') as f:
        f.write(generate_chunk2a(state, config))
    
    print(f"Generated: {state}")

print(f"\nGenerated templates for {len(STATES)} states")
print(f"Location: {output_dir}/")
print("\nNOTE: This generates CHUNK_1 and CHUNK_2A only.")
print("Need to add CHUNK_2B-2T and CHUNK_5A-5D for complete system.")
