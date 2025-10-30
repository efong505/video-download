"""
Generate election data chunk files for any US state.

USAGE:
    python generate_state_chunks.py --state "Pennsylvania" --tier "Large"
    python generate_state_chunks.py --state "Wyoming" --tier "Small"

TIERS:
    Large:  200+ candidates, 100+ races (PA, TX, FL, CA, NY, etc.)
    Medium: 120+ candidates, 60+ races (CO, KS, IA, etc.)
    Small:  70+ candidates, 35+ races (WY, VT, ND, etc.)
"""

import os
import argparse

# Tier configurations
TIER_CONFIG = {
    "Large": {
        "races_min": 100,
        "candidates_min": 200,
        "candidate_chunks": 20,  # 20 chunks × 10 candidates = 200
        "summary_words": [7000, 6000, 8000, 6500]  # 27,500 total
    },
    "Medium": {
        "races_min": 60,
        "candidates_min": 120,
        "candidate_chunks": 12,  # 12 chunks × 10 candidates = 120
        "summary_words": [5000, 4000, 5000, 4000]  # 18,000 total
    },
    "Small": {
        "races_min": 35,
        "candidates_min": 70,
        "candidate_chunks": 7,  # 7 chunks × 10 candidates = 70
        "summary_words": [3000, 2500, 3000, 2500]  # 11,000 total
    }
}

def generate_chunks(state_name, tier):
    """Generate all chunk files for a state."""
    
    config = TIER_CONFIG[tier]
    state_abbr = ''.join([word[0] for word in state_name.split()]).upper()
    
    # Create state directory
    state_dir = f"{state_abbr}_Election_Chunks"
    os.makedirs(state_dir, exist_ok=True)
    
    print(f"Generating chunks for {state_name} ({tier} tier)")
    print(f"Directory: {state_dir}/")
    print(f"Target: {config['races_min']}+ races, {config['candidates_min']}+ candidates\n")
    
    # Generate CHUNK_1_RACES.md
    generate_races_chunk(state_dir, state_name, config)
    
    # Generate candidate chunks (CHUNK_2A through CHUNK_2X)
    generate_candidate_chunks(state_dir, state_name, config)
    
    # Generate summary chunks (CHUNK_5A through CHUNK_5D)
    generate_summary_chunks(state_dir, state_name, config)
    
    # Generate combine script
    generate_combine_script(state_dir, state_name, state_abbr, config)
    
    # Generate HOW_TO_USE guide
    generate_how_to_guide(state_dir, state_name, state_abbr, config)
    
    print(f"\n Generated {1 + config['candidate_chunks'] + 4} chunk files")
    print(f" Created combine script and usage guide")
    print(f"\nNext steps:")
    print(f"1. cd {state_dir}")
    print(f"2. Run CHUNK_1_RACES.md through Grok, save as chunk1_output.txt")
    print(f"3. Run CHUNK_2A through CHUNK_2{chr(64 + config['candidate_chunks'])} through Grok")
    print(f"4. Run CHUNK_5A through CHUNK_5D through Grok")
    print(f"5. python combine_{state_abbr.lower()}_chunks.py")

