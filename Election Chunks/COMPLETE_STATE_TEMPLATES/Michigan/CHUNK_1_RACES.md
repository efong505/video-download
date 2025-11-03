# CHUNK 1: MICHIGAN RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Michigan 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 237 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Michigan.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 14 races
1. U.S. Senate
2-14. U.S. House Districts 1-13 (ALL 13)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 148 races
- House/Assembly: 110 seats (Districts 1-110)
- Senate: 38 seats (Districts 1-38)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Michigan",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Michigan.gov..."
    },
    # CONTINUE FOR ALL 237 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 237
- Federal: 14
- State: 2
- Legislature: 148
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
