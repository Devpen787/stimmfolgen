# StimmFolgen

Technical report - Hack Apertus Online, Track 2B - 15 October 2026

## 1. A private vote tracker with a reviewed historical case

StimmFolgen helps a voter examine what a referendum could change, who might be affected and what its source material does not establish. It gives no voting recommendation. The implemented prototype covers the 13th AHV old-age pension initiative of 3 March 2024 using the original German Federal Chancellery booklet.

The responsive desktop/mobile journey has three simple entry points: My votes, Upcoming votes and Search. A reader tracks a proposal without implying a Yes/No choice, then opens Explore my vote for its meaning, dated sources, official updates, related proposals and Me/Others/Switzerland perspectives. Detailed evidence is progressively disclosed. The catalogue contains five selected federal proposals; only AHV has reviewed Apertus analysis.

The October 2026 official AHV implementation update and November financing relationship were manually verified against official publisher pages. They are separate from the original pre-vote analysis, and not new model outputs. Source publication/check dates and explicit no-recorded-update states prevent historical forecasts being mistaken for observed outcomes. These web excerpts carry text hashes, not original HTML-byte provenance.

The web app is explicitly a **reviewed recorded case**. It publishes wording separately accepted by the user after genuine local Apertus inference and independent checks. Clicking a web control does not make a new model completion. The five-year cost statement is labelled reviewed source-reference context; it was not extracted in the final happy-path model trial.

Bounded Gate 0 was cleared before frontend files were created. This is a narrow, tested vertical slice, not a production civic-information service or a general policy accuracy claim.

<!-- page -->

## 2. Evidence pipeline and publication boundary

Original PDF bytes are authenticated, extracted with PyMuPDF 1.28.2 and indexed as 91 immutable source spans. Apertus selects span IDs and typed fields; quotations resolve from the ledger rather than being generated. Every selected ID must resolve to the source edition and correct PDF page. A separate, evaluation-only bounded semantic reference checks predicate, values, actor, epistemic type and missing facts. It is coding-agent-authored, not an independent academic benchmark. The user reviewed the five published statement meanings and wording, not every raw control trace.

Actor attribution uses two real completions: neutral source evidence/actor extraction and independent parsing of the requested actor. Application logic compares these actors symmetrically and retains extracted IDs unchanged. Neither model prompt nor comparator receives the expected actor, gold span or evaluation reference. The resulting conflict/refusal is application-composed, not a single LLM-generated answer.

The source hash is 53c7cc72c28f80969ed56d7813ad8c05e505b1817923418d0dfa45368a6bd07e (759,783 bytes, 32 pages). Its printed content cutoff is 29 November 2023. An exact-byte archived official copy establishes availability by 11 January 2024, 12:11:17 UTC. This is an archive-observation upper bound, not the first publication instant or a signed timestamp. The public case frame is 2 March 2024, 23:59:59 CET. These dates remain separate; older traces/span identities are not rewritten.

At backend startup, the release guard authenticates the original packet and release manifest, re-extracts the catalogue, checks pinned recorded model identity, verifies temporal admission, requires five bound ACCEPT decisions and independently replays the controls. Missing approval, changed source/model or failed control blocks startup. New inference candidates cannot automatically replace reviewed published statements.

The smaller implemented runtime contract is documented in docs/APP_CONTRACT.md. The larger blueprint remains a design target. ADR 0006 documents the deliberately smaller implemented browser-vault contract and its departures from that blueprint.

<!-- page -->

## 3. Real local Apertus use

Inference ran on the user's Apple Silicon M3 Pro Mac with 18 GiB RAM, macOS 26.6.2 arm64. Existing assets were inspected before runtime selection. The successful weights are a community text-only MLX 4-bit conversion, tokimoa/apertus-v1.5-8b-mlx-4bit, revision f08ed532a657bef7d322bd0cbca43dac13a9d0a3. Declared upstream is swiss-ai/Apertus-v1.5-8B, revision a411d838600baf0e3635a3daf66fb7c55fc97bb6. Model-card metadata declares Apache-2.0. Independent equivalence to official BF16 weights is not tested; multimodal capability is not claimed.

The safetensors weights occupy 4,530,491,646 bytes; SHA-256 is d0478edeb06bf18e5f4f7b50db77d89b839730b2d16cb1020015e6099e42074b. Group size 64, affine quantisation, 4 bits. Runtime: MLX 0.32.0, mlx-lm 0.31.3, transformers 5.15.0. The loopback server advertises the verified local path and serves default_model. Hub network access and telemetry are disabled during inference; no paid API is used.

Actual requests use temperature 0, 500 completion tokens and thinking disabled. The fresh 14 October release suite made eight genuine model completions for seven trials: provision, introduction cost, financing refusal, fabricated quote, false actor attribution, unsupported salary-based CHF charge and later-knowledge leakage. All seven passed independent bounded controls. The three-response combined happy path passed but remains an aggregate, not another completion.

Observed trial latency was 6.90-31.76 seconds, with the two-call actor trial taking 19.39 seconds. These timings measure this local execution, not production throughput or a service guarantee. Raw requests, HTTP responses, candidate fields, hashes, model metadata, timings and reference snapshots are preserved under docs/evidence/gate0-release-2026-10-14. Only the absolute local model directory is redacted. All preceding failed traces remain intact.

<!-- page -->

