# CHUNK 1: ILLINOIS RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Illinois 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 270 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Illinois.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 18 races
1. U.S. Senate
2-18. U.S. House Districts 1-17 (ALL 17)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 177 races
- House/Assembly: 118 seats (Districts 1-118)
- Senate: 59 seats (Districts 1-59)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Illinois",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Illinois.gov..."
    },
    # CONTINUE FOR ALL 270 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 270
- Federal: 18
- State: 2
- Legislature: 177
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
