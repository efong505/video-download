# CHUNK 1: VIRGINIA RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Virginia 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 226 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Virginia.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 11 races
1-11. U.S. House Districts 1-11 (ALL 11)

### State (2025) - 2 races
Governor, Lieutenant Governor

### State Legislature (2025) - 140 races
- House/Assembly: 100 seats (Districts 1-100)
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
        "state": "Virginia",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Virginia.gov..."
    },
    # CONTINUE FOR ALL 226 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 226
- Federal: 11
- State: 2
- Legislature: 140
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
