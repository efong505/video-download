# CHUNK 1: PENNSYLVANIA RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Pennsylvania 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 345 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Pennsylvania.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 17 races
1-17. U.S. House Districts 1-17 (ALL 17)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 253 races
- House/Assembly: 203 seats (Districts 1-203)
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
        "state": "Pennsylvania",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Pennsylvania.gov..."
    },
    # CONTINUE FOR ALL 345 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 345
- Federal: 17
- State: 2
- Legislature: 253
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
