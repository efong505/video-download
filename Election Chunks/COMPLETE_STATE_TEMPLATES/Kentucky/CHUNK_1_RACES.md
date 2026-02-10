# CHUNK 1: KENTUCKY RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Kentucky 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 220 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Kentucky.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 7 races
1. U.S. Senate
2-7. U.S. House Districts 1-6 (ALL 6)

### State (2027) - 2 races
Governor, Lieutenant Governor

### State Legislature (2027) - 138 races
- House/Assembly: 100 seats (Districts 1-100)
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
        "state": "Kentucky",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Kentucky.gov..."
    },
    # CONTINUE FOR ALL 220 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 220
- Federal: 7
- State: 2
- Legislature: 138
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
