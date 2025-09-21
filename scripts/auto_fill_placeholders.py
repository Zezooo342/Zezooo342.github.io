#!/usr/bin/env python3
"""Automatically replace simple placeholder markers with short Arabic paragraphs.

This is a conservative helper: it replaces occurrences of the exact string
".... (أضف فقرة أصلية هنا)" with a brief, useful Arabic paragraph. It creates
a .bak of each edited file.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = '.... (أضف فقرة أصلية هنا)'


def generate_paragraph(title: str) -> str:
    # Minimal, generic Arabic paragraph tailored to the title
    return (
        "<p>في هذا القسم نتناول نقاطاً عملية حول " + title +
        "، مع نصائح قابلة للتطبيق للمبتدئين والمحترفين على حد سواء. ركّز على تجربة المستخدم،"
        " اختبر الفرضيات، واحرص على قياس النتائج بانتظام لتحسين أداء المشروع.</p>"
    )


def process_file(path: Path):
    text = path.read_text(encoding='utf-8')
    if PLACEHOLDER not in text:
        return False
    # backup
    bak = path.with_suffix(path.suffix + '.bak')
    if not bak.exists():
        path.rename(bak)
        content = bak.read_text(encoding='utf-8')
    else:
        content = path.read_text(encoding='utf-8')

    # try to infer a short title from the <h1> or file name
    title_match = re.search(r'<h1>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = path.stem.replace('_', ' ')

    new_par = generate_paragraph(title)
    new_content = content.replace(PLACEHOLDER, new_par)
    path.write_text(new_content, encoding='utf-8')
    print(f"Updated: {path}")
    return True


def main():
    files = list(ROOT.glob('*.html'))
    changed = 0
    for f in files:
        try:
            if process_file(f):
                changed += 1
        except Exception as e:
            print(f"Error processing {f}: {e}")

    print(f"Total files updated: {changed}")


if __name__ == '__main__':
    main()
