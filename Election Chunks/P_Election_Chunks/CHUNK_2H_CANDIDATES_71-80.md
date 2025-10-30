# CHUNK 2H: Pennsylvania Candidates 71-80

Generate 10 complete candidate profiles for Pennsylvania 2025-2026 elections.

## MANDATORY REQUIREMENTS

### Research Mandate
- Research REAL candidates from:
  - Ballotpedia Pennsylvania elections
  - Pennsylvania Secretary of State candidate filings
  - Campaign websites
  - LinkedIn profiles
  - Local news coverage
- CITE sources in bios: [Ballotpedia, campaign website, LinkedIn]
- NO fictional candidates, NO placeholders

### Candidate Selection (Candidates 71-80)
Continue with next 10 candidates from:
- Remaining U.S. House districts
- State Legislature races
- School Board races (largest districts)
- County/local races

Prioritize: Federal > Gubernatorial > State Legislature > School Boards > Local

### Output Format
```python
    # CONTINUE FROM CANDIDATE 70 WITH COMMA
    {
        "name": "Full Legal Name",
        "state": "Pennsylvania",
        "office": "Exact Office Name (must match race)",
        "party": "Democrat/Republican/Independent/Nonpartisan",
        "status": "active",
        "bio": "200-300 word biography with real details, education, career, family, campaign focus. MUST cite sources. [Sources: Ballotpedia, campaign site, LinkedIn]",
        "faith_statement": "Direct quote or 'No publicly disclosed faith statement'",
        "website": "https://realcampaignwebsite.com or empty string",
        "positions": {
            "ABORTION": "Detailed position (150+ words)",
            "EDUCATION": "Detailed position (150+ words)",
            "RELIGIOUS-FREEDOM": "Detailed position (150+ words)",
            "GUNS": "Detailed position (150+ words)",
            "TAXES": "Detailed position (150+ words)",
            "IMMIGRATION": "Detailed position (150+ words)",
            "FAMILY-VALUES": "Detailed position (150+ words)",
            "ELECTION-INTEGRITY": "Detailed position (150+ words)"
        },
        "endorsements": ["Real Organization 1", "Real Organization 2", "Real Organization 3"]
    },
```

### Critical Rules
-  Office name MUST match race name exactly
-  Use "School Board" NOT "Board of Education"
-  Include seat numbers: "State House District 5 Seat 1"
-  ALL 8 position fields required (even if "No public position")
-  School board candidates: Mark ABORTION, GUNS, IMMIGRATION, TAXES, ELECTION-INTEGRITY as "N/A for school board role"
-  School board candidates: EDUCATION and FAMILY-VALUES must be detailed
-  Real endorsements from actual organizations
-  Cite sources in bio

### Output Requirements
- Start with: `    {` (4 spaces, opening brace)
- End with: `    },` (comma if not last chunk)
- NO array declaration (`candidates = [`)
- NO closing bracket (`]`)
- NO comments except continuation note
- Each candidate 200-300 words in bio
- Each position 150+ words

## BEGIN GENERATION
Research and generate 10 complete candidate profiles now.
