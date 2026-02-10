"""
Generate consistent CHUNK files for all 50 states using master template.
Ensures New Jersey's structure, style, and formatting carries to all states.
"""

# State configuration
STATES = {
    "Alabama": {"districts": 7, "senate_year": 2026, "gov_year": 2026},
    "Alaska": {"districts": 1, "senate_year": None, "gov_year": 2026},
    "Arizona": {"districts": 9, "senate_year": None, "gov_year": 2026},
    "Arkansas": {"districts": 4, "senate_year": None, "gov_year": 2026},
    "California": {"districts": 52, "senate_year": None, "gov_year": 2026},
    "Colorado": {"districts": 8, "senate_year": None, "gov_year": 2026},
    "Connecticut": {"districts": 5, "senate_year": None, "gov_year": 2026},
    "Delaware": {"districts": 1, "senate_year": 2026, "gov_year": None},
    "Florida": {"districts": 28, "senate_year": None, "gov_year": 2026},
    "Georgia": {"districts": 14, "senate_year": 2026, "gov_year": 2026},
    "Hawaii": {"districts": 2, "senate_year": None, "gov_year": 2026},
    "Idaho": {"districts": 2, "senate_year": 2026, "gov_year": 2026},
    "Illinois": {"districts": 17, "senate_year": None, "gov_year": 2026},
    "Indiana": {"districts": 9, "senate_year": None, "gov_year": 2026},
    "Iowa": {"districts": 4, "senate_year": 2026, "gov_year": 2026},
    "Kansas": {"districts": 4, "senate_year": 2026, "gov_year": 2026},
    "Kentucky": {"districts": 6, "senate_year": None, "gov_year": 2027},
    "Louisiana": {"districts": 6, "senate_year": 2026, "gov_year": 2027},
    "Maine": {"districts": 2, "senate_year": 2026, "gov_year": 2026},
    "Maryland": {"districts": 8, "senate_year": None, "gov_year": 2026},
    "Massachusetts": {"districts": 9, "senate_year": None, "gov_year": 2026},
    "Michigan": {"districts": 13, "senate_year": 2026, "gov_year": 2026},
    "Minnesota": {"districts": 8, "senate_year": 2026, "gov_year": 2026},
    "Mississippi": {"districts": 4, "senate_year": 2026, "gov_year": 2027},
    "Missouri": {"districts": 8, "senate_year": None, "gov_year": 2026},
    "Montana": {"districts": 2, "senate_year": None, "gov_year": 2026},
    "Nebraska": {"districts": 3, "senate_year": 2026, "gov_year": 2026},
    "Nevada": {"districts": 4, "senate_year": None, "gov_year": 2026},
    "New Hampshire": {"districts": 2, "senate_year": 2026, "gov_year": 2026},
    "New Jersey": {"districts": 12, "senate_year": 2026, "gov_year": 2025},
    "New Mexico": {"districts": 3, "senate_year": 2026, "gov_year": 2026},
    "New York": {"districts": 26, "senate_year": None, "gov_year": 2026},
    "North Carolina": {"districts": 14, "senate_year": 2026, "gov_year": 2026},
    "North Dakota": {"districts": 1, "senate_year": None, "gov_year": 2026},
    "Ohio": {"districts": 15, "senate_year": None, "gov_year": 2026},
    "Oklahoma": {"districts": 5, "senate_year": 2026, "gov_year": 2026},
    "Oregon": {"districts": 6, "senate_year": 2026, "gov_year": 2026},
    "Pennsylvania": {"districts": 17, "senate_year": None, "gov_year": 2026},
    "Rhode Island": {"districts": 2, "senate_year": 2026, "gov_year": 2026},
    "South Carolina": {"districts": 7, "senate_year": 2026, "gov_year": 2026},
    "South Dakota": {"districts": 1, "senate_year": 2026, "gov_year": 2026},
    "Tennessee": {"districts": 9, "senate_year": None, "gov_year": 2026},
    "Texas": {"districts": 38, "senate_year": None, "gov_year": 2026},
    "Utah": {"districts": 4, "senate_year": None, "gov_year": 2026},
    "Vermont": {"districts": 1, "senate_year": None, "gov_year": 2026},
    "Virginia": {"districts": 11, "senate_year": 2026, "gov_year": 2025},
    "Washington": {"districts": 10, "senate_year": None, "gov_year": 2026},
    "West Virginia": {"districts": 2, "senate_year": 2026, "gov_year": 2026},
    "Wisconsin": {"districts": 8, "senate_year": None, "gov_year": 2026},
    "Wyoming": {"districts": 1, "senate_year": 2026, "gov_year": 2026}
}

