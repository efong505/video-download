"""
Generate all 3 PDF guides at once
Run: python build_pdfs/generate_all.py
"""
import subprocess
import os

BASE = os.path.dirname(os.path.abspath(__file__))

scripts = [
    'generate_survival_guide.py',
    'generate_discussion_guide.py',
    'generate_parent_guide.py'
]

print("Generating all PDF guides...\n")

for script in scripts:
    path = os.path.join(BASE, script)
    print(f"Running {script}...")
    result = subprocess.run(['python', path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")

print("\nAll PDFs generated successfully!")
print("\nGenerated files:")
print("  - christian-ai-survival-guide.pdf")
print("  - church-discussion-guide.pdf")
print("  - ai-parent-guide.pdf")
