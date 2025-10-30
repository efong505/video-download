"""Generate all remaining candidate chunk files (2F through 2O)"""

# All 150 candidates organized by chunk
all_chunks = {
    "2F": [(51, "Nilsa I. Cruz-Perez", "D", "General Assembly District 5 Seat 2"),
           (52, "John M. Brangan", "R", "General Assembly District 5"),
           (53, "Pamela R. Lampitt", "D", "General Assembly District 6 Seat 1"),
           (54, "Carol Murphy", "D", "General Assembly District 6 Seat 2"),
           (55, "Dione Johnson", "R", "General Assembly District 6"),
           (56, "Herb Conaway", "D", "General Assembly District 7 Seat 1"),
           (57, "Andrea Katz", "D", "General Assembly District 7 Seat 2"),
           (58, "Michael Torrissi Jr.", "R", "General Assembly District 7"),
           (59, "Brian E. Rumpf", "R", "General Assembly District 8 Seat 1"),
           (60, "Lisa Bennett", "D", "General Assembly District 8 Seat 1")],
    
    "2G": [(61, "Greg Myhre", "R", "General Assembly District 8 Seat 2"),
           (62, "Janine G. Bauer", "D", "General Assembly District 8 Seat 2"),
           (63, "Paul Kanitra", "R", "General Assembly District 9 Seat 1"),
           (64, "John Catalano", "R", "General Assembly District 9 Seat 2"),
           (65, "Gregory P. McGuckin", "R", "General Assembly District 9"),
           (66, "Margie Donlon", "D", "General Assembly District 10 Seat 1"),
           (67, "Luanne M. Peterpaul", "D", "General Assembly District 10 Seat 2"),
           (68, "Margaret M. Donlon", "D", "General Assembly District 10"),
           (69, "Andrew C. Wardell", "R", "General Assembly District 10"),
           (70, "Kyler Dineen", "R", "General Assembly District 10")],
    
    "2H": [(71, "Robert D. Clifton", "R", "General Assembly District 11 Seat 1"),
           (72, "Alex Sauickie", "R", "General Assembly District 11 Seat 2"),
           (73, "Victoria A. Flynn", "R", "General Assembly District 12 Seat 1"),
           (74, "Gerard P. Scharfenberger", "R", "General Assembly District 12 Seat 2"),
           (75, "Wayne P. DeAngelo", "D", "General Assembly District 13 Seat 1"),
           (76, "Tennille R. McCoy", "D", "General Assembly District 13 Seat 2"),
           (77, "Verlina Reynolds-Jackson", "D", "General Assembly District 14 Seat 1"),
           (78, "Anthony S. Verrelli", "D", "General Assembly District 14 Seat 2"),
           (79, "Roy Freiman", "D", "General Assembly District 15 Seat 1"),
           (80, "Mitchelle Drulis", "D", "General Assembly District 15 Seat 2")],
    
    "2I": [(81, "Joseph Danielsen", "D", "General Assembly District 16 Seat 1"),
           (82, "Kevin Egan", "D", "General Assembly District 16 Seat 2"),
           (83, "Sterley Stanley", "D", "General Assembly District 17 Seat 1"),
           (84, "Robert Karabinchak", "D", "General Assembly District 17 Seat 2"),
           (85, "Craig Coughlin", "D", "General Assembly District 18 Seat 1"),
           (86, "Yvonne Lopez", "D", "General Assembly District 18 Seat 2"),
           (87, "Annette Quijano", "D", "General Assembly District 19 Seat 1"),
           (88, "Reginald W. Atkins", "D", "General Assembly District 19 Seat 2"),
           (89, "Nancy Munoz", "R", "General Assembly District 20 Seat 1"),
           (90, "Michele Matsikoudis", "R", "General Assembly District 20 Seat 2")],
    
    "2J": [(91, "Linda S. Carter", "D", "General Assembly District 21 Seat 1"),
           (92, "James J. Kennedy", "D", "General Assembly District 21 Seat 2"),
           (93, "John DiMaio", "R", "General Assembly District 22 Seat 1"),
           (94, "Erik Peterson", "R", "General Assembly District 22 Seat 2"),
           (95, "Parker Space", "R", "General Assembly District 23 Seat 1"),
           (96, "Dawn Fantasia", "R", "General Assembly District 23 Seat 2"),
           (97, "Christian E. Barranco", "R", "General Assembly District 24 Seat 1"),
           (98, "Aura K. Dunn", "R", "General Assembly District 24 Seat 2"),
           (99, "Brian Bergen", "R", "General Assembly District 25 Seat 1"),
           (100, "Jay Webber", "R", "General Assembly District 25 Seat 2")],
    
    "2K": [(101, "A'Dorian Murray-Thomas", "Nonpartisan", "Newark Board of Education At-Large Seat 1"),
           (102, "Kanileah Anderson", "Nonpartisan", "Newark Board of Education At-Large Seat 2"),
           (103, "Louis Maisonave Jr.", "Nonpartisan", "Newark Board of Education At-Large Seat 3"),
           (104, "Afaf Muhammad", "Nonpartisan", "Jersey City Board of Education Ward A"),
           (105, "Natalia Ioffe", "Nonpartisan", "Jersey City Board of Education Ward B"),
           (106, "Paula Jones", "Nonpartisan", "Jersey City Board of Education Ward C"),
           (107, "Eddie Gonzalez", "Nonpartisan", "Paterson Board of Education At-Large Seat 1"),
           (108, "Alex Mendez Jr.", "Nonpartisan", "Paterson Board of Education At-Large Seat 2"),
           (109, "Manny Martinez", "Nonpartisan", "Paterson Board of Education At-Large Seat 3"),
           (110, "Maria Richardson", "Nonpartisan", "Elizabeth Board of Education At-Large Seat 1")],
    
    "2L": [(111, "Carlos Cedeño", "Nonpartisan", "Elizabeth Board of Education At-Large Seat 2"),
           (112, "Charlene Bathelus", "Nonpartisan", "Elizabeth Board of Education At-Large Seat 3"),
           (113, "Jerry Shi", "Nonpartisan", "Edison Board of Education At-Large Seat 1"),
           (114, "Biral Patel", "Nonpartisan", "Edison Board of Education At-Large Seat 2"),
           (115, "Theresa Ward", "Nonpartisan", "Edison Board of Education At-Large Seat 3"),
           (116, "Kimberly Palmieri", "Nonpartisan", "Woodbridge Board of Education At-Large Seat 1"),
           (117, "Brian Small", "Nonpartisan", "Woodbridge Board of Education At-Large Seat 2"),
           (118, "Debbie Bayer", "Nonpartisan", "Woodbridge Board of Education At-Large Seat 3"),
           (119, "Wasim Muhammad", "Nonpartisan", "Camden Board of Education At-Large Seat 1"),
           (120, "Kathryn Blackshear", "Nonpartisan", "Camden Board of Education At-Large Seat 2")],
    
    "2M": [(121, "Tawanda Jones", "Nonpartisan", "Camden Board of Education At-Large Seat 3"),
           (122, "Robin Hill", "Nonpartisan", "Trenton Board of Education At-Large Seat 1"),
           (123, "Tonya McRae", "Nonpartisan", "Trenton Board of Education At-Large Seat 2"),
           (124, "Patrick Murray", "Nonpartisan", "Trenton Board of Education At-Large Seat 3"),
           (125, "Mary Sadrakula", "Nonpartisan", "Clifton Board of Education At-Large Seat 1"),
           (126, "Tina Nega", "Nonpartisan", "Clifton Board of Education At-Large Seat 2"),
           (127, "Vincent Sasso", "Nonpartisan", "Clifton Board of Education At-Large Seat 3"),
           (128, "Kenneth Simmons", "Nonpartisan", "Passaic Board of Education At-Large Seat 1"),
           (129, "Javier Fresse", "Nonpartisan", "Passaic Board of Education At-Large Seat 2"),
           (130, "Alicia D'Alessio", "Nonpartisan", "Passaic Board of Education At-Large Seat 3")],
    
    "2N": [(131, "Mussab Ali", "Nonpartisan", "Union City Board of Education At-Large Seat 1"),
           (132, "Wendy Grullon", "Nonpartisan", "Union City Board of Education At-Large Seat 2"),
           (133, "Silvia Rodriguez", "Nonpartisan", "Union City Board of Education At-Large Seat 3"),
           (134, "Maria Valado", "Nonpartisan", "Bayonne Board of Education At-Large Seat 1"),
           (135, "Dennis Jasinski", "Nonpartisan", "Bayonne Board of Education At-Large Seat 2"),
           (136, "Jodi Casais", "Nonpartisan", "Bayonne Board of Education At-Large Seat 3"),
           (137, "Christopher Cerf", "Nonpartisan", "Newark Board of Education (State-Appointed)"),
           (138, "Josephine Garcia", "Nonpartisan", "East Orange Board of Education At-Large Seat 1"),
           (139, "Tyrone Tarver", "Nonpartisan", "East Orange Board of Education At-Large Seat 2"),
           (140, "Casimiro Neto", "Nonpartisan", "East Orange Board of Education At-Large Seat 3")],
    
    "2O": [(141, "Fernando Gonzalez", "Nonpartisan", "Vineland Board of Education At-Large Seat 1"),
           (142, "Denise Troiano", "Nonpartisan", "Vineland Board of Education At-Large Seat 2"),
           (143, "Yusuf Abdul-Karim", "Nonpartisan", "Vineland Board of Education At-Large Seat 3"),
           (144, "Leslie Ramos", "Nonpartisan", "New Brunswick Board of Education At-Large Seat 1"),
           (145, "Hector Colon", "Nonpartisan", "New Brunswick Board of Education At-Large Seat 2"),
           (146, "Yolanda Jauregui", "Nonpartisan", "New Brunswick Board of Education At-Large Seat 3"),
           (147, "Armando Virguez", "Nonpartisan", "Perth Amboy Board of Education At-Large Seat 1"),
           (148, "Janine Walker", "Nonpartisan", "Perth Amboy Board of Education At-Large Seat 2"),
           (149, "Kenneth Armwood", "Nonpartisan", "Plainfield Board of Education At-Large Seat 1"),
           (150, "Emily Morgan", "Nonpartisan", "Plainfield Board of Education At-Large Seat 2")],
}

