"""
CSS and JavaScript Audit Script
Analyzes all HTML pages to identify shared and unique dependencies
"""

import os
import re
from collections import defaultdict
import json

# Production pages only (exclude test/backup files)
PRODUCTION_PAGES = [
    'index.html',
    'videos.html',
    'articles.html',
    'article.html',
    'news.html',
    'news-article.html',
    'resources.html',
    'election-map.html',
    'admin.html',
    'admin-contributors.html',
    'admin-resources.html',
    'admin-templates.html',
    'admin-pending-changes.html',
    'create-article.html',
    'edit-article.html',
    'create-news.html',
    'edit-news.html',
    'article-preview.html',
    'draft-manager.html',
    'video-downloader.html',
    'download-status.html',
    'login.html',
    'profile.html',
    'category.html',
    'tag-page.html',
    'authors.html',
    'user-page.html',
    'apply-correspondent.html',
    'candidate-404.html',
    'embed.html',
    'video-player.html'
]

def extract_css_links(html_content):
    """Extract all CSS link tags"""
    pattern = r'<link[^>]*href=["\']([^"\']+\.css[^"\']*)["\'][^>]*>'
    return re.findall(pattern, html_content, re.IGNORECASE)

def extract_inline_css(html_content):
    """Extract inline style blocks"""
    pattern = r'<style[^>]*>(.*?)</style>'
    matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
    return [f"INLINE_STYLE_{i+1}" for i in range(len(matches))]

def extract_js_scripts(html_content):
    """Extract all JavaScript script tags"""
    # External scripts
    external_pattern = r'<script[^>]*src=["\']([^"\']+)["\'][^>]*>'
    external = re.findall(external_pattern, html_content, re.IGNORECASE)
    
    # Inline scripts
    inline_pattern = r'<script(?![^>]*src=)[^>]*>(.*?)</script>'
    inline_matches = re.findall(inline_pattern, html_content, re.DOTALL | re.IGNORECASE)
    inline = [f"INLINE_SCRIPT_{i+1}" for i in range(len(inline_matches))]
    
    return external, inline

def normalize_url(url):
    """Normalize URLs for comparison"""
    # Remove query parameters for CDN URLs
    if 'cdn.jsdelivr.net' in url or 'cdnjs.cloudflare.com' in url or 'unpkg.com' in url:
        url = url.split('?')[0]
    return url

def audit_pages():
    """Audit all production pages"""
    results = {}
    css_usage = defaultdict(list)
    js_usage = defaultdict(list)
    inline_css_count = defaultdict(int)
    inline_js_count = defaultdict(int)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for page in PRODUCTION_PAGES:
        filepath = os.path.join(base_dir, page)
        
        if not os.path.exists(filepath):
            print(f"WARNING: Skipping {page} (not found)")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract dependencies
        css_links = extract_css_links(content)
        inline_css = extract_inline_css(content)
        js_external, js_inline = extract_js_scripts(content)
        
        # Normalize URLs
        css_links = [normalize_url(url) for url in css_links]
        js_external = [normalize_url(url) for url in js_external]
        
        # Store results
        results[page] = {
            'css_external': css_links,
            'css_inline_count': len(inline_css),
            'js_external': js_external,
            'js_inline_count': len(js_inline)
        }
        
        # Track usage
        for css in css_links:
            css_usage[css].append(page)
        for js in js_external:
            js_usage[js].append(page)
        
        inline_css_count[page] = len(inline_css)
        inline_js_count[page] = len(js_inline)
    
    return results, css_usage, js_usage, inline_css_count, inline_js_count

