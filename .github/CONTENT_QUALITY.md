Content quality checks
======================

This repository includes a GitHub Actions workflow `.github/workflows/content-quality.yml`
that runs on pull requests. It executes `scripts/ci_content_quality.py`, which in turn
runs the placeholder and duplicate detectors and fails the check if any issues are found.

If the workflow fails:
- Inspect `placeholder_report.json` and `duplicate_report.json` in the repository root.
- Fix the files listed (rewrite placeholders, merge or rewrite duplicate articles).
- Commit the fixes and push to the same branch to re-run the checks.
