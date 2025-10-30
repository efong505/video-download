# CHUNK 2: NEW JERSEY CANDIDATES 1-50

## TASK: Provide candidates 1-50 ONLY

**CRITICAL: You MUST write ALL 50 candidates completely. If you write "..." or "[continue]" or abbreviate ANY candidate, you have FAILED this task.**

**DO NOT provide:**
- ❌ Races array
- ❌ Summary
- ❌ Candidates 51-150
- ❌ Any explanatory text

**DO provide:**
- ✅ Complete Python array named `candidates`
- ✅ Candidates 1-50 with ALL fields filled
- ✅ Each candidate must have: name, state, office, party, status, bio (200-300 words), faith_statement, website, positions (8 fields), endorsements

## CANDIDATES TO INCLUDE (1-50):

### Federal Candidates (1-20)
1-4. U.S. Senate candidates (Cory Booker + 3 challengers)
5-20. U.S. House candidates (2 per district for Districts 1-8)

### Gubernatorial Candidates (21-26)
21-26. Governor candidates (Ciattarelli, Sherrill, + 4 others)

### State Legislature Candidates (27-50)
27-50. Assembly candidates (2 per district for Districts 1-12)

## FORMAT:

```python
candidates = [
    {
        "name": "Cory Booker",
        "state": "New Jersey",
        "office": "U.S. Senate",
        "party": "Democrat",
        "status": "active",
        "bio": "[200-300 word biography with background, career, family, accomplishments]",
        "faith_statement": "[Actual faith statement OR 'No publicly disclosed faith statement']",
        "website": "https://www.booker.senate.gov",
        "positions": {
            "ABORTION": "[Detailed position with specifics]",
            "EDUCATION": "[School choice stance, parental rights position]",
            "RELIGIOUS-FREEDOM": "[Specific stance on religious liberty]",
            "GUNS": "[2nd Amendment position with specifics]",
            "TAXES": "[Tax policy position]",
            "IMMIGRATION": "[Border security/immigration stance]",
            "FAMILY-VALUES": "[Traditional marriage, parental rights, gender ideology stance]",
            "ELECTION-INTEGRITY": "[Voter ID, election security position]"
        },
        "endorsements": ["Organization 1", "Organization 2", "Organization 3"]
    },
    # CONTINUE FOR CANDIDATES 2-50
]
```

## CRITICAL REQUIREMENTS:

- ✅ Bio must be 200-300 words with REAL data from NJ.gov PDFs, Ballotpedia, LinkedIn
- ✅ All 8 position fields must be filled with detailed text (NOT generic statements)
- ✅ Research REAL candidates from official sources
- ✅ Include actual faith statements where available
- ✅ Include REAL endorsements from organizations
- ✅ NO abbreviations like "D" or "R" in bio or positions
- ✅ NO placeholders like "TBD" or "To be determined"
- ✅ Cite sources in bio (e.g., "per NJ.gov", "per Ballotpedia")
- ✅ EVERY candidate must be a complete dictionary - NO shortcuts

## VERIFICATION:

At the end, provide:
```
CANDIDATES 1-50 COMPLETE
Total: 50
- Federal: 20
- Governor: 6
- Legislature: 24
```

**START OUTPUT NOW - CANDIDATES 1-50 ONLY**
