# CHUNK 1: OREGON RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Oregon 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 172 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Oregon.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 7 races
1. U.S. Senate
2-7. U.S. House Districts 1-6 (ALL 6)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 90 races
- House/Assembly: 60 seats (Districts 1-60)
- Senate: 30 seats (Districts 1-30)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Oregon",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Oregon.gov..."
    },
    # CONTINUE FOR ALL 172 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 172
- Federal: 7
- State: 2
- Legislature: 90
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
