# Four-case matching repair and live journeys — 15 October 2026

PR #4, branch `codex/local-apertus-gate0-evidence`; baseline `3c05f999856cc2e1bbb7e10096e2673216923f04`.
Public app: https://stimmfolgen-demo.stimmfolgen-hosted.workers.dev/ . No video edits, main merge, submission, payment, top-up or visitor hosting on the owner's Mac.

## Result and exact scope

Final actual Public AI `swiss-ai/apertus-v1.5-8b` inference passed **38/38 known development questions**, including the original AHV 13/13 and all four previous no-answer cases. This run verifies question matching over five already reviewed AHV statements, not new PDF extraction, general semantic accuracy, a blind benchmark or local MLX parity. Gold references are compared after inference and never supplied as expected answers to the model.

| Prior miss | Final observed result | Real trace |
| --- | --- | --- |
| Childcare/economy question in AHV reader | Other-proposal boundary, no factual claim | `frozen-base19/different_proposal.json` |
| Fabricated CHF 800 quotation | Reviewed P04 financing-uncertainty correction, no invented quotation | `frozen-base19/fabricated_quote_request.json` |
| Fireworks/business question in AHV reader | Other-proposal boundary, no factual claim | `frozen-extra19/other_new.json` |
| Workers would definitely pay nothing | Reviewed P04 correction; unknown is not zero | `frozen-extra19/zero_new.json` |

`frozen-base19/summary.json`: 19/19. `frozen-extra19/summary.json`: 19/19. The original 13 are identified by the earlier frozen original case list, not by alphabetical file order. Attribution, distinct initial/five-year estimates, comparison, German/French paraphrases, unsupported climate/retirement-age questions, later observations and voting-advice controls pass in this run. Temperature zero does not guarantee repeatability; earlier complete and partial failures remain preserved. No second/unseen ballot was tested.

## Repair and root cause

The previous directness system prompt accidentally included an extracted JavaScript evaluator tail. `v9-contaminated-contract.json` preserves that error. It did not contain an API secret or an actual gold answer table, but it was unintended model input. The new prompt is explicit JSON; contract guards reject evaluator-code markers and oversized system strings before inference. No prompt string is extracted from JavaScript.

Production/evaluation now share `hosted/matching.mjs`. Apertus generates a neutral search query without seeing source statements or gold IDs. Explicit alternative proposal names are checked by a small application-owned noun-modifier grammar against the selected title; implicit attribution questions retain the selected proposal. This grammar contains no AHV/fireworks/childcare answer mapping. It is bounded and can misroute unrecognised synonyms/name forms; it is not general entity understanding. A separate Apertus boolean distinguishes observed later events from historical forecasts.

BM25F still requires topical overlap. Generic change/effect/establish verbs and bare year/annual units no longer dominate matches. Generic pay/contribute-to-charge and receive-to-recipient expansions bridge vocabulary; no fixed CHF amounts or expected IDs enter runtime search logic. Fictional definite-fee tests demonstrate this can retrieve an established charge, rather than making every payment question return uncertainty. Renamed/reordered ID tests and an unrelated fictional ledger exercise generic retrieval.

Apertus separately checks each lexical candidate against the original question and its untrusted query translation. It can accept a correction to a false premise or identify the actual speaker. No model-only fallback is allowed. Every public factual text/type/actor/span is copied unchanged from the accepted ledger. This same-model relevance decision is fallible, not independent factual verification; source/wording validation and the original human approvals are independent constraints. Runtime matches remain explicitly unreviewed. The original PASS_BOUNDED_AHV certificate and experimental native v8 path are unchanged.

Rejected alternatives include source-conditioned planning, money-role taxonomies, source-topic/role classifiers and model proposal-identity booleans. They regressed attribution, multilingual retrieval or unsupported-topic handling, so they were not deployed. A 70B probe returned upstream HTTP 429 and was not enabled in production. No new weights, paid plan or larger pricing allowance was introduced.

## Live browser verification

Agent-operated Codex in-app browser through CUA; Browser plugin unavailable. Fresh temporary QA origins use the real production Durable Object, secret and persistent caps, not a synthetic model. They isolate synthetic note vaults from the owner's origin. Both QA Workers were subsequently deleted; no quota namespace was replaced or reset.

The full journey was Search AHV → Track → My votes → Explore my vote → real live question → dated source details → Updates → Related votes → Me (worker/recipient), Others and Switzerland → synthetic visit-only note → opt-in encrypted save → reload locked → unlock restores note. Choice stayed **Not recorded**. Desktop also followed the source PDF redirect to the official booklet page 11. Its browser PDF text/rendering was not independently inspected in this run. Phone opened the separate financing proposal and verified that reviewed Apertus analysis was unavailable, then returned to AHV.

