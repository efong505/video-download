#!/usr/bin/env python3
"""
Update a page to use common-styles.css with automatic backup and revert capability.
Usage: python update-page-css.py <filename>
"""

import sys
import shutil
import re
from pathlib import Path
from datetime import datetime

def backup_file(filepath):
    """Create timestamped backup of file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{filepath}.backup_{timestamp}"
    shutil.copy2(filepath, backup_path)
    print(f"[OK] Backup created: {backup_path}")
    return backup_path

def extract_nav_styles(content):
    """Extract navigation-related CSS that should be removed."""
    patterns = [
        r'\.dashboard-header\s*{[^}]+}',
        r'\.dashboard-nav\s*{[^}]+}',
        r'\.nav-brand\s*{[^}]+}',
        r'\.nav-links\s*{[^}]+}',
        r'\.nav-link\s*{[^}]+}',
        r'\.nav-link:hover\s*{[^}]+}',
        r'\.nav-link\.logout\s*{[^}]+}',
        r'\.nav-link\.logout:hover\s*{[^}]+}',
    ]
    
    found_styles = []
    for pattern in patterns:
        matches = re.findall(pattern, content, re.DOTALL)
        found_styles.extend(matches)
    
    return found_styles

def update_page(filepath):
    """Update page to use common-styles.css."""
    print(f"\n{'='*60}")
    print(f"Processing: {filepath}")
    print(f"{'='*60}\n")
    
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already using common-styles.css
    if 'assets/css/common-styles.css' in content:
        print("[SKIP] Page already uses common-styles.css")
        return False
    
    # Create backup
    backup_path = backup_file(filepath)
    
    # Find styles to remove
    nav_styles = extract_nav_styles(content)
    print(f"[OK] Found {len(nav_styles)} navigation styles to remove")
    
    # Add link to common-styles.css after Bootstrap
    if 'bootstrap' in content.lower():
        # Add after Bootstrap CSS
        content = re.sub(
            r'(<link[^>]*bootstrap[^>]*>)',
            r'\1\n    <link rel="stylesheet" href="assets/css/common-styles.css">',
            content,
            count=1
        )
        print("[OK] Added common-styles.css link after Bootstrap")
    else:
        # Add in <head> section
        content = re.sub(
            r'(<head[^>]*>)',
            r'\1\n    <link rel="stylesheet" href="assets/css/common-styles.css">',
            content,
            count=1
        )
        print("[OK] Added common-styles.css link in <head>")
    
    # Remove navigation styles (keep them commented for safety)
    for style in nav_styles:
        comment = f"/* MOVED TO common-styles.css\n{style}\n*/"
        content = content.replace(style, comment)
    
    print(f"[OK] Commented out {len(nav_styles)} duplicate styles")
    
    # Write updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n[OK] Updated: {filepath}")
    print(f"[OK] Backup: {backup_path}")
    print(f"\n{'='*60}")
    print("NEXT STEPS:")
    print("1. Open the page in browser and test")
    print("2. If it works: Keep changes")
    print(f"3. If broken: Run revert script with {backup_path}")
    print(f"{'='*60}\n")
    
    return True

def revert_file(backup_path):
    """Revert file from backup."""
    original_path = re.sub(r'\.backup_\d{8}_\d{6}$', '', backup_path)
    
    if not Path(backup_path).exists():
        print(f"[ERROR] Backup not found: {backup_path}")
        return False
    
    shutil.copy2(backup_path, original_path)
    print(f"[OK] Reverted: {original_path}")
    print(f"[OK] From backup: {backup_path}")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python update-page-css.py <filename>")
        print("   or: python update-page-css.py revert <backup_file>")
        sys.exit(1)
    
    if sys.argv[1] == 'revert':
        if len(sys.argv) < 3:
            print("Usage: python update-page-css.py revert <backup_file>")
            sys.exit(1)
        revert_file(sys.argv[2])
    else:
        filepath = sys.argv[1]
        if not Path(filepath).exists():
            print(f"[ERROR] File not found: {filepath}")
            sys.exit(1)
        update_page(filepath)

if __name__ == '__main__':
    main()
