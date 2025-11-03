# CHUNK 1: NEVADA RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Nevada 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 142 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Nevada.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 4 races
1-4. U.S. House Districts 1-4 (ALL 4)

### State (2026) - 2 races
Governor, Lieutenant Governor

### State Legislature (2026) - 63 races
- House/Assembly: 42 seats (Districts 1-42)
- Senate: 21 seats (Districts 1-21)

### Municipal & County (2025-2026) - 73 races
- School Boards: 25 seats across major cities
- City Councils: 35 seats across major cities
- Mayoral Races: 3 races
- County Positions: 10 races (sheriff, commissioner, clerk, etc.)

## FORMAT:

```python
races = [
    {
        "state": "Nevada",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Nevada.gov..."
    },
    # CONTINUE FOR ALL 142 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 142
- Federal: 4
- State: 2
- Legislature: 63
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
