# How to Use the AI Prompt for State Election Data

## How It Works: Understanding the Data Flow

### The Three-Table System

Your election system uses **three separate DynamoDB tables**:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. races table                                              │
│    - Stores individual race records                         │
│    - Each race has: race_id, state, office, date           │
│    - Example: "Texas Governor", "Florida U.S. Senate"      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 2. candidates table                                         │
│    - Stores individual candidate records                    │
│    - Each candidate has: candidate_id, name, party, bio    │
│    - Example: "Ron DeSantis", "Ted Cruz"                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 3. state-summaries table  ← WHERE THE PROBLEM WAS           │
│    - Stores the FULL MARKDOWN GUIDE as text                │
│    - Has a 'content' field with 20,000+ characters         │
│    - Includes hardcoded numbers like "Total Races: 40"     │
└─────────────────────────────────────────────────────────────┘
```

### What the Upload Script Does

**When you run `upload_texas_data.py`:**

```python
# Step 1: Upload races to 'races' table
races = [{...}, {...}, {...}]  # 40 race objects
for race in races:
    races_table.put_item(Item=race)  # Uploads 40 records

# Step 2: Upload candidates to 'candidates' table  
candidates = [{...}, {...}, {...}]  # 30 candidate objects
for candidate in candidates:
    candidates_table.put_item(Item=candidate)  # Uploads 30 records

# Step 3: Upload summary to 'state-summaries' table
summary = {
    "state": "Texas",
    "content": """# Texas Guide
    Total Races: 40  ← This is just TEXT, not calculated!
    Total Candidates: 30
    ...(rest of 20,000 char guide)...
    """
}
summaries_table.put_item(Item=summary)  # Uploads the text
```

**The Problem:**
- The script uploads 40 races to the `races` table ✓
- The script uploads 30 candidates to the `candidates` table ✓
- The script uploads text saying "40 races" to `state-summaries` table ✓
- **BUT** if the AI wrote "120 races" in the text, that's what gets uploaded! ✗

### How the Website Displays Data

**When someone clicks Texas on the election map:**

```javascript
// Website queries state-summaries table
const summary = await summaries_table.get({state: 'Texas'})

// Displays the 'content' field (the markdown text)
display(summary.content)  // Shows "Total Races: 120" if that's what's in the text!
```

**The website does NOT count the races table!** It just displays whatever text is in the summary.

### The Mismatch Problem

```
Database Reality:
├── races table: 40 records ✓ (CORRECT)
├── candidates table: 30 records ✓ (CORRECT)  
└── state-summaries content: "Total Races: 120" ✗ (WRONG TEXT!)

Website Shows: "120 races" ← Displays the wrong text from summary
```

### How the Fix Script Works

**When you run `fix_all_state_summaries.py`:**

```python
# Step 1: Count actual records in database
races = races_table.scan(state='Texas')  # Returns 40 records
actual_races = len(races)  # = 40

candidates = candidates_table.scan(state='Texas')  # Returns 30 records
actual_candidates = len(candidates)  # = 30

# Step 2: Get the summary text
summary = summaries_table.get(state='Texas')
content = summary['content']  # The full markdown text

# Step 3: Find and replace wrong numbers with correct ones
content = content.replace('Total Races: 120', 'Total Races: 40')
content = content.replace('Total Candidates: 300', 'Total Candidates: 30')

# Step 4: Save the corrected text back to database
summary['content'] = content
summaries_table.put_item(Item=summary)
```

**Result:**
```
Database After Fix:
├── races table: 40 records ✓
├── candidates table: 30 records ✓
└── state-summaries content: "Total Races: 40" ✓ (FIXED!)

Website Now Shows: "40 races" ← Correct!
```

### Key Insight

**The numbers in the summary are NOT calculated dynamically!**

They are **hardcoded text** that was written by the AI when it generated the script. If the AI writes the wrong numbers, those wrong numbers get uploaded to the database and displayed on the website.

**That's why verification is critical!**

---

## Step-by-Step Process

### 1. **Prepare the Prompt**
- Open `full_prompt.md`
- Replace `[STATE NAME]` with your target state (e.g., "Texas", "Florida")
- Copy the entire prompt

### 2. **Submit to AI**
- Paste the prompt into your AI tool (ChatGPT, Claude, etc.)
- Wait for the AI to generate the complete Python script

### 3. **Verify the Output**
The AI will provide a Python script with three main parts:

```python
races = [
    # 23 race objects (for example)
]

candidates = [
    # 45 candidate objects (for example)
]

summary = {
    "content": """
    ## 📊 Database Summary
    
    **Total Races Documented:** 23  ← MUST MATCH len(races)
    **Total Candidates Profiled:** 45  ← MUST MATCH len(candidates)
    """
}
```

### 4. **CRITICAL VERIFICATION**
Before running the script, manually verify:

✅ **Count the races array**:
```python
# Count the number of race dictionaries
races = [
    {...},  # 1
    {...},  # 2
    {...},  # 3
    # ... count them all
]
# If you count 23 races, the summary MUST say "23"
```

✅ **Count the candidates array**:
```python
# Count the number of candidate dictionaries
candidates = [
    {...},  # 1
    {...},  # 2
    {...},  # 3
    # ... count them all
]
# If you count 45 candidates, the summary MUST say "45"
```

✅ **Check the summary content**:
```python
summary = {
    "content": """
    **Total Races Documented:** 23  ← Does this match your count?
    **Total Candidates Profiled:** 45  ← Does this match your count?
    """
}
```

### 5. **Fix Mismatches (If Needed)**
If the numbers don't match:

**Option A: Manual Fix (Quick)**
```python
# Just edit the summary text to match the actual counts
summary = {
    "content": """
    **Total Races Documented:** 23  ← Change this number
    **Total Candidates Profiled:** 45  ← Change this number
    """
}
```

**Option B: Ask AI to Recount**
```
"Please recount the races and candidates arrays and update the Database Summary section with the exact counts. I count [X] races and [Y] candidates."
```

### 6. **Run the Script**
```bash
python upload_texas_data.py
```

The script will output:
```
Processing 23 Texas races...
[SUCCESS] Processed 23 races

