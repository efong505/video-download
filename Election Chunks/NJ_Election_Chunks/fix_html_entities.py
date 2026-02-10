import os
import html

# Fix all chunk output files
for filename in os.listdir('.'):
    if filename.endswith('_output.txt'):
        filepath = os.path.join('.', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Decode HTML entities
        fixed_content = html.unescape(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"Fixed: {filename}")

print("\nAll files fixed! Run combine_nj_chunks.py again.")
