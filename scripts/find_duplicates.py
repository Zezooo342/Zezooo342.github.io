#!/usr/bin/env python3
"""Detect simple near-duplicate HTML pages by comparing the first N characters of visible text."""
from pathlib import Path
import re
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: The 'bs4' package is required to run this script. Please install it with 'pip install bs4'.", file=sys.stderr)
    sys.exit(1)
import sys
import json


def extract_text(html: str) -> str:
    # Use BeautifulSoup with 'lxml' parser for better performance and robustness
    try:
        soup = BeautifulSoup(html, "lxml")
        for tag in soup(['script', 'style']):
            tag.decompose()
        text = soup.get_text(separator=' ', strip=True)
        return ' '.join(text.split())
    except Exception:
        return ""


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    samples = {}
    for p in base.glob('*.html'):
        try:
            text = p.read_text(encoding='utf-8')
            visible = extract_text(text)[:500]
            if visible.strip():
                samples[p.name] = visible
        except Exception:
            continue

    duplicates = []
    names = list(samples.keys())
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            a = samples[names[i]]
            b = samples[names[j]]
            if a and b:
                # compute simple similarity
                common = sum(1 for x,y in zip(a,b) if x==y)
                ratio = common / max(len(a), len(b))
                if ratio > 0.8:
                    duplicates.append({'a': names[i], 'b': names[j], 'ratio': round(ratio,2)})

    out = base / 'duplicate_report.json'
    out.write_text(json.dumps(duplicates, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Wrote duplicates: {len(duplicates)} pairs to {out}")


if __name__ == '__main__':
    main()
