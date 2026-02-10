# How to Use Pennsylvania Election Chunks

## Overview
This directory contains 25 chunk files to generate complete Pennsylvania 2025-2026 election data.

**Target Output:**
- 100+ races
- 200+ candidates
- 27,500 word voter guide

## Step-by-Step Process

### Step 1: Generate Races (5 minutes)
1. Open `CHUNK_1_RACES.md`
2. Copy entire content
3. Paste into Grok AI
4. Save Grok's output as `chunk1_output.txt`
5. Verify it starts with `races = [` and ends with `]`

### Step 2: Generate Candidates (20 sessions, ~100 minutes)
For each chunk from 2A to 2T:
1. Open `CHUNK_2A_CANDIDATES_1-10.md`
2. Copy entire content
3. Paste into Grok AI
4. Save output as `chunk2a_output.txt`
5. Verify it starts with `    {` and ends with `    },` (or `    }` for last chunk)
6. Repeat for chunks 2B through 2T

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
python combine_p_chunks.py
```

This creates `upload_p_data.py` with all data merged.

### Step 6: Upload to Database (2 minutes)
```bash
python upload_p_data.py
```

This uploads races, candidates, and summary to DynamoDB.

## Troubleshooting

### Problem: "chunk2X_output.txt not found"
**Solution:** Check filename - should be `chunk2a_output.txt` (lowercase, underscore)

### Problem: "SyntaxError: unterminated string literal"
**Solution:** Run `python ../fix_html_entities.py` to fix encoding

### Problem: "SyntaxError: unmatched ']'"
**Solution:** Last candidate chunk should end with `}` not `}]`

### Problem: Candidates in "Other Candidates" section
**Solution:** Run fix scripts:
```bash
python ../smart_fix_race_ids.py
python ../fix_orphaned_candidates.py
```

## Quality Checklist

Before uploading, verify:
- [ ] chunk1_output.txt has 100+ races
- [ ] All 20 candidate chunks saved (chunk2a through chunk2t)
- [ ] All 4 summary chunks saved (chunk5a through chunk5d)
- [ ] No HTML entities (`&quot;`, `&amp;`, etc.)
- [ ] No placeholders ("...", "[Continue]", "TBD")
- [ ] All emojis preserved in summary
- [ ] combine script runs without errors
- [ ] upload script completes successfully

## File Checklist

Input files (create these):
- [ ] chunk1_output.txt
- [ ] chunk2a_output.txt through chunk2t_output.txt (20 files)
- [ ] chunk5a_output.txt through chunk5d_output.txt (4 files)

Output files (auto-generated):
- [ ] upload_p_data.py
- [ ] Database records in DynamoDB

## Time Estimate

- Chunk generation: 125 minutes
- Fixing issues: 5 minutes
- Combining & uploading: 5 minutes
- **Total: ~135 minutes**

## Need Help?

See `../TROUBLESHOOTING.md` for detailed solutions to common problems.
