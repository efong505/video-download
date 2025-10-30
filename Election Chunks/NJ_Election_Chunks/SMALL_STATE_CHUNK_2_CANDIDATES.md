# CHUNK 2: Wyoming 2025-2026 Election Candidates Array

## YOUR TASK
Generate the COMPLETE `candidates` array for Wyoming's 2025-2026 elections. This is Part 2 of 3.

## CRITICAL REQUIREMENTS
- **MINIMUM 60 CANDIDATES** (Wyoming is small but competitive races have multiple candidates)
- **ALL 8 POSITION FIELDS REQUIRED**: ABORTION, EDUCATION, RELIGIOUS-FREEDOM, GUNS, TAXES, IMMIGRATION, FAMILY-VALUES, ELECTION-INTEGRITY
- **200-300 WORD BIOS**: Every candidate gets full biographical detail
- **NO ABBREVIATIONS**: Every field must be complete
- **NO PLACEHOLDERS**: No "TBD", "Research needed", or "Similar to above"

## CANDIDATE STRUCTURE
Each candidate must have:
```python
{
    "name": "Full Name",
    "state": "Wyoming",
    "office": "Exact office title matching races array",
    "party": "Republican" or "Democrat" or "Libertarian" or "Independent",
    "status": "active" or "dropped-out" or "withdrawn",
    "bio": "200-300 word biography with birth year, hometown, education, career, political experience, family, faith background",
    "faith_statement": "Direct quote or 'No publicly disclosed faith statement'",
    "website": "https://..." or "No official campaign website",
    "positions": {
        "ABORTION": "Full position statement, 30-50 words",
        "EDUCATION": "Full position statement, 30-50 words",
        "RELIGIOUS-FREEDOM": "Full position statement, 30-50 words",
        "GUNS": "Full position statement, 30-50 words",
        "TAXES": "Full position statement, 30-50 words",
        "IMMIGRATION": "Full position statement, 30-50 words",
        "FAMILY-VALUES": "Full position statement, 30-50 words",
        "ELECTION-INTEGRITY": "Full position statement, 30-50 words"
    },
    "endorsements": ["Organization 1", "Organization 2", "Organization 3"] or []
}
```

## REQUIRED CANDIDATE CATEGORIES

### Federal Candidates (4-8 candidates)
- U.S. Senate: Both major party candidates + any third party
- U.S. House At-Large: Republican primary candidates (2-4), Democrat primary candidates (1-2), general election candidates

### State Executive Candidates (4-6 candidates)
- Governor: Republican primary candidates (2-3), Democrat candidates (1-2)
- Other statewide offices if applicable

### State Legislature Candidates (30-40 candidates)
- **State Senate**: Focus on competitive districts
  - Districts with primaries (both parties)
  - Open seat races
  - Incumbent challenges
- **State House**: Focus on competitive districts
  - Districts with primaries (both parties)
  - Open seat races
  - Key conservative vs. moderate battles

### School Board Candidates (10-15 candidates)
- **Laramie County SD #1** (Cheyenne): 3-4 candidates
- **Natrona County SD #1** (Casper): 2-3 candidates
- **Sweetwater County SD #1** (Rock Springs): 2-3 candidates
- **Albany County SD #1** (Laramie): 2-3 candidates
- **Campbell County SD #1** (Gillette): 2-3 candidates

### Local Candidates (5-10 candidates)
- Mayor races (Cheyenne, Casper, Laramie)
- County Commissioners
- City Council members in key races

## SPECIAL INSTRUCTIONS

### For Dropped-Out Candidates
If a candidate dropped out, still include them with:
- `"status": "dropped-out"`
- Full bio explaining why they were significant
- All 8 position fields (their positions when active)
- Note in bio when/why they dropped out

### For School Board Candidates
School board races are often non-partisan, but research:
- Endorsements from conservative vs. progressive groups
- Positions on curriculum, parental rights, gender ideology
- Background in education or community involvement
- Faith background if publicly known

### Position Statement Guidelines
Each of the 8 position fields should be 30-50 words and include:
- Clear stance (support/oppose specific policies)
- Specific proposals or legislation mentioned
- Voting record if incumbent
- Comparison to opponent's position when relevant

## VERIFICATION CHECKLIST
Before submitting, verify:
- [ ] At least 60 candidates total
- [ ] Every candidate has 200-300 word bio
- [ ] Every candidate has ALL 8 position fields
- [ ] Every position statement is 30-50 words
- [ ] No abbreviations, placeholders, or "see above"
- [ ] Faith statements included (or noted as not disclosed)
- [ ] Websites included (or noted as not available)