## 4. Evaluation, limitations and privacy

The earlier full-booklet direct Apertus baseline ran genuinely and failed mechanical controls, including unsupported financing, required coverage and quote/role checks; latency was 54.95 seconds. The extractive baseline returns three real source passages with no model interpretation. Earlier generated-quote and span-selection protocols failed reproducibly. In particular, the source-actor discovery fix could select the government then relabel the answer as committee; immutable selection plus independent actor comparison removed that failure in the bounded case.

These are development diagnostics with different protocols, not a controlled held-out accuracy comparison. A quote check or schema pass cannot prove meaning. The current seven-trial result is pipeline performance on one AHV development case; retrieval, task types, null personal costs and refusal policy are application-supplied. The user approved P01-P05 source statements. No human approval of T01-T07 raw trials is claimed.

Eighty-six deterministic Python tests pass locally, covering source/span integrity, independent semantic rejection, actor comparison, public timing, pinned identity, review bindings, HTTP routing and privacy rejection. Separate Docker smoke checks load the real case, exercise personal-cost and unsupported-question abstention, reject private extra fields and serve authenticated source bytes. Browser checks cover desktop/mobile tracking, local search, source dates, keyboard tabs, Me/Others/Switzerland, honest unavailable analysis, encrypted backup download/recovery and reload locking. Native WebCrypto tests additionally reject wrong passwords/tampering and check fresh nonces, concurrent writes and cancelled lock races. No user comprehension study or comprehensive accessibility audit has been run.

Visit-only tracking is the default. Persistent choices and notes are opt-in: a passphrase derives a nonextractable AES-GCM-256 key with PBKDF2-SHA256 (600,000 iterations, random 16-byte salt); every write uses a fresh 12-byte nonce. Only authenticated ciphertext and cryptographic parameters persist. Keys stay in memory; reload, page hiding, idle timeout and cross-tab changes lock the private view. Backups are encrypted and restored locally. No passphrase recovery or cross-device sync exists.

Private choices, notes, local search and perspective selections are never sent to the backend or Apertus. An instrumented synthetic browser journey recorded 33 public GET requests and zero POST requests. The production server does not log requests. Same-origin CSP, no-store responses and rejection of extra private API fields remain. External official-source visits can be observed by their publishers. Encryption does not protect an unlocked or compromised browser/device; this implementation has not received an independent security audit.

Unverified: second referendum, unseen-ballot generalisation, language parity, independently audited production security, current-law coverage and official-BF16 conversion equivalence. Approximate expenditure figures remain attributed forecasts. Unknown personal cost does not mean zero.

<!-- page -->

## 5. Deployment, reproduction and delivery

The selected architecture is on-premise: native local model ingestion/evaluation, followed by Docker-contained reviewed publication. The frontend uses plain HTML/CSS/JavaScript and the backend Python's standard HTTP server. The Docker image pins PyMuPDF and its Python base digest, runs as a non-root user and uses a read-only filesystem. Root make run starts the app on host loopback port 8770; track_2b/make run delegates to it. Native MLX inference cannot run on the Mac GPU inside Linux Docker, and is not claimed to do so.

Image construction needs internet to retrieve the base/dependency packages and authenticated official booklet. The built reviewed-case application has no outbound runtime requirement. An offline container check with network disabled revalidates the stored Gate evidence without weights or an LLM endpoint. A separate clean-clone Docker launch and actual API journey are documented in docs/evidence/APP_RELEASE_2026-10-14.md. This proves publication/replay delivery under the stated environment, not portable fresh inference or full air-gap provisioning.

Judges can run make run, find and track AHV, inspect sources and perspectives, view the separate update/related vote, and exercise the optional local encrypted vault with synthetic notes. docs/JUDGE_RUN.md also gives the separate native inference commands and required pinned weights. The current 98-second tracker walkthrough is composed from actual app captures with local synthetic narration; it is not a continuous recording or a fresh-inference session. Demo choices/notes are synthetic. Captions and the production script are included. Current tracker screenshots and browser evidence are in docs/evidence/tracker-v2-2026-10-14. The earlier report is preserved byte-for-byte there for its original manifest. No hosted deployment, external video upload, merge or submission has been performed.

Source rights are separate from the project's Apache-2.0 code licence. The original PDF is downloaded for local processing and not committed as a dataset. Limited attributed passages are used for source analysis; broad document/image redistribution has not been licensed. Government web availability does not itself grant reuse rights. Do not publish a bundled source image/container as an openly licensed corpus. The immutable review packet includes eight full-page PNGs and extracted passages. Their redistribution basis remains unresolved; the owner must clear rights before accepting the organiser warranty. No blanket source relicensing is claimed. THIRD_PARTY_NOTICES.md records the hold and dependency licences, including PyMuPDF AGPL obligations.

Original report contributions: Creative Commons Attribution 4.0 (CC-BY-4.0), https://creativecommons.org/licenses/by/4.0/ . Third-party extracts retain their applicable rights.

References: official booklet/archive, pinned model cards, government terms, ADRs 0002–0006 and source/trace manifests. Links: docs/evidence/APP_RELEASE_2026-10-14.md and docs/JUDGE_RUN.md.

Next month: a second reviewed case, unseen import, language parity and comprehension study. Scaling needs measured review and refresh costs. Codex assisted development, tests and documentation; Apertus performed policy inference.
