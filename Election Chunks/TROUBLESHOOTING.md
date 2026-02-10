# Election Data Chunking - Troubleshooting Guide

This document covers all issues encountered during the New Jersey implementation and how to fix them for future states.

## Table of Contents
1. [File Naming Issues](#file-naming-issues)
2. [Encoding Problems](#encoding-problems)
3. [JSON/Python Syntax Errors](#jsonpython-syntax-errors)
4. [Data Matching Issues](#data-matching-issues)
5. [Prevention Checklist](#prevention-checklist)

---

## File Naming Issues

### Problem: Combine Script Can't Find Chunk Files
**Symptom:**
```
WARNING: chunk2c_output.txt not found - skipping
WARNING: chunk2d_output.txt not found - skipping
```

**Cause:** Files saved with wrong naming pattern (e.g., `chunk2c.output.txt` instead of `chunk2c_output.txt`)

**Fix:**
```powershell
# Rename all files to use underscore
ren chunk2c.output.txt chunk2c_output.txt
ren chunk2d.output.txt chunk2d_output.txt
# ... repeat for all files
```

**Prevention:** Always save Grok output as `chunk2X_output.txt` with underscore, not period.

---

## Encoding Problems

### Problem 1: HTML Entities in Output
**Symptom:**
```python
SyntaxError: unterminated string literal (detected at line 1862)
```

**Cause:** Copying from Grok web interface includes HTML entities (`&quot;` instead of `"`)

**Fix:**
```python
# Create fix_html_entities.py
import os
import html

for filename in os.listdir('.'):
    if filename.endswith('_output.txt'):
        filepath = os.path.join('.', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content = html.unescape(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Fixed: {filename}")
```

**Prevention:** Copy Grok output as plain text, or always run the fix script after saving chunks.

### Problem 2: Windows Emoji Encoding Error
**Symptom:**
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705'
```

**Cause:** Windows console can't display emoji characters in print statements

**Fix:** Remove emojis from Python print statements (keep them in data content)
```python
# Bad
print("✅ SUCCESS!")

# Good
print("SUCCESS!")
```

**Prevention:** Never use emojis in Python print/logging statements on Windows.

---

## JSON/Python Syntax Errors

### Problem 1: Malformed JSON Keys
**Symptom:**
```python
": "ABORTION": "Advocates for full access..."
```

**Cause:** Grok occasionally generates malformed JSON with extra characters

**Fix:** Manually edit the chunk file to remove extra characters
```python
# Before
"positions": {
   ": "ABORTION": "text",

# After
"positions": {
    "ABORTION": "text",
```

**Prevention:** Validate each chunk output before combining. Look for lines starting with `":` or other malformed keys.

### Problem 2: Array Declaration Duplication
**Symptom:**
```python
candidates = [
candidates = [
    {
```

**Cause:** Grok includes `candidates = [` in first chunk, but template also has it

**Fix:**
```python
# Remove from chunk2a_output.txt
# Delete this line:
candidates = [

# Keep only:
    {
        "name": "First Candidate",
```

**Prevention:** Instruct Grok to start chunks with `{` not `candidates = [`

### Problem 3: Extra Closing Bracket
**Symptom:**
```python
SyntaxError: unmatched ']'
```

**Cause:** Last chunk ends with `}]` instead of just `}`

**Fix:**
```python
# In last chunk file (chunk2o_output.txt)
# Change from:
    }
]

# To:
    }
```

**Prevention:** Instruct Grok that last chunk should end with `}` only, no closing bracket.

### Problem 4: Comment Lines in Chunks
**Symptom:**
```python
],
# CONTINUE FROM CANDIDATE 10 WITH COMMA
    {
```

**Cause:** Grok adds instructional comments that break Python syntax

**Fix:**
```powershell
# Remove all comment lines
powershell -Command "foreach($f in Get-ChildItem chunk2*_output.txt){(Get-Content $f) -replace '^\s*# CONTINUE FROM CANDIDATE.*$','' | Set-Content $f}"
```

**Prevention:** Instruct Grok to never include comments in output, only pure JSON.

### Problem 5: F-String Backslash Error
**Symptom:**
```python
SyntaxError: f-string expression part cannot include a backslash
```

**Cause:** Using f-strings with escaped characters like `\n` or `\"`

**Fix:** Convert from f-string to template string with `.replace()`
```python
# Bad
final_script = f'''
content = """{full_summary}"""
'''

# Good
script_template = '''
content = """{{SUMMARY_CONTENT}}"""
'''
final_script = script_template.replace('{{SUMMARY_CONTENT}}', full_summary)
```

**Prevention:** Use template strings with placeholders, not f-strings for large multi-line content.

### Problem 6: Double Braces Causing Dict Error
**Symptom:**
```python
TypeError: unhashable type: 'dict'
```

**Cause:** Template has `{{` and `}}` for f-string escaping, but after switching to `.replace()` they become literal

**Fix:**
```powershell
# Replace all double braces with single
powershell -Command "(Get-Content combine_script.py) -replace '{{','{' -replace '}}','}' | Set-Content combine_script.py"
```

**Prevention:** When using `.replace()` method, use single braces `{` not double `{{`.

---

## Data Matching Issues

### Problem 1: Incorrect Summary Counts
**Symptom:** Summary says "41 races and 102 candidates" but database has 151 races and 150 candidates

**Cause:** Grok didn't count correctly when writing narrative summary

**Fix:**
```python
# Create fix_summary_counts.py
import boto3
import re

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

response = summaries_table.get_item(Key={'state': 'New Jersey'})
summary = response['Item']
content = summary['content']

# Fix the counts
content = re.sub(r'\b41\s+races?\b', '151 races', content, flags=re.IGNORECASE)
content = re.sub(r'\b102\s+candidates?\b', '150 candidates', content, flags=re.IGNORECASE)

summary['content'] = content
summaries_table.put_item(Item=summary)
print("Summary counts fixed")
```

**Prevention:** Manually verify counts in summary match actual data before finalizing.

### Problem 2: Office Name Mismatches
**Symptom:** Candidates appear in "Other Candidates" section instead of their races

**Cause:** Race names don't match candidate office names
- Races: "Edison School Board Seat 1"
- Candidates: "Edison Board of Education At-Large Seat 1"

**Fix:**
```python
# Create smart_fix_race_ids.py
import boto3
import re

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

races = races_table.scan(FilterExpression='#s = :state', ExpressionAttributeNames={'#s': 'state'}, ExpressionAttributeValues={':state': 'STATE_NAME'})['Items']
candidates = candidates_table.scan(FilterExpression='#s = :state', ExpressionAttributeNames={'#s': 'state'}, ExpressionAttributeValues={':state': 'STATE_NAME'})['Items']

race_map = {r['office']: r['race_id'] for r in races}

def normalize_office(office):
    office = office.replace('Board of Education At-Large', 'School Board')
    office = office.replace('Board of Education Ward', 'School Board')
    office = office.replace('Board of Education', 'School Board')
    office = re.sub(r'\s+', ' ', office).strip()
    return office

fixed = 0
for candidate in candidates:
    office = candidate['office']
    normalized = normalize_office(office)
    
    if normalized in race_map:
        correct_race_id = race_map[normalized]
        if candidate.get('race_id') != correct_race_id:
            candidate['race_id'] = correct_race_id
            candidates_table.put_item(Item=candidate)
            print(f"Fixed: {candidate['name']}")
            fixed += 1

print(f"{fixed} candidates fixed")
```

**Prevention:** Standardize office names in chunk prompts. Use "School Board" consistently, not "Board of Education".

### Problem 3: Missing Seat Numbers
**Symptom:** Candidates with "General Assembly District 9" can't match to "General Assembly District 9 Seat 1"

**Cause:** Grok omitted seat numbers for some candidates

**Fix:**
```python
# Create fix_orphaned_candidates.py
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

# Manual mapping of candidates to correct offices
fixes = {
    "Gregory P. McGuckin": "General Assembly District 9 Seat 2",
    "Kyler Dineen": "General Assembly District 10 Seat 1",
    # ... add all orphaned candidates
}

candidates = candidates_table.scan(FilterExpression='#s = :state', ExpressionAttributeNames={'#s': 'state'}, ExpressionAttributeValues={':state': 'STATE_NAME'})['Items']

for candidate in candidates:
    name = candidate['name']
    if name in fixes:
        candidate['office'] = fixes[name]
        candidate['race_id'] = ''  # Will be fixed by next script
        candidates_table.put_item(Item=candidate)
        print(f"Fixed: {name}")
```

**Prevention:** In chunk prompts, explicitly require seat numbers for all multi-seat races.

### Problem 4: Missing Races
**Symptom:** Candidates exist but their races don't (e.g., Perth Amboy School Board)

**Cause:** Race list incomplete or candidates added for races not in original list

**Fix:**
```python
# Create add_missing_races.py
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')

missing_races = [
    {
        "state": "STATE_NAME",
        "office": "Perth Amboy School Board Seat 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Perth Amboy Board of Education At-Large Seat 1"
    },
    # ... add all missing races
]

for race in missing_races:
    race['race_id'] = str(uuid.uuid4())
    race['created_at'] = datetime.now().isoformat()
    race['created_by'] = 'system'
    races_table.put_item(Item=race)
    print(f"Created: {race['office']}")
```

**Prevention:** Generate complete race list BEFORE generating candidates. Verify all candidate offices have matching races.

### Problem 5: Duplicate Data from Previous Uploads
**Symptom:** Database shows 261 races and 158 candidates (old + new mixed together)

**Cause:** Upload script is duplicate-safe (updates existing) but doesn't delete old data first

**Fix:**
```python
# Create delete_state_data.py
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

STATE = 'STATE_NAME'

# Delete all races
races = races_table.scan(FilterExpression='#s = :state', ExpressionAttributeNames={'#s': 'state'}, ExpressionAttributeValues={':state': STATE})['Items']
for race in races:
    races_table.delete_item(Key={'race_id': race['race_id']})
    print(f"Deleted race: {race['office']}")

# Delete all candidates
candidates = candidates_table.scan(FilterExpression='#s = :state', ExpressionAttributeNames={'#s': 'state'}, ExpressionAttributeValues={':state': STATE})['Items']
for candidate in candidates:
    candidates_table.delete_item(Key={'candidate_id': candidate['candidate_id']})
    print(f"Deleted candidate: {candidate['name']}")

# Delete summary
try:
    summaries_table.delete_item(Key={'state': STATE})
    print("Summary deleted")
except:
    print("No summary found")

print(f"All {STATE} data deleted!")
```

**Prevention:** Always delete existing state data before uploading new complete dataset.

---

## Prevention Checklist

### Before Starting a New State

- [ ] Create state-specific directory: `Election_Chunks/STATE_Election_Chunks/`
- [ ] Copy chunk template files from NJ implementation
- [ ] Update state name in all chunk prompts
- [ ] Verify race count requirements (large state: 200+ candidates, medium: 120+, small: 70+)

### When Generating Chunks in Grok

- [ ] Use exact filename format: `chunk2a_output.txt` (underscore, not period)
- [ ] Copy output as plain text to avoid HTML entities
- [ ] Verify first chunk starts with `{` not `candidates = [`
- [ ] Verify last chunk ends with `}` not `}]`
- [ ] Check for no comment lines (no `# CONTINUE FROM...`)
- [ ] Validate JSON structure before saving

### After Saving All Chunks

- [ ] Run `fix_html_entities.py` to decode any HTML entities
- [ ] Verify all chunk files exist with correct names
- [ ] Check first and last chunks for proper formatting
- [ ] Run `combine_chunks.py` to merge into upload script
- [ ] Review generated upload script for syntax errors

### Before Uploading to DynamoDB

- [ ] Delete existing state data with `delete_state_data.py`
- [ ] Verify race count matches expected (check CHUNK_1 output)
- [ ] Verify candidate count matches expected (10 per chunk × number of chunks)
- [ ] Check summary word count is within range

### After Upload

- [ ] Run `fix_summary_counts.py` to correct any count discrepancies
- [ ] Run `smart_fix_race_ids.py` to match candidates to races
- [ ] Check for orphaned candidates in "Other Candidates" section
- [ ] If orphans exist, run `fix_orphaned_candidates.py` with manual mapping
- [ ] If races missing, run `add_missing_races.py`
- [ ] Verify all candidates appear in proper races on election map

### Common Fix Script Execution Order

```bash
# 1. Fix encoding issues
python fix_html_entities.py

# 2. Combine all chunks
python combine_chunks.py

# 3. Delete old data
python delete_state_data.py

# 4. Upload new data
python upload_state_data.py

# 5. Fix summary counts
python fix_summary_counts.py

# 6. Match candidates to races
python smart_fix_race_ids.py

# 7. Fix any orphaned candidates
python fix_orphaned_candidates.py

# 8. Add any missing races
python add_missing_races.py

# 9. Re-run race matching
python smart_fix_race_ids.py
```

---

## Quick Reference: Error Messages

| Error Message | Likely Cause | Fix Script |
|--------------|--------------|------------|
| `WARNING: chunk2X_output.txt not found` | Wrong filename | Rename files |
| `SyntaxError: unterminated string literal` | HTML entities | `fix_html_entities.py` |
| `SyntaxError: unmatched ']'` | Extra closing bracket | Edit last chunk |
| `SyntaxError: f-string expression part cannot include a backslash` | F-string with escapes | Convert to template string |
| `TypeError: unhashable type: 'dict'` | Double braces `{{` | Replace with single `{` |
| `UnicodeEncodeError: 'charmap' codec` | Emoji in print | Remove emoji |
| Candidates in "Other Candidates" | Office name mismatch | `smart_fix_race_ids.py` |
| Wrong counts in summary | Grok miscounted | `fix_summary_counts.py` |
| Duplicate data | Old data not deleted | `delete_state_data.py` |

---

## Contact & Support

If you encounter new issues not covered here, document them following this format:
1. **Symptom:** What error/behavior you see
2. **Cause:** Why it's happening
3. **Fix:** How to resolve it
4. **Prevention:** How to avoid it next time

Add to this document for future reference.
