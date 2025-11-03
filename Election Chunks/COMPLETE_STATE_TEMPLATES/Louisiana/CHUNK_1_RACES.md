# CHUNK 1: LOUISIANA RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Louisiana 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 226 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Louisiana.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 7 races
1. U.S. Senate
2-7. U.S. House Districts 1-6 (ALL 6)

### State (2027) - 2 races
Governor, Lieutenant Governor

### State Legislature (2027) - 144 races
- House/Assembly: 105 seats (Districts 1-105)
- Senate: 39 seats (Districts 1-39)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Louisiana",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Louisiana.gov..."
    },
    # CONTINUE FOR ALL 226 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 226
- Federal: 7
- State: 2
- Legislature: 144
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
