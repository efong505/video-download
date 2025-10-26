# Election Data and Files - Complete Directory Guide

## Overview

This directory contains all resources for managing the Christian Conservatives Today election tracking system covering all 50 US states.

**Current Status:** All 50 states have election data with accurate race and candidate counts! ✅

---

## Directory Structure

```
Election Data and Files/
├── CSV files/                    # Race and candidate data in CSV format
├── Documentation/                # System documentation
├── Email and Tracking/           # Email subscription and analytics
├── Marketing and Promotion/      # Marketing materials and social media
├── Scripts/                      # Python scripts for data management
│   ├── upload_*.py              # State data upload scripts
│   ├── audit_all_states_data.py # Check for data discrepancies
│   ├── fix_all_state_summaries.py # Auto-fix incorrect counts
│   └── README.md                # Scripts documentation
├── Templates/                    # AI prompts and templates
│   ├── full_prompt.md           # Complete AI prompt for state data
│   ├── HOW_TO_USE_PROMPT.md     # Verification guide (CRITICAL!)
│   └── README.md                # Templates documentation
└── Voter Guides_Summaries/      # State summary markdown files
    ├── [state]_summary_guide.md # Local source files
    └── UpdatedGuides/           # Updated guide versions
```

---

## Quick Start

### Adding a New State

1. **Use the AI Prompt**
   ```
   Open: Templates/full_prompt.md
   Replace: [STATE NAME] with your target state
   Submit to AI (ChatGPT, Claude, etc.)
   ```

2. **CRITICAL: Verify the Output**
   ```python
   # Count the arrays manually
   len(races) = ?
   len(candidates) = ?
   
   # Verify summary text matches
   "Total Races: [must match len(races)]"
   "Total Candidates: [must match len(candidates)]"
   ```

3. **Run the Upload Script**
   ```bash
   python Scripts/upload_texas_data.py
   ```

4. **Verify on Website**
   - Check election map
   - Click on the state
   - Confirm counts are correct

### Fixing Incorrect Counts

If you uploaded data with wrong numbers:

```bash
# Check all states for discrepancies
python Scripts/audit_all_states_data.py

# Automatically fix all summaries
python Scripts/fix_all_state_summaries.py
```

---

## ⚠️ CRITICAL: Data Accuracy

### The Problem We Solved

In January 2025, we discovered that **43 out of 50 states** had incorrect race and candidate counts displayed on the website.

**Example:**
- Florida showed "120 races, 300 candidates"
- But database only had 40 races, 30 candidates
- Website displayed the wrong text from the summary

### Why It Happened

AI-generated upload scripts had **hardcoded wrong numbers** in the summary text:

```python
races = [{...}, {...}]  # 40 actual races
candidates = [{...}]  # 30 actual candidates

summary = {
    "content": """
    Total Races: 120  ← AI wrote wrong number!
    Total Candidates: 300  ← AI wrote wrong number!
    """
}
```

The script uploaded:
- ✅ 40 races to `races` table (correct)
- ✅ 30 candidates to `candidates` table (correct)
- ❌ Text saying "120 races" to `state-summaries` table (WRONG!)

### The Solution

**Created three tools:**

1. **audit_all_states_data.py** - Checks for discrepancies
2. **fix_all_state_summaries.py** - Auto-fixes all summaries
3. **Updated AI prompt** - Includes verification instructions

**Result:** All 50 states now have accurate counts! 🎉

### Prevention Going Forward

**ALWAYS verify before uploading:**

```
1. Count races array: len(races) = ?
2. Count candidates array: len(candidates) = ?
3. Check summary text matches these numbers
4. Edit summary if wrong
5. Then run the script
```

**Read the complete guide:**
- `Templates/HOW_TO_USE_PROMPT.md` - Step-by-step verification
- `../ELECTION_DATA_ACCURACY_SUMMARY.md` - Full explanation

---

## Key Files

### Must-Read Documentation

| File | Purpose | When to Use |
|------|---------|-------------|
| `Templates/HOW_TO_USE_PROMPT.md` | Complete guide on using AI prompt correctly | Before creating any new state data |
| `Templates/full_prompt.md` | AI prompt template for generating state data | When adding a new state |
| `Scripts/README.md` | Documentation for all Python scripts | When running any script |
| `../ELECTION_DATA_ACCURACY_SUMMARY.md` | Complete explanation of data accuracy system | To understand how everything works |

### Critical Scripts

| Script | Purpose | Command |
|--------|---------|---------|
| `audit_all_states_data.py` | Check for data discrepancies | `python Scripts/audit_all_states_data.py` |
| `fix_all_state_summaries.py` | Auto-fix incorrect counts | `python Scripts/fix_all_state_summaries.py` |
| `upload_[state]_data.py` | Upload state data to DynamoDB | `python Scripts/upload_texas_data.py` |
| `delete_[state]_data.py` | Delete state data (for re-upload) | `python Scripts/delete_hawaii_data.py` |

---

## How the System Works

