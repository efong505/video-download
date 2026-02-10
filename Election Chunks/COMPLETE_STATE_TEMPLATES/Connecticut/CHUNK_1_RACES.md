# CHUNK 1: CONNECTICUT RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Connecticut 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 267 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Connecticut.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 5 races
1-5. U.S. House Districts 1-5 (ALL 5)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 187 races
- House/Assembly: 151 seats (Districts 1-151)
- Senate: 36 seats (Districts 1-36)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Connecticut",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Connecticut.gov..."
    },
    # CONTINUE FOR ALL 267 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 267
- Federal: 5
- State: 2
- Legislature: 187
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
