# Implemented application contract

## Evidence and publication

The original AHV Gate authenticates the source PDF, recorded model requests/responses, source spans, historical availability witness and five bound human statement decisions. All retained authenticated packets are unchanged. A hash, source, model or approval mismatch prevents startup. This certifies a bounded historical case, not arbitrary policy accuracy.

Published quotations resolve to immutable source spans. Factual answer fields copy accepted wording, actor and epistemic type; live Apertus cannot supply replacement factual prose. Forecasts remain attributed; unresolved financing never becomes a definite personal CHF charge. Historical evidence, editorial cutoff, public availability and later official updates are separate.

Additional cases require real source bytes/spans and a human wording acceptance bound to the statement hash. The homeownership-tax candidate is not admitted. The public catalogue has six selected entries, with official information available independently of whether analysis is published.

## Public API

- GET `/api/catalog`: selected votes, official source dates, separate updates and relationships.
- GET `/api/cases`, `/api/case?case=ahv13`: allowlisted published cases. Unknown cases fail instead of falling back to another vote.
- GET `/api/health`: bounded source-Gate health, not proof of fresh inference.
- GET `/api/booklet.pdf?case=ahv13`: authenticated local source or official publisher redirect, depending on runtime.
- GET `/api/live/status`: configuration and hosting/privacy disclosures.
- POST `/api/live/question?case=ahv13`: exactly one public question string, 3–700 characters. Extra fields, oversized bodies and cross-origin browser requests are rejected.
- The reviewed Python replay route also accepts POST `/api/question` with one supported topic. It is explicitly recorded publication, not fresh inference.

The selected public case is in the URL; private notes and selections never enter the JSON body. A browser answer is bound to case ID, source SHA, exact statement wording and epistemic type. Delayed answers cannot migrate to a different vote. Saved notes pin the source for their own vote.

## Runtime modes

Default `make run` serves authenticated reviewed evidence in a non-root read-only Docker container. New inference is absent in this mode.

`make run ONPREM=1` inspects pinned Apertus v1.5 8B MLX weights and the served local identity, starts native MLX on literal loopback and runs the Docker app through Docker Desktop's host bridge. No hosted fallback is allowed. Local native generation uses small advice/search tasks plus shared retrieval/directness checks. Original question terms are retained. Some policy refusals are deterministic application checks, not model calls. Port collisions fail without stopping unrelated services; shutdown only stops owned services. Setup/build require network. No air-gap or other-hardware claim.

The deployed online path uses provider-reported `swiss-ai/apertus-v1.5-8b` via Public AI and Cloudflare. Neutral query planning receives no expected answer IDs. Deterministic lexical retrieval and a separate original-question directness check select immutable reviewed facts. Same-model relevance is fallible and is not independent factual verification. The hosted and local generation protocols differ; parity is not established. The optional Infomaniak adapter exists but has not been deployment-verified.

Hosted quotas persist across deployments: 200 lifetime reservations, 80/day, six per five minutes per network, one active request. The service is finite-credit, temporary and not exclusively Swiss hosting. Questions/IPs are not persisted by application code; provider/platform processing remains outside application control. Execution-contract and case guards reject mismatched inference during deployment propagation.

## Browser privacy

Visit-only tracking is default. Optional saved choices/notes use PBKDF2-SHA256 with 600,000 iterations and a random salt, plus AES-GCM-256 with fresh nonces. Only authenticated ciphertext and parameters persist. Keys stay in memory; reload, page hiding, idle timeout and cross-tab changes lock the view. Encrypted backups are created/restored locally. No account, cross-device sync or forgotten-passphrase recovery exists.

API responses are no-store with same-origin CSP; application handlers do not log request bodies. A compromised/unlocked device remains outside the storage-encryption guarantee. No independent security audit, user-comprehension study, broad language parity or unseen-ballot accuracy is claimed.

[Run and test](JUDGE_RUN.md) · [Evidence](evidence/README.md) · [Threat model](PRIVATE_TRACKER_THREAT_MODEL.md)
