"""
Generate detailed state-specific templates with actual race breakdowns.

This replaces generic templates with specific race counts and examples
based on each state's actual congressional districts and elections.
"""

STATE_INFO = {
    "Alabama": {"districts": 7, "senate_year": None, "gov_year": 2026, "assembly_districts": 105, "senate_districts": 35},
    "Alaska": {"districts": 1, "senate_year": None, "gov_year": 2026, "assembly_districts": 40, "senate_districts": 20},
    "Arizona": {"districts": 9, "senate_year": None, "gov_year": 2026, "assembly_districts": 30, "senate_districts": 30},
    "Arkansas": {"districts": 4, "senate_year": None, "gov_year": 2026, "assembly_districts": 100, "senate_districts": 35},
    "California": {"districts": 52, "senate_year": None, "gov_year": 2026, "assembly_districts": 80, "senate_districts": 40},
    "Colorado": {"districts": 8, "senate_year": None, "gov_year": 2026, "assembly_districts": 65, "senate_districts": 35},
    "Connecticut": {"districts": 5, "senate_year": None, "gov_year": 2026, "assembly_districts": 151, "senate_districts": 36},
    "Delaware": {"districts": 1, "senate_year": 2026, "gov_year": None, "assembly_districts": 41, "senate_districts": 21},
    "Florida": {"districts": 28, "senate_year": None, "gov_year": 2026, "assembly_districts": 120, "senate_districts": 40},
    "Georgia": {"districts": 14, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 180, "senate_districts": 56},
    "Hawaii": {"districts": 2, "senate_year": None, "gov_year": 2026, "assembly_districts": 51, "senate_districts": 25},
    "Idaho": {"districts": 2, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 70, "senate_districts": 35},
    "Illinois": {"districts": 17, "senate_year": None, "gov_year": 2026, "assembly_districts": 118, "senate_districts": 59},
    "Indiana": {"districts": 9, "senate_year": None, "gov_year": 2026, "assembly_districts": 100, "senate_districts": 50},
    "Iowa": {"districts": 4, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 100, "senate_districts": 50},
    "Kansas": {"districts": 4, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 125, "senate_districts": 40},
    "Kentucky": {"districts": 6, "senate_year": None, "gov_year": 2027, "assembly_districts": 100, "senate_districts": 38},
    "Louisiana": {"districts": 6, "senate_year": 2026, "gov_year": 2027, "assembly_districts": 105, "senate_districts": 39},
    "Maine": {"districts": 2, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 151, "senate_districts": 35},
    "Maryland": {"districts": 8, "senate_year": None, "gov_year": 2026, "assembly_districts": 141, "senate_districts": 47},
    "Massachusetts": {"districts": 9, "senate_year": None, "gov_year": 2026, "assembly_districts": 160, "senate_districts": 40},
    "Michigan": {"districts": 13, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 110, "senate_districts": 38},
    "Minnesota": {"districts": 8, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 134, "senate_districts": 67},
    "Mississippi": {"districts": 4, "senate_year": 2026, "gov_year": 2027, "assembly_districts": 122, "senate_districts": 52},
    "Missouri": {"districts": 8, "senate_year": None, "gov_year": 2026, "assembly_districts": 163, "senate_districts": 34},
    "Montana": {"districts": 2, "senate_year": None, "gov_year": 2026, "assembly_districts": 100, "senate_districts": 50},
    "Nebraska": {"districts": 3, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 49, "senate_districts": 0},
    "Nevada": {"districts": 4, "senate_year": None, "gov_year": 2026, "assembly_districts": 42, "senate_districts": 21},
    "New Hampshire": {"districts": 2, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 400, "senate_districts": 24},
    "New Jersey": {"districts": 12, "senate_year": 2026, "gov_year": 2025, "assembly_districts": 40, "senate_districts": 40},
    "New Mexico": {"districts": 3, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 70, "senate_districts": 42},
    "New York": {"districts": 26, "senate_year": None, "gov_year": 2026, "assembly_districts": 150, "senate_districts": 63},
    "North Carolina": {"districts": 14, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 120, "senate_districts": 50},
    "North Dakota": {"districts": 1, "senate_year": None, "gov_year": 2026, "assembly_districts": 94, "senate_districts": 47},
    "Ohio": {"districts": 15, "senate_year": None, "gov_year": 2026, "assembly_districts": 99, "senate_districts": 33},
    "Oklahoma": {"districts": 5, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 101, "senate_districts": 48},
    "Oregon": {"districts": 6, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 60, "senate_districts": 30},
    "Pennsylvania": {"districts": 17, "senate_year": None, "gov_year": 2026, "assembly_districts": 203, "senate_districts": 50},
    "Rhode Island": {"districts": 2, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 75, "senate_districts": 38},
    "South Carolina": {"districts": 7, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 124, "senate_districts": 46},
    "South Dakota": {"districts": 1, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 70, "senate_districts": 35},
    "Tennessee": {"districts": 9, "senate_year": None, "gov_year": 2026, "assembly_districts": 99, "senate_districts": 33},
    "Texas": {"districts": 38, "senate_year": None, "gov_year": 2026, "assembly_districts": 150, "senate_districts": 31},
    "Utah": {"districts": 4, "senate_year": None, "gov_year": 2026, "assembly_districts": 75, "senate_districts": 29},
    "Vermont": {"districts": 1, "senate_year": None, "gov_year": 2026, "assembly_districts": 150, "senate_districts": 30},
    "Virginia": {"districts": 11, "senate_year": 2026, "gov_year": 2025, "assembly_districts": 100, "senate_districts": 40},
    "Washington": {"districts": 10, "senate_year": None, "gov_year": 2026, "assembly_districts": 98, "senate_districts": 49},
    "West Virginia": {"districts": 2, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 100, "senate_districts": 34},
    "Wisconsin": {"districts": 8, "senate_year": None, "gov_year": 2026, "assembly_districts": 99, "senate_districts": 33},
    "Wyoming": {"districts": 1, "senate_year": 2026, "gov_year": 2026, "assembly_districts": 60, "senate_districts": 30}
}

