# Project status (2026-10-12)

| Area | Status | Evidence or blocker |
| --- | --- | --- |
| Official Track 2B template | PRESENT | Generated from `HackApertus/project-template`; `track_2b/` directory retained |
| Architecture, journeys, privacy, schema docs | STAGED | v0.1 authored design; not an implemented product |
| Source registry | STAGED | References only; live retrieval, licensing and page mapping not verified |
| Illustrative UX concept | STAGED | Static HTML; not a deployed product |
| Public/private JSON schemas, fixture, design tool | STAGED | Text transferred from blueprint ZIP; local original-ZIP synthetic validator PASS, GitHub CI NOT_RUN |
| ZIP original checksum manifest | STAGED | Manifest included; PNG screenshots missing from repository; see `MIGRATION_AUDIT.md` |
| Actual Apertus v1.5 inference | VERIFIED / bounded suite PASS / REVIEW_REQUIRED | Two unchanged source-first actor-comparison suites pass; human review and public-frame adoption remain blockers; pre-vote exact-byte availability verified |
| Existing legacy Apertus inference | VERIFIED / diagnostic FAIL | Original 2509 weights and all genuine failed traces retained |
| Real 13th-AHV source evidence, temporal controls | SOURCE PASS / bounded pipeline PASS | Exact official PDF hash/cutoff and five pages verified locally; deterministic guards pass; model output not human reviewed |
| Privacy implementation | NOT_RUN | Encrypted/private vault exists only as a design |
| Docker `make run` | FAIL / NOT IMPLEMENTED | Organiser placeholder still exits with an error |
| Demo, report and submission | NOT STARTED | Hack Apertus deadline 16 October 2026 |

Latest evidence: [publication verification and pending semantic review](evidence/GATE0_PUBLICATION_AND_REVIEW_2026-10-12.md). Seventy-three deterministic unit tests and the design-contract validator pass locally. These checks do not establish semantic correctness or a clean Docker application.

Next action: human review of P01-P05 and T01-T07 in the [prepared packet](evidence/ahv-semantic-review-2026-10-12/REVIEW.md), then reconcile runtime temporal admission and final Gate 0 clearance. Pre-vote availability is verified by the exact official bytes archived on 11 January 2024; the precise first publication instant remains unknown. The original 29 November cutoff is content knowledge, not a public availability date. Proposed review frame: 2 March 2024, 23:59:59 CET. All human decisions remain PENDING. Frontend work remains stopped.

Human review progress: [P01 accepted with revised wording](evidence/ahv-human-review-2026-10-12/DECISIONS.md). P02 is next; remaining claims, trial outcomes, temporal-frame adoption and overall Gate 0 clearance are pending. Frontend blocked.

Human review progress: [P02 accepted with the approximate annual-cost wording](evidence/ahv-human-review-2026-10-12/P02.json). P01 and P02 are accepted with their recorded wording; P03 is next. All trial decisions and overall Gate 0 clearance remain pending. Frontend blocked.
