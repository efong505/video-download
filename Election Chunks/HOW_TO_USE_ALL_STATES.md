# How to Use Templates for All 50 States

## Quick Start (5 Steps)

### Step 1: Get Accurate State Data
Upload `AI_RESEARCH_PROMPT.md` to AI (Grok/Claude/ChatGPT) to get researched STATE_INFO dictionary.

### Step 2: Generate Templates
```powershell
# Generate detailed race templates (CHUNK_1)
python generate_detailed_state_templates.py

# Generate enhanced candidate/summary templates (CHUNK_2, CHUNK_5)
python generate_complete_template_system.py
```

### Step 3: Select State
Navigate to `COMPLETE_STATE_TEMPLATES/[State_Name]/`

### Step 4: Upload Templates to AI
Upload chunks in order:
1. CHUNK_1_RACES.md → Get races array
2. CHUNK_2A_CANDIDATES_1-10.md → Get first 10 candidates
3. CHUNK_2B, 2C, etc. → Get remaining candidates
4. CHUNK_5A-5D → Get summary (4 parts)

### Step 5: Combine and Upload
```powershell
# Save AI outputs to text files
# chunk1_output.txt, chunk2a_output.txt, etc.

# Copy combine script from NJ folder
cp NJ_Election_Chunks/combine_nj_chunks.py combine_[state]_chunks.py

# Edit state name in script (3 places)
# Run combine script
python combine_[state]_chunks.py

# Upload to database
python upload_[state]_data.py
```

## Detailed Workflow

### Phase 1: Research (One-Time Setup)

**Goal**: Get accurate race counts for all 50 states

1. Open `AI_RESEARCH_PROMPT.md`
2. Upload to AI (Grok recommended for research)
3. AI returns STATE_INFO dictionary with:
   - Congressional districts
   - Senate race year (2026 or None)
   - Governor election year (2025/2026/2027)
   - State legislature sizes
   - School board seats
   - City council seats
   - Mayoral races
   - County races

4. Copy STATE_INFO to `generate_detailed_state_templates.py`
5. Run script to generate accurate CHUNK_1 templates

### Phase 2: Template Generation

**Goal**: Create complete template sets for all 50 states

```powershell
cd "Election Chunks"

# Generate race templates with accurate counts
python generate_detailed_state_templates.py
# Output: COMPLETE_STATE_TEMPLATES/[State]/CHUNK_1_RACES.md (50 files)

# Generate candidate and summary templates
python generate_complete_template_system.py
# Output: COMPLETE_STATE_TEMPLATES/[State]/CHUNK_2A-2T, CHUNK_5A-5D (950 files)
```

### Phase 3: State Data Generation

**Goal**: Generate election data for one state

**Example: Pennsylvania**

1. **Navigate to state folder**:
   ```powershell
   cd COMPLETE_STATE_TEMPLATES/Pennsylvania
   ```

2. **Upload CHUNK_1 to AI**:
   - Open `CHUNK_1_RACES.md`
   - Upload to AI (Grok/Claude)
   - AI generates races array
   - Save output to `chunk1_output.txt`

3. **Upload CHUNK_2A-2T to AI** (one at a time):
   - Upload `CHUNK_2A_CANDIDATES_1-10.md`
   - AI generates 10 candidates
   - Save to `chunk2a_output.txt`
   - Repeat for 2B, 2C, 2D... (Pennsylvania has 20 candidate chunks)

4. **Upload CHUNK_5A-5D to AI**:
   - Upload `CHUNK_5A_SUMMARY_PART1.md`
   - AI generates first part of summary
   - Save to `chunk5a_output.txt`
   - Repeat for 5B, 5C, 5D

5. **Combine outputs**:
   ```powershell
   # Copy combine script
   cp ../../NJ_Election_Chunks/combine_nj_chunks.py combine_pennsylvania_chunks.py
   
   # Edit script: Change "New Jersey" to "Pennsylvania" (3 places)
   # Adjust candidate loop: ['a', 'b', 'c', ..., 't'] for 20 chunks
   
   # Run combine script
   python combine_pennsylvania_chunks.py
   ```

6. **Upload to database**:
   ```powershell
   python upload_pennsylvania_data.py
   ```

