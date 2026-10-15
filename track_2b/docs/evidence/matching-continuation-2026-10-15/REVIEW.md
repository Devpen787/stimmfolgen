# Matching continuation — 15 October 2026

PR #4; previous baseline `3e9083b`. Public demo: https://stimmfolgen-demo.stimmfolgen-hosted.workers.dev/.
Video assets and submission materials were not edited. No payment, top-up, paid plan or visitor access to the Mac was enabled.

## What changed and why

Hosted Apertus interprets the public question into a neutral English search query. Deterministic BM25F retrieves authenticated reviewed statements; Apertus then checks each candidate against the original question and its untrusted translated focus. Strict structured output and mechanical validation prevent model-authored prose/IDs from entering factual fields. All displayed factual wording, types, actors and source spans remain the accepted P01–P05 ledger. There is no runtime question-to-answer map. Planner prompts contain no ledger IDs or expected answers. A fictional library example teaches comparison cardinality; it is labelled fictional, not source evidence.

No lexical match means no candidate. A model-only fallback was rejected after it answered a worker-charge question with a pension benefit. Expanded source-index prompts and more permissive quotation prompts were also rejected after reproducible routing/directness regressions. The actor-attribution question is recovered through query interpretation and retrieval, rather than assigning every speaker question to one fixed card: cost-estimate speaker questions correctly retrieve the distinct initial/five-year statements.

The same-model directness check is fallible and is not independent truth verification. Deterministic source integrity and accepted wording provide a separate constraint. A request's match is not human reviewed. The bounded original Gate 0 certificate remains unchanged; general live accuracy is not certified.

## Actual final inference results

Provider-reported `swiss-ai/apertus-v1.5-8b`, temperature 0, structured JSON decoding, actual hosted requests. These are development evaluations: both sets were inspected while debugging and are not an untouched benchmark. Expected IDs are used only after inference. No expected IDs enter runtime prompts.

| Set | Exact scope + reference-set matches | Evidence |
| --- | --- | --- |
| Original real AHV suite | 13/13 | First 13 questions in the frozen original case list |
| Original suite plus six earlier paraphrases | 17/19 | `verified-19/` |
| Nineteen additional multilingual/attribution/unsupported-topic paraphrases | 17/19 | `verified-new19/` |
| Combined | 34/38 | Full requests, responses and expected/observed IDs preserved |

All four final exact-match failures returned no factual claims:

- `different_proposal`: childcare question classified EVIDENCE instead of OUTSIDE_EVIDENCE; no statement published.
- `fabricated_quote_request`: requested fabricated CHF 800 quotation safely produced no match, but missed the useful financing-uncertainty correction.
- `other_new`: fireworks/business question classified EVIDENCE instead of OUTSIDE_EVIDENCE; no statement published.
- `zero_new`: “workers would definitely pay nothing” had no lexical match; no charge/zero-cost answer was invented, but the useful uncertainty correction was missed.

This is improved core-suite coverage and verified attribution recovery, not a claim that every matching failure is solved. Temperature 0 did not eliminate variation between repeated hosted runs. Earlier iterations include unsafe relevance errors; they have not been deleted or relabelled as passes.

## Desktop and phone journeys

Agent-operated Codex browser on fresh temporary QA origins, sharing the production Durable Object and its persistent caps/secret. No owner vault was opened, cleared or overwritten. Desktop 1280×800 and responsive phone 389×845; this is not physical-device proof or independent human research.

Both journeys exercised Search AHV → Track → My votes → Explore → actual free-form attribution question → dated source details → Updates → Related votes → Me/Others/Switzerland perspectives → synthetic note → visit-only keep → opt-in encrypted save → reload locked → unlock recovered. Choice remained NOT_RECORDED. Desktop source link opened the actual booklet at page 16, including the correct argument section. Phone additionally followed the related financing vote and checked its no-reviewed-analysis/no-verified-update states. Desktop voting-advice refusal and phone unsupported-climate no-match left the reviewed evidence available. A concurrent follow-up request showed the expected honest BUSY state and succeeded after the other request completed. Both consoles had no observed errors/warnings; observed document width matched viewport width.

A test-harness issue applied the viewport override before creating a tab, leaving an initial phone-labelled tab at desktop width. This was detected from DOM dimensions. That trace/screenshot is retained as `phone-tab-before-viewport.png`; the full mobile flow was restarted and rerun after verifying 389 pixels. The `*-389` screenshot is the phone proof. AX roles sometimes differed from DOM roles; locator failures were resolved using fresh DOM snapshots, not treated as product failures.

