# Complete Template System for All 50 States

## Overview
This directory contains a comprehensive template generation system for creating consistent, high-quality election data across all 50 US states.

## Directory Structure

### COMPLETE_STATE_TEMPLATES/
Contains complete template sets for all 50 states (950 total files):
- **Alabama/** through **Wyoming/** - 50 state folders
- Each state has 15-25 template files depending on size
- Templates include: CHUNK_1, CHUNK_2A-2T, CHUNK_5A-5D

### Generation Scripts
- **generate_complete_template_system.py** - Master script that generates all templates
- **generate_state_chunks.py** - Earlier version (CHUNK_5A only)
- **generate_all_chunk_templates.py** - Intermediate version

### Reference Templates
- **NJ_Election_Chunks/** - New Jersey templates (detailed reference implementation)
- **P_Election_Chunks/** - Pennsylvania templates (comparison)
- **STATE_TEMPLATES/** - Individual CHUNK_5A templates for all 50 states

## Template Types

### CHUNK_1: Races Array
- Complete Python array of all races for the state
- Includes: state, office, election_date, race_type, description
- State-specific race counts based on congressional districts

### CHUNK_2A-2T: Candidate Arrays
- 10 candidates per chunk (flexible with "UP TO" language)
- Each candidate: name, state, office, party, bio, faith_statement, positions, endorsements
- Number of chunks varies by state size (15-25 total files)

### CHUNK_5A-5D: Summary Parts
- **CHUNK_5A**: Database Summary, Political Landscape, Federal Races, State Races, School Boards, Municipal
- **CHUNK_5B**: County Elections, Key Issues (8 focus areas), Church Mobilization
- **CHUNK_5C**: Critical Dates, Resources, Bottom Line
- **CHUNK_5D**: Prayer Points with scripture verses

## State Size Scaling

### Large States (20+ Congressional Districts)
- **Examples**: California (52), Texas (38), Florida (28), New York (26)
- **Template Files**: 25 files (CHUNK_1 + CHUNK_2A-2T + CHUNK_5A-5D)
- **Candidate Capacity**: UP TO 200 candidates
- **Summary Length**: 17,000+ words

### Medium States (10-19 Congressional Districts)
- **Examples**: Pennsylvania (17), Illinois (17), Ohio (15), Michigan (13)
- **Template Files**: 20 files (CHUNK_1 + CHUNK_2A-2O + CHUNK_5A-5D)
- **Candidate Capacity**: UP TO 150 candidates
- **Summary Length**: 14,000+ words

### Small States (<10 Congressional Districts)
- **Examples**: Wyoming (1), Vermont (1), Delaware (1), Montana (2)
- **Template Files**: 15 files (CHUNK_1 + CHUNK_2A-2J + CHUNK_5A-5D)
- **Candidate Capacity**: UP TO 100 candidates
- **Summary Length**: 11,000+ words

## Key Features

### Flexible Candidate Counts
- Templates use "UP TO X candidates" instead of "EXACTLY X"
- Prevents AI from generating fake candidates to meet quotas
- Handles states with fewer viable candidates gracefully
- Verification sections track actual counts provided

### Consistent Structure
- All templates based on New Jersey's proven detailed structure
- Comprehensive formatting with Database Summary sections
- Anti-abbreviation rules prevent incomplete output
- Explicit instructions for complete candidate arrays

### Quality Control
- Verification sections in each template
- Actual count tracking vs. expected counts
- Source citation requirements (Ballotpedia, state.gov)
- Faith statement and position requirements

## Usage Workflow

### Step 1: Select State Template
Navigate to `COMPLETE_STATE_TEMPLATES/[State_Name]/`

### Step 2: Use Templates with AI
Upload templates to AI (Grok, Claude, ChatGPT) in sequence:
1. CHUNK_1_RACES.md → Generate races array
2. CHUNK_2A_CANDIDATES_1-10.md → Generate first 10 candidates
3. Continue with CHUNK_2B, 2C, etc. → Generate remaining candidates
4. CHUNK_5A-5D → Generate comprehensive summary in 4 parts

### Step 3: Combine Output
**Process**: Use the combine script to automatically merge all chunk outputs

1. **Save AI outputs to text files**:
   - `chunk1_output.txt` - Races array from CHUNK_1
   - `chunk2a_output.txt` through `chunk2t_output.txt` - Candidates (10 per file)
   - `chunk5a_output.txt` through `chunk5d_output.txt` - Summary parts

2. **Create combine script** (copy from `NJ_Election_Chunks/combine_nj_chunks.py`):
   ```python
   import os
   
   # Read chunk outputs
   races_content = open('chunk1_output.txt').read()
   
   # Combine candidates (adjust letters based on state size)
   candidates_parts = []
   for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']:
       candidates_parts.append(open(f'chunk2{letter}_output.txt').read())
   
   # Combine summary
   summary = open('chunk5a_output.txt').read() + "\n\n" + \
             open('chunk5b_output.txt').read() + "\n\n" + \
             open('chunk5c_output.txt').read() + "\n\n" + \
             open('chunk5d_output.txt').read()
   
   # Generate upload_[state]_data.py with duplicate-safe code
   ```

3. **Run combine script**: `python combine_[state]_chunks.py`
   - Generates `upload_[state]_data.py` with all data merged
   - Includes duplicate-safe upload logic
   - Ready to run immediately

### Step 4: Upload to Database
Run upload script to populate DynamoDB with races, candidates, and summary.

## Template Improvements Over Previous Versions

### Pennsylvania vs New Jersey Comparison
**Problem**: Pennsylvania templates were simpler and less detailed than New Jersey
**Solution**: All 50 states now use New Jersey's comprehensive structure

### Key Enhancements
1. **Database Summary Section**: Added to all CHUNK_5A templates
2. **Detailed Candidate Templates**: Specific examples and formatting
3. **Comprehensive Summary Structure**: All 8 key issues with Biblical foundations
4. **Anti-Abbreviation Rules**: Explicit instructions against shortcuts
5. **Verification Sections**: Track actual vs. expected counts

## File Counts by State

### Large States (25 files each)
California, Texas, Florida, New York, Pennsylvania, Illinois, Ohio, Georgia, North Carolina, Michigan

### Medium States (20 files each)
New Jersey, Virginia, Washington, Arizona, Massachusetts, Tennessee, Indiana, Missouri, Maryland, Wisconsin, Colorado, Minnesota, Alabama, South Carolina, Louisiana, Kentucky, Oregon, Oklahoma, Connecticut, Utah, Iowa, Nevada, Arkansas, Mississippi, Kansas, New Mexico, Nebraska, West Virginia, Idaho, Hawaii, New Hampshire, Maine, Montana, Rhode Island, Delaware, South Dakota, North Dakota, Alaska, Vermont, Wyoming

### Small States (15 files each)
Wyoming, Vermont, Delaware, Montana, South Dakota, North Dakota, Alaska, Rhode Island, New Hampshire, Maine

## Generation Statistics
- **Total States**: 50
- **Total Template Files**: 950
- **Average Files Per State**: 19
- **Generation Time**: ~5 minutes for all 50 states
- **Template Consistency**: 100% based on New Jersey structure

## Maintenance

### Updating Templates
To regenerate templates with changes:
1. Edit `generate_complete_template_system.py`
2. Modify template strings (CHUNK1_TEMPLATE, CHUNK2_TEMPLATE, etc.)
3. Run script: `python generate_complete_template_system.py`
4. Review output in COMPLETE_STATE_TEMPLATES/

### Adding New States
Templates support all 50 states. For territories:
1. Add territory to STATE_INFO dictionary
2. Set districts, senate_year, gov_year
3. Run generation script

## Best Practices

### AI Generation Tips
1. **Use One Chunk at a Time**: Don't overwhelm AI with all templates at once
2. **Verify Counts**: Check actual candidate counts match verification sections
3. **Source Citations**: Ensure all data cites Ballotpedia or official sources
4. **Faith Statements**: Require actual statements or "No publicly disclosed faith statement"
5. **Complete Arrays**: Never accept abbreviated output with "continue..." or "etc."

### Quality Checks
- Minimum 12,000 characters for summaries
- All 8 key issues covered (Pro-life, School Choice, Religious Liberty, etc.)
- Database Summary section present
- Prayer Points with scripture verses
- Church Mobilization strategy included

## Support & Documentation
- **Main Documentation**: `docs/PROGRESS.md` - Complete project history
- **Troubleshooting**: `Election Chunks/TROUBLESHOOTING.md`
- **How to Use**: `NJ_Election_Chunks/HOW_TO_USE_CHUNKS.md`

## Version History
- **v1.0** (January 2025): Initial template system with 50 CHUNK_5A files
- **v2.0** (January 2025): Complete system with all chunk types (CHUNK_1, 2A-2T, 5A-5D)
- **v2.1** (January 2025): Added flexible candidate counts and verification sections

## Status
✅ **COMPLETE**: All 50 states have comprehensive template sets ready for AI-assisted data generation
