"""
Generate all 15 candidate chunk files (10 candidates each)
"""

chunks = [
    # Chunk 2C: Candidates 21-30
    {
        "file": "CHUNK_2C_CANDIDATES_21-30.md",
        "start": 21,
        "end": 30,
        "candidates": [
            ("Bill Pascrell", "D", "U.S. House District 9"),
            ("Billy Prempeh", "R", "U.S. House District 9"),
            ("Donald Payne Jr.", "D", "U.S. House District 10"),
            ("Carmen Bucco", "R", "U.S. House District 10"),
            ("Mikie Sherrill", "D", "U.S. House District 11"),
            ("Joseph Belnome", "R", "U.S. House District 11"),
            ("Bonnie Watson Coleman", "D", "U.S. House District 12"),
            ("Darius Mayfield", "R", "U.S. House District 12"),
            ("Jack Ciattarelli", "R", "Governor"),
            ("Mikie Sherrill", "D", "Governor"),
        ]
    },
    # Chunk 2D: Candidates 31-40
    {
        "file": "CHUNK_2D_CANDIDATES_31-40.md",
        "start": 31,
        "end": 40,
        "candidates": [
            ("Ras Baraka", "D", "Governor"),
            ("Steve Fulop", "D", "Governor"),
            ("Bill Spadea", "R", "Governor"),
            ("Jon Bramnick", "R", "Governor"),
            ("Erik K. Simonsen", "R", "General Assembly District 1 Seat 1"),
            ("Carolyn Rush", "D", "General Assembly District 1 Seat 1"),
            ("Antwan McClellan", "R", "General Assembly District 1 Seat 2"),
            ("Maureen Rowan", "D", "General Assembly District 1 Seat 2"),
            ("Don Guardian", "R", "General Assembly District 2 Seat 1"),
            ("Heather Simmons", "D", "General Assembly District 2 Seat 1"),
        ]
    },
    # Chunk 2E: Candidates 41-50
    {
        "file": "CHUNK_2E_CANDIDATES_41-50.md",
        "start": 41,
        "end": 50,
        "candidates": [
            ("Claire Swift", "R", "General Assembly District 2 Seat 2"),
            ("Chris Konawel", "D", "General Assembly District 2 Seat 2"),
            ("Dave Bailey Jr.", "D", "General Assembly District 3 Seat 1"),
            ("Dan Hutchison", "D", "General Assembly District 3 Seat 1"),
            ("Bethanne McCarthy Patrick", "R", "General Assembly District 3 Seat 2"),
            ("Amanda Esposito", "R", "General Assembly District 3 Seat 2"),
            ("William F. Moen Jr.", "D", "General Assembly District 4 Seat 1"),
            ("Cody D. Miller", "D", "General Assembly District 4 Seat 2"),
            ("Constance Ditzel", "R", "General Assembly District 4"),
            ("Louis D. Greenwald", "D", "General Assembly District 5 Seat 1"),
        ]
    },
    # Add more chunks as needed...
]

template = """# CHUNK {chunk_id}: NEW JERSEY CANDIDATES {start}-{end}

## TASK: Provide EXACTLY 10 candidates ({start}-{end}) - NO MORE, NO LESS

**CRITICAL: Write ALL 10 candidates COMPLETELY. {continuation}**

## CANDIDATES {start}-{end}:

{candidate_list}

## FORMAT:

```python
{array_start}
    {{
        "name": "{first_name}",
        "state": "New Jersey",
        "office": "{first_office}",
        "party": "{first_party}",
        "status": "active",
        "bio": "[200-300 words from Ballotpedia/official sources]",
        "faith_statement": "[Statement OR 'No publicly disclosed faith statement']",
        "website": "",
        "positions": {{
            "ABORTION": "[Detailed]",
            "EDUCATION": "[Detailed]",
            "RELIGIOUS-FREEDOM": "[Detailed]",
            "GUNS": "[Detailed]",
            "TAXES": "[Detailed]",
            "IMMIGRATION": "[Detailed]",
            "FAMILY-VALUES": "[Detailed]",
            "ELECTION-INTEGRITY": "[Detailed]"
        }},
        "endorsements": ["Org 1", "Org 2", "Org 3"]
    }},
    # WRITE CANDIDATES {next_start}-{end}
{array_end}
```

**START OUTPUT NOW - WRITE ALL 10 CANDIDATES COMPLETELY**
"""

for chunk in chunks:
    start = chunk["start"]
    end = chunk["end"]
    chunk_id = f"2{chr(65 + (start-21)//10)}"  # 2C, 2D, 2E, etc.
    
    candidate_list = "\n".join([
        f"{i}. {name} ({party}) - {office}"
        for i, (name, party, office) in enumerate(chunk["candidates"], start=start)
    ])
    
    first_name, first_party, first_office = chunk["candidates"][0]
    
    continuation = "Start with comma after previous candidate." if start > 10 else ""
    array_start = "    # CONTINUE FROM PREVIOUS WITH COMMA" if start > 10 else "candidates = ["
    array_end = "]" if end == 150 else ""
    next_start = start + 1
    
    content = template.format(
        chunk_id=chunk_id,
        start=start,
        end=end,
        continuation=continuation,
        candidate_list=candidate_list,
        array_start=array_start,
        first_name=first_name,
        first_office=first_office,
        first_party=first_party,
        next_start=next_start,
        array_end=array_end
    )
    
    with open(chunk["file"], 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created {chunk['file']}")

print("\nDone! Created 3 chunk files (2C, 2D, 2E)")
print("Run this script again after adding more chunks to the list")