def generate_report(results, css_usage, js_usage, inline_css_count, inline_js_count):
    """Generate comprehensive audit report"""
    
    report = []
    report.append("=" * 80)
    report.append("CSS AND JAVASCRIPT AUDIT REPORT")
    report.append("=" * 80)
    report.append("")
    
    # Summary
    total_pages = len(results)
    report.append(f"📊 SUMMARY")
    report.append(f"   Total Pages Analyzed: {total_pages}")
    report.append(f"   Unique External CSS Files: {len(css_usage)}")
    report.append(f"   Unique External JS Files: {len(js_usage)}")
    report.append("")
    
    # CSS Analysis
    report.append("=" * 80)
    report.append("CSS ANALYSIS")
    report.append("=" * 80)
    report.append("")
    
    # Sort by usage frequency
    css_sorted = sorted(css_usage.items(), key=lambda x: len(x[1]), reverse=True)
    
    report.append("📦 EXTERNAL CSS FILES (by usage frequency):")
    report.append("")
    for css, pages in css_sorted:
        usage_count = len(pages)
        percentage = (usage_count / total_pages) * 100
        report.append(f"   {css}")
        report.append(f"   Used in: {usage_count}/{total_pages} pages ({percentage:.1f}%)")
        if usage_count >= total_pages * 0.5:  # Used in 50%+ of pages
            report.append(f"   ✅ CANDIDATE FOR SHARED CSS")
        report.append(f"   Pages: {', '.join(pages[:5])}{' ...' if len(pages) > 5 else ''}")
        report.append("")
    
    # Inline CSS
    report.append("📝 INLINE CSS BLOCKS:")
    report.append("")
    for page, count in sorted(inline_css_count.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            report.append(f"   {page}: {count} inline <style> block(s)")
    report.append("")
    
    # JavaScript Analysis
    report.append("=" * 80)
    report.append("JAVASCRIPT ANALYSIS")
    report.append("=" * 80)
    report.append("")
    
    # Sort by usage frequency
    js_sorted = sorted(js_usage.items(), key=lambda x: len(x[1]), reverse=True)
    
    report.append("📦 EXTERNAL JAVASCRIPT FILES (by usage frequency):")
    report.append("")
    for js, pages in js_sorted:
        usage_count = len(pages)
        percentage = (usage_count / total_pages) * 100
        report.append(f"   {js}")
        report.append(f"   Used in: {usage_count}/{total_pages} pages ({percentage:.1f}%)")
        if usage_count >= total_pages * 0.5:  # Used in 50%+ of pages
            report.append(f"   ✅ CANDIDATE FOR SHARED JS")
        report.append(f"   Pages: {', '.join(pages[:5])}{' ...' if len(pages) > 5 else ''}")
        report.append("")
    
    # Inline JS
    report.append("📝 INLINE JAVASCRIPT BLOCKS:")
    report.append("")
    for page, count in sorted(inline_js_count.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            report.append(f"   {page}: {count} inline <script> block(s)")
    report.append("")
    
    # Recommendations
    report.append("=" * 80)
    report.append("CONSOLIDATION RECOMMENDATIONS")
    report.append("=" * 80)
    report.append("")
    
    # Shared CSS candidates
    shared_css = [css for css, pages in css_usage.items() if len(pages) >= total_pages * 0.5]
    report.append(f"🎯 CREATE SHARED CSS FILE (used in 50%+ of pages):")
    report.append("")
    for css in shared_css:
        report.append(f"   - {css}")
    report.append("")
    
    # Shared JS candidates
    shared_js = [js for js, pages in js_usage.items() if len(pages) >= total_pages * 0.5]
    report.append(f"🎯 CREATE SHARED JS FILE (used in 50%+ of pages):")
    report.append("")
    for js in shared_js:
        report.append(f"   - {js}")
    report.append("")
    
    # Page-specific dependencies
    report.append("=" * 80)
    report.append("PAGE-BY-PAGE BREAKDOWN")
    report.append("=" * 80)
    report.append("")
    
    for page in sorted(results.keys()):
        data = results[page]
        report.append(f"📄 {page}")
        report.append(f"   External CSS: {len(data['css_external'])}")
        report.append(f"   Inline CSS: {data['css_inline_count']}")
        report.append(f"   External JS: {len(data['js_external'])}")
        report.append(f"   Inline JS: {data['js_inline_count']}")
        report.append("")
    
    return "\n".join(report)

def main():
    print("Starting CSS and JavaScript audit...")
    print("")
    
    results, css_usage, js_usage, inline_css_count, inline_js_count = audit_pages()
    
    report = generate_report(results, css_usage, js_usage, inline_css_count, inline_js_count)
    
    # Save report
    output_file = 'CSS-JS-AUDIT-REPORT.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Audit complete! Report saved to: {output_file}")
    print("")
    print("Quick Summary:")
    print(f"   - {len(results)} pages analyzed")
    print(f"   - {len(css_usage)} unique CSS files")
    print(f"   - {len(js_usage)} unique JS files")
    print("")
    
    # Also save raw data as JSON
    json_output = {
        'results': results,
        'css_usage': {k: v for k, v in css_usage.items()},
        'js_usage': {k: v for k, v in js_usage.items()}
    }
    
    with open('css-js-audit-data.json', 'w', encoding='utf-8') as f:
        json.dump(json_output, f, indent=2)
    
    print(f"Raw data saved to: css-js-audit-data.json")

if __name__ == '__main__':
    main()
