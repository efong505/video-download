# CHUNK 1: NEW MEXICO RACES ARRAY ONLY

## TASK: Provide ONLY the races array for New Mexico 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 191 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, New Mexico.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 4 races
1. U.S. Senate
2-4. U.S. House Districts 1-3 (ALL 3)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 112 races
- House/Assembly: 70 seats (Districts 1-70)
- Senate: 42 seats (Districts 1-42)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "New Mexico",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and New Mexico.gov..."
    },
    # CONTINUE FOR ALL 191 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 191
- Federal: 4
- State: 2
- Legislature: 112
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
