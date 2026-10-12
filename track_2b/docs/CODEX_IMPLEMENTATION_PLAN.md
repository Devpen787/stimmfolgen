# StimmFolgen — Codex execution plan (risk first)

**2026-10-12 | Planned, not implemented.** Scope: Hack Apertus Track 2B, October 16 submission. Authoritative organiser constraints: `track_2b/README.md`, mandatory use of actual Apertus model family, one of on-premise/air-gapped/Swiss sovereign runtime architectures, Docker-root `make run`, PDF report and 2-minute demo. The organiser's original Track 2B files are intentionally unchanged on this setup branch.

## Gate 0 — Baseline and evidence hygiene

1. Read repository `AGENTS.md`, `docs/PROJECT_STATUS.md`, `docs/CONTEXT_AND_DECISIONS.md`, v0.1 product schema, privacy design, sources registry and the organiser requirements.
2. Verify `schemas/public_case.schema.json` and `schemas/private_vault.schema.json` against the **synthetic** fixture by running `python track_2b/docs/blueprint-v0.1/tools/validate_design.py` with `jsonschema` installed.
3. Record SHA-256, publisher, publication date, original PDF bytes/page mapping, reuse rights and `available_at` timestamp for the selected primary Swiss federal sources. Do not embed unlicensed document bytes. Keep real people's deliberations and all credentials out of Git.
4. Record optional screenshot assets absent from repo separately. Do not present the source registry as proof that sources were acquired.

## Gate 1 — Actual Apertus inference (hard block)

1. Select a legal-to-use and reproducible inference runtime using **Apertus v1.5 8B** (or explicitly documented v1.5 70B). Record exact model ID/checkpoint, revision, licence, provider/host, runtime jurisdiction, inference stack, quantisation, temperature, sampling parameters, prompt text and raw response.
2. Use one short inspected official federal booklet passage from the 13th AHV referendum of 3 March 2024. Retrieve and hash source and establish page numbers and contemporary `as_of` boundaries; no retrospective events may contaminate pre-vote claims.
3. Produce raw output trace + structured *candidate* JSON; benchmark against deterministic source passage/extractive baseline. A valid JSON schema does **not** mean correct interpretation.
4. If there is no genuine inference / provider access, mark `NOT_RUN` with precise blocker. Never fake model output, silently switch model families or claim an Apertus deployment based only on a stub.

## Gate 2 — Verified constrained pipeline

Implement `source -> extraction candidate -> deterministic verifier -> human-review-ready/public response` with explicit refusals. Required invariants: real source span IDs and page map; provenance back to publisher + SHA; factual vs prediction vs disputed uncertainty types; as-of availability; referenced IDs resolve; no unsupported precise personal finance figures; competing actor claims retain attribution; a machine-valid but unsupported claim must be withheld. Require adversarial tests: nonexistent source, stale page, wrong claim type, time travel, hallucinated numbers, fabricated personal profile, unavailable Apertus.

## Gate 3 — One honest vertical-slice journey

Use minimal S01–S05 from v0.1 UX as needed. Public evidence explorer, no chat-first marketing homepage; scenario selector uses only explicit non-sensitive choices. Inspect citations inline and open official documents. Missing financing or unpredictable effects are displayed as "not determined" rather than a confident model sentence. Avoid vote recommendations or partisan nudges. Personal notes are local-only in an isolated domain; never claim encryption or E2EE without audited implementation and threat-model review.

## Gate 4 — Cold release contract

The organiser expects a **clean-checkout** `make run` from `track_2b/` to start Docker-contained application end-to-end. Pin dependencies, document model weights and their legal acquisition, record startup duration, CPU/GPU resource needs and runtime data flows. Then run fresh checkout test, policy/data provenance audit, fail-closed tests, UX smoke tests and accessibility pass. Write factual `technical_report.md`, a <=6-page PDF `TeamName_Report.pdf`, and <=2-minute demo video; no invented scores/results.

## Release verdicts

Each gate: `PASS`, `FAIL`, `BLOCKED` or `NOT_RUN` with link to exact logs/commit/test evidence. **Do not merge or represent as ready until reviewed.** Current evidence: **all runtime gates NOT_RUN**, design docs staged. The repo's current `track_2b/Makefile` is still a placeholder.

**Next task:** open a narrowly scoped implementation PR proving genuine Apertus v1.5 inference on the sourced 13th AHV passage before adding UI.
