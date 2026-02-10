# CHUNK 3: NEW JERSEY CANDIDATES 51-100

## TASK: Provide candidates 51-100 ONLY

**DO NOT provide:**
- ❌ Races array
- ❌ Summary
- ❌ Candidates 1-50 or 101-150
- ❌ Any explanatory text

**DO provide:**
- ✅ Candidates 51-100 with ALL fields filled
- ✅ Each candidate must have: name, state, office, party, status, bio (200-300 words), faith_statement, website, positions (8 fields), endorsements

## CANDIDATES TO INCLUDE (51-100):

### State Legislature Candidates (51-70)
51-70. Assembly candidates (2 per district for Districts 13-22)

### School Board Candidates (71-100)
71-100. School board candidates (30 candidates across major districts)
- Newark Board of Education (3 candidates)
- Jersey City Board of Education (3 candidates)
- Paterson Board of Education (3 candidates)
- Elizabeth Board of Education (3 candidates)
- Edison Board of Education (3 candidates)
- Woodbridge Board of Education (3 candidates)
- Camden Board of Education (3 candidates)
- Trenton Board of Education (3 candidates)
- Clifton Board of Education (3 candidates)
- Passaic Board of Education (3 candidates)

## FORMAT:

```python
# CONTINUE FROM CANDIDATE 51
    {
        "name": "[Full Name]",
        "state": "New Jersey",
        "office": "[Office - must match race]",
        "party": "[Republican/Democrat/Nonpartisan]",
        "status": "active",
        "bio": "[200-300 word biography]",
        "faith_statement": "[Actual statement OR 'No publicly disclosed faith statement']",
        "website": "[URL or '']",
        "positions": {
            "ABORTION": "[Detailed position OR 'N/A for school board role']",
            "EDUCATION": "[Detailed position - REQUIRED for all]",
            "RELIGIOUS-FREEDOM": "[Detailed position]",
            "GUNS": "[Detailed position]",
            "TAXES": "[Detailed position]",
            "IMMIGRATION": "[Detailed position]",
            "FAMILY-VALUES": "[Detailed position]",
            "ELECTION-INTEGRITY": "[Detailed position]"
        },
        "endorsements": ["Organization 1", "Organization 2", "Organization 3"]
    },
    # CONTINUE THROUGH CANDIDATE 100
```

## CRITICAL REQUIREMENTS:

- ✅ Bio must be 200-300 words with REAL data from NJ.gov PDFs, Ballotpedia, LinkedIn
- ✅ All 8 position fields must be filled with detailed text (NOT generic statements)
- ✅ Research REAL candidates from official sources
- ✅ Include actual faith statements where available
- ✅ Include REAL endorsements from organizations
- ✅ Cite sources in bio (e.g., "per NJ.gov", "per Ballotpedia")
- ✅ EVERY candidate must be a complete dictionary - NO shortcuts

## SPECIAL NOTE FOR SCHOOL BOARD CANDIDATES:

- For positions not relevant to school boards (like ABORTION, IMMIGRATION), you may write "N/A for school board role"
- EDUCATION and FAMILY-VALUES positions are MANDATORY and must be detailed
- Focus on: parental rights, curriculum transparency, gender ideology, CRT, school choice

## VERIFICATION:

At the end, provide:
```
CANDIDATES 51-100 COMPLETE
Total: 50
- Legislature: 20
- School Boards: 30
```

**START OUTPUT NOW - CANDIDATES 51-100 ONLY**
