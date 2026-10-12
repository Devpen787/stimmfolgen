# Build Handoff — Proposed Workstreams and Integration Gates

**This is a handoff plan for Codex/implementation agents, not evidence any agent or repo was started.** Work from the official Hack Apertus Track 2B project template with its expected directory structure and `make run` contract. Do not confuse this architecture pack with the submission repository.

## Workstream A — Trust & Evidence (owner: ingestion/review)
Deliver: AHV primary source PDF bytes (if permitted), hash, validated pagination, narrowly scoped extracted passages, source IDs; source manifest / fallback to links. Then the property-tax case only if the first case is reliable. Report unknown rights/unstable URLs, don't paper over them.

**Contract:** `source_manifest.json` + `source_spans.jsonl` with immutable IDs, publisher, printed page, PDF page, `available_at`, `sha256`, actor attribution. No review, no publication.

## Workstream B — Model & Evaluation (owner: Apertus)
Deliver: real Apertus 1.5 inference proof and recorded model config, two candidate extraction prompts, comparison with a direct prompt and extractive baseline, specific false-precision refusal case, residual errors. Everything tied to actual raw responses; `NOT_RUN` if blocked. Structured candidate JSON must satisfy `schemas/public_case.schema.json` after normalisation, but machine-valid output is not automatically semantically valid.

**Contract:** `model_trace.json` + `case_candidate.json` + `eval_report.json`. Include version and runtime; no invented model outputs, no silently substituting proprietary model for Apertus.

## Workstream C — Surface / UX (owner: product)
Deliver: accessible S01–S05 with minimal onboarding, no chat-first homepage, one-click source inspection, neutral scenario chooser, clear uncertainty states, no account barrier. `UX_CONCEPT.html` is conceptual input, not production code.

**Contract:** UI binds only to published `CaseVersion` public model. No hardcoded per-referendum answer text in production components. User notes and optional saved vote history remain local and opt-in; no personalised vote advice.

## Workstream D — Release / Security (owner: independent auditor)
Deliver: clean root `make run` Docker experience, tests for source linkage, historical leakage and model-outage refusal, private data inspection, licensing manifest, technical report and demo. Review code produced in A–C adversarially.

**Contract:** `test_report.json`, reproducible scripts, source version checks, data-rights notes, truthful release status.

## Integration ordering
1. Freeze case/source contracts and a small set of named product states.
2. Confirm actual Apertus service and a real PDF retrieval before shipping AI capability.
3. Connect evidence outputs to UI; disallow direct arbitrary LLM prose to bypass checks.
4. Test one entire journey (including uncertainty and saved user brief).
5. Generalise with second referendum and an unprepared third/holdout import.
6. Only then expand design polish, languages or extra perspectives.

## Blockers and stop rules
- No valid Apertus inference → do NOT label the app an operational Apertus assistant; use an explicitly named replay/preview and resolve access.
- No inspected official source span → do NOT show a definitively verified personal effect.
- No privacy implementation → hide `save personal voting history` / do not claim E2EE.
- Broken mobile or poor comprehension → reduce number of cards/actions; don't add dashboard controls.
- Failing baseline/generalisation → report failures, narrow coverage, no victory claim.

## Immediate next 90 minutes
1. Create the actual Track 2B project from official template **only after owner authorises repo creation**.
2. In the intended runtime, make one successful Apertus v1.5 8B request (or report exact authentication/hardware blocker).
3. Fetch and hash 2024-03-03 booklet; inspect two page numbers manually.
4. Run existing 12 seed questions; identify at least one unsupported-cost abstention.
5. Record evidence and stop to reassess scope if initial model cannot distinguish claim from fact.
