# CHUNK 1: NEW JERSEY RACES ARRAY ONLY

## TASK: Provide ONLY the races array for New Jersey 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 164 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, New Jersey.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 13 races
1. U.S. Senate
2-13. U.S. House Districts 1-12 (ALL 12)

### State (2025) - 2 races
Governor, Lieutenant Governor

### State Legislature (2025) - 80 races
- House/Assembly: 40 seats (Districts 1-40)
- Senate: 40 seats (Districts 1-40)

### Municipal & County (2025-2026) - 69 races
- School Boards: 22 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 9 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "New Jersey",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and New Jersey.gov..."
    },
    # CONTINUE FOR ALL 164 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 164
- Federal: 13
- State: 2
- Legislature: 80
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