| Check | Desktop | Responsive phone |
| --- | --- | --- |
| Full journey viewport, verified from DOM | 1280×800 (repeated) | 389×845 |
| Correct page/title and meaningful content | PASS | PASS |
| Framework error overlay | None observed | None observed |
| Console errors/warnings | None observed | None observed |
| Document width equals viewport | PASS | PASS |
| Live useful correction | Fabricated-quote premise → P04, 3.31s (repeat; initial 1.89s) | Zero-cost premise → P04, 4.23s |
| Live other-proposal boundary | Childcare, 2.47s | Fireworks, 3.26s |
| Encrypted save/reload/unlock | PASS | PASS |

A final production desktop check at **1280×800** returned the Federal Council/Parliament attribution (3.97s), with no observed console errors/warnings. `browser/production-desktop.png` records this final layout. The owner-origin vault remained locked and was never read, cleared or overwritten. An initial desktop run began at 1280×720 but changed to 781×835 after external-source tab activity. Its traces are retained as mixed-size evidence, not fixed desktop proof; the complete desktop flow was repeated with an explicit 1280×800 override and without creating another tab. DOM dimension logs are the viewport authority. The newly created desktop-final QA origin initially returned a Cloudflare nothing-here page and then a loading shell; reload/waiting for assets resolved it. Selector timeouts in those states were not treated as completed actions, and no raw network trace was retained for that startup interval. Mobile screenshots were captured only after verifying 389 pixels. These are responsive browser checks, not physical-phone, independent human research or network-forensics proof. Unknown personal cost, runtime-match fallibility and global hosting remain visibly disclosed. The interface still carries substantial caveat text.

Browser snapshots, dimensions, console logs, screenshots and `browser/journeys.json` are retained. No real political choice or personal note was used. Synthetic passphrases have no production credential value.

## Deployment and technical verification

Contract: `live-ahv-scoped-query-v10`. Authenticated bundle SHA-256:
`5f8611be7e6d6c3fc555a95c3c3117a56e28500d8b64fd48ea6c37a8d2e5582d`.
Final production version: `ba949f47-77d9-420a-9412-f0da20f68c03`.

The first upload `7c3432e1-b736-41b5-a28a-873f6f134ca3` reached the router before its Durable Object. Early public probes and one desktop request correctly withheld the old v9 execution. A diagnostic-only follow-up exposed expected/observed public execution hashes and preserved the truthful inference-performed flag when the old instance had actually run. A brief official Wrangler tail diagnostic was opened/closed; no application request bodies or private contents were logged. After propagation, `public-execution-pin-04.json` returned HTTP 200, EVIDENCE_MATCH, P05 and the exact new hash. Browser corrections and final production attribution then passed. Upload success alone was not treated as inference proof. Cloudflare documents this eventual-consistency window: https://developers.cloudflare.com/durable-objects/platform/known-issues/#code-updates . Old failures and transitions remain in the archive.

Final checks: **24/24 hosted tests**, including actual compiled workerd/SQLite Durable Object concurrency, malformed-output rejection, private-field rejection and quota persistence across restart with a labelled synthetic provider; **104 Python tests**; actual WebCrypto vault failure/recovery tests; authenticated source/bundle parity; Docker build; network-disabled original Gate check; five deliberately mutated real-source/approval/frame/checkpoint negative controls; Docker HTTP journey. These deterministic/synthetic checks are not substitutes for the separate real inference traces.

## Preservation and reproduction

`preserved-experiments.jsonl` retains all available matching experiments, request/response bodies, rejected contracts/code, logs, larger-model failure, deployment transitions and final check logs. Each record carries its original path/hash and published-content hash. Machine home paths, account/email identifiers and network-address strings are redacted; no authentication headers/key contents, weights or raw booklet are committed. The previous evidence packet is untouched. Runs without a summary are partial/stopped experiments; missing trials are not passes. Earlier snapshot coverage is limited to what was retained; no missing trace is reconstructed as model output.

Reproduce actual provider evaluation with existing authorised credit/key (token contents never belong in command arguments or Git):

```sh
node track_2b/tools/evaluate_hosted_matching.mjs CASES_JSON NEW_OUTPUT_DIRECTORY TOKEN_FILE_PATH
```

Reference questions are in each final trace under `reference`; source/contract are the authenticated public bundle. Use a new output directory. The final evaluator and production call the same matching module. The manifest binds implementation hashes and preserved evidence, excluding itself.

See [product assessment](PRODUCT_ASSESSMENT.md) for the candid 3/5 rating and Track 2B gaps. Full sovereign deployment/submission clearance, broad vote coverage, independent user testing and dependable service beyond finite starter credit remain open. Video files were left unchanged.