### Phase 4: Verification

**Goal**: Verify data uploaded correctly

1. **Check race count**:
   ```powershell
   python check_state_data.py Pennsylvania
   ```

2. **Fix orphaned candidates** (if any):
   ```powershell
   python fix_orphaned_candidates.py Pennsylvania
   python smart_fix_race_ids.py Pennsylvania
   ```

3. **Verify summary**:
   - Check character count (12,000+ minimum)
   - Verify all sections present
   - Check markdown formatting

## State Size Reference

### Large States (20 candidate chunks)
California, Texas, Florida, New York, Pennsylvania, Illinois, Ohio, Georgia, North Carolina, Michigan

**Template files**: 25 total
- 1 CHUNK_1 (races)
- 20 CHUNK_2A-2T (candidates, 10 each = 200 max)
- 4 CHUNK_5A-5D (summary parts)

### Medium States (15 candidate chunks)
Most states with 10-19 congressional districts

**Template files**: 20 total
- 1 CHUNK_1 (races)
- 15 CHUNK_2A-2O (candidates, 10 each = 150 max)
- 4 CHUNK_5A-5D (summary parts)

### Small States (10 candidate chunks)
Wyoming, Vermont, Delaware, Montana, etc.

**Template files**: 15 total
- 1 CHUNK_1 (races)
- 10 CHUNK_2A-2J (candidates, 10 each = 100 max)
- 4 CHUNK_5A-5D (summary parts)

## Tips for Success

### AI Selection
- **Grok**: Best for research and large datasets
- **Claude**: Best for detailed candidate bios
- **ChatGPT**: Good all-around, may abbreviate

### Preventing Abbreviation
- Upload one chunk at a time
- Check output for "..." or "[continue]"
- If abbreviated, re-upload with emphasis on "NO ABBREVIATIONS"
- Use verification sections to catch incomplete output

### Candidate Count Flexibility
- Templates say "UP TO X candidates"
- If state has fewer viable candidates, that's OK
- Don't force AI to invent fake candidates
- Quality over quantity

### Summary Quality
- Minimum 12,000 characters
- All 8 key issues required
- Database Summary section mandatory
- Prayer Points with scripture verses

## Troubleshooting

### Issue: AI abbreviates candidate list
**Solution**: Re-upload chunk with added emphasis:
```
CRITICAL: Write ALL 10 candidates COMPLETELY. 
If you abbreviate ANY candidate, START OVER.
```

### Issue: Candidates missing race_id
**Solution**: Run fix scripts:
```powershell
python fix_orphaned_candidates.py [State]
python smart_fix_race_ids.py [State]
```

### Issue: Summary too short
**Solution**: Re-upload CHUNK_5 templates with emphasis on word counts

### Issue: Duplicate candidates
**Solution**: Upload scripts are duplicate-safe, just re-run

## File Organization

```
Election Chunks/
├── AI_RESEARCH_PROMPT.md              # Step 1: Research prompt
├── generate_detailed_state_templates.py   # Step 2a: Generate CHUNK_1
├── generate_complete_template_system.py   # Step 2b: Generate CHUNK_2/5
├── COMPLETE_STATE_TEMPLATES/          # Generated templates
│   ├── Alabama/
│   ├── Alaska/
│   ├── ...
│   └── Wyoming/
├── NJ_Election_Chunks/                # Reference implementation
│   └── combine_nj_chunks.py           # Copy this for each state
└── HOW_TO_USE_ALL_STATES.md          # This file
```

## Next Steps

1. **Get STATE_INFO**: Upload AI_RESEARCH_PROMPT.md to AI
2. **Generate templates**: Run both generation scripts
3. **Pick a state**: Start with small state (Wyoming, Vermont)
4. **Generate data**: Upload chunks to AI
5. **Combine and upload**: Use combine script
6. **Verify**: Check database and fix issues
7. **Repeat**: Move to next state

## Support Files

- **TEMPLATE_SYSTEM_README.md**: Detailed template documentation
- **PROGRESS.md**: Complete project history
- **TROUBLESHOOTING.md**: Common issues and solutions
- **NJ_Election_Chunks/HOW_TO_USE_CHUNKS.md**: Original NJ workflow
