# CHUNK 1: INDIANA RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Indiana 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 82 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Indiana.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 9 races
1-9. U.S. House Districts 1-9 (ALL 9)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Indiana",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Indiana.gov..."
    },
    # CONTINUE FOR ALL 82 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 82
- Federal: 9
- State: 0
- Legislature: 0
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