## OUTPUT FORMAT
Provide ONLY valid Python array syntax:

```python
candidates = [
    {
        "name": "Harriet Hageman",
        "state": "Wyoming",
        "office": "U.S. House - At-Large District",
        "party": "Republican",
        "status": "active",
        "bio": "Harriet Maxine Hageman, born October 18, 1962, in Fort Laramie, Wyoming, is the U.S. Representative for Wyoming's at-large congressional district, serving since 2023. Raised on a ranch in Goshen County, she is the fourth of five children in a family with deep Wyoming roots dating to the 1870s. Hageman earned a B.S. in business administration from the University of Wyoming in 1986 and a J.D. from the University of Wyoming College of Law in 1989. She practiced natural resources and water law for over 30 years, representing ranchers, farmers, and irrigation districts in disputes with the federal government. Hageman served on the Republican National Committee from 2012-2016 and ran for governor in 2018, finishing third in the primary. In 2022, she challenged incumbent Liz Cheney for the U.S. House seat, winning the primary with 66.3% after receiving Donald Trump's endorsement. She won the general election with 68.6% of the vote. Hageman is unmarried and resides in Cheyenne. Her legislative focus includes energy independence, federal land management reform, and protecting Wyoming's agricultural economy. She serves on the House Judiciary Committee and Natural Resources Committee, advocating for state sovereignty and limited federal overreach.",
        "faith_statement": "Hageman has stated, 'My faith guides my commitment to protecting life, family, and the freedoms our founders enshrined in the Constitution.'",
        "website": "https://www.harrietforcongress.com",
        "positions": {
            "ABORTION": "Hageman is strongly pro-life, supporting a federal ban on abortion after 15 weeks with exceptions for rape, incest, and the mother's life. She opposes federal funding for Planned Parenthood and supports overturning Roe v. Wade, which she celebrated as a victory for states' rights.",
            "EDUCATION": "Hageman opposes federal control of education, supporting the elimination of the Department of Education and returning authority to states and parents. She advocates for school choice, including vouchers for private and religious schools, and opposes critical race theory and gender ideology in curricula.",
            "RELIGIOUS-FREEDOM": "Hageman is a staunch defender of religious liberty, supporting the First Amendment Defense Act to protect faith-based organizations from government discrimination. She opposes mandates that force religious employers to provide contraception or participate in same-sex marriage ceremonies.",
            "GUNS": "Hageman is a strong Second Amendment advocate, opposing all gun control measures including universal background checks and red flag laws. She supports constitutional carry and has received an A+ rating from the NRA, emphasizing that gun rights are essential to Wyoming's culture and security.",
            "TAXES": "Hageman supports making the Trump tax cuts permanent, eliminating the estate tax, and reducing corporate tax rates to stimulate economic growth. She opposes any tax increases and advocates for a balanced budget amendment to control federal spending and reduce the national debt.",
            "IMMIGRATION": "Hageman calls for completing the border wall, ending catch-and-release policies, and deporting criminal illegal immigrants immediately. She opposes amnesty and sanctuary cities, supporting mandatory E-Verify for all employers and increased funding for ICE and Border Patrol to secure the southern border.",
            "FAMILY-VALUES": "Hageman supports traditional marriage between one man and one woman, opposes transgender athletes in women's sports, and advocates for parental rights in education. She opposes gender-affirming care for minors and supports policies that strengthen the nuclear family as the foundation of society.",
            "ELECTION-INTEGRITY": "Hageman supports voter ID requirements, paper ballots, and audits of election machines to ensure transparency. She opposes mail-in voting without strict verification and supports purging inactive voters from rolls to prevent fraud, emphasizing that only legal citizens should vote."
        },
        "endorsements": ["Donald Trump", "Wyoming Right to Life", "National Rifle Association", "Club for Growth"]
    },
    # ... continue for all 60+ candidates
]
```

## ANTI-OMISSION RULES
❌ FORBIDDEN: "# 60 total candidates"
❌ FORBIDDEN: "... (continuing pattern for remaining candidates)"
❌ FORBIDDEN: Character counts like "(256 chars)"
❌ FORBIDDEN: "Similar positions to above candidate"
❌ FORBIDDEN: Abbreviated bios under 200 words

✅ REQUIRED: Every single candidate fully written out
✅ REQUIRED: 200-300 word bios for each
✅ REQUIRED: All 8 position fields for each
✅ REQUIRED: 30-50 words per position statement

Generate the complete candidates array now.
