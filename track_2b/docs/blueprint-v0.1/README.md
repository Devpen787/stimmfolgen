# StimmFolgen — Product & System Blueprint v0.1

**Date:** 12 October 2026  **Stage:** Design/proposed architecture, not implemented or model validated.  **Target:** Hack Apertus Track 2B; submission deadline 16 October 2026, subject to organiser confirmation.  **Working name only; no name clearance.**

## Promise
**Understand what a Swiss vote could change, who it could affect, why, and what remains uncertain—without receiving a voting recommendation.**

StimmFolgen helps citizens navigate referendum proposals by linking (a) exact provisions, (b) attributed claims, (c) the proposed mechanism connecting a policy to possible consequences, and (d) different factual circumstances and levels of society. It distinguishes what the source *establishes* from what it *predicts*, and can say `not established`. It does not optimise or predict voting preferences.

## Architecture decisions / non-negotiables
1. **Public evidence / private deliberation separation**: authoritative-ish public source snapshots and machine-generated interpretations are shared; users' questions, selected scenarios, notes and optional vote history remain local by default.
2. **Evidence is not truth**: an authentic quotation can support what someone *said* but not prove the accuracy of the claim. Each item needs semantic validation and editorial status, not just an existing citation.
3. **Time-frame integrity**: 2024 pre-vote analysis never incorporates post-vote information unless the user explicitly switches to a labelled retrospective mode.
4. **No personal persuasion**: no vote recommendations, side ranking, moral utility score, covert salience ranking or voter profiling. Scenario matching checks factual applicability only.
5. **Fail closed on unsupported certainty**: unverified, misleading or missing evidence is displayed as unresolved or withheld from established-fact surfaces.
6. **One narrow journey first, then breadth**: 13th AHV 2024 deep case, homeownership tax 2025 second deep case; highways 2024 and e-ID 2025 for coverage if quality allows; one unseen case to prove the same importer works.
7. **Reproducible project**: official Hack Apertus `track_2b/` template, Docker `make run`, actual Apertus family, <=100 MB submitted `data/`, report/demo per official challenge rubric.

## Artifact map
- [`01_SYSTEM_AND_SOURCES.md`](01_SYSTEM_AND_SOURCES.md) — architecture, source adapters, ingest, inference and publication contracts.
- [`02_JOURNEYS_AND_UX.md`](02_JOURNEYS_AND_UX.md) — personas/jobs, complete journeys, information architecture, screen designs, error states and UX evaluation.
- [`03_PRIVACY_AND_UPDATES.md`](03_PRIVACY_AND_UPDATES.md) — storage, local vault, private user context, threat model, synchronisation and freshness.
- [`04_PRODUCT_SCHEMA.md`](04_PRODUCT_SCHEMA.md) — normalized data/relationship schema, enums, invariant rules and end-to-end traceability.
- [`05_GATES_AND_EXECUTION.md`](05_GATES_AND_EXECUTION.md) — prototype scope, system tests, holdout strategy, release gates, timeline, demo.
- [`INGEST_RUNBOOK.md`](INGEST_RUNBOOK.md) — repeatable new-referendum process with proposed CLI and acceptance checks.
- [`BUILD_HANDOFF.md`](BUILD_HANDOFF.md) — bounded implementation workstreams and integration gates.
- [`SOURCE_REGISTRY.csv`](SOURCE_REGISTRY.csv) — checked starting endpoints vs adapter readiness, licensing review.
- [`schemas/public_case.schema.json`](schemas/public_case.schema.json) — machine-validatable public evidence-case structure (proposed).
- [`schemas/private_vault.schema.json`](schemas/private_vault.schema.json) — private export payload (proposed; envelope encryption specified separately).
- [`fixtures/synthetic_case.json`](fixtures/synthetic_case.json) — clearly fabricated schema-validation fixture, not a referendum fact or Apertus result.
- [`UX_CONCEPT.html`](UX_CONCEPT.html) — tested responsive, clickable UX study with example warnings; not a live AI product.
- [`UX_PREVIEW_desktop.png`](UX_PREVIEW_desktop.png) and [`UX_PREVIEW_mobile.png`](UX_PREVIEW_mobile.png) — concept screenshots.

## Current implementation/evidence status
- Prior kickoff packet established 12 **author-defined, NOT RUN** development checks for the 13th AHV source booklet.
- Verified public *source locations*: Swiss Federal Chancellery booklet archive, federal VoteInfo information, Swissvotes federal dataset, federal open voting results and Fedlex.
- **Not yet demonstrated**: authenticated Apertus inference, stable automated downloads, production adapters, semantic correctness, human validation, encrypted vault, live UI, user testing, Docker startup or a public repository.
- Prior project kickoff retained at `/mnt/data/ripple-kickoff/DECISION_AND_FIRST_TEST.md` in conversation artifacts (not duplicated to imply new work).

## External sources / source status
- Federal Chancellery booklet archive: https://www.bk.admin.ch/de/sammlung-der-abstimmungsbuechlein-seit-1978
- Federal Chancellery VoteInfo overview: https://www.bk.admin.ch/de/abstimmungsinformationen
- Swissvotes dataset, federal coverage / CC BY 4.0: https://swissvotes.ch/page/dataset
- Official voting-result open data: https://opendata.swiss/en/dataset/echtzeitdaten-zu-den-eidgenossischen-abstimmungen-gemeindestand-am-datum-der-abstimmung
- Fedlex legislation portal: https://www.fedlex.admin.ch/
- Hack Apertus template: https://github.com/HackApertus/project-template
- First deep test primary source: https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf
