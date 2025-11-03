# CHUNK 1: KANSAS RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Kansas 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 245 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Kansas.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 5 races
1. U.S. Senate
2-5. U.S. House Districts 1-4 (ALL 4)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 165 races
- House/Assembly: 125 seats (Districts 1-125)
- Senate: 40 seats (Districts 1-40)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Kansas",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Kansas.gov..."
    },
    # CONTINUE FOR ALL 245 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 245
- Federal: 5
- State: 2
- Legislature: 165
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
