# Product reliability pass — 15 October 2026

**Bounded result:** useful hosted AHV evidence is no longer rejected by a model grading its own prose. Live Apertus selects source IDs; published factual wording comes unchanged from the five accepted statements. This is live question interpretation and source matching, not newly generated factual analysis. The runtime match is not human reviewed. PR #4 remains the review vehicle; video files were left unchanged.

## Why useful answers were withheld

The former prose generator/auditor could judge the user's impossible request rather than the response explaining its uncertainty. Reworded audit targets reduced false rejection, but real negative controls then approved a wrong speaker and denial of an existing source. Those prompt-only fixes were rejected. See `diagnostics/diagnostic-01.jsonl`, `adversarial-01.jsonl`, `v6-*` and `v7-*`.

The implemented `live-ahv-reviewed-source-match-v8` accepts only `{kind,fact_ids}`, followed for evidence by a separate `{fact_ids}` relevance check. Known IDs resolve server-side to exact accepted text, epistemic kinds and immutable source spans. No model-written quote, amount, actor, date or factual explanation can enter public claim fields. Malformed output and unknown/duplicate references fail closed. The independent source/approval gate and authored reference comparisons remain distinct from the fallible same-model relevance call. [Decision](../../adr/0007-live-source-matching-with-immutable-reviewed-wording.md).

Advice and evidence-limit messages are application-composed and labelled. A missed match offers all reviewed statements as explicit browsing alternatives; these are not substituted live answers. Later events link to separately dated official Updates. The UI explains exactly where Apertus helps and where encryption protects private data.

## Actual inference, including failures

All hosted calls request exact provider model `swiss-ai/apertus-v1.5-8b`, temperature 0, max 250 output tokens per phase. Identity is provider-reported, not attested weights. The server still enforces the model/pricing allowlist, finite starter credit, 200 lifetime/80 daily reservations, six per five minutes per network and one active request. No payment, top-up, new model download or Mac exposure was enabled.

Final authenticated bundle SHA-256: `4a61c0100bec8b4ad5949292710ef0a3cff7d9013d433aa32be9ee7d5b2d7354`.
Source SHA-256: `53c7cc72c28f80969ed56d7813ad8c05e505b1817923418d0dfa45368a6bd07e`.
Historical frame: 2 March 2024, 23:59:59 CET. Source statements, human approvals and the original bounded Gate certificate were not changed.

| Evaluation | Exact authored-reference matches | Limits |
| --- | --- | --- |
| Final hosted 13-question development suite | **12/13** | German financing includes extra P05 argument context alongside the correct P04 uncertainty; wording/actor stay reviewed |
| Additional six authored paraphrases | **4/6** | A government-attribution paraphrase misses; fabricated-quote request safely returns no match rather than the expected corrective P04. No fabricated quote is published |
| Local 4-bit matcher before fictional examples | **7/13** | Wrong/extra relevance matches, including personal costs and an unrelated proposal |
| Final local matcher with unrelated fictional examples | **9/13** | Benefit and personal uncertainty corrected; false-actor question has extra P04; both German questions add context; unrelated fireworks question still matches AHV costs |

Final hosted references: `diagnostics/hosted-final-01.jsonl`; additional paraphrases: `heldout-01.jsonl`. Local final: `local-final-01.jsonl`. Gold references are in [cases.json](cases.json) and [heldout-cases.json](heldout-cases.json), outside prompts. Local examples concern a fictional library, not AHV answers or expected IDs. Local weights remain the previously inspected pinned Apertus v1.5 8B MLX 4-bit conversion on the M3 Pro/18 GiB Mac. Local matching is explicitly experimental, **not full live acceptance**.

Earlier malformed local completions, false rejections, scope errors, negative-control false approvals, later prompt variants and an upstream 70B HTTP 429 remain in `diagnostics/`. A tested no-match recovery that searched every fact was rejected: it recovered one actor query but incorrectly returned AHV costs for unrelated proposals. Do not revive it as a fix. These are development questions, not a blind benchmark, broad accuracy measurement or independent semantic approval of runtime output.

## First-visit journey proof

