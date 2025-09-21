#!/usr/bin/env python3
"""Script: إصلاح رؤوس صفحات HTML المفقودة (DOCTYPE, head charset, html lang/dir)
ينسخ الملفات الأصلية إلى ملف بلاحقة .bak ثم يضيف ترويسة HTML إذا كانت مفقودة.
Usage: python scripts/fix_html_headers.py [path]
If path omitted, fixes .html files in repository root.
"""
from pathlib import Path
import sys

TEMPLATE_HEAD = ("<!doctype html>\n<html lang=\"ar\" dir=\"rtl\">\n<head>\n  <meta charset=\"utf-8\">\n  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n</head>\n<body>\n")

TEMPLATE_FOOT = "\n</body>\n</html>\n"


def is_fragment(content: str) -> bool:
    """Return True if the file looks like an HTML fragment (missing <html> or <!doctype>)."""
    low = content.lower()
    return not ("<!doctype" in low or "<html" in low)


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not is_fragment(text):
        return False
    bak = path.with_suffix(path.suffix + ".bak")
    bak.write_text(text, encoding="utf-8")
    new_text = TEMPLATE_HEAD + text + TEMPLATE_FOOT
    path.write_text(new_text, encoding="utf-8")
    return True


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    files = []
    if base.is_dir():
        files = list(base.glob('*.html'))
    elif base.is_file():
        files = [base]
    else:
        print("Path not found:", base)
        return

    fixed = []
    for f in files:
        try:
            if fix_file(f):
                fixed.append(f.name)
        except Exception as e:
            print(f"Failed to fix {f}: {e}")

    if fixed:
        print("Fixed files:", ", ".join(fixed))
    else:
        print("No fragment HTML files found or nothing to fix.")


if __name__ == '__main__':
    main()
