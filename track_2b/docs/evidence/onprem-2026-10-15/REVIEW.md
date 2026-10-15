# On-premise installation and two-vote continuation - 15 October 2026

PR #4, implementation commits `917e77c` and `b9e4b27`. No video changes, main merge or submission. The original AHV Gate remains bounded; additional cases do not inherit that certificate.

## Fresh installation actually executed

A fresh clone of the public GitHub branch at `917e77c53a4f9e45ad1db3eadb7acbbe3354ab23` had a clean working tree, a newly created Python environment and no-cache Docker application builds. Pinned model artifacts were APFS-copied from existing downloads, then SHA/served-identity checked. This was the same M3 Pro / 18 GiB Mac; not a second machine, new remote 4.53 GB model download, fresh Docker base-layer download or air-gap test. Exact dependencies and commands are retained in the trace archive.

`make run ONPREM=1 APP_PORT=8784 ONPREM_FLAGS=--no-cache` started real native MLX on 127.0.0.1:8768 and a non-root read-only Docker app on 127.0.0.1:8784. Docker Desktop's host bridge reached the inspected model. No API credential, hosted fallback, public Mac listener or tunnel was used. The browser received the correct pension-recipient answer in 7.522 seconds. The isolated checkout was subsequently fast-forwarded to `b9e4b27`, rebuilt and relaunched; an actual HTTP attribution question returned P05 with live inference true. Private extra fields returned 400; unknown case returned 404.

The native model is `swiss-ai/Apertus-v1.5-8B`, community MLX 4-bit conversion `tokimoa/apertus-v1.5-8b-mlx-4bit`, revision `f08ed532a657bef7d322bd0cbca43dac13a9d0a3`. Weight SHA-256 `d0478edeb06bf18e5f4f7b50db77d89b839730b2d16cb1020015e6099e42074b`, 4,530,491,646 bytes. MLX 0.32.0 / mlx-lm 0.31.3 / transformers 5.15.0. Native inference uses temperature zero and disabled thinking, with Hub network/telemetry disabled. Setup/build still need network. Official BF16 equivalence and other hardware were not tested.

## Second real source and honest review boundary

Homeownership tax reform, ballot 28 September 2025: actual 48-page Federal Chancellery booklet, SHA-256 `39c020145299913685e4d0b6899fa23bb1f94938652a417e0c1da08d316ade8a`. Four immutable source-bound candidates cover the linked legal change, cantonal discretion, renters and conditional individual effects. Printed editorial cutoff is 20 June 2025, distinct from actual October 2026 retrieval. No exact-byte pre-vote public archive witness is asserted; mode is DOCUMENT_EXPLANATION.

**Human wording acceptance is still pending.** The production registry has only AHV; the second vote's public entry exposes official information, separate dated result and private tracking/notes. It cannot run candidate analysis. The private localhost preview injected the candidate solely for end-to-end engineering checks and visibly said it awaited approval. This is not public release/admission evidence. Exact statements and spans: [review packet](../property-tax-2026-10-15/REVIEW.md).

## Actual model evaluation

Final local set: **20/20**, original AHV 13 and seven second-case questions. Sixteen questions invoked real local Apertus; four intentional advice/later-event cases were deterministic application-policy refusals without a model call. Raw per-completion requests/responses are in `fresh-and-final-traces.jsonl` under `onprem-two-cases-final/`. Original question terms stay in retrieval because the quantised model omitted important subjects. Final native response parser additionally authenticates the server's advertised default_model alias and rejects invalid/truncated responses.

Hosted set: **45/45**, including seven second-case candidate questions, with real Public AI `swiss-ai/apertus-v1.5-8b` calls and v10 query/directness protocol. Candidate data is injected only into the explicit evaluation command, never automatically into production. These are known inspected development cases, not held-out accuracy, language parity, source-extraction success or native/hosted protocol equivalence. Answer IDs are evaluation references only, absent from model prompts as expected outputs.

Reproduce with the local model running and a new output directory:

```sh
node track_2b/tools/evaluate_onprem.mjs track_2b/docs/evidence/onprem-2026-10-15/onprem-two-cases.json .local/new-local-run track_2b/docs/evidence/property-tax-2026-10-15/case-candidate.json
```

For hosted evaluation, use the companion `hosted-two-cases45.json`, the documented private token file and `tools/evaluate_hosted_matching.mjs`; the candidate path is the fourth argument. Never place a token in shell arguments, logs or committed files.

## Browser and deterministic proof

Fresh-install AHV desktop journey: search, track, explore, actual local answer, source/date drawer, updates, related proposal and perspectives. Synthetic encrypted notes survived reload; wrong passphrase was rejected, correct unlock restored them; actual encrypted backup download was decrypted with the test passphrase to check only test entries. Idle locking and cancelled removal were observed. No owner's production vault was read, changed or cleared.

Private candidate preview: both votes at actual CSS 389x844 and desktop 1280x800. Live local AHV attribution returned P05; second-home discretion returned H02 and renter question H03, each with the correct source drawer. Updates, no-related state, perspectives and private note paths were exercised. Actual desktop backup restored both notes on the mobile test origin locally, with no upload. Reload locked them. Switching to the tax case while AHV inference was pending did not display a pension answer; returning to AHV displayed its own answer. Console error/warning captures were empty. These are agent-operated responsive browser tests, not physical-phone or independent-user proof.

Final checks: **108 Python tests; 29/29 compiled workerd tests, no skips; actual WebCrypto tests; offline Docker Gate replay; fail-closed mutations; cold HTTP smoke; authenticated hosted export parity.** Synthetic Worker/provider tests prove application behaviour, not real inference. Production/isolated hosted browser verification is recorded separately in `PUBLIC_RELEASE.md`. Ordinary screens have no statement IDs, source hashes, task receipts or failed-run commentary. Necessary source uncertainty, privacy and service availability disclosures remain; About this demo links reviewer detail separately.

## Preserved failures and limits

`attempts-before-fresh.jsonl` is the earlier immutable archive. `fresh-and-final-traces.jsonl` adds raw text/JSON logs and model traces with original and redacted-content SHA-256; only absolute home paths are redacted. Excluded: weights, Python environment, source PDFs, credentials and encrypted private backups. Browser records contain explicitly synthetic notes only. PNG captures are supplementary, not a substitute for actual inference traces.

Failures include invalid native four-field JSON, copied placeholders, omitted recipient query terms, an 11/13 local run, incorrect second-source extraction references/legal overstatement, legacy PDF fetch 502, Python transport 403 and an incorrectly resolved Worker-build test path. The latter test harness failure was corrected and actual compiled tests rerun. A tiny-width viewport calibration mismatch was recorded before verified CSS dimensions; requested dimensions alone are not proof. Earlier failures remain failures. A syntax-check mistake and locator ambiguity were corrected; no fabricated raw transcript is supplied for uncaptured terminal/UI events.

No general civic accuracy, autonomous fact verification, independent security audit, perpetually free hosting or whole-product/submission clearance is claimed. Rights/terms and reviewed main integration remain separate owner gates.