def generate_races_chunk(state_dir, state_name, config):
    """Generate CHUNK_1_RACES.md"""
    
    content = f"""# CHUNK 1: {state_name} Races Array

Generate a Python list of dictionaries for ALL {state_name} 2025-2026 election races.

## MANDATORY REQUIREMENTS

### Research Mandate
- You MUST research real {state_name} elections using:
  - {state_name} Secretary of State website
  - Ballotpedia {state_name} elections page
  - {state_name} State Legislature website
  - Local county election boards
- CITE sources in descriptions: [{state_name}.gov election calendar, Ballotpedia]
- NO placeholders, NO generic text, NO "TBD"

### Race Count Target
- **MINIMUM {config['races_min']} races required**
- Include: Federal (Senate, House), Gubernatorial, State Legislature, School Boards, County offices

### Output Format
```python
races = [
    {{
        "state": "{state_name}",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent [Name] seeks re-election. [Real details from research]. (source: Ballotpedia, {state_name}.gov)"
    }},
    # ... continue for ALL {config['races_min']}+ races
]
```

### Race Categories to Include

1. **Federal Races**
   - U.S. Senate (if applicable in 2026)
   - U.S. House (all districts in {state_name})

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
-  Real election dates from {state_name} election calendar
-  Real descriptions with incumbent names and context
-  Cite sources in descriptions

### Output Requirements
- Start with: `races = [`
- End with: `]`
- Each race is a complete dictionary
- NO abbreviations in descriptions
- NO placeholders or "..."
- Minimum {config['races_min']} races

## BEGIN GENERATION
Research {state_name} 2025-2026 elections and generate the complete races array now.
"""
    
    with open(os.path.join(state_dir, "CHUNK_1_RACES.md"), 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f" Created CHUNK_1_RACES.md")

