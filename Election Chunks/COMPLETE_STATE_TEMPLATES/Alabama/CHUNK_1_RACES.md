# CHUNK 1: ALABAMA RACES ARRAY ONLY

## TASK: Provide ONLY the races array for Alabama 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 27 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (Ballotpedia, Alabama.gov)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 7 races
1-7. U.S. House Districts 1-7 (ALL 7)

### School Boards + County (2025) - ~20 races
Major city school boards and county positions

## FORMAT:

```python
races = [
    {
        "state": "Alabama",
        "office": "U.S. Senate" if senate_year else "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Research from Ballotpedia and Alabama.gov..."
    },
    # CONTINUE FOR ALL 27 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 27
- Federal: 7
- State: 0
- Legislature: 0
- School/County: ~20
```

**START OUTPUT NOW - RACES ARRAY ONLY**
