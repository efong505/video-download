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
        "major_cities": ["Birmingham", "Montgomery", "Mobile"],  # Top 3-5 cities
        "school_board_seats": 15,  # Total school board seats across major cities
        "city_council_seats": 20,  # Total city council seats across major cities
        "mayoral_races": 5,  # Number of mayoral races in major cities
        "county_races": 10  # County-level races (sheriff, commissioner, clerk, etc.)
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
- List 3-5 largest cities by population
- Source: Wikipedia "List of cities in [State]"

### 6. School Board Seats
- Count total school board seats across major cities
- Typically 5-9 seats per city
- Source: City websites, Ballotpedia

### 7. City Council Seats
- Count total city council seats across major cities
- Typically 5-15 seats per city
- Source: City websites, Wikipedia

### 8. Mayoral Races
- Count mayoral races in major cities (2025-2026)
- Check election schedules for each city
- Source: Ballotpedia, city websites

### 9. County Races
- Estimate 5-15 county-level races (sheriff, commissioner, clerk, prosecutor)
- Larger states = more races
- Source: Ballotpedia county elections

## EXAMPLE (New Jersey)

```python
"New Jersey": {
    "districts": 12,  # 12 US House districts
    "senate_year": 2026,  # Cory Booker up for re-election
    "gov_year": 2025,  # Phil Murphy term ends 2026, election Nov 2025
    "assembly_districts": 40,  # 40 Assembly districts (2 seats each = 80 total)
    "senate_districts": 40,  # 40 Senate districts
    "major_cities": ["Newark", "Jersey City", "Paterson", "Elizabeth", "Edison"],
    "school_board_seats": 22,  # Newark (9), Jersey City (9), Paterson (9), Elizabeth (9), Edison (9) = 45 total, but only competitive seats
    "city_council_seats": 35,  # Newark (9), Jersey City (9), Paterson (6), Elizabeth (5), Edison (5)
    "mayoral_races": 3,  # Newark, Paterson, Elizabeth (2025)
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
- [ ] School board seats counted for major cities
- [ ] City council seats counted for major cities
- [ ] Mayoral races checked for 2025-2026
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