Browser captures, source/notes/refusal snapshots and dimensions are preserved in the archive. Notes and passphrases in these QA workflows were synthetic; no real political choice was recorded. Privacy boundary tests verify encryption and reject extra private fields; this is not an independent security audit or a network-forensics claim.

## Runtime deployment and verification

The contract is `live-ahv-query-retrieval-v9`. The authenticated bundle SHA-256 is `50f2efef9b196e6bd1469a2e8744c6732262d64ae545d21df8d371464c25f1dc`.

Cloudflare script retrieval confirmed that updated code was uploaded, while inference briefly came from an older Durable Object instance (its new execution counter was absent). Cloudflare documents eventual consistency between Worker and Durable Object updates: https://developers.cloudflare.com/durable-objects/concepts/durable-object-lifecycle/.

The final router now rejects actual inference whose `execution_contract_sha256` does not match the authenticated bundle. It leaves reviewed publication available during propagation. This prevents a successful upload from being mistaken for proof that the current inference contract is executing. No quota was reset or namespace replaced. Actual production attribution proof (`public-execution-pin-01.json`) returned HTTP 200, EVIDENCE_MATCH, the exact bundle hash above and one directness check. Final deployed version: `23d32333-9545-4915-924b-3691f20865c3`; this follow-up only extracted/tested the identical execution-hash predicate. Production and QA browser attribution were rechecked after the pinned execution was observed.

A permissive quotation experiment was briefly deployed (`65ea5a7d-2ac8-4b4e-89fd-5afb4cb4fc46`) before its unsupported-topic regression completed. It was replaced by the strict guard (`86414810-6e05-445a-8f3f-1296cebd350f`); the model-only fallback was subsequently removed. Those transitions and raw failures remain preserved. No claim is made about unobserved visitor requests during that interval.

Verification: 104 Python tests; 16 hosted tests including real workerd/Durable Object concurrency, rejection, persistent quota across restart and deployment-contract pinning; actual vault crypto tests; authenticated source/bundle parity; cold Docker Gate check. Hosted tests use a labelled synthetic provider, not substitute inference evidence. Renamed/reordered IDs and a fictional non-AHV ledger test generic retrieval, not real second-case accuracy.

## Optional local investigation

Existing Apple Silicon M3 Pro/18 GiB, pinned 4-bit Apertus v1.5 MLX conversion and authenticated original booklet were used. No model weights or vendor tokenizer files changed. Retained experimental local evaluations scored 10/19 (`local-pair-01`), 12/19 (`local-search-01`), and 11/19 (`local-noun-01` with explicit native reasoning-prefix compatibility adapter). Reasoning support did not establish semantic correctness. The adapter and model-probe/launcher changes were not shipped. Owned loopback test services were stopped; unrelated local services were untouched. Local matching remains experimental under the existing v8 contract and disclosure.

## Reproduction and preservation

Final real provider evaluation (requires existing credit/key; do not put the key in a command argument or commit it):

```sh
node track_2b/tools/evaluate_hosted_matching.mjs CASES_JSON NEW_OUTPUT_DIRECTORY TOKEN_FILE_PATH
```

`verified-19/*.json` and `verified-new19/*.json` include the frozen public questions/gold references as well as complete actual model requests/responses. The tool loads the authenticated export and shares the production retrieval/validators. It compares gold only after inference and records every failure.

`preserved-experiments.jsonl` retains experimental prompts, raw requests/responses, rejected approaches, logs, scripts and native diagnostics. Each record has its original path/hash and the hash of its published content. Home/account/email paths are redacted; no auth headers or key contents are included. Some early HTML/transport failures were parsed before raw-body capture and lack that raw body; later capture records non-JSON bodies explicitly. Two rejected permissive-contract evaluation processes were stopped after the regression was established; their partial records remain, and missing trials are not counted as passes. One Python HTTP probe failed before retaining its non-JSON body; later Node probes capture status/body before parsing. One cold Worker invocation initially used the wrong build output path; its ENOENT log and corrected 16-test run remain preserved.

`experiment-counts.json` counts only recorded result objects, not planned/absent trials. `MANIFEST.json` authenticates published files. Earlier evidence packets are unchanged. Public inference remains finite starter-credit hosting outside Swiss sovereignty; no permanent free-compute or uptime promise is made.

Temporary QA Worker scripts were deleted successfully after testing; their deletion responses are retained. The production Worker and its persistent usage namespace remain in place. The final public desktop tab is left open; original user/private tabs were not modified.
