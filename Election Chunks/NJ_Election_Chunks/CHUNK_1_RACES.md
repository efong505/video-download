# CHUNK 1: NEW JERSEY RACES ARRAY ONLY

## TASK: Provide ONLY the races array for New Jersey 2025-2026

**DO NOT provide:**
- ❌ Candidates array
- ❌ Summary
- ❌ Upload script
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `races`
- ✅ EXACTLY 128 races (MANDATORY - COUNT AND VERIFY)
- ✅ Every race must have: state, office, election_date, race_type, description
- ✅ Base ALL data on real sources (NJ.gov PDFs, Ballotpedia)
- ✅ Cite sources in descriptions

## REQUIRED RACES:

### Federal (2026) - 13 races
1. U.S. Senate
2-13. U.S. House Districts 1-12 (ALL 12)

### State (2025) - 2 races
14. Governor
15. Lieutenant Governor

### State Legislature (2025) - 80 races
16-95. General Assembly Districts 1-40 (ALL 40 districts × 2 seats each = 80 races)
  - District 1 Seat 1, District 1 Seat 2, District 2 Seat 1, District 2 Seat 2, etc.

### School Boards (2025) - 22 races
96-117. School board seats for:
- Newark (3 seats)
- Jersey City (3 seats)
- Paterson (3 seats)
- Elizabeth (3 seats)
- Edison (3 seats)
- Woodbridge (3 seats)
- Camden (3 seats)
- Trenton (3 seats)
- Clifton (3 seats)
- Passaic (3 seats)
- Union City (3 seats)
- Bayonne (3 seats)
- East Orange (3 seats)
- Vineland (3 seats)
- New Brunswick (3 seats)

### County (2025) - 9 races
118-126. Bergen Commissioner, Essex Sheriff, Middlesex Clerk, Ocean Commissioner, Camden Prosecutor, Monmouth Sheriff, Hudson Clerk, Union Commissioner, Passaic Sheriff

### Statewide (2026) - 2 races
127-128. Attorney General (appointed but list), Secretary of State (appointed but list)

## FORMAT:

```python
races = [
    {
        "state": "New Jersey",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Democratic Senator Cory Booker seeks re-election..."
    },
    {
        "state": "New Jersey",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Donald Norcross (D) represents South Jersey..."
    },
    # CONTINUE FOR ALL 128 RACES
]
```

## VERIFICATION:

At the end, provide:
```
TOTAL RACES: 128
- Federal: 13
- State: 2
- Legislature: 80 (40 districts × 2 seats)
- School Boards: 22
- County: 9
- Statewide: 2
```

**START OUTPUT NOW - RACES ARRAY ONLY**
