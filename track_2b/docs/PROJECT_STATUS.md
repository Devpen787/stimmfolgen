# Project status (2026-10-12)

| Area | Status | Evidence or blocker |
| --- | --- | --- |
| Official Track 2B template | PRESENT | Generated from `HackApertus/project-template`; `track_2b/` directory retained |
| Architecture, journeys, privacy, schema docs | STAGED | v0.1 authored design; not an implemented product |
| Source registry | STAGED | References only; live retrieval, licensing and page mapping not verified |
| Illustrative UX concept | STAGED | Static HTML; not a deployed product |
| Public/private JSON schemas, fixture, design tool | STAGED | Text transferred from blueprint ZIP; local original-ZIP synthetic validator PASS, GitHub CI NOT_RUN |
| ZIP original checksum manifest | STAGED | Manifest included; PNG screenshots missing from repository; see `MIGRATION_AUDIT.md` |
| Actual Apertus v1.5 inference | VERIFIED / Gate 0 FAIL | Pinned v1.5 text-only MLX conversion actually ran locally; immutable span selection verified; actor attribution fails in two unchanged runs |
| Existing legacy Apertus inference | VERIFIED / diagnostic FAIL | Original 2509 weights and all genuine failed traces retained |
| Real 13th-AHV source evidence, temporal controls | SOURCE PASS / model FAIL | Exact official PDF hash/cutoff and five pages verified locally; deterministic guards pass; model output not human reviewed |
| Privacy implementation | NOT_RUN | Encrypted/private vault exists only as a design |
| Docker `make run` | FAIL / NOT IMPLEMENTED | Organiser placeholder still exits with an error |
| Demo, report and submission | NOT STARTED | Hack Apertus deadline 16 October 2026 |

Observed experiment: [immutable spans and independent reference](evidence/GATE0_SPANS_2026-10-12.md). Sixty deterministic unit tests and the design-contract validator pass locally. These checks do not establish semantic correctness or a clean Docker application.

Next action: resolve the reproduced actor-attribution failure, obtain human semantic review, and verify source publication availability. Immutable span construction and a bounded evaluation-only reference are implemented; those are not general semantic proof. Editorial cutoff is verified; public publication date is unknown. Frontend work remains stopped. Never call candidate schema validation a successful policy inference.
