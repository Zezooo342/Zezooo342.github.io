#!/usr/bin/env python3
"""
HTML Template Updater for Arab Money Guide
محدث قوالب HTML لدليل المال العربي

This script helps automate the remaining HTML page updates to ensure:
- Consistent viewport meta tags
- Unified navigation structure  
- Updated JSON-LD structured data dates
- Proper CSS/JS linking to assets/

Usage: python update_html_template.py
"""

import glob
import re
import os
from datetime import datetime

def add_viewport_meta(content):
    """Add viewport meta tag if missing"""
    if 'viewport' not in content:
        # Add after charset
        content = re.sub(
            r'(<meta charset=["\'][^"\']*["\']>\s*)',
            r'\1  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n',
            content
        )
    return content

def update_json_ld_date(content):
    """Update JSON-LD datePublished to current date"""
    current_date = "2025-09-16"
    
    # Update datePublished
    content = re.sub(
        r'"datePublished":\s*"[^"]*"',
        f'"datePublished": "{current_date}"',
        content
    )
    
    # Add dateModified if missing
    if '"dateModified"' not in content:
        content = re.sub(
            r'("datePublished":\s*"[^"]*"),',
            r'\1,\n    "dateModified": "' + current_date + '",',
            content
        )
    
    return content

def standardize_navigation(content):
    """Ensure consistent navigation structure"""
    standard_nav = '''<nav>
  <ul>
    <li><a href="index.html">الرئيسية</a></li>
    <li><a href="article.html">مقالات</a></li>
    <li><a href="about.html">من نحن</a></li>
    <li><a href="contact.html">تواصل</a></li>
    <li><a href="privacy.html">الخصوصية</a></li>
    <li><a href="legal/terms.html">الشروط</a></li>
  </ul>
</nav>'''
    
    # Replace existing nav if it has old structure
    nav_pattern = r'<nav>.*?</nav>'
    if re.search(nav_pattern, content, re.DOTALL):
        content = re.sub(nav_pattern, standard_nav, content, flags=re.DOTALL)
    
    return content

def update_css_js_links(content, filename):
    """Update CSS and JS links to use assets/ directory"""
    # Update CSS link to use assets/css/style.css
    if 'assets/css/style.css' not in content and '<style>' in content:
        # Add CSS link before </head>
        css_link = '  <link rel="stylesheet" href="assets/css/style.css">\n'
        content = re.sub(r'</head>', css_link + '</head>', content)
    
    # Add JS script before closing body tag if not present
    if 'assets/js/main.js' not in content:
        js_script = '\n<script src="assets/js/main.js" defer></script>\n'
        content = re.sub(r'</body>', js_script + '</body>', content)
    
    return content

def add_last_updated_meta(content):
    """Add last updated meta information"""
    if 'آخر تحديث:' not in content:
        # Add before closing main div
        update_meta = '  \n  <p class="meta">آخر تحديث: 16 سبتمبر 2025</p>\n'
        content = re.sub(r'</div>\s*<footer>', update_meta + '</div>\n\n<footer>', content)
    
    return content

def process_html_file(filepath):
    """Process a single HTML file with all updates"""
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Apply all transformations
    content = add_viewport_meta(content)
    content = update_json_ld_date(content)
    content = standardize_navigation(content)
    content = update_css_js_links(content, filepath)
    content = add_last_updated_meta(content)
    
    # Only write if content changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated {filepath}")
        return True
    else:
        print(f"ℹ️  No changes needed for {filepath}")
        return False

def main():
    """Main function to process all HTML files"""
    print("🔄 Starting HTML template update process...")
    
    # Get all HTML files except index.html and files in legal/ directory
    html_files = []
    for pattern in ['*.html']:
        html_files.extend(glob.glob(pattern))
    
    # Filter out files we don't want to auto-process
    skip_files = ['index.html', 'amp-article.html']  # Keep AMP separate, index has special structure
    html_files = [f for f in html_files if os.path.basename(f) not in skip_files]
    
    updated_count = 0
    
    for filepath in sorted(html_files):
        if process_html_file(filepath):
            updated_count += 1
    
    print(f"\n✅ Template update completed!")
    print(f"📊 Updated {updated_count} out of {len(html_files)} files")
    print(f"🎯 Ready for AdSense compliance review")

if __name__ == "__main__":
    main()