# State Election Data Generation - Complete Guide

This guide explains how to generate comprehensive state election data (races, candidates, and voter guides) using AI and upload to DynamoDB.

---

## Overview

**What This Does:**
- Generates complete election data for any state
- Creates races, candidates, and 20,000+ character voter guides
- Uploads to DynamoDB with duplicate checking
- Safe to run multiple times (updates existing data)

**Files You Need:**
- `full_prompt.md` - Master prompt template (in Downloads folder)
- AI tool with file upload (Grok, Claude, ChatGPT, etc.)
- Python 3.x with boto3 installed
- Visual Studio Code with terminal

---

## Step-by-Step Process

### Step 1: Prepare the Prompt

1. Open `full_prompt.md` from your Downloads folder
2. Edit the first line: Change `[STATE NAME] equals, <state>` to your target state
   - Example: `Where [STATE NAME] equals, Indiana, create complete...`
   - This automatically replaces all `[STATE NAME]` placeholders throughout the prompt
3. Save the file

**Result:** Prompt ready to submit to AI

---

### Step 2: Submit to AI

1. Open your AI tool (Grok, Claude, ChatGPT, etc.)
2. Upload the `full_prompt.md` file to the AI
3. Press start/submit and wait for response (may take 2-3 minutes)

**What AI Returns:**
- Complete Python script
- Populated races array (8-15 races)
- Populated candidates array (2-10+ candidates with full profiles)
- Comprehensive summary (20,000+ characters)
- Duplicate-safe upload code

---

### Step 3: Create and Save the Upload Script

1. Open terminal in Visual Studio Code
2. Navigate to Scripts directory: `cd Scripts`
3. Create new file: `code .\upload_<state>_data.py`
   - Example: `code .\upload_indiana_data.py`
4. Copy the Python code from AI response
5. Paste into the editor
6. Save the file (Ctrl+S)

**Verify the file has:**
- `races = [...]` with actual race data
- `candidates = [...]` with actual candidate profiles
- `summary = {...}` with comprehensive markdown content
- Upload code at the bottom

---

### Step 4: Run the Upload Script

```bash
# Already in Scripts directory from Step 3
python upload_indiana_data.py
```

**Expected Output:**
```
Checking for existing California races...
Found 0 existing races

Processing 8 California races...
  Created: Governor
  Created: Lieutenant Governor
  Created: Attorney General
  ...

[SUCCESS] Processed 8 races

Checking for existing California candidates...
Found 0 existing candidates

Processing 2 California candidates...
  Created: Chad Bianco - Governor
  Created: Steve Hilton - Governor

[SUCCESS] Processed 2 candidates

Processing California summary...
  Creating new summary...
[SUCCESS] Summary uploaded: 21,456 chars

[SUCCESS] California data upload complete!
```

---

### Step 5: Verify Upload

**Check DynamoDB:**
1. Go to AWS Console → DynamoDB
2. Check `races` table - should see new California races
3. Check `candidates` table - should see new California candidates
4. Check `state-summaries` table - should see California summary

**Check Website:**
1. Open your election map
2. Click on California
3. Verify summary displays correctly
4. Check races and candidates appear

---

## Re-Running Scripts (Updates)

**Safe to Run Multiple Times:**
- Script checks for existing data
- Updates existing races/candidates instead of creating duplicates
- Uses (name, office) as unique key for candidates
- Uses (state, office) as unique key for races

**When to Re-Run:**
- Update candidate information
- Add new races
- Refresh summary content
- Fix errors in data

---

## Troubleshooting

### Problem: AI Returns Generic Content

**Solution:**
- Emphasize "Research REAL candidates currently running"
- Add "Find ACTUAL faith statements from sources"
- Specify "Include state-specific laws and policies"

### Problem: Script Has Syntax Errors

**Solution:**
- Check for unmatched quotes in summary content
- Verify all brackets/braces are closed
- Look for special characters that need escaping

### Problem: Upload Fails

**Solution:**
- Verify AWS credentials are configured
- Check DynamoDB table names match (`races`, `candidates`, `state-summaries`)
- Ensure boto3 is installed: `pip install boto3`

### Problem: Duplicates Created

**Solution:**
- Verify you're using the updated `full_prompt.md` with duplicate-safe code
- Check that upload code includes `existing_race_map` and `existing_candidate_map`

---

## State Priority List

**Remaining States (17 total):**

**High Priority:**
1. California ✅ (completed)
2. Arizona
3. Minnesota
4. Colorado

**Medium Priority:**
5. Maine
6. Rhode Island
7. New Jersey
8. Delaware
9. Kansas
10. Iowa
11. Kentucky
12. Nevada

**Low Priority:**
13. Oklahoma
14. Louisiana
15. Tennessee
16. South Dakota
17. Wyoming

---

## File Structure

```
AWS/
├── Downloader/Election Data and Files/
│   ├── Templates/
│   │   ├── full_prompt.md (Master prompt)
│   │   ├── README_STATE_DATA_GENERATION.md (This file)
│   │   └── upload_template_no_duplicates.py (Reference)
│   └── Voter Guides_Summaries/UpdatedGuides/
│       └── california_full.md (AI output example)
└── Scripts/
    ├── upload_california_data.py (Generated script)
    ├── upload_arizona_data.py (Next state)
    └── ...
```

---

## Best Practices

1. **One State at a Time** - Don't try to generate multiple states in one prompt
2. **Verify AI Output** - Check that races/candidates are real, not generic
3. **Test Before Production** - Run script in test environment first
4. **Keep Backups** - Save AI outputs before running upload
5. **Document Changes** - Note what was updated when re-running scripts

---

## Quick Reference Commands

```bash
# Generate for new state
1. Edit full_prompt.md first line: "Where [STATE NAME] equals, Indiana"
2. Upload full_prompt.md to AI (Grok/Claude/ChatGPT)
3. cd Scripts
4. code .\upload_indiana_data.py
5. Paste AI output, save (Ctrl+S)
6. python upload_indiana_data.py

# Update existing state
1. Edit existing upload_[state]_data.py
2. Modify races/candidates/summary
3. cd Scripts
4. python upload_[state]_data.py
5. Script will update existing data

# Check what's in database
cd Scripts
python identify_states_needing_work.py
```

---

## Support

**Issues?**
- Check AWS credentials: `aws configure`
- Verify table names in DynamoDB console
- Review error messages in script output
- Check this README for troubleshooting section

**Need Help?**
- Review example: `california_full.md`
- Check template: `full_prompt.md`
- Reference: `upload_template_no_duplicates.py`

---

**Last Updated:** October 2025
**Version:** 1.0
