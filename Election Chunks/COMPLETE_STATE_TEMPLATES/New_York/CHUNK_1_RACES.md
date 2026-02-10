# CHUNK 1: NEW YORK RACES ARRAY ONLY

## TASK: Provide ONLY the races array for New York 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 314 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, New York.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 26 races
1-26. U.S. House Districts 1-26 (ALL 26)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 213 races
- House/Assembly: 150 seats (Districts 1-150)
- Senate: 63 seats (Districts 1-63)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "New York",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and New York.gov..."
    },
    # CONTINUE FOR ALL 314 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 314
- Federal: 26
- State: 2
- Legislature: 213
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
