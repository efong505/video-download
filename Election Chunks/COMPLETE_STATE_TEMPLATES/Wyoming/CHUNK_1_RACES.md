# CHUNK 1: WYOMING RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Wyoming 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 170 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Wyoming.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 2 races
1. U.S. Senate
2-2. U.S. House Districts 1-1 (ALL 1)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 93 races
- House/Assembly: 62 seats (Districts 1-62)
- Senate: 31 seats (Districts 1-31)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Wyoming",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Wyoming.gov..."
    },
    # CONTINUE FOR ALL 170 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 170
- Federal: 2
- State: 2
- Legislature: 93
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
