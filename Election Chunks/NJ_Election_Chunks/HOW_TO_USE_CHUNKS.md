# How to Use Chunk Files to Generate Complete New Jersey Data

## The Problem
Grok AI has token output limits (~4,000-8,000 tokens) that prevent generating 128 races + 150 candidates + 27,500 word summary in one response.

## The Solution
Split the task into 8 separate chunks that can be run independently.

---

## Step-by-Step Process

### STEP 1: Run CHUNK_1_RACES.md in Grok

1. Open `CHUNK_1_RACES.md`
2. Copy the entire content
3. Paste into Grok AI
4. Grok will generate 128 races
5. Copy Grok's output (the Python races array)
6. Save to: `chunk1_output.txt`

**Expected output:** 
```python
races = [
    {"state": "New Jersey", "office": "U.S. Senate", ...},
    {"state": "New Jersey", "office": "U.S. House District 1", ...},
    # ... 128 total races
]
```

---

### STEP 2A: Run CHUNK_2A_CANDIDATES_1-25.md in Grok

1. Open `CHUNK_2A_CANDIDATES_1-25.md`
2. Copy the entire content
3. Paste into **NEW** Grok chat session
4. Grok will generate candidates 1-25
5. Copy Grok's output (just the candidate dictionaries, NOT the array wrapper)
6. Save to: `chunk2a_output.txt`

---

### STEP 2B: Run CHUNK_2B_CANDIDATES_26-50.md in Grok

1. Open `CHUNK_2B_CANDIDATES_26-50.md`
2. Copy the entire content
3. Paste into **NEW** Grok chat session
4. Grok will generate candidates 26-50
5. Copy Grok's output
6. Save to: `chunk2b_output.txt`

**Expected output:**
```python
    {"name": "Cory Booker", "state": "New Jersey", ...},
    {"name": "Christine Serrano Glassner", ...},
    # ... 50 total candidates
```

---

### STEP 3: Run CHUNK_3_CANDIDATES_51-100.md in Grok

1. Open `CHUNK_3_CANDIDATES_51-100.md`
2. Copy the entire content
3. Paste into **NEW** Grok chat session
4. Grok will generate candidates 51-100
5. Copy Grok's output
6. Save to: `chunk3_output.txt`

---

### STEP 4: Run CHUNK_4_CANDIDATES_101-150.md in Grok

1. Open `CHUNK_4_CANDIDATES_101-150.md`
2. Copy the entire content
3. Paste into **NEW** Grok chat session
4. Grok will generate candidates 101-150
5. Copy Grok's output
6. Save to: `chunk4_output.txt`

---

### STEP 5: Run CHUNK_5A_PART1.md in Grok

1. Open `CHUNK_5A_PART1.md`
2. Copy the entire content
3. Paste into **NEW** Grok chat session
4. Grok will generate summary part 1 (Database Summary + Political Landscape + Federal Races)
5. Copy Grok's output (the markdown content)
6. Save to: `chunk5a_output.txt`

---

### STEP 6: Run CHUNK_5B_PART2.md in Grok

1. Open `CHUNK_5B_PART2.md`
2. Copy the entire content
3. Paste into **NEW** Grok chat session
4. Grok will generate summary part 2 (State Legislative + School Board Races)
5. Copy Grok's output
6. Save to: `chunk5b_output.txt`

---

### STEP 7: Run CHUNK_5C_PART3.md in Grok

1. Open `CHUNK_5C_PART3.md`
2. Copy the entire content
3. Paste into **NEW** Grok chat session
4. Grok will generate summary part 3 (Municipal + County + Key Issues)
5. Copy Grok's output
6. Save to: `chunk5c_output.txt`

---

### STEP 8: Run CHUNK_5D_PART4.md in Grok

1. Open `CHUNK_5D_PART4.md`
2. Copy the entire content
3. Paste into **NEW** Grok chat session
4. Grok will generate summary part 4 (Church Mobilization + Dates + Bottom Line + Prayer)
5. Copy Grok's output
6. Save to: `chunk5d_output.txt`

---

### STEP 9: Combine All Chunks

1. Make sure all 8 output files are in `C:\Users\Ed\Downloads\`:
   - chunk1_output.txt
   - chunk2_output.txt
   - chunk3_output.txt
   - chunk4_output.txt
   - chunk5a_output.txt
   - chunk5b_output.txt
   - chunk5c_output.txt
   - chunk5d_output.txt

2. Run the combiner script:
   ```bash
   cd C:\Users\Ed\Downloads
   python combine_nj_chunks.py
   ```

3. This creates: `upload_new_jersey_data.py`

---

### STEP 10: Upload to DynamoDB

1. Review the generated file: `upload_new_jersey_data.py`
2. Run it:
   ```bash
   python upload_new_jersey_data.py
   ```

---

## Tips

- **Use separate Grok chat sessions** for each chunk to avoid context confusion
- **Save outputs immediately** after each chunk generation
- **Check for placeholders** like "..." or "[Continue]" - if you see them, the chunk failed and needs to be re-run
- **Verify counts** at the end of each chunk output
- If a chunk fails, just re-run that specific chunk - no need to start over

---

## File Structure

```
C:\Users\Ed\Downloads\
├── CHUNK_1_RACES.md              (Input: prompt for races)
├── CHUNK_2_CANDIDATES_1-50.md    (Input: prompt for candidates 1-50)
├── CHUNK_3_CANDIDATES_51-100.md  (Input: prompt for candidates 51-100)
├── CHUNK_4_CANDIDATES_101-150.md (Input: prompt for candidates 101-150)
├── CHUNK_5A_PART1.md             (Input: prompt for summary part 1)
├── CHUNK_5B_PART2.md             (Input: prompt for summary part 2)
├── CHUNK_5C_PART3.md             (Input: prompt for summary part 3)
├── CHUNK_5D_PART4.md             (Input: prompt for summary part 4)
├── chunk1_output.txt             (Output: races from Grok)
├── chunk2_output.txt             (Output: candidates 1-50 from Grok)
├── chunk3_output.txt             (Output: candidates 51-100 from Grok)
├── chunk4_output.txt             (Output: candidates 101-150 from Grok)
├── chunk5a_output.txt            (Output: summary part 1 from Grok)
├── chunk5b_output.txt            (Output: summary part 2 from Grok)
├── chunk5c_output.txt            (Output: summary part 3 from Grok)
├── chunk5d_output.txt            (Output: summary part 4 from Grok)
├── combine_nj_chunks.py          (Script to combine all outputs)
└── upload_new_jersey_data.py     (Final combined script - ready to run)
```

---

## Expected Results

- **128 races** (80 Assembly + 22 School Boards + 13 Federal + 9 County + 4 Statewide)
- **150 candidates** (50 + 50 + 50)
- **27,500+ word summary** (7,000 + 6,000 + 8,000 + 6,500)
- **Complete Python script** ready to upload to DynamoDB

---

## Troubleshooting

**Problem:** Grok abbreviates with "..." or "[Continue]"
**Solution:** Re-run that specific chunk with emphasis on "NO ABBREVIATIONS"

**Problem:** Chunk output has syntax errors
**Solution:** Manually fix the Python syntax before combining

**Problem:** combine_nj_chunks.py fails
**Solution:** Check that all 8 output files exist and have content

**Problem:** Candidate counts don't match
**Solution:** Verify each chunk output has exactly 50 candidates (except chunk 4 which may have fewer)
