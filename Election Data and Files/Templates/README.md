# State Election Data Templates

This directory contains templates and formatting rules for creating consistent state election summaries for the Christian conservative election platform.

## Project Context

**Platform:** State election coverage system with interactive US map  
**Database:** DynamoDB tables (races, candidates, state-summaries)  
**Admin Interface:** CSV bulk import for races and candidates  
**Public Interface:** Election map displays state summaries with markdown/HTML support  
**Perspective:** Christian conservative voter guides emphasizing pro-life, religious liberty, parental rights, and biblical values

## Files in This Directory

### 1. FORMATTING_RULES.md
**Purpose:** Complete formatting standards for all state summaries
**Use:** Reference this document before creating any state summary to ensure consistency

**Key Rules:**
- Markdown structure with `#`, `##`, `###` headers
- Bold formatting with `**text**`
- Required emojis for each section
- Horizontal dividers `---` between sections
- Specific order of sections

### 2. state_summary_template.md
**Purpose:** Blank template showing exact structure
**Use:** Copy this structure when writing state summary content

**How to Use:**
1. Copy the template
2. Replace all `[PLACEHOLDERS]` with actual state data
3. Follow the exact section order
4. Maintain all formatting (bold, emojis, dividers)

### 3. upload_state_template.py
**Purpose:** Python script template for uploading state data to DynamoDB
**Use:** Copy and customize for each state

**How to Use:**
1. Copy file and rename: `upload_[state_name]_data.py`
2. Replace all `[PLACEHOLDERS]` with actual data
3. Fill in races, candidates, and summary content
4. Run: `python upload_[state_name]_data.py`

**Important Notes:**
- Use `[SUCCESS]` instead of emoji in print statements (Windows compatibility)
- Match candidate `race_id` to race `race_id` for proper linking
- Summary content must follow `state_summary_template.md` structure

## Workflow for Adding a New State

### Step 1: Research
Gather information about:
- All races (federal, statewide, municipal) for 2025-2026 election cycle
- Major candidates with bios, positions, endorsements, **faith statements**
- State political landscape and demographics
- Christian conservative priorities: pro-life, school choice, religious liberty, family values, 2nd Amendment, election integrity
- Election dates and deadlines
- Local Christian conservative organizations and resources
- State-specific issues affecting Christian voters

### Step 2: Write Summary Content
1. Open `state_summary_template.md`
2. Copy the entire template
3. Replace all `[PLACEHOLDERS]` with state-specific content
4. Follow `FORMATTING_RULES.md` exactly
5. Verify all required sections are present
6. Check character count (aim for 15,000-25,000 for comprehensive 20-30 page guide)
7. Ensure Christian conservative perspective throughout
8. Include detailed candidate analysis with faith statements
9. Address all 8 key focus areas (pro-life, school choice, religious liberty, family values, 2nd Amendment, election integrity, border security, economic freedom)

### Step 3: Create Upload Script
1. Copy `upload_state_template.py`
2. Rename to `upload_[state_name]_data.py`
3. Fill in races array with all state races
4. Fill in candidates array with all candidates
5. Paste your summary content from Step 2 into the content field
6. Verify all race_id matching is correct

### Step 4: Upload to Database
1. Navigate to Scripts directory
2. Run: `python upload_[state_name]_data.py`
3. Verify success messages
4. Check website to confirm data appears correctly

### Step 5: Quality Check
- [ ] All races appear on state page
- [ ] All candidates linked to correct races
- [ ] Summary displays with proper formatting
- [ ] Emojis render correctly
- [ ] Bold text appears bold
- [ ] Section dividers visible
- [ ] Download buttons work (TXT and PDF)

## Quick Reference

### Required Emojis
- 📊 Database Summary
- 🔴 Political Landscape / Races
- 🎯 Key Issues
- 📅 Critical Dates
- 🗳️ Church Mobilization
- 📞 Resources
- 🔥 Bottom Line
- 🙏 Prayer Points
- ✅ Positive/Allowed items
- ❌ Negative/Prohibited items

### Section Order
1. Title
2. Database Summary
3. Political Landscape
4. Races (Federal → Statewide → Municipal)
5. Key Issues
6. Critical Dates
7. Church Mobilization
8. Resources
9. Bottom Line
10. Prayer Points
11. Footer

### Common Mistakes
❌ Forgetting bold formatting on key terms
❌ Missing horizontal dividers between sections
❌ Wrong emoji for section
❌ Sections out of order
❌ Missing "Why It Matters" explanations
❌ No footer with contact info

## Examples

See completed states for reference:
- **Hawaii 2025-2026:** 50+ races, 8 candidates, full guide
- **California 2025-2026:** 90+ races, 35+ candidates, full guide
- **Virginia 2025-2026:** 150+ races, 30+ candidates, full guide
- **New Jersey 2025-2026:** 135+ races, 25+ candidates, full guide
- **Texas 2025-2026:** Municipal races with Christian conservative analysis
- **New Mexico 2025-2026:** Comprehensive state guide with church mobilization
- **Pennsylvania 2025-2026:** Federal and statewide races
- **Georgia 2025-2026:** Full state coverage
- **Florida 2025-2026:** Complete voter guide

## Questions?

If formatting is unclear, always refer to:
1. `FORMATTING_RULES.md` - The authoritative standard
2. Existing state summaries - Real examples
3. `state_summary_template.md` - Blank structure

## CSV Import Option

The admin interface supports CSV bulk import for races and candidates:

**Races CSV Format:**
```
state,office,election_date,race_type,description
Texas,Governor,2026-11-03,general,Texas Gubernatorial Race
```

**Candidates CSV Format:**
```
name,state,office,party,bio,website,faith_statement,positions,endorsements
Ted Cruz,Texas,U.S. Senate,Republican,Conservative senator...,https://tedcruz.org,Strong Christian faith,abortion:pro-life;guns:strong-support,NRA;Texas Right to Life
```

**Note:** Python upload scripts provide more control and are recommended for comprehensive state data.

## Version History

- v1.0 (January 2025) - Initial template creation
- Templates based on Hawaii, California, Virginia, New Jersey, Texas, New Mexico, Pennsylvania formats
- Standardized for consistency across all 50 states
- Christian conservative perspective emphasized throughout
