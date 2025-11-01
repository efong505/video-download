# AI Research Prompt: Get Accurate Race Counts for All 50 States

## TASK
Research and provide EXACT race counts for 2025-2026 elections for all 50 US states.

## REQUIRED OUTPUT FORMAT

Provide a Python dictionary with this EXACT structure:

```python
STATE_INFO = {
    "Alabama": {
        "districts": 7,  # US House districts
        "senate_year": None,  # 2026 if Senate race, else None
        "gov_year": 2026,  # Year of governor election (2025, 2026, 2027, or None)
        "assembly_districts": 105,  # State House/Assembly seats
        "senate_districts": 35,  # State Senate seats
        "major_cities": ["Birmingham", "Montgomery", "Mobile"],  # Top 3-5 cities for school boards
        "county_races": 10  # Estimated county-level races (sheriff, commissioner, etc.)
    },
    # ... repeat for all 50 states
}
```

## RESEARCH SOURCES
- **Ballotpedia.org** - Most comprehensive election database
- **[State].gov** - Official state election websites
- **Wikipedia** - State legislature sizes and congressional districts

## SPECIFIC DATA NEEDED

### 1. Congressional Districts
- Number of US House districts (1-52)
- Source: Wikipedia "List of United States congressional districts"

### 2. US Senate Race
- Is there a Senate race in 2026? (Yes = 2026, No = None)
- Check Senate Class I (2024), Class II (2026), Class III (2028)

### 3. Governor Election
- What year is the next governor election? (2025, 2026, 2027, or None if 2024)
- Most states: 2026
- Special cases: NJ/VA (2025), KY/LA/MS (2027)

### 4. State Legislature Size
- **Assembly/House seats**: Total number of state house/assembly districts
- **Senate seats**: Total number of state senate districts
- Source: Wikipedia "[State] Legislature"

### 5. Major Cities
- List 3-5 largest cities for school board races
- Source: Wikipedia "List of cities in [State]"

### 6. County Races
- Estimate 5-15 county-level races (sheriff, commissioner, clerk, prosecutor)
- Larger states = more races

## EXAMPLE (New Jersey)

```python
"New Jersey": {
    "districts": 12,  # 12 US House districts
    "senate_year": 2026,  # Cory Booker up for re-election
    "gov_year": 2025,  # Phil Murphy term ends 2026, election Nov 2025
    "assembly_districts": 40,  # 40 Assembly districts (2 seats each = 80 total)
    "senate_districts": 40,  # 40 Senate districts
    "major_cities": ["Newark", "Jersey City", "Paterson", "Elizabeth", "Edison"],
    "county_races": 9  # Bergen, Essex, Middlesex, Ocean, Camden, Monmouth, Hudson, Union, Passaic
}
```

## VERIFICATION CHECKLIST

For each state, verify:
- [ ] Congressional districts match current count (post-2020 census)
- [ ] Senate race year is correct (Class II = 2026)
- [ ] Governor election year is accurate
- [ ] State legislature sizes are current
- [ ] Major cities are by population (top 3-5)
- [ ] County races are reasonable estimate

## OUTPUT INSTRUCTIONS

1. Research ALL 50 states
2. Provide complete Python dictionary
3. Include comments for any uncertain data
4. Cite sources where helpful
5. Double-check Senate Class II states (2026 races)

## SENATE CLASS II STATES (2026 RACES)

These states have Senate races in 2026:
- Alabama, Alaska, Arkansas, Colorado, Delaware, Georgia, Idaho, Illinois, Iowa, Kansas, Kentucky, Louisiana, Maine, Massachusetts, Michigan, Minnesota, Mississippi, Montana, Nebraska, New Hampshire, New Jersey, New Mexico, North Carolina, Oklahoma, Oregon, Rhode Island, South Carolina, South Dakota, Tennessee, Texas, Virginia, West Virginia, Wyoming

## STATES WITH 2025 ELECTIONS

- New Jersey: Governor (Nov 2025)
- Virginia: Governor (Nov 2025)

## STATES WITH 2027 ELECTIONS

- Kentucky: Governor (Nov 2027)
- Louisiana: Governor (Nov 2027)
- Mississippi: Governor (Nov 2027)

## START RESEARCH NOW

Provide the complete STATE_INFO dictionary for all 50 states.
