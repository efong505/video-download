# CHUNK 1: FLORIDA RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Florida 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 263 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Florida.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 28 races
1-28. U.S. House Districts 1-28 (ALL 28)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 160 races
- House/Assembly: 120 seats (Districts 1-120)
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
        "state": "Florida",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Florida.gov..."
    },
    # CONTINUE FOR ALL 263 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 263
- Federal: 28
- State: 2
- Legislature: 160
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
