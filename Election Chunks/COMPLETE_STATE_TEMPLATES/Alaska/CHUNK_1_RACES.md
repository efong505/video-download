# CHUNK 1: ALASKA RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Alaska 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 137 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Alaska.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 2 races
1. U.S. Senate
2-2. U.S. House Districts 1-1 (ALL 1)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 60 races
- House/Assembly: 40 seats (Districts 1-40)
- Senate: 20 seats (Districts 1-20)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Alaska",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Alaska.gov..."
    },
    # CONTINUE FOR ALL 137 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 137
- Federal: 2
- State: 2
- Legislature: 60
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