Agent-operated real in-app browser, desktop **1280×800** and responsive phone **389×845**. Fresh, temporary `stimmfolgen-qa-desktop` and `stimmfolgen-qa-phone` origins avoided the owner's existing storage. Both used the production Worker Durable Object, exact same Public AI secret and **same persistent quota**; no key was copied into the QA websites. The Mac was not a visitor host. Temporary QA sites were removed after evidence capture.

Both journeys exercised:

1. Empty My votes → Search AHV → Track → My votes → Explore my vote, without inferring a voting choice.
2. Meaning and actual live inference. Production benefit returned P01; desktop personal-cost query returned P04; phone false-attribution query returned P05 with the government speaker intact.
3. Source/date dialog with original German passage, actor, historical frame, span/hash details and original PDF page link. The desktop link opened the official booklet on page 11.
4. Dated official Updates, Related votes, and Me/Others/Switzerland perspectives, including changing the factual situation. These static reviewed perspectives are not falsely labelled fresh inference.
5. Synthetic private note → visit save → opt-in encrypted vault → save → reload lock → unlock and restore. Choice stayed **Not recorded**. Real user notes/storage were not inspected or cleared.
6. Voting-advice refusal; later-events no-match → working Updates button; unreviewed upcoming proposal and no-recorded-update states; empty search. Missing catalogue updates never imply nothing happened.

Phone inspection found hidden Explore sections in the horizontally scrolling row; all five now wrap into two rows with 44px-high buttons. No horizontal document overflow at 389px; desktop document width was 1280px. Browser console checks had no warnings/errors. These are responsive browser interactions, **not physical iOS/Android testing or independent human usability research**.

A deployment recheck found stale JavaScript: static assets bypassed the Worker, so intended cache/security headers were not applied. Static routes now run through the Worker; versioned script/style URLs replace cached builds. Actual deployed app/style/guide bytes matched local files, with `Cache-Control: no-store` and CSP. A runtime test covers those asset headers. Browser snapshots/screenshots in [browser/](browser/) include both successful and superseded states; final cache-fixed states are identified by filename.

## Deterministic and release checks

- **104 Python tests pass:** source/provenance/meaning/approval boundaries, exact reviewed composition, strict selection/relevance schemas, HTTP/private-field rejection and admission controls.
- **9 hosted tests pass**, none skipped: real workerd + SQLite Durable Object with a clearly synthetic provider; malformed/invented output, concurrent requests, quota persistence across restart, model identity/pricing/redirect boundaries and asset headers.
- Actual vault crypto test passes: encrypted-only persistence, fresh nonces, wrong-password/tamper rejection, reload lock, concurrent saves, backup recovery and cancelled-lock races.
- Authenticated export parity passes. Fresh Docker build verifies the original Gate offline and the real recorded-case HTTP journey on an isolated loopback port. Test-only container/services were stopped.
- Public HTTP boundaries reject notes/choice/salary/history fields and cross-origin requests. Hosted inference remains available without the local model/app processes.

## Reproduce

From the repository root, using the existing approved private token file (never put a token in chat, a command argument or Git):

```sh
node track_2b/tools/evaluate_live_match.mjs \
  --cases track_2b/docs/evidence/product-reliability-2026-10-15/cases.json \
  --token-file .local/secrets/publicai_token --out .local/hosted-match-recheck-new
```

This makes actual provider requests using finite credit and saves request/response bodies without auth headers. Output directories must be new. A nonzero exit for imperfect exact matching is intentional.

For actual local inference, start `make local-run APP_PORT=8784`, then in another terminal:

```sh
.local/runtime/bin/python track_2b/tools/evaluate_local_match.py \
  --source-pdf .local/local/booklet.pdf \
  --model-dir .local/models/apertus-v1.5-8b-mlx-4bit \
  --cases track_2b/docs/evidence/product-reliability-2026-10-15/cases.json \
  --out .local/local-match-recheck-new
```

`MANIFEST.json` describes archived trace hashes and local-path redaction. Raw auth headers were never captured; the token was checked absent before committing. Generated/raw model weights and source PDF stay local. Production does not persist visitor questions. Original failed traces and prior Gate packets remain intact. No submission-ready/general-accuracy claim is made.
