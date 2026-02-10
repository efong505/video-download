# CHUNK 1: NEW HAMPSHIRE RACES ARRAY ONLY

## TASK: Provide ONLY the races array for New Hampshire 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 502 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, New Hampshire.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 3 races
1. U.S. Senate
2-3. U.S. House Districts 1-2 (ALL 2)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 424 races
- House/Assembly: 400 seats (Districts 1-400)
- Senate: 24 seats (Districts 1-24)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "New Hampshire",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and New Hampshire.gov..."
    },
    # CONTINUE FOR ALL 502 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 502
- Federal: 3
- State: 2
- Legislature: 424
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
