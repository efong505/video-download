# CHUNK 1: TENNESSEE RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Tennessee 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 217 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Tennessee.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 10 races
1. U.S. Senate
2-10. U.S. House Districts 1-9 (ALL 9)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 132 races
- House/Assembly: 99 seats (Districts 1-99)
- Senate: 33 seats (Districts 1-33)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Tennessee",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Tennessee.gov..."
    },
    # CONTINUE FOR ALL 217 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 217
- Federal: 10
- State: 2
- Legislature: 132
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
