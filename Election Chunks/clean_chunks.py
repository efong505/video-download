import os
import re
import sys

# Get the directory containing chunk files
if len(sys.argv) > 1:
    chunk_dir = sys.argv[1]
else:
    chunk_dir = input("Enter the path to the chunk directory (e.g., P_Election_Chunks): ").strip()

# Make it absolute path if relative
if not os.path.isabs(chunk_dir):
    chunk_dir = os.path.join(os.getcwd(), chunk_dir)

if not os.path.exists(chunk_dir):
    print(f"Directory not found: {chunk_dir}")
    exit(1)

# Process all .txt files in the directory
for filename in os.listdir(chunk_dir):
    if filename.endswith('.txt') or filename.endswith('_output.txt'):
        filepath = os.path.join(chunk_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove chunk headers like "# CHUNK 5D: Pennsylvania Summary PART4"
        # This regex matches lines starting with # CHUNK followed by anything
        cleaned_content = re.sub(r'^#\s*CHUNK\s+\d+[A-Z]*:.*$', '', content, flags=re.MULTILINE)
        
        # Remove any leading/trailing whitespace
        cleaned_content = cleaned_content.strip()
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"Cleaned: {filename}")

print("\nAll chunks cleaned! Headers removed.")
