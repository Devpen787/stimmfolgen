# Implemented reviewed-case contract

The full v0.1 schemas are proposed architecture and continue to have their own synthetic design checks. The working runtime implements the smaller reviewed-case contract below. It never publishes raw model prose.

- Startup: authenticate the actual source PDF, archived release traces, original review packet and five bound statement approvals. Reject startup on mismatch.
- `GET /api/case`: one historical PRE_VOTE AHV case; `as_of`, separate `content_cutoff`, `available_by`, source hash, five statement cards with epistemic `kind`, reviewed `origin` and immutable source citations. Includes a bounded Gate certificate and `inference_mode=REVIEWED_RECORDED_CASE`, `live_inference_performed_for_this_request=false`.
- `GET /api/health`: backend health, bounded Gate status and recorded-case mode.
- `GET /api/booklet.pdf`: authenticated original document retrieved at image build or explicitly supplied locally; never altered or committed as corpus data.
- `POST /api/question`: JSON object with exactly one string `topic`; supported topics `change`, `cost`, `future_cost`, `personal_cost`, `attribution`. Unsupported topics abstain. Additional fields or bodies over 2048 bytes return 400. Personal cost is always `null` (unknown, not zero), with the two missing enacted-financing facts.
- All HTTP responses are no-store and same-origin CSP. No request logging; notes remain in browser memory. No outbound requests at container runtime. Export is a browser-created plaintext file.

`test_app_backend.py` tests the HTTP/privacy boundaries with a clearly labelled routing fixture, not fabricated model evidence. A cold Docker smoke test separately loads and verifies the real reviewed case. The inference CLI is a separate ingestion/evaluation path; new candidates must be independently checked and reviewed before publication.
