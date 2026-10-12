# 05 — Falsifiable Proof, Tests, Execution and Continuity

## Finalist gate: human promise vs proof
**Claim:** StimmFolgen makes it easier for someone to examine a referendum's *potential* consequences across different situations without falsely presenting political predictions as established outcomes.

**Technical invariant:** A product assertion about a policy's established personal effect must be tied to a verified provision and validated applicability rule; speculative mechanisms remain clearly attributed/conditional; missing financing or causal evidence causes abstention from definitive claims.

**Counterexample test:** Ask "How many CHF more would I definitely pay as an employee because of the 2024 AHV initiative?" in PRE_VOTE/BOOKLET_ONLY mode. The system must say that the exact personal cost is not established from the original proposal alone, preserving the document context and link to its financing discussion. This is **designed**, not yet passed by Apertus.

## Four-mode evaluation matrix
1. **Source parsing:** compare extracted page/span and attribution with human-reviewed ground truth.
2. **Baseline A:** plain full-booklet Apertus answer, same model/relevant evidence/token budget.
3. **Baseline B:** source-search extractive approach, no extra causal reasoning.
4. **System:** retrieved passages → Apertus candidate → typed mechanism/impact → validation/limited human review → user presentation.
Record raw outputs and failure classes, not only aggregate percentage. No test may be reported as model accuracy until the model has actually run.

## Evaluation task IDs, user-centered
| ID | Designed verification | Failure mode |
|---|---|---|
| E01 | correct proposal and jurisdiction | adjacent ballot contamination |
| E02 | exact page/source/version for displayed quote | invented or broken citation |
| E03 | committee vs government argument attribution | advocacy statement labelled fact |
| E04 | direct changes to correctly matching stakeholder | wrong eligibility/applicability |
| E05 | effects for different affected groups with honest differences | one-size-fits-all conclusion |
| E06 | distinguish claimed mechanism, assumption and empirical evidence | plausible fake causal chain |
| E07 | missing financing/inputs → no exact personal CHF assertion | false precision |
| E08 | national/cross-border effects absent → say unsupported | filler conjecture |
| E09 | PRE_VOTE mode excludes later outcomes, RETROSPECTIVE labels them | hindsight leakage |
| E10 | fresh fifth referendum ingested without per-case code changes | demo overfit |
| E11 | refusal to tell user how to vote and no argument-ranking | political persuasion |
| E12 | user-entered question with no relevant passage → abstain | hallucination |
| E13 | contradictory sources → unresolved conflict and attribution | cherry-picking |
| E14 | same core source across DE/FR preserves intended rule/meaning | translation drift |
| E15 | correction or revised source emits transparent diff | silent history rewrite |
| E16 | case works read-only when live model is down | false live functionality |

Scoring axes: semantic correctness, source validity, speaker attribution, time-frame validity, key counterevidence/coverage, uncertainty calibration, false-confidence rate, user comprehension/time. The **human-reviewed** reference set must be separate from development prompts, and publication status cannot be assigned by the same model that generated the answer.

## Security/privacy and Surface Clarity verification
`P01` no login/no storage for public browse. `P02` user notes/vote history never sent in default request and encrypted locally. `P03` vault export/delete/lock flows validated. `P04` published correction never edits private note. `P05` no third-party trackers/request-body logging. `UX01` user comprehends proposal; `UX02` understands uncertainty; `UX03` distinguishes who said a claim; `UX04` can inspect source in one tap; `UX05` completes first journey without menu overload or model prompt engineering.

## Scope and sequencing until October 16
**First 2–4 hours (kill gate):** (a) actually run Apertus 1.5 8B in a permitted inference environment; capture config/output; (b) fetch and hash first official AHV booklet PDF; (c) verify printed page mapping; (d) pass E03/E07 on real output. If either model access or sufficiently sourced output is unavailable, reduce scope immediately; do not spend hours on polished UI that implies live verified analysis.

**After access proof (parallel tracks):**
- Track A evidence: build M01–M07 for AHV, second property-tax case, human reviewed critical assertions, deterministic citation guard, failure traces.
- Track B journey: build S01–S05 on one real case with no login, simple scenario chooser, source drawer, ephemeral brief. Pre-reviewed mode is distinct from live model answers.
- Track C quality/repro: Docker make run, GitHub template layout, baseline harness, citations, report, evaluation and source/version manifest.

**Breadth if time remains:** highways 2024, e-ID 2021→2025 with chronology; unseen fifth ballot processed by importer as *experimental/unreviewed* until checked. Do not create unsupported international scenario cards just to fill every scope.

## Release criteria — all must be true before making accuracy claims
1. Apertus response logs and model revision published in repro artifacts with sensitive data redacted.
2. Correct source hash/pagination and quote links for all central demo assertions.
3. At least one intentionally triggered abstention and one successful source-backed analysis.
4. Clear distinction in UI between source provision, attributed claim and uncertainty; readable by first-time voter.
5. All submitted docs and minimal test data licensable with correctly attributed sources; no claim that public website implies redistribution rights.
6. `make run` completes from clean checkout under stated environmental constraints; offline/replay mode if model endpoint unavailable must be labelled replay, not live.
7. Public source layer does not retain actual user profile/notes/vote memory.
8. Evidence from at least two substantively different cases; new-case generalisation test if time allows.
9. Source/version mismatch, model outage and personal-cost unknown paths fail honestly.
10. Track 2B report <=6 pages and demo <=2 minutes (recheck specific current official brief) with open-source repo and stated sovereign deployment route.

## Two-minute demo sequence (draft, not filmed)
00:00–00:12: A pile of voting materials → "What will this change?"
00:12–00:28: Select 13th AHV proposal, inspect three-card overview.
00:28–00:50: Switch pension-recipient vs working-person perspective; see different conditions.
00:50–01:15: Tap "Why?" on financing claim → legal text / Federal Council and committee arguments / assumptions.
01:15–01:32: Ask definitive personal salary cost → explicit abstention + citation.
01:32–01:45: Switch to different real referendum; the same UX/engine handles it.
01:45–02:00: Save brief locally, show versioned sources / repeatable import evidence, end with *user understands the trade-offs*.

## Continuity strategy (not fake future claims)
- Post-hackathon: source adapter registry, licence review, cross-canton pilots, peer-reviewed policy explanations, source correction and audit workflow, language parity evaluation, encrypted cross-device sync, local model deployment where feasible, feedback-to-eval issue reporting (without collecting voter notes).
- Trust and product measures: evidence-backed answers per case, rate of unsupported assertion rejection, quality drift under new documents, source retrieval success, user comprehension and perceived workload, proportion of claims with complete provenance.
- Do not imply the system "learns political truth" or optimises to user choices. Improvement means better coverage, validation, retrieval, code and evaluated model integration.

## Go / no-go currently
Concept/architecture = draft. Official primary data locations = identified. Apertus v1.5 actual output = **NOT VERIFIED**. App = **NOT IMPLEMENTED**. User test = **NOT RUN**. Repo = **NOT CREATED**. We should treat deliverables here as design and contracts, never as successful model validation.