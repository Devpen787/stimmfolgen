# StimmFolgen v0.1 migration audit

Date: 2026-10-12. Source of authority for design bytes: `StimmFolgen_Product_Blueprint_v0.1.zip`, with the archived text branch `Devpen787/ethglobal-build-os@archive/stimmfolgen-blueprint-v0.1` used to stage existing text documents. The 10 archived text files had lost their final newline when initially copied; this setup commit restores the newline to match the original ZIP and its SHA-256 manifest.

## Files in the original archive

- **Migrated / present under `track_2b/docs/blueprint-v0.1/`:** the 10 top-level text/HTML/CSV files; `MANIFEST.json`; `fixtures/synthetic_case.json`; both `schemas/*.schema.json`; `tools/validate_design.py`.
- **Not yet migrated:** `UX_PREVIEW_desktop.png` and `UX_PREVIEW_mobile.png` are present in the original ZIP but not yet transferred through the connected GitHub text/Git-object interface. Their hashes and sizes remain in `MANIFEST.json`; do not claim that the repository copy of the archive is complete.
- **Static UX:** `UX_CONCEPT.html` is a concept artifact, not an application.

## Integrity checks

The original local ZIP was independently checked on 2026-10-12: all 16 listed files matched its SHA-256 manifest; the original `tools/validate_design.py` passed synthetic fixture, foreign-key and Draft 2020-12 schema checks when `jsonschema` was installed. These are **local original-ZIP checks**, not CI or checks of the full GitHub branch. After migration, run a manifest audit and verify any missing images from the ZIP before declaring complete provenance.

## Responsible engineering

No actual Apertus inference, sourced policy interpretation, encrypted private vault, deployed app, Docker cold run, accessibility audit or unbiasedness evaluation is established by this migration. The organiser's `track_2b/README.md`, `technical_report.md`, `Makefile` and `src/` have not been replaced.
