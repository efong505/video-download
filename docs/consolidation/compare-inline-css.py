#!/usr/bin/env python3
"""
Compare inline CSS blocks across HTML pages to identify consolidation opportunities.
"""

import os
import re
from collections import defaultdict
from pathlib import Path

def extract_css_rules(css_content):
    """Extract individual CSS rules from a style block."""
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    # Extract rules (selector { properties })
    rules = re.findall(r'([^{]+)\{([^}]+)\}', css_content)
    
    normalized_rules = {}
    for selector, properties in rules:
        selector = selector.strip()
        # Normalize properties
        props = [p.strip() for p in properties.split(';') if p.strip()]
        props.sort()
        normalized_rules[selector] = props
    
    return normalized_rules

def extract_inline_css(html_file):
    """Extract all inline CSS from an HTML file."""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all <style> blocks
        style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
        
        all_rules = {}
        for block in style_blocks:
            rules = extract_css_rules(block)
            all_rules.update(rules)
        
        return all_rules
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
        return {}

def main():
    # Get all HTML files
    html_files = list(Path('.').glob('*.html'))
    
    # Extract CSS from each file
    file_css = {}
    for html_file in html_files:
        css_rules = extract_inline_css(html_file)
        if css_rules:
            file_css[html_file.name] = css_rules
    
    # Find common selectors
    selector_usage = defaultdict(list)
    for filename, rules in file_css.items():
        for selector in rules.keys():
            selector_usage[selector].append(filename)
    
    # Generate report
    print("=" * 80)
    print("INLINE CSS COMPARISON REPORT")
    print("=" * 80)
    print()
    
    # Common selectors (used in 3+ pages)
    common_selectors = {sel: files for sel, files in selector_usage.items() if len(files) >= 3}
    
    print(f"SUMMARY")
    print(f"   Total pages analyzed: {len(file_css)}")
    print(f"   Unique CSS selectors: {len(selector_usage)}")
    print(f"   Common selectors (3+ pages): {len(common_selectors)}")
    print()
    
    print("=" * 80)
    print("COMMON CSS SELECTORS (used in 3+ pages)")
    print("=" * 80)
    print()
    
    # Sort by usage frequency
    sorted_common = sorted(common_selectors.items(), key=lambda x: len(x[1]), reverse=True)
    
    for selector, files in sorted_common[:20]:  # Top 20
        print(f"TARGET: {selector}")
        print(f"   Used in {len(files)} pages ({len(files)/len(file_css)*100:.1f}%)")
        print(f"   Pages: {', '.join(sorted(files)[:5])}{'...' if len(files) > 5 else ''}")
        print()
    
    # Find exact duplicate rule sets
    print("=" * 80)
    print("EXACT DUPLICATE CSS RULES")
    print("=" * 80)
    print()
    
    rule_signatures = defaultdict(list)
    for filename, rules in file_css.items():
        for selector, properties in rules.items():
            signature = f"{selector}::{';'.join(properties)}"
            rule_signatures[signature].append(filename)
    
    duplicates = {sig: files for sig, files in rule_signatures.items() if len(files) >= 3}
    
    print(f"Found {len(duplicates)} CSS rules duplicated across 3+ pages")
    print()
    
    sorted_duplicates = sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True)
    
    for signature, files in sorted_duplicates[:10]:  # Top 10
        selector, props = signature.split('::', 1)
        print(f"DUPLICATE: {selector}")
        print(f"   Duplicated in {len(files)} pages")
        print(f"   Properties: {props[:100]}{'...' if len(props) > 100 else ''}")
        print(f"   Pages: {', '.join(sorted(files)[:5])}{'...' if len(files) > 5 else ''}")
        print()
    
    # Consolidation recommendations
    print("=" * 80)
    print("CONSOLIDATION RECOMMENDATIONS")
    print("=" * 80)
    print()
    
    print("HIGH PRIORITY (50%+ usage):")
    high_priority = [sel for sel, files in common_selectors.items() if len(files) >= len(file_css) * 0.5]
    for selector in sorted(high_priority)[:10]:
        files = selector_usage[selector]
        print(f"   - {selector} ({len(files)} pages)")
    print()
    
    print("MEDIUM PRIORITY (25-50% usage):")
    medium_priority = [sel for sel, files in common_selectors.items() 
                      if len(file_css) * 0.25 <= len(files) < len(file_css) * 0.5]
    for selector in sorted(medium_priority)[:10]:
        files = selector_usage[selector]
        print(f"   - {selector} ({len(files)} pages)")
    print()
    
    print("POTENTIAL SAVINGS:")
    total_rules = sum(len(rules) for rules in file_css.values())
    duplicate_rules = sum(len(files) - 1 for files in duplicates.values())
    print(f"   Total CSS rules: {total_rules}")
    print(f"   Duplicate rules: {duplicate_rules}")
    print(f"   Potential reduction: {duplicate_rules/total_rules*100:.1f}%")
    print()

if __name__ == '__main__':
    main()
