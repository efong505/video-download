# CHUNK 1: HAWAII RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Hawaii 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 153 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Hawaii.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 2 races
1-2. U.S. House Districts 1-2 (ALL 2)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 76 races
- House/Assembly: 51 seats (Districts 1-51)
- Senate: 25 seats (Districts 1-25)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Hawaii",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Hawaii.gov..."
    },
    # CONTINUE FOR ALL 153 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 153
- Federal: 2
- State: 2
- Legislature: 76
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
