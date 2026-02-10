# CHUNK 1: WISCONSIN RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Wisconsin 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 215 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Wisconsin.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 8 races
1-8. U.S. House Districts 1-8 (ALL 8)

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
        "state": "Wisconsin",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Wisconsin.gov..."
    },
    # CONTINUE FOR ALL 215 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 215
- Federal: 8
- State: 2
- Legislature: 132
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
