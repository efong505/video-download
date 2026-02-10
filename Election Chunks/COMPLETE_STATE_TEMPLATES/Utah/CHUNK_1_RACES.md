# CHUNK 1: UTAH RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Utah 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 77 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Utah.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 4 races
1-4. U.S. House Districts 1-4 (ALL 4)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Utah",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Utah.gov..."
    },
    # CONTINUE FOR ALL 77 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 77
- Federal: 4
- State: 0
- Legislature: 0
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
