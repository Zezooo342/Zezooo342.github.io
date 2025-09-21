#!/usr/bin/env python3
"""Add loading="lazy" to <img> tags in HTML files (if missing). Creates .bak before changes."""
from pathlib import Path
import re
import sys


def process_file(p: Path):
    text = p.read_text(encoding='utf-8')
    new_text, n = re.subn(r"<img(?![^>]*loading=)([^>]*)>", lambda m: f"<img{m.group(1)} loading=\"lazy\">", text, flags=re.IGNORECASE)
    if n:
        bak = p.with_suffix(p.suffix + '.bak')
        bak.write_text(text, encoding='utf-8')
        p.write_text(new_text, encoding='utf-8')
    return n


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    total = 0
    for p in base.glob('*.html'):
        try:
            n = process_file(p)
            if n:
                print(f"Updated {p.name}: {n} images")
                total += n
        except Exception as e:
            print(f"Error processing {p}: {e}")
    print(f"Total images updated: {total}")


if __name__ == '__main__':
    main()
