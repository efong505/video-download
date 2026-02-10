# CHUNK 1: WASHINGTON RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Washington 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 83 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Washington.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 10 races
1-10. U.S. House Districts 1-10 (ALL 10)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Washington",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Washington.gov..."
    },
    # CONTINUE FOR ALL 83 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 83
- Federal: 10
- State: 0
- Legislature: 0
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
