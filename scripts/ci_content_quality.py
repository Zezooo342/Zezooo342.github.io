#!/usr/bin/env python3
"""CI wrapper to run content quality checks used by GitHub Actions.

This script runs the repository's placeholder and duplicate detectors and exits
with a non-zero status if any placeholders or duplicates are detected. That
prevents PR merges until human review.
"""
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run(cmd):
    print(f"Running: {cmd}")
    res = subprocess.run(cmd, shell=True, cwd=ROOT)
    if res.returncode != 0:
        print(f"Command failed: {cmd}")
    return res.returncode


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"Failed to read {path}: {e}")
        return None


def main():
    # Run existing scripts if present
    placeholders_script = ROOT / 'scripts' / 'find_placeholders.py'
    duplicates_script = ROOT / 'scripts' / 'find_duplicates.py'

    if placeholders_script.exists():
        rc = run(f"python {placeholders_script}")
        if rc != 0:
            print('Placeholder script returned non-zero')

    if duplicates_script.exists():
        rc = run(f"python {duplicates_script}")
        if rc != 0:
            print('Duplicate script returned non-zero')

    placeholder_report = load_json(ROOT / 'placeholder_report.json')
    duplicate_report = load_json(ROOT / 'duplicate_report.json')

    problems = 0

    if placeholder_report:
        # placeholder_report may be a dict with 'files' key or a list
        if isinstance(placeholder_report, dict):
            files = placeholder_report.get('files') or placeholder_report.get('files_with_placeholders') or []
            if not files:
                # fallback: count keys/entries
                try:
                    files = list(placeholder_report)
                except Exception:
                    files = []
        elif isinstance(placeholder_report, list):
            files = placeholder_report
        else:
            files = []

        total = len(files)
        if total:
            print(f"Found {total} files with placeholders. See placeholder_report.json")
            problems += total

    if duplicate_report:
        # duplicate_report may be a dict with 'pairs' or a list of pairs
        if isinstance(duplicate_report, dict):
            pairs = duplicate_report.get('pairs') or duplicate_report.get('duplicates') or []
        elif isinstance(duplicate_report, list):
            pairs = duplicate_report
        else:
            pairs = []

        pairs_count = len(pairs)
        if pairs_count:
            print(f"Found {pairs_count} potential duplicate pairs. See duplicate_report.json")
            problems += pairs_count

    if problems:
        print("Content quality checks failed. Please fix placeholders/duplicates before merging.")
        sys.exit(1)

    print("Content quality checks passed.")


if __name__ == '__main__':
    main()