template = """# CHUNK {chunk_id}: NEW JERSEY CANDIDATES {start}-{end}

## TASK: Provide EXACTLY 10 candidates ({start}-{end}) - NO MORE, NO LESS

**CRITICAL: Write ALL 10 candidates COMPLETELY. Start with comma after candidate {prev}.**

## CANDIDATES {start}-{end}:

{candidate_list}

## FORMAT:

```python
    # CONTINUE FROM CANDIDATE {prev} WITH COMMA
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
            "ABORTION": "{abortion_note}",
            "EDUCATION": "[Detailed - REQUIRED]",
            "RELIGIOUS-FREEDOM": "{rf_note}",
            "GUNS": "{guns_note}",
            "TAXES": "{taxes_note}",
            "IMMIGRATION": "{immigration_note}",
            "FAMILY-VALUES": "[Detailed - REQUIRED]",
            "ELECTION-INTEGRITY": "{ei_note}"
        }},
        "endorsements": ["Org 1", "Org 2", "Org 3"]
    }},
    # WRITE CANDIDATES {next_start}-{end}
{array_end}
```

{school_board_note}

**START OUTPUT NOW - WRITE ALL 10 CANDIDATES COMPLETELY**
"""

for chunk_id, candidates in all_chunks.items():
    start = candidates[0][0]
    end = candidates[-1][0]
    prev = start - 1
    
    candidate_list = "\n".join([
        f"{num}. {name} ({party}) - {office}"
        for num, name, party, office in candidates
    ])
    
    first_num, first_name, first_party, first_office = candidates[0]
    
    # Check if school board candidates
    is_school_board = "Board of Education" in first_office
    
    if is_school_board:
        abortion_note = "N/A for school board role"
        rf_note = "N/A for school board role"
        guns_note = "N/A for school board role"
        taxes_note = "N/A for school board role"
        immigration_note = "N/A for school board role"
        ei_note = "N/A for school board role"
        school_board_note = """
## SCHOOL BOARD NOTE:
For positions not relevant to school boards (ABORTION, GUNS, IMMIGRATION, etc.), write "N/A for school board role"
EDUCATION and FAMILY-VALUES are MANDATORY and must be detailed (parental rights, curriculum transparency, CRT, gender ideology)
"""
    else:
        abortion_note = "[Detailed]"
        rf_note = "[Detailed]"
        guns_note = "[Detailed]"
        taxes_note = "[Detailed]"
        immigration_note = "[Detailed]"
        ei_note = "[Detailed]"
        school_board_note = ""
    
    array_end = "]" if end == 150 else ""
    next_start = start + 1
    
    content = template.format(
        chunk_id=chunk_id,
        start=start,
        end=end,
        prev=prev,
        candidate_list=candidate_list,
        first_name=first_name,
        first_office=first_office,
        first_party=first_party,
        next_start=next_start,
        array_end=array_end,
        abortion_note=abortion_note,
        rf_note=rf_note,
        guns_note=guns_note,
        taxes_note=taxes_note,
        immigration_note=immigration_note,
        ei_note=ei_note,
        school_board_note=school_board_note
    )
    
    filename = f"CHUNK_{chunk_id}_CANDIDATES_{start}-{end}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created {filename}")

print(f"\nSUCCESS! Created all 10 remaining chunk files (2F through 2O)")
print(f"\nYou now have 15 total chunks:")
print(f"  CHUNK_2A (1-10)")
print(f"  CHUNK_2B (11-20)")
print(f"  CHUNK_2C (21-30)")
print(f"  CHUNK_2D (31-40)")
print(f"  CHUNK_2E (41-50)")
print(f"  CHUNK_2F (51-60)")
print(f"  CHUNK_2G (61-70)")
print(f"  CHUNK_2H (71-80)")
print(f"  CHUNK_2I (81-90)")
print(f"  CHUNK_2J (91-100)")
print(f"  CHUNK_2K (101-110)")
print(f"  CHUNK_2L (111-120)")
print(f"  CHUNK_2M (121-130)")
print(f"  CHUNK_2N (131-140)")
print(f"  CHUNK_2O (141-150)")
