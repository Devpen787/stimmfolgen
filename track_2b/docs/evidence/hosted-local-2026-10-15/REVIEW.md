# Actual hosted and optional local delivery - 15 October 2026

Public URL: https://stimmfolgen-demo.stimmfolgen-hosted.workers.dev/ . PR #4, `codex/local-apertus-gate0-evidence`. This is **agent-operated browser/API testing**, not an independent user study, physical-phone test, load test or general accuracy certification.

## What is actually running

- Global Cloudflare Worker with static assets and one SQLite Durable Object. Public AI model **`swiss-ai/apertus-v1.5-8b`**, provider-reported identity, not attested weight bytes. A real generation request and separate same-model audit precede each published answer. No gold answer, expected actor or evaluation reference is passed in live prompts; the five reviewed statements are the explicit inference context.
- The user approved a seven-day Public AI credential and scoped official Wrangler access. Secret saved privately and installed server-side; never in frontend/Git/evidence. No card, paid plan, top-up or custom-domain configuration. The automatically allocated workers.dev hostname serves the app. This deployment is **not Swiss-sovereign**. The owner's Mac is not exposed/tunnelled.
- Finite free allowance: 200 lifetime reservations, 80/day, six/5min/network, one active pair. Failed attempts reserve capacity too. Persistent aggregate counts survive restart; network buckets are salted and ephemeral. No question, note, choice or IP is stored in the application database. Platform/provider retention remains outside the app's control. Price caps are USD .10/M input and .20/M output; two bounded 16KB prompts plus 850+200 output tokens imply approximately USD .70 maximum model usage across 200 pairs. Other wallet use can exhaust starter credit sooner. No permanent-free or uptime promise.
- Local launcher is a separate installation: M3 Pro 18 GiB, macOS 26.6.2; fresh `.local/runtime` with pinned MLX 0.32.0, MLX-LM 0.31.3, Transformers 5.15.0, HF Hub 1.27.0, PyMuPDF 1.28.2. Setup fetched/authenticated the booklet and reused existing pinned 4-bit weights. No new 4.6GB download was repeated. Both model and app bind only to loopback; hosted credentials are removed from the app environment. Other platforms are unverified.

## Real model results and failures

The source remains SHA-256 `53c7cc72c28f80969ed56d7813ad8c05e505b1817923418d0dfa45368a6bd07e`; historical public frame 2 March 2024, 23:59:59 CET. Review spans, actor/type/time boundaries and human approvals remain unchanged. Bounded reviewed Gate 0 remains PASS; live answers do not inherit human approval.

| Evidence | Observed result | Interpretation |
| --- | --- | --- |
| Direct Public AI 70B, v4 | Five upstream HTTP 429 errors | 70B availability was not established; not used in the deployed service |
| Direct 8B, v4 | One supported; four withheld | Real API diagnostic, not broad live acceptance |
| Direct 8B, v5, five questions | One supported pension answer; one voting-advice abstention; three withheld | Three useful-answer/refusal candidates still fail same-model audit; not all passed |
| Public HTTPS request, actor question | WITHHELD, actual inference | No unverified actor claim published; reviewed actor explanation remains available |
| Public HTTPS voting-advice question | INSUFFICIENT_EVIDENCE, zero claims | Successful deliberate abstention, not a voting recommendation |
| Public HTTPS pension question | SUPPORTED with P01/P02/P03 source references | Actual remote endpoint, no localhost/model download dependency |
| Public HTTPS, local model/app ports 8766/8783 stopped | SUPPORTED with actual provider response | Visitors do not depend on the Mac; closed ports verified before request |
| Fresh local runtime, pension question | SUPPORTED, 28.67s | Real inference with authenticated existing pinned weights |
| Fresh local runtime, voting-advice question | WITHHELD, 29.19s | Honest withheld path; no claim that local live abstention quality is fully solved |

The v5 change clarifies generic audit semantics: empty claims are permitted for an abstention; an evidence-gap explanation needs no claim ID; incorrect attribution fails, absence of an attributed claim does not. It does not hardcode question outcomes or expected actors. The same-model audit is **not independent semantic review** and can reject good answers or miss errors. Supported output also included cost context beyond the narrow pension question; relevance remains a limitation.

Raw current direct-provider request/response pairs are in `direct-8b-v5/`; prompts/outputs are retained without authorization headers. All original local failed trials in the preceding evidence directories remain intact. For the new 70B diagnostic, the five-error summary log survives but only raw trials 4 and 5 remain: an initial harness reused its output directory and overwrote raw trials 1-3. This is a recording failure, not five fully preserved raw traces. Later output directories are distinct.

