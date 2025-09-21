#!/usr/bin/env python3
"""Scan HTML files for placeholder markers and weak content indicators.
Generates report `placeholder_report.json` listing files and matched lines.
"""
from pathlib import Path
import re
import json
import sys

PLACEHOLDER_PATTERNS = [
    r"\.{4,}\s*\(أضف فقرة أصلية هنا\)",
    r"أضف\s+فقرة",
]


def scan_dir(base: Path):
    report = {}
    patterns = [re.compile(p, flags=re.IGNORECASE | re.UNICODE) for p in PLACEHOLDER_PATTERNS]
    for p in base.glob('*.html'):
        text = p.read_text(encoding='utf-8')
        matches = []
        for i, line in enumerate(text.splitlines(), 1):
            for pat in patterns:
                if pat.search(line):
                    matches.append({'line': i, 'text': line.strip()})
                    break
        if matches:
            report[p.name] = matches
    return report


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    report = scan_dir(base)
    out = base / 'placeholder_report.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Wrote report: {out} ({len(report)} files)")


if __name__ == '__main__':
    main()
