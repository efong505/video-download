# CHUNK 1: MAINE RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Maine 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 264 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Maine.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 3 races
1. U.S. Senate
2-3. U.S. House Districts 1-2 (ALL 2)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 186 races
- House/Assembly: 151 seats (Districts 1-151)
- Senate: 35 seats (Districts 1-35)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Maine",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Maine.gov..."
    },
    # CONTINUE FOR ALL 264 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 264
- Federal: 3
- State: 2
- Legislature: 186
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