def calculate_words(districts):
    """Calculate word counts based on state size"""
    if districts >= 20:  # Large states
        federal = 8000
        state_races = 4000
    elif districts >= 10:  # Medium states
        federal = 6000
        state_races = 3000
    else:  # Small states
        federal = 4000
        state_races = 2000
    
    total = 2000 + federal + state_races + 3000 + 2000
    return federal, state_races, total

def generate_chunk5a(state_name, config):
    """Generate CHUNK_5A for a state"""
    districts = config["districts"]
    federal_words, state_words, total_words = calculate_words(districts)
    
    # Determine federal race type
    if config["senate_year"] == 2026:
        federal_race = f"Senate + ALL {districts} House Districts"
    elif config["gov_year"] in [2025, 2026]:
        federal_race = f"Governor + ALL {districts} House Districts"
    else:
        federal_race = f"ALL {districts} House Districts"
    
    template = f"""# CHUNK 5A: {state_name.upper()} SUMMARY - PART 1

## TASK: Generate FIRST HALF of summary only

**This chunk covers:**
1. Database Summary + Political Landscape (2,000 words)
2. 2026 Federal Races - {federal_race} ({federal_words:,} words)
3. 2025 State Races ({state_words:,} words)
4. 2025 School Board Races (3,000 words)
5. 2025 Municipal Races (2,000 words)

**TOTAL FOR PART 1: {total_words:,} words minimum**

## 🚨 CRITICAL ANTI-ABBREVIATION RULES:

### ABSOLUTELY FORBIDDEN:
- ❌ "[REPEAT FOR Districts 2-{districts}]"
- ❌ "[Full format]"
- ❌ "[Continue...]"
- ❌ "etc."
- ❌ "..."
- ❌ "(2,847 words)"
- ❌ "D" or "R" abbreviations

### ABSOLUTELY REQUIRED:
- ✅ Write EVERY House district (1-{districts}) completely with full candidate profiles
- ✅ Write EVERY school board completely with full candidate profiles
- ✅ Full paragraphs, no shortcuts
- ✅ Spell out "Democrat" and "Republican" every time

## OUTPUT FORMAT:

```markdown
# {state_name} 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** [NUMBER]
**Total Candidates Profiled:** [NUMBER]
**Election Dates:**
- November 4, 2025 (State/Local Races)
- November 3, 2026 (Federal Races)

---

## 🔴 {state_name.upper()} POLITICAL LANDSCAPE

[Write 5-7 full paragraphs covering political landscape, urban-rural divide, why {state_name} matters, conservative opportunities, etc. MINIMUM 2,000 words]

---

[FEDERAL RACES - FULL FORMAT FOR EACH RACE]

---

## 🔴 2026 U.S. HOUSE RACES

### **U.S. House District 1** - November 3, 2026

[COMPLETE FORMAT - NO ABBREVIATIONS]

[REPEAT FOR ALL {districts} DISTRICTS]

---

## 🔴 2025 STATE RACES

[State-specific races with full candidate profiles]

---

## 🔴 2025 SCHOOL BOARD RACES

[Major school districts with full candidate profiles]

---

## 🔴 2025 MUNICIPAL RACES

[Major cities with full candidate profiles]

---

**END OF PART 1**

Word count for Part 1: [Count and verify minimum {total_words:,} words]
```

## VERIFICATION:
Count words and confirm:
- Section 1 (Landscape): 2,000+ words
- Section 2 (Federal): {federal_words:,}+ words
- Section 3 (State): {state_words:,}+ words
- Section 4 (School Boards): 3,000+ words
- Section 5 (Municipal): 2,000+ words

**TOTAL PART 1: {total_words:,}+ words**

Generate Part 1 now with NO abbreviations or shortcuts.
"""
    return template

# Generate for all states
import os

output_dir = "STATE_TEMPLATES"
os.makedirs(output_dir, exist_ok=True)

for state, config in STATES.items():
    chunk5a = generate_chunk5a(state, config)
    filename = f"{output_dir}/{state.replace(' ', '_')}_CHUNK_5A.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(chunk5a)
    print(f"Generated: {filename}")

print(f"\nGenerated {len(STATES)} state templates")
print(f"All templates use New Jersey's structure")
print(f"Location: {output_dir}/")
