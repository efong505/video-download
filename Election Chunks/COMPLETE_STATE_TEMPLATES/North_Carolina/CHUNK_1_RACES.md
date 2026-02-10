# CHUNK 1: NORTH CAROLINA RACES ARRAY ONLY

## TASK: Provide ONLY the races array for North Carolina 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 88 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, North Carolina.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 15 races
1. U.S. Senate
2-15. U.S. House Districts 1-14 (ALL 14)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "North Carolina",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and North Carolina.gov..."
    },
    # CONTINUE FOR ALL 88 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 88
- Federal: 15
- State: 0
- Legislature: 0
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
