import json
import re

# Read all chunk2 files and extract unique candidates
all_candidates = []
seen = set()

for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']:
    filename = f'chunk2{letter}_output.txt'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract candidates array
            content = content.replace('candidates = [', '').strip()
            if content.endswith(']'):
                content = content[:-1].strip()
            
            # Parse candidates (simple regex approach)
            candidates = re.findall(r'\{[^}]+\}', content, re.DOTALL)
            
            for candidate_str in candidates:
                # Extract name and office
                name_match = re.search(r'"name":\s*"([^"]+)"', candidate_str)
                office_match = re.search(r'"office":\s*"([^"]+)"', candidate_str)
                
                if name_match and office_match:
                    name = name_match.group(1)
                    office = office_match.group(1)
                    key = (name, office)
                    
                    if key not in seen:
                        seen.add(key)
                        all_candidates.append(candidate_str)
                        print(f"Added: {name} - {office}")
                    else:
                        print(f"SKIPPED DUPLICATE: {name} - {office}")
    except FileNotFoundError:
        print(f"File not found: {filename}")

print(f"\n\nTotal unique candidates: {len(all_candidates)}")
print(f"Duplicates removed: {119 - len(all_candidates)}")

# Write deduplicated candidates to new file
with open('chunk2_deduplicated.txt', 'w', encoding='utf-8') as f:
    f.write('candidates = [\n')
    f.write(',\n'.join(all_candidates))
    f.write('\n]')

print("\nCreated: chunk2_deduplicated.txt")
print("Now update combine script to use this file instead of individual chunks")
