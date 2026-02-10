# CHUNK 1: IOWA RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Iowa 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 230 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Iowa.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 5 races
1. U.S. Senate
2-5. U.S. House Districts 1-4 (ALL 4)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 150 races
- House/Assembly: 100 seats (Districts 1-100)
- Senate: 50 seats (Districts 1-50)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Iowa",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Iowa.gov..."
    },
    # CONTINUE FOR ALL 230 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 230
- Federal: 5
- State: 2
- Legislature: 150
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
