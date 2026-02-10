# CHUNK 1: Wyoming 2025-2026 Election Races Array

## YOUR TASK
Generate ONLY the `races` array for Wyoming's 2025-2026 elections. This is Part 1 of 3.

## CRITICAL REQUIREMENTS
- **MINIMUM 35 RACES** (Wyoming is small but must be comprehensive)
- **NO ABBREVIATIONS**: Every field must be complete
- **NO PLACEHOLDERS**: No "TBD", "N/A", or "See above"
- **NO COMMENTS**: No "# 35 total races" - just provide them all

## RACE STRUCTURE
Each race must have:
```python
{
    "office": "Full office name",
    "state": "Wyoming",
    "election_date": "YYYY-MM-DD",
    "race_type": "primary" or "general",
    "description": "50-100 word description of race significance",
    "key_issues": ["issue1", "issue2", "issue3", "issue4", "issue5"],  # Exactly 5 issues
    "christian_conservative_priority": "low" or "medium" or "high" or "critical"
}
```

## REQUIRED RACE CATEGORIES

### Federal Races (3 races minimum)
- U.S. Senate (if applicable in 2025-2026)
- U.S. House (Wyoming has 1 at-large district)
- Include both primary and general for each

### State Executive (2 races minimum)
- Governor (if applicable in 2026)
- Other statewide offices

### State Legislature (20 races minimum)
- Wyoming State Senate (30 seats total, focus on competitive/open seats)
- Wyoming State House (60 seats total, focus on competitive/open seats)
- Include primaries for key districts

### School Boards (5 races minimum)
- Laramie County School District #1 (Cheyenne)
- Natrona County School District #1 (Casper)
- Sweetwater County School District #1 (Rock Springs)
- Albany County School District #1 (Laramie)
- Campbell County School District #1 (Gillette)

### Local Races (5 races minimum)
- Mayor races (Cheyenne, Casper, Laramie)
- County Commissioner races
- City Council races

## VERIFICATION CHECKLIST
Before submitting, verify:
- [ ] At least 35 races total
- [ ] Every race has all 6 fields filled
- [ ] Every race has exactly 5 key_issues
- [ ] Descriptions are 50-100 words each
- [ ] No abbreviations, placeholders, or comments
- [ ] Christian conservative priority set for each race

## OUTPUT FORMAT
Provide ONLY valid Python array syntax:

```python
races = [
    {
        "office": "U.S. House - At-Large District",
        "state": "Wyoming",
        "election_date": "2026-08-18",
        "race_type": "primary",
        "description": "Wyoming's single congressional seat is up for election...",
        "key_issues": ["Energy independence", "Federal land management", "Second Amendment rights", "Border security", "Inflation"],
        "christian_conservative_priority": "high"
    },
    # ... continue for all 35+ races
]
```

## ANTI-OMISSION RULES
❌ FORBIDDEN: "# 35 total races"
❌ FORBIDDEN: "... (continuing pattern for remaining races)"
❌ FORBIDDEN: Character counts like "(512 chars)"
❌ FORBIDDEN: "See above for structure"

✅ REQUIRED: Every single race fully written out
✅ REQUIRED: Complete descriptions for each
✅ REQUIRED: All fields populated

Generate the complete races array now.
