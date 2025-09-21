#!/usr/bin/env python3
"""Upgrade simple HTML files to include the site's common CSS and a basic header/nav.
Creates a .bak of each file before modifying.

It looks for files that contain a simple head (meta charset + viewport) and do NOT already
link to assets/css/common.min.css, then replaces the <head> content and injects a header
snippet after the opening <body> tag. It attempts to extract the page title from the first
<h1> on the page; otherwise a default site title is used.

Usage: python3 scripts/upgrade_html_template.py [directory]
If no directory given, uses repository root.
"""
from pathlib import Path
import re
import sys

DEFAULT_TITLE = "دليل المال العربي"

# Load template files if present
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / 'templates'
HEAD_INJECTION = ''
HEADER_SNIPPET = ''
FOOTER_SNIPPET = ''
if TEMPLATES_DIR.exists():
        head_file = TEMPLATES_DIR / 'head.html'
        header_file = TEMPLATES_DIR / 'header.html'
        footer_file = TEMPLATES_DIR / 'footer.html'
        if head_file.exists():
                HEAD_INJECTION = head_file.read_text(encoding='utf-8')
        else:
                HEAD_INJECTION = '''<meta charset="utf-8">\n  <meta name="viewport" content="width=device-width,initial-scale=1">\n  <link rel=\"stylesheet\" href=\"assets/css/common.min.css\">\n  <link rel=\"stylesheet\" href=\"assets/css/nav.min.css\">\n  <meta name=\"theme-color\" content=\"#0c7954\">\n  <meta property=\"og:image\" content=\"https://zezooo342.github.io/assets/images/og-default.png\"/>\n'''
        if header_file.exists():
                HEADER_SNIPPET = header_file.read_text(encoding='utf-8')
        else:
                HEADER_SNIPPET = '<header class="site-header">\n  <nav class="site-nav">\n    <a href="/index.html" class="logo">دليل المال العربي</a>\n  </nav>\n</header>\n'
        if footer_file.exists():
                FOOTER_SNIPPET = footer_file.read_text(encoding='utf-8')
        else:
                FOOTER_SNIPPET = '<footer class="site-footer">\n  <div class="wrap">\n    <p>© {year} دليل المال العربي — كل الحقوق محفوظة.</p>\n  </div>\n</footer>\n'


def extract_h1(text: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return DEFAULT_TITLE
    title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return title or DEFAULT_TITLE


def upgrade_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    # skip if already links common.min.css
    if 'assets/css/common.min.css' in text:
        return False

    # find head block
    head_match = re.search(r"<head>(.*?)</head>", text, flags=re.IGNORECASE | re.DOTALL)
    if not head_match:
        return False

    # create new head using extracted title
    title = extract_h1(text)
    new_head = f"<head>\n  <title>{title} | {DEFAULT_TITLE}</title>\n  {HEAD_INJECTION}</head>"

    new_text = text[:head_match.start()] + new_head + text[head_match.end():]

    # inject header snippet after opening body tag
    new_text, n = re.subn(r"<body( [^>]*)?>", lambda m: m.group(0) + "\n" + HEADER_SNIPPET, new_text, count=1, flags=re.IGNORECASE)
    if n == 0:
        # no <body> tag found, skip
        return False

    # insert footer before closing </body>
    year = str(__import__('datetime').datetime.today().year)
    footer = FOOTER_SNIPPET.replace('{year}', year)
    if '</body>' in new_text.lower():
        # case-insensitive replace closing body
        new_text = re.sub(r'</body>', footer + '\n</body>', new_text, flags=re.IGNORECASE, count=1)

    bak = path.with_suffix(path.suffix + '.bak')
    bak.write_text(text, encoding='utf-8')
    path.write_text(new_text, encoding='utf-8')
    return True


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    files = [p for p in base.glob('*.html')]
    updated = []
    for p in files:
        try:
            if upgrade_file(p):
                updated.append(p.name)
        except Exception as e:
            print(f"Failed to upgrade {p}: {e}")

    if updated:
        print("Upgraded files:", ", ".join(updated))
    else:
        print("No files needed upgrading or they already use site CSS.")


if __name__ == '__main__':
    main()
