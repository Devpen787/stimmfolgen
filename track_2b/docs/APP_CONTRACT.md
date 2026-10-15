# Implemented reviewed-case contract

The full v0.1 schemas are proposed architecture and continue to have their own synthetic design checks. The working runtime implements the smaller reviewed-case contract below. It never publishes raw model prose.

- Startup: authenticate the actual source PDF, archived release traces, original review packet and five bound statement approvals. Reject startup on mismatch.
- `GET /api/case`: one historical PRE_VOTE AHV case; `as_of`, separate `content_cutoff`, `available_by`, source hash, five statement cards with epistemic `kind`, reviewed `origin` and immutable source citations. Includes a bounded Gate certificate and `inference_mode=REVIEWED_RECORDED_CASE`, `live_inference_performed_for_this_request=false`.
- `GET /api/health`: backend health, bounded Gate status and recorded-case mode.
- `GET /api/booklet.pdf`: authenticated original document retrieved at image build or explicitly supplied locally; never altered or committed as corpus data.
- `POST /api/question`: JSON object with exactly one string `topic`; supported topics `change`, `cost`, `future_cost`, `personal_cost`, `attribution`. Unsupported topics abstain. Additional fields or bodies over 2048 bytes return 400. Personal cost is always `null` (unknown, not zero), with the two missing enacted-financing facts.
- All HTTP responses are no-store and same-origin CSP. No request logging; private data stays in browser memory by default, or an opt-in encrypted browser vault. No outbound requests at container runtime. Backup export is encrypted and created in the browser. No choices, notes or search queries are sent to the backend or model.

`test_app_backend.py` tests the HTTP/privacy boundaries with a clearly labelled routing fixture, not fabricated model evidence. A cold Docker smoke test separately loads and verifies the real reviewed case. The inference CLI is a separate ingestion/evaluation path; new candidates must be independently checked and reviewed before publication.

- `GET /api/catalog`: five selected proposals, source dates/check dates and separate official updates/relationships. These manually checked public web excerpts are not new Apertus outputs, original HTML byte hashes or part of the historical inference frame.
- Browser vault: native WebCrypto PBKDF2-SHA256 (600,000 iterations), random 16-byte salt, AES-GCM-256 with fresh 12-byte nonce per write. Only ciphertext and cryptographic parameters persist; passphrase/key stay in memory. Reload, page hiding, idle timeout and cross-tab changes lock private data. See ADR 0006 and the threat model.

## Live source-match contract — 15 October, product reliability pass

Default reviewed routes retain their recorded labels. `GET /api/live/status` reports actual provider configuration. `POST /api/live/question` accepts exactly one public `question` string, 3–700 characters; extra private fields, oversized bodies and cross-origin browser requests are rejected. Public delivery uses exact allowlisted `swiss-ai/apertus-v1.5-8b` on Public AI through Cloudflare, with provider-reported identity rather than weight attestation. The optional local route authenticates pinned v1.5 8B MLX weights on loopback. The prepared Infomaniak adapter remains unverified and inactive.

`live-ahv-reviewed-source-match-v8` publishes no model-written factual prose:

- Selection: exactly `{kind, fact_ids}`, with kind `EVIDENCE`, `VOTING_ADVICE` or `OUTSIDE_EVIDENCE`. IDs must be unique known ledger entries; only `EVIDENCE` has nonempty IDs.
- Separate relevance call for evidence: exactly `{fact_ids}`, a unique subset of the selection. Empty relevance is an honest no-match. No generated text field is accepted.
- Published claims contain exact reviewed statement text, source citations and epistemic kinds, resolved server-side. `EVIDENCE_MATCH` / `REVIEWED_EVIDENCE` identifies this composition. `statements_human_reviewed=true` describes the statements; `human_reviewed=false` describes the runtime match. The original source/approval Gate and deterministic reference checks are independent of model agreement; the same-model relevance call is not an independent semantic guarantee.
- `SERVICE_LIMIT` and `EVIDENCE_LIMIT` contain application-composed scope/policy messages. Unsupported, withheld, busy, unavailable and allowance-limit states never replay recorded material as fresh inference. The UI labels its reviewed-source browsing alternatives explicitly.
- No questions, private notes or choices are logged/persisted by the production route. Explicit evaluation tools alone save authored public-question traces. Provider processing of public questions is disclosed.

The public demo has persistent caps of 200 lifetime question reservations, 80/day and six per five minutes per network, with one active request. No payment/card/top-up is enabled. The owner's Mac is never exposed. Static assets now pass through the Worker for no-store and CSP headers, with versioned app/style URLs for existing cached clients.

The local 4-bit matcher uses fictional, unrelated formatting/reasoning examples. Its remaining relevance failures are disclosed in the app and local guide. The original bounded reviewed Gate remains PASS; this does not certify arbitrary live matching. See [retained failures, actual inference and browser proof](evidence/product-reliability-2026-10-15/REVIEW.md) and [ADR 0007](adr/0007-live-source-matching-with-immutable-reviewed-wording.md).
