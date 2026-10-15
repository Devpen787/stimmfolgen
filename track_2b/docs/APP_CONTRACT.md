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

## Optional live QA contract — 15 October

Default reviewed routes keep their recorded labels. `GET /api/live/status` reports whether a live provider is configured; `POST /api/live/question` accepts exactly one public `question` string, 3–700 characters. Extra private fields and cross-origin browser requests are rejected. Only explicitly configured local pinned v1.5 weights or the allowlisted Infomaniak v1.5 70B API can serve it. No hosted request has yet been verified.

The generator selects human-reviewed fact IDs and writes an explanation using those facts. Original quotations and citations are resolved by the server, never generated. Schema validation and a separate same-model semantic pass fail closed. Live answers remain `LIVE_AI_UNREVIEWED`; neither check grants human-reviewed status. Unknown, withheld, busy, unavailable and budget-limit states do not replay recorded content as fresh inference. See [development failures](evidence/live-apertus-2026-10-15/REVIEW.md). Only explicit evaluation code persists test traces; the production route does not log/store questions or attach voter notes.
