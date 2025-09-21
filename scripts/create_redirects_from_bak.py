#!/usr/bin/env python3
"""Create HTML redirect pages for files that were renamed.

For each file named NAME.html.bak, this script will create NAME.html (if missing)
that redirects (meta refresh + link) to the sanitized filename produced by the
sanitize_filenames script.

Usage: python3 scripts/create_redirects_from_bak.py [directory]
"""
from pathlib import Path
import re
import sys


def safe_name(name: str) -> str:
    # reuse the same renaming rules as sanitize_filenames
    import re
    p = Path(name)
    stem = p.stem
    ext = p.suffix
    s = stem
    s = s.replace(" ", "_")
    s = s.replace("'", "_")
    s = re.sub(r"[^A-Za-z0-9_\-\u0600-\u06FF]", "", s)
    s = re.sub(r"_+", "_", s)
    if not s:
        s = "file"
    return s + ext


def make_redirect(old_name: str, new_name: str, out_dir: Path):
    content = f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=/{new_name}" />
  <title>Redirecting...</title>
  <link rel="canonical" href="https://zezooo342.github.io/{new_name}" />
</head>
<body>
  <p>تم نقل هذه الصفحة إلى <a href="/{new_name}">{new_name}</a>.</p>
</body>
</html>
'''
    out = out_dir / old_name
    if out.exists():
        return False
    out.write_text(content, encoding='utf-8')
    return True


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    created = []
    for bak in base.glob('*.html.bak'):
        old = bak.name[:-4]  # strip .bak
        new = safe_name(old)
        # if the sanitized file exists, create redirect at old
        if (base / new).exists():
            if make_redirect(old, new, base):
                created.append((old, new))

    if created:
        for o, n in created:
            print(f"Created redirect: {o} -> {n}")
    else:
        print("No redirects created.")


if __name__ == '__main__':
    main()
