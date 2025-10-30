# CHUNK 1: Pennsylvania Races Array

Generate a Python list of dictionaries for ALL Pennsylvania 2025-2026 election races.

## MANDATORY REQUIREMENTS

### Research Mandate
- You MUST research real Pennsylvania elections using:
  - Pennsylvania Secretary of State website
  - Ballotpedia Pennsylvania elections page
  - Pennsylvania State Legislature website
  - Local county election boards
- CITE sources in descriptions: [Pennsylvania.gov election calendar, Ballotpedia]
- NO placeholders, NO generic text, NO "TBD"

### Race Count Target
- **MINIMUM 100 races required**
- Include: Federal (Senate, House), Gubernatorial, State Legislature, School Boards, County offices

### Output Format
```python
races = [
    {
        "state": "Pennsylvania",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent [Name] seeks re-election. [Real details from research]. (source: Ballotpedia, Pennsylvania.gov)"
    },
    # ... continue for ALL 100+ races
]
```

### Race Categories to Include

1. **Federal Races**
   - U.S. Senate (if applicable in 2026)
   - U.S. House (all districts in Pennsylvania)

2. **Statewide Races**
   - Governor (if applicable in 2025)
   - Lieutenant Governor
   - Attorney General
   - Secretary of State
   - Other constitutional offices

3. **State Legislature**
   - State Senate seats up in 2025/2026
   - State House/Assembly seats up in 2025/2026
   - Use format: "State Senate District X" or "State House District X Seat Y"

4. **School Boards** (Top 10-15 largest districts)
   - Format: "[City] School Board Seat X"
   - NOT "Board of Education" - use "School Board"

5. **County/Local Offices**
   - County Commissioners
   - Sheriffs
   - Prosecutors/District Attorneys
   - County Clerks

### Critical Rules
-  Use "School Board" NOT "Board of Education"
-  Include seat numbers for multi-seat races: "State House District 5 Seat 1"
-  Real election dates from Pennsylvania election calendar
-  Real descriptions with incumbent names and context
-  Cite sources in descriptions

### Output Requirements
- Start with: `races = [`
- End with: `]`
- Each race is a complete dictionary
- NO abbreviations in descriptions
- NO placeholders or "..."
- Minimum 100 races

## BEGIN GENERATION
Research Pennsylvania 2025-2026 elections and generate the complete races array now.
