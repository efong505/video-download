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

## Future Scripts (To Be Created)

- `import_races.py` - Bulk import races from CSV
- `import_candidates.py` - Bulk import candidates from CSV
- `generate_summary_template.py` - Create summary template for state
- `candidate_tracker.py` - Monitor candidate announcements
- `export_data.py` - Export data for backup/analysis
