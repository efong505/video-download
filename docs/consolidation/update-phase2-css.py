import os
import re
from datetime import datetime

# Pages that use card styles
CARD_PAGES = [
    'articles.html', 'news.html', 'resources.html', 'videos.html',
    'user-page.html', 'videos-from-s3.html', 'videos-live.html',
    'tag-page.html'
]

# Pages that use form styles
FORM_PAGES = [
    'admin.html', 'admin-pending-changes.html', 'admin-templates.html',
    'create-article.html', 'create-news.html', 'edit-article.html',
    'edit-news.html', 'login.html', 'register.html', 'apply-correspondent.html'
]

# CSS selectors to comment out for card styles
CARD_SELECTORS = [
    '.video-card', '.video-card:hover', '.thumbnail-container', '.thumbnail',
    '.play-button', '.play-button:hover', '.video-player',
    '.horizontal-scroll-container', '.scroll-wrapper', '.scroll-btn',
    '.scroll-btn:hover', '.scroll-btn-left', '.scroll-btn-right',
    '.article-card', '.article-card:hover', '.article-card-wrapper'
]

# CSS selectors to comment out for form styles
FORM_SELECTORS = [
    '.btn-primary', '.btn-primary:hover', '.btn-secondary', '.btn-secondary:hover',
    '.btn-danger', '.btn-danger:hover', '.loading', '.error', '.success',
    '.warning', '.form-control', '.form-control:focus', '.form-label',
    '.template-card', '.template-card:hover'
]

def backup_file(filepath):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{filepath}.backup_{timestamp}"
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return backup_path

def add_css_link(content, css_file, after='bootstrap'):
    # Find Bootstrap CSS link
    bootstrap_pattern = r'(<link[^>]*bootstrap[^>]*>)'
    match = re.search(bootstrap_pattern, content, re.IGNORECASE)
    
    if match:
        css_link = f'\n    <link rel="stylesheet" href="{css_file}">'
        insert_pos = match.end()
        content = content[:insert_pos] + css_link + content[insert_pos:]
        return content, True
    return content, False

def comment_out_selectors(content, selectors):
    count = 0
    for selector in selectors:
        # Escape special regex characters
        escaped = re.escape(selector)
        # Match selector and its rules
        pattern = rf'(\s*)({escaped}\s*{{[^}}]*}})'
        matches = list(re.finditer(pattern, content, re.DOTALL))
        
        for match in reversed(matches):  # Reverse to maintain positions
            indent = match.group(1)
            rule = match.group(2)
            commented = f'{indent}/* CONSOLIDATED TO card-styles.css or form-styles.css\n{indent}{rule}\n{indent}*/'
            content = content[:match.start()] + commented + content[match.end():]
            count += 1
    
    return content, count

def update_page(filepath, css_file, selectors):
    print(f"\n{'='*60}")
    print(f"Processing: {os.path.basename(filepath)}")
    print(f"{'='*60}\n")
    
    if not os.path.exists(filepath):
        print(f"[SKIP] File not found: {filepath}")
        return False
    
    # Create backup
    backup_path = backup_file(filepath)
    print(f"[OK] Backup created: {os.path.basename(backup_path)}")
    
    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add CSS link
    content, added = add_css_link(content, css_file)
    if added:
        print(f"[OK] Added {css_file} link after Bootstrap")
    else:
        print(f"[SKIP] Could not find Bootstrap link")
    
    # Comment out duplicate selectors
    content, count = comment_out_selectors(content, selectors)
    print(f"[OK] Commented out {count} duplicate styles")
    
    # Write updated file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n[OK] Updated: {os.path.basename(filepath)}")
    print(f"[OK] Backup: {os.path.basename(backup_path)}")
    
    return True

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    print("\n" + "="*60)
    print("CSS CONSOLIDATION - PHASE 2")
    print("="*60)
    print("\nUpdating pages with card-styles.css and form-styles.css\n")
    
    # Update card pages
    print("\n" + "="*60)
    print("CARD STYLES CONSOLIDATION")
    print("="*60)
    for page in CARD_PAGES:
        filepath = os.path.join(base_dir, page)
        update_page(filepath, 'assets/css/card-styles.css', CARD_SELECTORS)
    
    # Update form pages
    print("\n" + "="*60)
    print("FORM STYLES CONSOLIDATION")
    print("="*60)
    for page in FORM_PAGES:
        filepath = os.path.join(base_dir, page)
        update_page(filepath, 'assets/css/form-styles.css', FORM_SELECTORS)
    
    print("\n" + "="*60)
    print("PHASE 2 COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Test pages in browser")
    print("2. Upload to S3: card-styles.css, form-styles.css")
    print("3. Upload updated HTML pages")
    print("4. Create CloudFront invalidation")
    print("5. Commit to git")

if __name__ == '__main__':
    main()
