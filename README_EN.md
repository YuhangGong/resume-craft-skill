# ResumeCraft Skill

A portable Agent Skill and Python 3.11+ toolkit for evidence-grounded A4 resumes.
Three original templates render local HTML, selectable-text PDF, screenshots and
quality reports. No cloud API is needed by the scripts. The host Agent structures
and reviews prose; deterministic code validates provenance and layout.

## Setup / quick start

```sh
python -m venv .venv
# Windows: .venv/Scripts/python.exe; macOS/Linux: .venv/bin/python
python -m pip install -e ".[dev]"
python -m playwright install chromium
python scripts/build_resume.py examples/sample_profile.json --no-photo --output outputs
python -m pytest -q
```

Use the venv's Python in every command. Linux may need Playwright --with-deps.
Alternatively install requirements.txt; install pytest separately for tests.
Optional OCR requires Tesseract chi_sim+eng (plus pytesseract for images).

## Codex and WorkBuddy

Copy the complete folder to ~/.agents/skills/resume-craft-skill (or project
.agents/skills/), install dependencies there, and invoke `$resume-craft-skill`.
Codex normally discovers changes automatically; restart if necessary.
Example: “Use ResumeCraft to make an A4 Resume001-MinimalBusiness resume from these real
experiences. Output HTML and PDF.” Follow-ups reuse the fact bank and create versions.
See [official Codex docs](https://learn.chatgpt.com/docs/build-skills) and
[Agent Skills specification](https://agentskills.io/specification).

WorkBuddy offers local package upload through its Skills UI. Its marketplace has
extra required metadata; run package_project.py --workbuddy for that variant.
Local Python/Chromium permissions are required; WorkBuddy E2E was not tested.
Official links and Windows-specific instructions are in README.md.

## Inputs and workflow

extract_profile.py reads TXT/MD/PDF/DOCX and preserves quoted sources, extracting
labeled identity only. The host structures remaining experiences into Profile.
Scanned inputs require optional OCR or host vision. Read references/profile-schema.md
and examples/sample_profile.json; machine schemas are in schemas/.

```sh
python scripts/parse_job.py examples/sample_job.txt --output user_data/job.json
python scripts/match_job.py examples/sample_profile.json user_data/job.json --output user_data/match.json
python scripts/build_resume.py examples/sample_profile.json --job user_data/job.json --template Resume002-AcademicResearch --no-photo --output outputs
```

Config supports language zh/en, sections/order/counts, photo dimensions, name size,
licensed local font embedding and bounded repairs. It does not translate content.
Five original styles are listed below, including sidebar and date-axis designs. Add Word references via
parse_template.py then maintain HTML/CSS adapters; complex layouts are not losslessly
converted. See references/template-guide.md.

Each version has resume.html/pdf, preview.png, profile/config snapshots, quality and
optional matching reports. Never overwrite the master fact bank. Failed hard checks
return 2. Maximum three repairs; omit low-priority entries before sacrificing readable
type. Huge irreducible entries fail explicitly. All omissions are reported.

## Guarantees and limits

Source quotes, metadata and numeric tokens are checked. Unverifiable rewrites require
user confirmation; code cannot prove real-world truth, semantic fidelity, paper/patent
status or individual ownership of team outcomes. Host review remains mandatory.
JD matching is a transparent vocabulary baseline, not semantic AI or an ATS guarantee.
Never invent facts or import JD requirements as personal skills.

Programmatic DOM/PDF checks cover A4/page count, text extraction, bounds/overlaps,
photo placement, typography thresholds and glyph/text mismatches. Inspect browser
and actual PDF renders for aesthetics, glyph shapes and reading order. See
references/formatting-rules.md. Run `python -m pytest -q` to view test results. OCR and non-Windows hosts are
not claimed tested. Troubleshooting is documented in references/troubleshooting.md.

Private data belongs outside this repo. Scripts do not upload it, but a cloud host
may process submitted content under its provider policy. Logs are sanitized; snapshots
are sensitive. Delete only your verified private directory, including versions/photos.
Never put real resumes into tests. All examples are synthetic DEMO content.

To contribute, run tests and visually inspect generated PDFs; submit synthetic
reproductions. Before release audit licenses/privacy, review the allowlisted ZIP,
test clean environments and other hosts, and resolve dependency updates. Nothing is
automatically published or pushed. Packaging preserves the source folder and omits
user_data, outputs, caches and environments. MIT applies to original code/templates;
third-party resources retain separate licenses (THIRD_PARTY_NOTICES.md).

Architecture: concise SKILL.md routes to references, scripts expose CLI wrappers,
src contains typed models/parsers/matching/rendering/validation; assets/templates
is the canonical template source and is copied into wheels at build time.


## Current public template library / 当前公开模板库

- `Resume001-MinimalBusiness`
- `Resume002-AcademicResearch`
- `Resume003-ModernTech`
- `Resume004-SidebarProfile`
- `Resume005-TimelineLedger`

Five original MIT designs. The two new designs are sidebar and date-axis layouts.
See [new-designs.md](references/new-designs.md) and [template-naming.md](references/template-naming.md).
Next template: Resume006-NewEnglishName. Third-party Word-derived templates are not included.
