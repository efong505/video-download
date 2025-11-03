# CHUNK 1: SOUTH CAROLINA RACES ARRAY ONLY

## TASK: Provide ONLY the races array for South Carolina 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 253 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, South Carolina.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 8 races
1. U.S. Senate
2-8. U.S. House Districts 1-7 (ALL 7)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 170 races
- House/Assembly: 124 seats (Districts 1-124)
- Senate: 46 seats (Districts 1-46)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "South Carolina",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and South Carolina.gov..."
    },
    # CONTINUE FOR ALL 253 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 253
- Federal: 8
- State: 2
- Legislature: 170
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