def generate_candidate_chunks(state_dir, state_name, config):
    """Generate CHUNK_2A through CHUNK_2X (10 candidates each)"""
    
    num_chunks = config['candidate_chunks']
    
    for i in range(num_chunks):
        chunk_letter = chr(65 + i)  # A, B, C, ...
        start_num = i * 10 + 1
        end_num = (i + 1) * 10
        
        content = f"""# CHUNK 2{chunk_letter}: {state_name} Candidates {start_num}-{end_num}

Generate 10 complete candidate profiles for {state_name} 2025-2026 elections.

## MANDATORY REQUIREMENTS

### Research Mandate
- Research REAL candidates from:
  - Ballotpedia {state_name} elections
  - {state_name} Secretary of State candidate filings
  - Campaign websites
  - LinkedIn profiles
  - Local news coverage
- CITE sources in bios: [Ballotpedia, campaign website, LinkedIn]
- NO fictional candidates, NO placeholders

### Candidate Selection (Candidates {start_num}-{end_num})
"""
        
        # Add candidate list based on position in sequence
        if i == 0:
            content += f"""1. U.S. Senate - Incumbent (if applicable)
2. U.S. Senate - Top challenger
3. U.S. House District 1 - Incumbent
4. U.S. House District 1 - Challenger
5. U.S. House District 2 - Incumbent
6. U.S. House District 2 - Challenger
7. Governor - Leading Democrat (if 2025 race)
8. Governor - Leading Republican (if 2025 race)
9. State Senate District 1 - Candidate 1
10. State Senate District 1 - Candidate 2
"""
        else:
            content += f"""Continue with next 10 candidates from:
- Remaining U.S. House districts
- State Legislature races
- School Board races (largest districts)
- County/local races

Prioritize: Federal > Gubernatorial > State Legislature > School Boards > Local
"""
        
        content += f"""
### Output Format
```python
{'' if i == 0 else '    # CONTINUE FROM CANDIDATE ' + str(start_num - 1) + ' WITH COMMA'}
    {{
        "name": "Full Legal Name",
        "state": "{state_name}",
        "office": "Exact Office Name (must match race)",
        "party": "Democrat/Republican/Independent/Nonpartisan",
        "status": "active",
        "bio": "200-300 word biography with real details, education, career, family, campaign focus. MUST cite sources. [Sources: Ballotpedia, campaign site, LinkedIn]",
        "faith_statement": "Direct quote or 'No publicly disclosed faith statement'",
        "website": "https://realcampaignwebsite.com or empty string",
        "positions": {{
            "ABORTION": "Detailed position (150+ words)",
            "EDUCATION": "Detailed position (150+ words)",
            "RELIGIOUS-FREEDOM": "Detailed position (150+ words)",
            "GUNS": "Detailed position (150+ words)",
            "TAXES": "Detailed position (150+ words)",
            "IMMIGRATION": "Detailed position (150+ words)",
            "FAMILY-VALUES": "Detailed position (150+ words)",
            "ELECTION-INTEGRITY": "Detailed position (150+ words)"
        }},
        "endorsements": ["Real Organization 1", "Real Organization 2", "Real Organization 3"]
    }}{',' if i < num_chunks - 1 else ''}
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
- Start with: `    {{` (4 spaces, opening brace)
- End with: `    }}{',' if i < num_chunks - 1 else ''}` (comma if not last chunk)
- NO array declaration (`candidates = [`)
- NO closing bracket (`]`)
- NO comments except continuation note
- Each candidate 200-300 words in bio
- Each position 150+ words

## BEGIN GENERATION
Research and generate 10 complete candidate profiles now.
"""
        
        filename = f"CHUNK_2{chunk_letter}_CANDIDATES_{start_num}-{end_num}.md"
        with open(os.path.join(state_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f" Created {filename}")

def generate_summary_chunks(state_dir, state_name, config):
    """Generate CHUNK_5A through CHUNK_5D"""
    
    parts = [
        ("A", "PART1", config['summary_words'][0], "Landscape, Federal Races, Top State Races"),
        ("B", "PART2", config['summary_words'][1], "State Legislature, School Boards"),
        ("C", "PART3", config['summary_words'][2], "County/Local Races, Priority Races"),
        ("D", "PART4", config['summary_words'][3], "Church Mobilization Strategy")
    ]
    
    for letter, part_name, word_count, section_desc in parts:
        content = f"""# CHUNK 5{letter}: {state_name} Summary {part_name}

Generate {word_count} words of the {state_name} 2025-2026 Election Voter Guide.

## MANDATORY REQUIREMENTS

### Content for This Part
{section_desc}

### Word Count
- **EXACTLY {word_count} words required**
- Count every word, no abbreviations

### Format Requirements
-  ALL emojis MUST be included: 📊 🔴 🎯 📅 🗳️ 📞 🔥 🙏
-  ALL checkmarks:  ❌
-  Markdown headers (##, ###)
-  Bold text for emphasis
-  Bullet points and numbered lists

### Content Structure

"""
        
        if letter == "A":
            content += f"""#### Part 1: Landscape + Federal Races ({word_count} words)

1. **Election Landscape** (1,500 words)
   - 📊 Overview of {state_name} 2025-2026 elections
   - 🔴 Political climate and key issues
   - 🎯 What's at stake for Christian conservatives
   - 📅 Critical dates and deadlines

2. **U.S. Senate Race** (if applicable - 2,000 words)
   - Full profiles of both major candidates
   - 200-300 word bios each
   - Christian conservative analysis (scoring 1-10)
   - Detailed position breakdowns
   - Why it matters section

3. **U.S. House Races** (remaining words)
   - All {state_name} congressional districts
   - Both major candidates per district
   - 150-200 words per candidate
   - Christian conservative scoring
   - Key positions on 8 issues
"""
        elif letter == "B":
            content += f"""#### Part 2: State Legislature + School Boards ({word_count} words)

1. **State Senate Races** (3,000 words)
   - Top 10-15 competitive races
   - Both candidates per race
   - Christian conservative analysis
   - Position summaries

2. **State House Races** (2,000 words)
   - Top 10-15 competitive races
   - Focus on districts with strong Christian conservative presence
   - Candidate profiles

3. **School Board Races** (remaining words)
   - Top 5-10 largest districts
   - Candidates fighting CRT, gender ideology, parental rights
   - Detailed education positions
"""
        elif letter == "C":
            content += f"""#### Part 3: County/Local + Priority Races ({word_count} words)

1. **County Races** (3,000 words)
   - Sheriffs, Commissioners, Prosecutors
   - Focus on law enforcement and public safety
   - Christian conservative priorities

2. **Priority Races** (3,000 words)
   - 🔥 TOP 10 RACES Christians Must Win
   - Detailed analysis of each
   - Why they matter
   - How to help

3. **Voter Guide Summary** (remaining words)
   - Quick reference tables
   - Endorsement lists
   - Resources for voters
"""
        else:  # D
            content += f"""#### Part 4: Church Mobilization Strategy ({word_count} words)

1. **🗳️ Church Mobilization Strategy** (2,500 words)
   - What Pastors Can Do (501c3 Compliant)
   - Distribute non-partisan voter guides
   - Host candidate forums
   - Preach on biblical citizenship
   - Organize voter registration drives

2. **📞 Action Steps for Believers** (2,000 words)
   - Register to vote (deadlines, links)
   - Request absentee ballot
   - Find your polling place
   - Volunteer for campaigns
   - Pray for candidates

3. **🙏 Prayer Points** (remaining words)
   - Specific prayers for {state_name}
   - Scripture-based intercession
   - 30-day prayer guide
   - Church prayer meeting resources
"""
        
        content += f"""
### Critical Rules
-  NO abbreviations (write out full words)
-  NO placeholders ("...", "[Continue]", "TBD")
-  Real candidate names and details
-  All emojis preserved
-  Markdown formatting maintained
-  Exactly {word_count} words

### Output Format
Pure markdown text, starting immediately with content (no code blocks, no "```markdown").

## BEGIN GENERATION
Write {word_count} words of the {state_name} voter guide now.
"""
        
        filename = f"CHUNK_5{letter}_SUMMARY_{part_name}.md"
        with open(os.path.join(state_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f" Created {filename}")

def generate_combine_script(state_dir, state_name, state_abbr, config):
    """Generate combine script for this state"""
    
    num_chunks = config['candidate_chunks']
    chunk_letters = [chr(65 + i).lower() for i in range(num_chunks)]
    
    content = f'''"""
Combine {state_name} election data chunks into single upload script.

USAGE:
1. Run each CHUNK file through Grok AI
2. Save Grok's output to text files:
   - chunk1_output.txt (races array)
   - chunk2a_output.txt through chunk2{chunk_letters[-1]}_output.txt (candidates 1-{config['candidates_min']}, 10 per file)
   - chunk5a_output.txt through chunk5d_output.txt (summary parts 1-4)
3. Run: python combine_{state_abbr.lower()}_chunks.py
"""

import os

def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(filepath):
        print(f"WARNING: {{filename}} not found - skipping")
        return ""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

print("Reading chunk outputs...")

# Read races
races_content = read_file('chunk1_output.txt')

# Read candidates (combine all {num_chunks} parts - 10 candidates each)
candidates_parts = []
for letter in {chunk_letters}:
    content = read_file(f'chunk2{{letter}}_output.txt')
    if content:
        candidates_parts.append(content.strip())

# Read summary (combine all 4 parts)
summary_part1 = read_file('chunk5a_output.txt')
summary_part2 = read_file('chunk5b_output.txt')
summary_part3 = read_file('chunk5c_output.txt')
summary_part4 = read_file('chunk5d_output.txt')

# Combine summary
full_summary = summary_part1 + "\\n\\n" + summary_part2 + "\\n\\n" + summary_part3 + "\\n\\n" + summary_part4

# Create final script (build without f-string to avoid backslash issues)
script_template = \'\'\'import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# {state_name} Races
{{{{RACES_CONTENT}}}}

# {state_name} Candidates
candidates = [
{{{{CANDIDATES_CONTENT}}}}
]

# {state_name} Summary
summary = {{
    "state": "{state_name}",
    "title": "{state_name} 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """{{{{SUMMARY_CONTENT}}}}""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing {state_name} races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={{'#s': 'state'}},
    ExpressionAttributeValues={{':state': '{state_name}'}}
)['Items']
existing_race_map = {{r['office']: r['race_id'] for r in existing_races}}
print(f"Found {{len(existing_races)}} existing races")

print(f"\\nProcessing {{len(races)}} {state_name} races...")
race_ids = {{}}
for race in races:
    office = race['office']
    if office in existing_race_map:
        race_id = existing_race_map[office]
        race['race_id'] = race_id
        race['updated_at'] = datetime.now().isoformat()
        races_table.put_item(Item=race)
        print(f"  Updated: {{office}}")
    else:
        race_id = str(uuid.uuid4())
        race['race_id'] = race_id
        race['created_at'] = datetime.now().isoformat()
        race['created_by'] = 'system'
        races_table.put_item(Item=race)
        print(f"  Created: {{office}}")
    race_ids[office] = race_id
print(f"\\n[SUCCESS] Processed {{len(races)}} races")

print(f"\\nChecking for existing {state_name} candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={{'#s': 'state'}},
    ExpressionAttributeValues={{':state': '{state_name}'}}
)['Items']
existing_candidate_map = {{(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}}
print(f"Found {{len(existing_candidates)}} existing candidates")

print(f"\\nProcessing {{len(candidates)}} {state_name} candidates...")
for candidate in candidates:
    name = candidate['name']
    office = candidate['office']
    key = (name, office)
    if office in race_ids:
        candidate['race_id'] = race_ids[office]
    else:
        candidate['race_id'] = ''
    if key in existing_candidate_map:
        candidate_id = existing_candidate_map[key]
        candidate['candidate_id'] = candidate_id
        candidate['updated_at'] = datetime.now().isoformat()
        candidate['status'] = 'active'
        candidates_table.put_item(Item=candidate)
        print(f"  Updated: {{name}} - {{office}}")
    else:
        candidate_id = str(uuid.uuid4())
        candidate['candidate_id'] = candidate_id
        candidate['created_at'] = datetime.now().isoformat()
        candidate['created_by'] = 'system'
        candidate['status'] = 'active'
        candidates_table.put_item(Item=candidate)
        print(f"  Created: {{name}} - {{office}}")
print(f"\\n[SUCCESS] Processed {{len(candidates)}} candidates")

print("\\nProcessing {state_name} summary...")
try:
    existing_summary = summaries_table.get_item(Key={{'state': '{state_name}'}})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {{len(summary['content']):,}} chars")
print("\\n[SUCCESS] {state_name} data upload complete!")
\'\'\'

# Replace placeholders
final_script = script_template.replace('{{{{RACES_CONTENT}}}}', races_content)
final_script = final_script.replace('{{{{CANDIDATES_CONTENT}}}}', ',\\n'.join(candidates_parts))
final_script = final_script.replace('{{{{SUMMARY_CONTENT}}}}', full_summary)

# Write final script
output_file = os.path.join(os.path.dirname(__file__), 'upload_{state_abbr.lower()}_data.py')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(final_script)

print(f"\\nSUCCESS! Created: {{output_file}}")
print(f"\\nNext steps:")
print(f"1. Review the file")
print(f"2. Run: python upload_{state_abbr.lower()}_data.py")
'''
    
    with open(os.path.join(state_dir, f"combine_{state_abbr.lower()}_chunks.py"), 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f" Created combine_{state_abbr.lower()}_chunks.py")

def generate_how_to_guide(state_dir, state_name, state_abbr, config):
    """Generate HOW_TO_USE guide"""
    
    num_chunks = config['candidate_chunks']
    
    content = f"""# How to Use {state_name} Election Chunks

## Overview
This directory contains {1 + num_chunks + 4} chunk files to generate complete {state_name} 2025-2026 election data.

**Target Output:**
- {config['races_min']}+ races
- {config['candidates_min']}+ candidates
- {sum(config['summary_words']):,} word voter guide

## Step-by-Step Process

### Step 1: Generate Races (5 minutes)
1. Open `CHUNK_1_RACES.md`
2. Copy entire content
3. Paste into Grok AI
4. Save Grok's output as `chunk1_output.txt`
5. Verify it starts with `races = [` and ends with `]`

### Step 2: Generate Candidates ({num_chunks} sessions, ~{num_chunks * 5} minutes)
For each chunk from 2A to 2{chr(64 + num_chunks)}:
1. Open `CHUNK_2A_CANDIDATES_1-10.md`
2. Copy entire content
3. Paste into Grok AI
4. Save output as `chunk2a_output.txt`
5. Verify it starts with `    {{` and ends with `    }},` (or `    }}` for last chunk)
6. Repeat for chunks 2B through 2{chr(64 + num_chunks)}

**IMPORTANT:** 
- Save as `chunk2a_output.txt` (lowercase letter, underscore)
- First chunk should NOT have `candidates = [`
- Last chunk should NOT have `]`
- No comment lines like `# CONTINUE FROM...`

### Step 3: Generate Summary (4 sessions, ~20 minutes)
For each summary chunk:
1. Open `CHUNK_5A_SUMMARY_PART1.md`
2. Copy entire content
3. Paste into Grok AI
4. Save output as `chunk5a_output.txt`
5. Verify emojis are preserved (📊 🔴 🎯 📅 🗳️ 📞 🔥 🙏)
6. Repeat for chunks 5B, 5C, 5D

### Step 4: Fix Common Issues (2 minutes)
Run the fix script to handle HTML entities:
```bash
python ../fix_html_entities.py
```

This decodes any `&quot;` to `"` and other HTML entities.

### Step 5: Combine All Chunks (1 minute)
```bash
python combine_{state_abbr.lower()}_chunks.py
```

This creates `upload_{state_abbr.lower()}_data.py` with all data merged.

### Step 6: Upload to Database (2 minutes)
```bash
python upload_{state_abbr.lower()}_data.py
```

This uploads races, candidates, and summary to DynamoDB.

## Troubleshooting

### Problem: "chunk2X_output.txt not found"
**Solution:** Check filename - should be `chunk2a_output.txt` (lowercase, underscore)

### Problem: "SyntaxError: unterminated string literal"
**Solution:** Run `python ../fix_html_entities.py` to fix encoding

### Problem: "SyntaxError: unmatched ']'"
**Solution:** Last candidate chunk should end with `}}` not `}}]`

### Problem: Candidates in "Other Candidates" section
**Solution:** Run fix scripts:
```bash
python ../smart_fix_race_ids.py
python ../fix_orphaned_candidates.py
```

## Quality Checklist

Before uploading, verify:
- [ ] chunk1_output.txt has {config['races_min']}+ races
- [ ] All {num_chunks} candidate chunks saved (chunk2a through chunk2{chr(64 + num_chunks).lower()})
- [ ] All 4 summary chunks saved (chunk5a through chunk5d)
- [ ] No HTML entities (`&quot;`, `&amp;`, etc.)
- [ ] No placeholders ("...", "[Continue]", "TBD")
- [ ] All emojis preserved in summary
- [ ] combine script runs without errors
- [ ] upload script completes successfully

## File Checklist

Input files (create these):
- [ ] chunk1_output.txt
- [ ] chunk2a_output.txt through chunk2{chr(64 + num_chunks).lower()}_output.txt ({num_chunks} files)
- [ ] chunk5a_output.txt through chunk5d_output.txt (4 files)

Output files (auto-generated):
- [ ] upload_{state_abbr.lower()}_data.py
- [ ] Database records in DynamoDB

## Time Estimate

- Chunk generation: {5 + num_chunks * 5 + 20} minutes
- Fixing issues: 5 minutes
- Combining & uploading: 5 minutes
- **Total: ~{5 + num_chunks * 5 + 30} minutes**

## Need Help?

See `../TROUBLESHOOTING.md` for detailed solutions to common problems.
"""
    
    with open(os.path.join(state_dir, "HOW_TO_USE.md"), 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f" Created HOW_TO_USE.md")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate election data chunks for a US state")
    parser.add_argument("--state", required=True, help="State name (e.g., 'Pennsylvania')")
    parser.add_argument("--tier", required=True, choices=["Large", "Medium", "Small"], 
                       help="State tier based on population/races")
    
    args = parser.parse_args()
    
    generate_chunks(args.state, args.tier)