import os

def generate_chunk1_detailed(state, info):
    """Generate CHUNK_1 with actual race breakdown"""
    
    districts = info['districts']
    senate_year = info['senate_year']
    gov_year = info['gov_year']
    assembly = info['assembly_districts']
    senate_districts = info['senate_districts']
    
    # Calculate race counts
    federal_races = (1 if senate_year else 0) + districts
    state_races = 2 if gov_year == 2025 else 0
    legislature_races = assembly + senate_districts if gov_year == 2025 else 0
    
    total_races = federal_races + state_races + legislature_races + 20  # +20 for school/county
    
    template = f"""# CHUNK 1: {state.upper()} RACES ARRAY ONLY

## TASK: Provide ONLY the races array for {state} 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY {total_races} races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, {state}.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal ({senate_year or 2026}) - {federal_races} races
"""
    
    if senate_year:
        template += f"1. U.S. Senate\n"
        template += f"2-{federal_races}. U.S. House Districts 1-{districts} (ALL {districts})\n\n"
    else:
        template += f"1-{federal_races}. U.S. House Districts 1-{districts} (ALL {districts})\n\n"
    
    if state_races > 0:
        template += f"""### State (2025) - {state_races} races
Governor, Lieutenant Governor

"""
    
    if legislature_races > 0:
        template += f"""### State Legislature (2025) - {legislature_races} races
- House/Assembly: {assembly} seats (Districts 1-{assembly})
- Senate: {senate_districts} seats (Districts 1-{senate_districts})

"""
    
    template += f"""### School Boards + County (2025) - ~20 races
Major city school boards and county positions

## FORMAT:

```python
races = [
    {{
        "state": "{state}",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "{senate_year or 2026}-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and {state}.gov..."
    }},
    # CONTINUE FOR ALL {total_races} RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: {total_races}
- Federal: {federal_races}
- State: {state_races}
- Legislature: {legislature_races}
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
"""
    
    return template

# Generate for all states
output_dir = "COMPLETE_STATE_TEMPLATES"
for state, info in STATE_INFO.items():
    state_dir = os.path.join(output_dir, state.replace(" ", "_"))
    os.makedirs(state_dir, exist_ok=True)
    
    chunk1_content = generate_chunk1_detailed(state, info)
    
    with open(os.path.join(state_dir, "CHUNK_1_RACES.md"), 'w', encoding='utf-8') as f:
        f.write(chunk1_content)
    
    print(f"Generated {state}")

print(f"\nGenerated detailed CHUNK_1 for all 50 states")
