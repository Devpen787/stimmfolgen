# AGENTS.md — Codex/agent instructions for StimmFolgen

Always read `track_2b/docs/CONTEXT_AND_DECISIONS.md`, `track_2b/docs/PROJECT_STATUS.md`, `track_2b/docs/blueprint-v0.1/04_PRODUCT_SCHEMA.md`, `track_2b/docs/blueprint-v0.1/05_GATES_AND_EXECUTION.md`, and `track_2b/README.md` before proposing implementation.

This is the NEW hackathon submission repository. Do not merge implementation into main without review. Do not copy Build OS generic code as if built during the event. Preserve the official `track_2b/` structure. Avoid unnecessary refactors or adding nonessential dependencies.

**Blocking gate:** actual Apertus 1.5 model access/inference. Prove end-to-end evidence handling on real federal booklet first, then UI. Do not present manually-authored fixtures as model results. Record exact model ID, output, prompt, evidence reference, dates, validation and reproducibility in `track_2b/docs/evidence/` or equivalent. No invented outcome or claim evaluation.

**Invariants:** separation of public evidence and private notes; each claim has identified provenance/attribution, epistemic classification and temporal availability; unsupported predictions must not masquerade as established; nonpartisan no vote recommendations; private notes never in public repo or public prompts.

**Testing:** favour deterministic validation (IDs, source references, timestamps, schema, refusals, provenance, no temporal leakage), real inference benchmark vs baseline and a cold judge clone/ Docker `make run`. Disclose limitations, failures and absent tests. One complete happy path AND one deliberate abstention path are minimum.

**Collaboration:** preserve the existing design, record decisions in ADRs, create focused PRs and only mark verified things complete when exact test results are available. Scope and deployment constraints supersede speculative features.
