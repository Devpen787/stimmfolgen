# StimmFolgen

Technical report - Hack Apertus Online, Track 2B - 14 October 2026

## 1. A usable historical referendum reader

StimmFolgen helps a voter examine what a referendum could change, who might be affected and what its source material does not establish. It gives no voting recommendation. The implemented prototype covers the 13th AHV old-age pension initiative of 3 March 2024 using the original German Federal Chancellery booklet.

The complete journey has four sections: overview, factual situations, evidence and disagreements, and a personal understanding brief. A provision, an attributed government projection and unresolved financing carry different labels. A pension recipient can inspect the proposed benefit; a working-age person sees that a definite personal financing charge is unknown. Each central statement opens the actual supporting source passage, actor, page, document hash and temporal context. Both committee and Council/Parliament argument sections are accessible.

The web app is explicitly a **reviewed recorded case**. It publishes wording separately accepted by the user after genuine local Apertus inference and independent checks. Clicking a web control does not make a new model completion. The five-year cost statement is labelled reviewed source-reference context; it was not extracted in the final happy-path model trial.

Bounded Gate 0 was cleared before frontend files were created. This is a narrow, tested vertical slice, not a production civic-information service or a general policy accuracy claim.

<!-- page -->

## 2. Evidence pipeline and publication boundary

Original PDF bytes are authenticated, extracted with PyMuPDF 1.28.2 and indexed as 91 immutable source spans. Apertus selects span IDs and typed fields; quotations resolve from the ledger rather than being generated. Every selected ID must resolve to the source edition and correct PDF page. A separate, evaluation-only bounded semantic reference checks predicate, values, actor, epistemic type and missing facts. It is coding-agent-authored, not an independent academic benchmark. The user reviewed the five published statement meanings and wording, not every raw control trace.

Actor attribution uses two real completions: neutral source evidence/actor extraction and independent parsing of the requested actor. Application logic compares these actors symmetrically and retains extracted IDs unchanged. Neither model prompt nor comparator receives the expected actor, gold span or evaluation reference. The resulting conflict/refusal is application-composed, not a single LLM-generated answer.

The source hash is 53c7cc72c28f80969ed56d7813ad8c05e505b1817923418d0dfa45368a6bd07e (759,783 bytes, 32 pages). Its printed content cutoff is 29 November 2023. An exact-byte archived official copy establishes availability by 11 January 2024, 12:11:17 UTC. This is an archive-observation upper bound, not the first publication instant or a signed timestamp. The public case frame is 2 March 2024, 23:59:59 CET. These dates remain separate; older traces/span identities are not rewritten.

At backend startup, the release guard authenticates the original packet and release manifest, re-extracts the catalogue, checks pinned recorded model identity, verifies temporal admission, requires five bound ACCEPT decisions and independently replays the controls. Missing approval, changed source/model or failed control blocks startup. New inference candidates cannot automatically replace reviewed published statements.

The smaller implemented runtime contract is documented in docs/APP_CONTRACT.md. The larger blueprint and encrypted-vault schemas remain design targets, not implemented functionality.

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

Eighty-three deterministic tests pass locally, covering source/span integrity, independent semantic rejection, actor comparison, public timing, pinned identity, review bindings, HTTP routing and privacy rejection. Separate Docker smoke checks load the real case, exercise personal-cost and unsupported-question abstention, reject private extra fields and serve authenticated source bytes. Browser checks cover the four-section journey, source dialog/actor label, narrow layout, keyboard dismissal, explicit export and clearing notes on reload. No user comprehension study or comprehensive accessibility audit has been run.

Notes exist only in browser-tab memory. They are not sent to the backend or written to request logs. Export is an explicit plaintext download, not an encrypted vault. The backend accepts only a topic field and rejects notes/salary additions; same-origin CSP and no-store headers apply. No login, analytics, political preference collection, persuasion or voting recommendation is implemented.

Unverified: second referendum, unseen-ballot generalisation, language parity, production encryption, current-law coverage and official-BF16 conversion equivalence. Approximate expenditure figures remain attributed forecasts. Unknown personal cost does not mean zero.

<!-- page -->

## 5. Deployment, reproduction and delivery

The selected architecture is on-premise: native local model ingestion/evaluation, followed by Docker-contained reviewed publication. The frontend uses plain HTML/CSS/JavaScript and the backend Python's standard HTTP server. The Docker image pins PyMuPDF and its Python base digest, runs as a non-root user and uses a read-only filesystem. Root make run starts the app on host loopback port 8770; track_2b/make run delegates to it. Native MLX inference cannot run on the Mac GPU inside Linux Docker, and is not claimed to do so.

Image construction needs internet to retrieve the base/dependency packages and authenticated official booklet. The built reviewed-case application has no outbound runtime requirement. An offline container check with network disabled revalidates the stored Gate evidence without weights or an LLM endpoint. A separate clean-clone Docker launch and actual API journey are documented in docs/evidence/APP_RELEASE_2026-10-14.md. This proves publication/replay delivery under the stated environment, not portable fresh inference or full air-gap provisioning.

Judges can run make run, inspect provision/source, switch pension-recipient and working-person situations, deliberately ask for a definite CHF charge, inspect attributed arguments and export an ephemeral brief. docs/JUDGE_RUN.md also gives the separate native inference commands and required pinned weights. The local walkthrough is assembled from real running-app captures with narration, not a continuous live-generation screen recording. No hosted deployment, external video upload, merge or submission has been performed.

Source rights are separate from the project's Apache-2.0 code licence. The original PDF is downloaded for local processing and not committed as a dataset. Limited attributed passages are used for source analysis; broad document/image redistribution has not been licensed. Government web availability does not itself grant reuse rights. Do not publish a bundled source image/container as an openly licensed corpus. Source licensing remains a submission-scope check.

References: Federal Chancellery original 2024 booklet; the exact archived government copy of 11 January 2024; tokimoa model card and declared swiss-ai upstream; admin.ch conditions of use; repository ADRs 0002-0005, source/trace manifests and human decision records. Direct links are listed in docs/evidence/APP_RELEASE_2026-10-14.md and docs/JUDGE_RUN.md.
