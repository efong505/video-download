# CHUNK 1: VERMONT RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Vermont 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 256 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Vermont.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 1 races
1-1. U.S. House Districts 1-1 (ALL 1)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 180 races
- House/Assembly: 150 seats (Districts 1-150)
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
        "state": "Vermont",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Vermont.gov..."
    },
    # CONTINUE FOR ALL 256 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 256
- Federal: 1
- State: 2
- Legislature: 180
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
