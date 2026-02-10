# AI Prompt Template for State Election Data Creation

Use this prompt template when requesting AI assistance to create comprehensive state election data.

---

## Standard Prompt Template

```
I need help creating election data (races, candidates, and state summaries) for a Christian conservative election platform. Here's the context:

**System Overview**
- Platform: State election coverage system with interactive US map
- Database: DynamoDB tables (races, candidates, state-summaries)
- Admin Interface: CSV bulk import for races and candidates
- Public Interface: Election map displays state summaries with markdown/HTML support

**Data Structure**

Races CSV Format:
state,office,election_date,race_type,description

Example:
Texas,Governor,2026-11-03,general,Texas Gubernatorial Race
California,U.S. Senate,2026-11-03,general,U.S. Senate Race

Candidates CSV Format:
name,state,office,party,bio,website,faith_statement,positions,endorsements

Example:
Ted Cruz,Texas,U.S. Senate,Republican,Conservative senator...,https://tedcruz.org,Strong Christian faith,abortion:pro-life;guns:strong-support;immigration:secure-border,NRA;Texas Right to Life

**State Summary Format:**
Comprehensive markdown voter guide (20-30 pages) covering:
- Political landscape and demographics
- Top priority races (Governor, Senate, House, Legislature)
- Candidate profiles with Christian conservative analysis
- Key issues (Life, Education, Religious Liberty, etc.)
- Church mobilization strategy
- Prayer points and resources

**Examples Completed:**
- Hawaii 2025-2026 (50+ races, 8 candidates, full guide)
- California 2025-2026 (90+ races, 35+ candidates, full guide)
- Virginia 2025-2026 (150+ races, 30+ candidates, full guide)
- New Jersey 2025-2026 (135+ races, 25+ candidates, full guide)
- Texas 2025-2026 (Municipal races)
- New Mexico 2025-2026 (Comprehensive guide)
- Pennsylvania 2025-2026 (Federal/statewide)
- Georgia 2025-2026 (Full coverage)
- Florida 2025-2026 (Complete guide)

**What I Need:**
Create comprehensive election data for [STATE NAME] including:
1. Races CSV with all major 2025-2026 races
2. Candidates CSV with major candidates and their positions
3. State summary markdown guide following the established format

**Focus on Christian conservative perspective with emphasis on:**
- Pro-life candidates and positions
- School choice and parental rights
- Religious liberty
- Traditional family values
- Second Amendment rights
- Election integrity
- Border security (where applicable)
- Economic freedom and limited government

**Important:**
- Follow the templates in `Election Data and Files\Templates\`
- Use the formatting rules in `FORMATTING_RULES.md`
- Match the structure in `state_summary_template.md`
- Create Python upload script using `upload_state_template.py`
- Ensure 15,000-25,000 character comprehensive guide
- Include faith statements for all candidates
- Address all 8 key Christian conservative focus areas

Please research current election information and create comprehensive data following the established format.
```

---

## Quick Reference Prompt (For Continuing Work)

```
Create [STATE NAME] election data following the templates in `Election Data and Files\Templates\`:
- Use `state_summary_template.md` for structure
- Follow `FORMATTING_RULES.md` for formatting
- Base upload script on `upload_state_template.py`
- Christian conservative perspective throughout
- 15,000-25,000 character comprehensive guide
- Include all 8 key focus areas
```

---

## Prompt for Specific Components

### Races Only
```
Create races data for [STATE NAME] 2025-2026 elections:
- All federal races (Senate, House)
- All statewide races (Governor, Lt. Gov, AG, etc.)
- Major municipal races (if applicable)
- Format: Python array for upload_state_template.py
```

### Candidates Only
```
Create candidate profiles for [STATE NAME] 2025-2026 elections:
- Major candidates for top races
- Include: name, party, bio, faith statement, positions, endorsements
- Christian conservative analysis
- Format: Python array for upload_state_template.py
```

### Summary Only
```
Create state summary for [STATE NAME] following `state_summary_template.md`:
- 15,000-25,000 characters
- Christian conservative perspective
- All required sections with proper markdown formatting
- Bold text, emojis, horizontal dividers
- Address all 8 key focus areas
```

---

## Key Reminders for AI

When creating state data, always:
1. ✅ Reference the templates in `Election Data and Files\Templates\`
2. ✅ Follow `FORMATTING_RULES.md` exactly
3. ✅ Use markdown with `**bold**` and proper headers
4. ✅ Include all required emojis (🔴, ✅, ❌, 📅, 🗳️, 🔥, 🙏)
5. ✅ Add horizontal dividers `---` between sections
6. ✅ Maintain Christian conservative perspective
7. ✅ Include faith statements for candidates
8. ✅ Address all 8 key focus areas
9. ✅ Create comprehensive 20-30 page equivalent guides
10. ✅ Use `[SUCCESS]` not emoji in Python print statements

---

## Example State Request

```
Create comprehensive election data for Arizona 2025-2026 following the templates in `Election Data and Files\Templates\`:

Include:
- All federal races (Senate, 9 House districts)
- Statewide races (Governor, AG, Secretary of State, etc.)
- Major municipal races (Phoenix, Tucson mayors)
- Detailed candidate profiles with faith statements
- Christian conservative analysis emphasizing:
  * Pro-life positions (Arizona abortion laws)
  * School choice (ESA expansion)
  * Border security (critical issue)
  * Election integrity (2020/2022 concerns)
  * Religious liberty
  * Parental rights

Use `state_summary_template.md` structure, follow `FORMATTING_RULES.md`, and create Python upload script based on `upload_state_template.py`.
```

---

## Troubleshooting

**If AI output doesn't match format:**
1. Point to specific template: "Follow the structure in `state_summary_template.md`"
2. Reference formatting rules: "Use the formatting in `FORMATTING_RULES.md`"
3. Show example: "Match the Texas/New Mexico format exactly"
4. Be explicit: "Use `**bold**` markdown, include 🔴 emoji, add `---` dividers"

**If output is too short:**
- "Expand to 15,000-25,000 characters for comprehensive 20-30 page guide"
- "Add more detail to each section following Hawaii/California examples"

**If Christian conservative perspective is missing:**
- "Emphasize Christian conservative analysis throughout"
- "Include faith statements and biblical values alignment for all candidates"
- "Address all 8 key focus areas: pro-life, school choice, religious liberty, family values, 2nd Amendment, election integrity, border security, economic freedom"
