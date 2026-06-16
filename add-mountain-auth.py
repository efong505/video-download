"""
Add authentication check to all mountain hub pages
"""

import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# List of mountain hub pages (excluding 7-mountains.html which stays public)
mountain_pages = [
    'religion-mountain.html',
    'education-mountain.html',
    'media-mountain.html',
    'art-mountain.html',
    'government-mountain.html'
]

base_path = r'c:\Users\Ed\Documents\Programming\AWS\Downloader'

auth_script = '''    <!-- Authentication Check -->
    <script src="mountain-hub-auth.js"></script>
    '''

for page in mountain_pages:
    file_path = os.path.join(base_path, page)
    
    if not os.path.exists(file_path):
        print(f"⚠️  File not found: {page}")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if auth script already added
    if 'mountain-hub-auth.js' in content:
        print(f"✓ Already has auth: {page}")
        continue
    
    # Add auth script right after <body> tag
    if '<body>' in content:
        content = content.replace('<body>', f'<body>\n{auth_script}')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Added auth to: {page}")
    else:
        print(f"❌ No <body> tag found in: {page}")

print("\n✅ Done! All mountain hub pages now require authentication.")
