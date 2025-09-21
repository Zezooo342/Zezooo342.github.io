#!/usr/bin/env python3
"""A conservative helper to reduce near-duplicate content in flagged pairs.

It reads `duplicate_report.json` (expected to be a list of pairs or a dict with 'pairs')
and for each pair prepends a short unique sentence to the second file to make it
less identical. Creates .bak backups before editing.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_pairs():
    p = ROOT / 'duplicate_report.json'
    if not p.exists():
        print('No duplicate_report.json found.')
        return []
    data = json.loads(p.read_text(encoding='utf-8'))
    if isinstance(data, dict):
        return data.get('pairs') or data.get('duplicates') or []
    return data


def make_backup(path: Path):
    bak = path.with_suffix(path.suffix + '.bak')
    if not bak.exists():
        path.rename(bak)
        path.write_text(bak.read_text(encoding='utf-8'), encoding='utf-8')
        # restore original to path by copying content


def prepend_unique(path: Path, note: str):
    text = path.read_text(encoding='utf-8')
    if note in text:
        return False
    new = f"<p class=\"unique-note\">{note}</p>\n" + text
    # backup
    bak = path.with_suffix(path.suffix + '.bak')
    if not bak.exists():
        bak.write_text(text, encoding='utf-8')
    path.write_text(new, encoding='utf-8')
    print(f"Prepended unique note to {path}")
    return True


def main():
    pairs = load_pairs()
    if not pairs:
        print('No pairs to process.')
        return
    changed = 0
    for pair in pairs:
        # pair could be tuple/list of two filenames or a dict
        if isinstance(pair, dict):
            a = pair.get('a')
            b = pair.get('b')
        elif isinstance(pair, (list, tuple)):
            if len(pair) >= 2:
                a, b = pair[0], pair[1]
            else:
                continue
        else:
            continue

        path_b = ROOT / b
        if not path_b.exists():
            print(f"File not found: {b}")
            continue
        note = 'ملاحظة: هذه النسخة تحتوي على تحليل محدث وملاحظات حصرية تهدف لخدمة قراءنا بشكل أفضل.'
        try:
            if prepend_unique(path_b, note):
                changed += 1
        except Exception as e:
            print(f"Error editing {b}: {e}")

    print(f"Total duplicate files adjusted: {changed}")


if __name__ == '__main__':
    main()
