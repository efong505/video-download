# CHUNK 1: ARIZONA RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Arizona 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 144 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Arizona.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 9 races
1-9. U.S. House Districts 1-9 (ALL 9)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 60 races
- House/Assembly: 30 seats (Districts 1-30)
- Senate: 30 seats (Districts 1-30)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Arizona",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Arizona.gov..."
    },
    # CONTINUE FOR ALL 144 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 144
- Federal: 9
- State: 2
- Legislature: 60
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