### Three-Table Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ races table (DynamoDB)                                      │
│ - Individual race records                                   │
│ - Fields: race_id, state, office, election_date            │
│ - Example: Texas has 9 race records                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ candidates table (DynamoDB)                                 │
│ - Individual candidate records                              │
│ - Fields: candidate_id, name, party, bio, positions         │
│ - Example: Texas has 14 candidate records                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ state-summaries table (DynamoDB)                            │
│ - Full markdown guide as text (20,000+ characters)          │
│ - Fields: state, title, content, election_year             │
│ - The 'content' field has hardcoded numbers                 │
│ - Website displays this text directly                       │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

**Upload:**
```
upload_texas_data.py
├─→ Uploads races to races table
├─→ Uploads candidates to candidates table
└─→ Uploads summary text to state-summaries table
    └─→ Text includes "Total Races: X" (hardcoded)
```

**Display:**
```
User clicks Texas on map
└─→ Website queries state-summaries table
    └─→ Displays 'content' field (the markdown text)
        └─→ Shows whatever numbers are in the text
```

**Key Insight:** The website displays the text from the summary, NOT a count of the database records!

---

## Current Status (January 2025)

### All 50 States - Accurate Data ✅

| Status | Count | Details |
|--------|-------|---------|
| ✅ Fixed | 43 states | Had incorrect counts, now corrected |
| ✅ Correct | 7 states | Already had accurate counts |
| ✅ Total | 50 states | 100% accuracy achieved |

### States with Most Data

| State | Races | Candidates |
|-------|-------|------------|
| California | 95 | 57 |
| Ohio | 39 | 26 |
| Florida | 40 | 30 |
| Georgia | 28 | 31 |
| Pennsylvania | 27 | 8 |

---

## Best Practices

### ✅ DO:
1. **Always verify counts** before running upload scripts
2. **Use the updated prompt template** with verification instructions
3. **Count arrays manually** - don't trust AI estimates
4. **Run audit script** after bulk uploads
5. **Keep fix script handy** as a safety net
6. **Read HOW_TO_USE_PROMPT.md** before creating new state data

### ❌ DON'T:
1. **Don't trust AI-generated numbers** without verification
2. **Don't use estimates** like "50+", "100-150" - use exact counts
3. **Don't skip verification** - it takes 30 seconds, saves hours
4. **Don't assume the script validates** - it uploads whatever AI wrote
5. **Don't forget to test** on one state before doing all 50

### 🎯 Golden Rule:
**The numbers in the summary text MUST match the actual array lengths!**

```python
len(races) == number in summary text ✓
len(candidates) == number in summary text ✓
```

---

## Troubleshooting

### Problem: Website shows wrong race/candidate counts

**Solution:**
```bash
# Check which states have wrong counts
python Scripts/audit_all_states_data.py

# Fix all states automatically
python Scripts/fix_all_state_summaries.py
```

### Problem: AI generated wrong numbers in upload script

**Solution:**
1. Don't run the script yet!
2. Count the arrays manually
3. Edit the summary text to match
4. Then run the script

### Problem: Already uploaded with wrong numbers

**Solution:**
```bash
# Just run the fix script
python Scripts/fix_all_state_summaries.py
```

### Problem: Need to re-upload a state

**Solution:**
```bash
# Delete the old data first
python Scripts/delete_texas_data.py

# Then upload new data
python Scripts/upload_texas_data.py
```

---

## Resources

### Documentation
- `Templates/HOW_TO_USE_PROMPT.md` - Complete verification guide
- `Templates/README.md` - Template usage instructions
- `Scripts/README.md` - Script documentation
- `../ELECTION_DATA_ACCURACY_SUMMARY.md` - Full system explanation

### Tools
- `Scripts/audit_all_states_data.py` - Check for discrepancies
- `Scripts/fix_all_state_summaries.py` - Auto-fix summaries
- `Scripts/delete_[state]_data.py` - Delete state data
- `Scripts/upload_[state]_data.py` - Upload state data

### Templates
- `Templates/full_prompt.md` - AI prompt for state data
- `Templates/state_summary_template.md` - Blank summary structure
- `Templates/upload_state_template.py` - Python script template

---

## Quick Reference Commands

```bash
# Check all states for discrepancies
python Scripts/audit_all_states_data.py

# Fix all summaries automatically
python Scripts/fix_all_state_summaries.py

# Upload new state data
python Scripts/upload_texas_data.py

# Delete state data (to re-upload)
python Scripts/delete_texas_data.py

# Validate data quality
python Scripts/validate_election_data.py

# Update candidate info
python Scripts/update_candidate.py "Name" "State" --field status --value withdrawn
```

---

## Version History

- **v1.0** (January 2025) - Initial election system with 50 states
- **v1.1** (January 2025) - Data accuracy fix
  - Fixed 43 states with incorrect counts
  - Created audit and fix tools
  - Updated AI prompt with verification
  - Added comprehensive documentation

---

## Contact

For questions or issues:
- Email: contact@ekewaka.com
- Review documentation in this directory
- Check `../docs/` for additional platform documentation

---

**Status: All 50 states have accurate election data! 🎉**

**Last Updated:** January 2025
