#!/usr/bin/env python3
"""Detect simple near-duplicate HTML pages by comparing the first N characters of visible text."""
from pathlib import Path
import re
import sys
import json


def extract_text(html: str) -> str:
    # Extract main content area only, excluding headers, nav, and footers
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL|re.IGNORECASE)
    
    # Try to extract content within main tag or container
    main_match = re.search(r'<main[^>]*>(.*?)</main>', text, flags=re.DOTALL|re.IGNORECASE)
    if main_match:
        content = main_match.group(1)
    else:
        # Fallback: look for content within container div
        container_match = re.search(r'<div[^>]*class="container"[^>]*>(.*?)</div>', text, flags=re.DOTALL|re.IGNORECASE)
        if container_match:
            content = container_match.group(1)
        else:
            content = text
    
    # Remove all HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    
    # Clean up whitespace
    content = ' '.join(content.split())
    
    return content


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    samples = {}
    for p in base.glob('*.html'):
        try:
            text = p.read_text(encoding='utf-8')
            visible = extract_text(text)[:1000]  # Take more content for comparison
            if visible.strip() and len(visible) > 100:
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
                if ratio > 0.7:  # Lower threshold since we're comparing main content
                    duplicates.append({'a': names[i], 'b': names[j], 'ratio': round(ratio,2)})

    out = base / 'duplicate_report.json'
    out.write_text(json.dumps(duplicates, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Wrote duplicates: {len(duplicates)} pairs to {out}")


if __name__ == '__main__':
    main()
