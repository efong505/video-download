import re

all_candidates = []
seen = set()

for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']:
    filename = f'chunk2{letter}_output.txt'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Remove wrapper
            content = content.replace('candidates = [', '').strip()
            if content.endswith(']'):
                content = content[:-1].strip()
            
            # Split by },\n{ pattern to get individual candidates
            # Add back the braces
            parts = content.split('},')
            
            for i, part in enumerate(parts):
                if not part.strip():
                    continue
                    
                # Add back closing brace if not last item
                if i < len(parts) - 1:
                    candidate_str = part.strip() + '}'
                else:
                    candidate_str = part.strip()
                
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
                        print(f"SKIPPED: {name} - {office}")
    except FileNotFoundError:
        print(f"Not found: {filename}")

print(f"\nUnique: {len(all_candidates)}")

# Write deduplicated
with open('chunk2_deduplicated.txt', 'w', encoding='utf-8') as f:
    f.write('candidates = [\n')
    for i, cand in enumerate(all_candidates):
        f.write('    ' + cand)
        if i < len(all_candidates) - 1:
            f.write(',\n')
        else:
            f.write('\n')
    f.write(']')

print("Created: chunk2_deduplicated.txt")
