"""
Fix CHUNK_5C and CHUNK_5D templates for Large states (20+ districts).
Replaces placeholder templates with comprehensive detailed templates.
"""

import os

# Large states (20+ districts) that need CHUNK_5C and CHUNK_5D
LARGE_STATES = {
    "California": 52,
    "Texas": 38,
    "Florida": 28,
    "New York": 26
}

# Read template files
with open("CHUNK_5C_TEMPLATE.md", 'r', encoding='utf-8') as f:
    chunk5c_template = f.read()

with open("CHUNK_5D_TEMPLATE.md", 'r', encoding='utf-8') as f:
    chunk5d_template = f.read()

# Update each large state
for state, districts in LARGE_STATES.items():
    state_dir = f"COMPLETE_STATE_TEMPLATES/{state.replace(' ', '_')}"
    
    # Update CHUNK_5C
    chunk5c_path = f"{state_dir}/CHUNK_5C_SUMMARY_PART3.md"
    with open(chunk5c_path, 'w', encoding='utf-8') as f:
        f.write(chunk5c_template.format(STATE=state.upper(), state=state))
    print(f"Updated: {chunk5c_path}")
    
    # Update CHUNK_5D
    chunk5d_path = f"{state_dir}/CHUNK_5D_SUMMARY_PART4.md"
    with open(chunk5d_path, 'w', encoding='utf-8') as f:
        f.write(chunk5d_template.format(STATE=state.upper(), state=state))
    print(f"Updated: {chunk5d_path}")

print(f"\nFixed CHUNK_5C and CHUNK_5D for {len(LARGE_STATES)} large states")
print("\nNOTE: Medium and Small states should NOT use CHUNK_5C/5D")
print("  - Small states: Use only CHUNK_5A")
print("  - Medium states: Use CHUNK_5A + CHUNK_5B")
print("  - Large states: Use CHUNK_5A + CHUNK_5B + CHUNK_5C + CHUNK_5D")
