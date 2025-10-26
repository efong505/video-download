# Election Data Management Scripts

## Available Scripts

### 1. update_candidate.py
Updates existing candidate information in DynamoDB.

**Usage:**
```bash
python update_candidate.py "John Doe" "Texas" --field status --value withdrawn
python update_candidate.py "Jane Smith" "California" --field bio --value "New bio text"
```

**Common Updates:**
- Change status: `--field status --value withdrawn`
- Update bio: `--field bio --value "New biography"`
- Add website: `--field website --value "https://example.com"`

---

### 2. validate_election_data.py
Checks data quality and identifies issues.

**Usage:**
```bash
python validate_election_data.py
```

**Checks:**
- Races without candidates
- Candidates without race_id
- Missing candidate information
- Data completeness

**Run this weekly to maintain data quality!**

---

## Quick Reference

### Update Candidate Status
```bash
# Candidate dropped out
python update_candidate.py "Candidate Name" "State" --field status --value withdrawn

# Candidate won primary
python update_candidate.py "Candidate Name" "State" --field status --value primary_winner
```

### Check Data Quality
```bash
# Run validation
python validate_election_data.py

# Review output for issues
# Fix any problems identified
```

---

## Workflow Integration

**Weekly Tasks:**
1. Run `validate_election_data.py`
2. Fix any issues identified
3. Update candidates as needed with `update_candidate.py`

**When Candidate Drops Out:**
```bash
python update_candidate.py "Candidate Name" "State" --field status --value withdrawn
```

**When New Endorsement:**
```bash
# Add to CSV and re-import, or update directly in database
```

---

---

## Data Accuracy Tools

### 3. audit_all_states_data.py
Checks for discrepancies between database counts and summary text.

**Usage:**
```bash
python audit_all_states_data.py
```

**What it checks:**
- Actual race count in `races` table vs summary text
- Actual candidate count in `candidates` table vs summary text
- Reports discrepancies, missing data, and perfect matches

**When to run:**
- After bulk uploads
- Before major releases
- When you suspect incorrect counts

---

### 4. fix_all_state_summaries.py
Automatically corrects all summary counts to match database reality.

**Usage:**
```bash
python fix_all_state_summaries.py
```

**What it does:**
1. Counts actual records in `races` and `candidates` tables
2. Gets summary text from `state-summaries` table
3. Uses regex to find and replace wrong numbers
4. Saves corrected text back to database

**When to use:**
- After uploading data with incorrect summary counts
- As a safety check after AI-generated uploads
- Anytime audit shows discrepancies

**Results:** Fixed 43 out of 50 states in January 2025!

---

### 5. delete_[state]_data.py
Deletes all races and candidates for a specific state.

**Usage:**
```bash
python delete_hawaii_data.py
# Type: DELETE HAWAII
```

**When to use:**
- Before re-uploading corrected data
- To start fresh with new data
- To remove test data

**Safety:** Requires explicit confirmation to prevent accidents

---

## ⚠️ Critical: AI-Generated Upload Scripts

### The Problem

When using AI to generate upload scripts, the AI may write **incorrect numbers** in the summary text!

**Example:**
```python
races = [{...}, {...}]  # 40 actual races
candidates = [{...}]  # 30 actual candidates

summary = {
    "content": "Total Races: 120"  # AI wrote wrong number!
}
```

### The Solution

**ALWAYS verify before running upload scripts:**

1. Count `len(races)` manually
2. Count `len(candidates)` manually  
3. Check summary text matches your counts
4. Edit summary if numbers are wrong
5. Then run the script

**If you forget:**
```bash
python fix_all_state_summaries.py  # Fixes all states automatically
```

### Documentation

For complete details, see:
- `../Templates/HOW_TO_USE_PROMPT.md` - Verification guide
- `../../ELECTION_DATA_ACCURACY_SUMMARY.md` - Full explanation

---

## Future Scripts (To Be Created)

- `import_races.py` - Bulk import races from CSV
- `import_candidates.py` - Bulk import candidates from CSV
- `generate_summary_template.py` - Create summary template for state
- `candidate_tracker.py` - Monitor candidate announcements
- `export_data.py` - Export data for backup/analysis