## Deployment-specific failure fixed and reproduced

Initial deployed requests failed before reaching the provider. Actual workerd tests reproduced Cloudflare's rejection of Fetch `redirect: 'error'`. Changed to `redirect: 'manual'` and reject non-success HTTP statuses before parsing, so credentials are never forwarded to a redirected host. Retained the failed workerd log. Eight hosted tests now pass, including actual Worker/Durable Object execution with a **synthetic** provider: rejection of private extra fields/cross-origin requests, one active request, immutable reference resolution, invented quote/malformed completion withholding with accurate inference flags, daily limit without provider calls, and aggregate persistence across two restarts. Synthetic tests are not inference evidence.

## Public browser journey actually operated

1. New public origin opened with empty My votes; no account or model download. Search `AHV` returned past AHV and related financing. Tracked AHV without recording a choice.
2. Opened Explore and submitted the pension question. Browser displayed a fresh service response, immutable source buttons and AI-unreviewed label (observed 0.82s desktop, 8.88s phone-sized run; not an SLA or proof of provider cache policy).
3. Source drawer showed the original German passages, PDF pages, government actor, content cutoff 29 November 2023, public availability by 11 January 2024 and historical frame 2 March 2024.
4. Updates showed separately dated 5 October 2026 official implementation information; Related showed the distinct 29 November financing proposal. These are publisher metadata, not generated current-law answers.
5. Me: switched worker to pension recipient; Others: separate factual situation; Switzerland: attributed historical expenditure projection. No perspective selection was supplied as a model profile.
6. Entered a clearly synthetic note with choice left Not recorded. Created an on-device encrypted QA vault, saved, reloaded, observed locked view, unlocked and recovered exact note and tracked vote. No real user's political choice or note was used. Screenshot is labelled synthetic. Network non-transmission is supported by the explicit request construction, API rejection and crypto tests; no new browser network HAR was captured here.
7. At **actual CSS 389x845**, document width remained 389, with no horizontal overflow. Ran the voting-advice abstention and source-backed answer on this layout. No browser error/warning logs. This is responsive browser proof, not an actual iPhone/Android hardware result.

Screenshots: [phone answer](hosted-phone-happy.png), [phone abstention](hosted-phone-abstention.png), [synthetic private note restored](hosted-private-note.png). The manifest hashes files; raw API reports remain distinguishable from screenshots and fixture tests.

## Reproduce

- Hosted: open public URL and follow the journey; inspect service receipts and source hashes. Availability is finite, not guaranteed. Extra private fields in the API are rejected; `check_modes.py --url <origin>` checks boundaries without inference.
- Local: `make local-setup` with existing pinned model, or `make local-download` to permit downloading weights; `make local-run APP_PORT=8783`. Actual setup/cold-launch results are recorded. Ctrl+C ownership cleanup was tested before fresh installation: owned app stopped, pre-existing model remained. SIGTERM cleanup handler was added; a full signal matrix was not run.
- Build: `export_hosted.py --source-pdf <booklet> --check` must match the authenticated native case and exact prompts/hash. CI repeats this before hosted tests; static JSON is not an alternate unchecked source.
- Hosted fixture tests: install locked npm dependencies, Wrangler dry-run to an absolute output directory, set `WORKER_BUILD=/absolute/output/worker.js`, run `node --test track_2b/hosted/test/*.test.mjs`. 100 Python tests and actual Node WebCrypto suite pass separately.

## Remaining submission work

No main merge, organiser submission or terms acceptance. The earlier 98-second tracker video is historical. A new 115.09-second H.264/AAC 1280x720 live walkthrough is composed from actual public-app captures, with local Samantha synthetic narration and no trimmed audio. It is edited footage, not continuous recording. Script, capture hashes, captions and media metadata are in `track_2b/demo/`. Public watch page: https://stimmfolgen-demo.stimmfolgen-hosted.workers.dev/demo . A later voting-advice capture was WITHHELD rather than a published abstention, demonstrating the disclosed audit variability. Final package review remains necessary. Source rights/owner warranties remain separately documented. No second-case/unseen-ballot accuracy, permanent free hosting, independent semantic/security audit or human comprehension study is claimed.

Public video playback was verified in the browser without login: media readyState 4, duration 115.093343 seconds, one caption track and advancing playback time; then paused. Static video assets are staged from public files and a hash-verified MP4 only. No secrets/runtime directory is part of the asset bundle.
