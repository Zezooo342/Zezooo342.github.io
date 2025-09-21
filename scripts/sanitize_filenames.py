#!/usr/bin/env python3
"""Rename unsafe filenames (spaces, apostrophes, special chars) to web-safe names
and update internal links in HTML files. Creates .bak backups of changed files.

Usage: python scripts/sanitize_filenames.py [directory]
If no directory is given, uses repository root.
"""
from pathlib import Path
import re
import sys


def safe_name(name: str) -> str:
    # keep extension
    p = Path(name)
    stem = p.stem
    ext = p.suffix
    # replace spaces and apostrophes with underscore
    s = stem
    s = s.replace(" ", "_")
    s = s.replace("'", "_")
    # remove characters that are not alnum, underscore, hyphen
    s = re.sub(r"[^A-Za-z0-9_\-\u0600-\u06FF]", "", s)
    # collapse multiple underscores
    s = re.sub(r"_+", "_", s)
    if not s:
        s = "file"
    return s + ext


def update_links_in_file(path: Path, mapping: dict):
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new in mapping.items():
        # replace href="old" and href='old' and plain occurrences
        text = text.replace(f'"{old}"', f'"{new}"')
        text = text.replace(f"'{old}'", f"'{new}'")
        # also replace /old and /old
        text = text.replace(f'/{old}', f'/{new}')
    if text != original:
        bak = path.with_suffix(path.suffix + '.bak')
        bak.write_text(original, encoding='utf-8')
        path.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    files = [p for p in base.glob('*.html')]
    mapping = {}
    # find unsafe files
    for p in files:
        if ' ' in p.name or "'" in p.name or re.search(r"[^A-Za-z0-9_\-\.\u0600-\u06FF]", p.stem):
            new = safe_name(p.name)
            if new != p.name:
                new_path = p.with_name(new)
                if new_path.exists():
                    print(f"Skipping rename {p.name} -> {new} (target exists)")
                    continue
                # backup
                bak = p.with_suffix(p.suffix + '.bak')
                bak.write_text(p.read_text(encoding='utf-8'), encoding='utf-8')
                p.rename(new_path)
                mapping[p.name] = new
                print(f"Renamed: {p.name} -> {new}")

    # update links in remaining html files
    if mapping:
        changed = []
        for p in base.glob('*.html'):
            if update_links_in_file(p, mapping):
                changed.append(p.name)
        print("Updated links in:", ", ".join(changed))
    else:
        print("No filenames needed renaming.")


if __name__ == '__main__':
    main()
