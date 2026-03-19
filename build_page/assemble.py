"""
Assembles the-necessary-evil-book.html from parts in build_page/.
Run from the Downloader directory:
    python build_page/assemble.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
OUTPUT = os.path.join(ROOT, 'the-necessary-evil-book.html')

PARTS = [
    'part1_head.html',
    'part2_hero.html',
    'part2b_hook.html',
    'part3_kit.html',
    'part4_preview.html',
    'part5_content.html',
    'part6_purchase_author.html',
    'part7_modals_footer.html',
    'part8a_scripts_pdf.html',
    'part8b_scripts_paypal_signup.html',
]

content = ''
for part in PARTS:
    path = os.path.join(BASE, part)
    with open(path, 'r', encoding='utf-8') as f:
        content += f.read()

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Assembled {len(PARTS)} parts -> {OUTPUT}')
print(f'Total size: {len(content):,} characters')