Processing 45 Texas candidates...
[SUCCESS] Processed 45 candidates

[SUCCESS] Summary uploaded: 18,543 chars
```

**IMPORTANT: The script does NOT verify the numbers before uploading!**

The script:
1. ✓ Uploads races to database (23 records)
2. ✓ Uploads candidates to database (45 records)
3. ✓ Uploads summary text AS-IS (whatever numbers are in the text)

**It does NOT:**
- ✗ Check if summary numbers match array lengths
- ✗ Automatically fix wrong numbers
- ✗ Warn you if numbers are incorrect

**This means:** If the AI wrote "Total Races: 100" in the summary but only created 23 races in the array, the script will upload "100" to the database even though it's wrong!

**That's why YOU must verify BEFORE running the script!**

### Visual: What Gets Uploaded

```
AI Generates Script:
┌────────────────────────────────────────────────────────────┐
│ races = [{...}, {...}, {...}]  # 23 items                  │
│ candidates = [{...}, {...}]  # 45 items                   │
│ summary = {                                                │
│   "content": "Total Races: 100"  ← AI WROTE WRONG NUMBER! │
│ }                                                          │
└────────────────────────────────────────────────────────────┘
                    │
                    │ You run: python upload_texas_data.py
                    │
                    ↓
┌────────────────────────────────────────────────────────────┐
│ DynamoDB After Upload:                                    │
│                                                            │
│ races table: 23 records ✓ CORRECT                       │
│ candidates table: 45 records ✓ CORRECT                  │
│ state-summaries: "Total Races: 100" ✗ WRONG!            │
│                                                            │
│ Website will show: "100 races" ← DISPLAYS WRONG NUMBER! │
└────────────────────────────────────────────────────────────┘

The script uploads EXACTLY what the AI wrote - it doesn't verify!
```

### 7. **Verify on Website**
- Go to your election map page
- Click on the state
- Check that the summary shows the correct numbers

---

## Why This Matters

### The Problem We Solved:
Previously, AI would:
1. Create 40 races in the array
2. Create 30 candidates in the array
3. Write "Total Races: 120" in the summary (WRONG!)

This happened because the AI estimated or used placeholder numbers instead of counting the actual arrays.

### The Solution:
The updated prompt now:
1. Explicitly instructs AI to count: `len(races)` and `len(candidates)`
2. Provides verification checklist
3. Shows examples of correct vs incorrect

### What Happens If Numbers Are Wrong:
- Website shows incorrect counts
- Users see "120 races" but only 40 exist in database
- Looks unprofessional and confusing
- Requires running the fix script we just created

### What Happens If Numbers Are Correct:
- Website shows accurate counts
- Users see "40 races" and 40 races exist
- Professional and trustworthy
- No fix needed!

---

## Quick Reference

### Before Running Script:
```python
# 1. Count races
len(races)  # Should match summary

# 2. Count candidates  
len(candidates)  # Should match summary

# 3. Verify summary text matches
```

### After Running Script:
```bash
# Check the output
python upload_state_data.py

# Look for these lines:
# "Processed X races" ← Should match summary
# "Processed Y candidates" ← Should match summary
```

### If Website Shows Wrong Numbers:
```bash
# Run the fix script
python fix_all_state_summaries.py

# This will update all summaries to match actual database counts
```

---

## Pro Tips

1. **Always verify before running** - Takes 30 seconds, saves hours of fixing
2. **Use exact numbers** - Never "50+", "100-150", always "53", "147"
3. **Keep the fix script handy** - If you forget to verify, you can always fix it
4. **Test on one state first** - Before doing all 50 states, test the process
5. **Document your counts** - Keep a spreadsheet of state/races/candidates for reference

---

## Example Workflow

```
1. Copy full_prompt.md, replace [STATE NAME] with "Idaho"
2. Submit to AI
3. AI generates upload_idaho_data.py
4. Open file, count races array: 15 races
5. Count candidates array: 22 candidates
6. Check summary: "Total Races: 15" ✓ "Total Candidates: 22" ✓
7. Run: python upload_idaho_data.py
8. Check website: Idaho shows "15 races, 22 candidates" ✓
9. Done!
```

---

## Troubleshooting

**Q: AI gave me "50+ races" in the summary**
A: Edit the summary to show the exact count from your races array

**Q: I already uploaded with wrong numbers**
A: Run `python fix_all_state_summaries.py` to fix all states at once

**Q: How do I count a large array quickly?**
A: Use your code editor's line numbers or search for `{` in the array

**Q: Can I automate the counting?**
A: Yes! Add this to the end of your script:
```python
print(f"Races: {len(races)}, Candidates: {len(candidates)}")
```

---

## Success Checklist

Before uploading any state data:

- [ ] Counted races array manually
- [ ] Counted candidates array manually
- [ ] Verified summary shows exact counts
- [ ] Numbers match: len(races) = summary races count
- [ ] Numbers match: len(candidates) = summary candidates count
- [ ] Ready to run script!

After uploading:
- [ ] Script output shows correct counts
- [ ] Website displays correct counts
- [ ] No fix script needed!

---

**Remember: 30 seconds of verification saves hours of fixing!**
