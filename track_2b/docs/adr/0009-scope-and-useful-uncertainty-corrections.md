# ADR 0009 — Recover useful corrections without generating factual answers

Date: 2026-10-15. Scope: hosted AHV matching on PR #4; supersedes hosted routing details in ADR 0008.

## Problem and investigation

Four development questions returned no useful answer: two explicitly concerned other proposals, while two demanded certainty or a quotation about personal payments. A separate defect was found in the v9 directness prompt: it contained an accidentally extracted tail of evaluation JavaScript. The exact contaminated contract and every retained failed experiment are preserved. The v10 contract uses explicit JSON strings; runtime/tests reject evaluator-code markers and oversized system prompts before inference.

Source-conditioned query planning, money-role taxonomies and model proposal-identity classifiers were tested and rejected after attribution, multilingual or unrelated-topic regressions. These experiments were never deployed. A probe of the larger v1.5 70B endpoint returned HTTP 429; the production model and price bounds remain unchanged.

## Decision

One shared matching module drives production and the real-provider evaluator. Apertus makes a neutral English source query without seeing the ledger, gold IDs or expected answers. A small application-owned name guard detects an explicitly named different proposal by comparing a noun modifier with the selected proposal title; implicit questions retain the selected proposal. This is conservative name routing, not general proposal understanding. Unsupported names or alternative synonyms can still be misrouted, especially outside the tested language forms. Another Apertus call distinguishes actual later observations from historical forecasts. Voting advice remains a refusal.

Deterministic BM25F then requires topical lexical support. Generic question verbs and bare annual/year units are stopwords so they cannot swamp the actual requested variable or horizon. Generic query-only pay/contribute-to-charge and receive-to-recipient expansions bridge vocabulary; they contain no AHV IDs, CHF values or expected outcomes. Independent fictional fee tests prove a known definite charge can be retrieved, rather than mapping every payment question to uncertainty.

A separate strict boolean Apertus call checks each candidate against the original question. A candidate can correct a false premise or identify the actual speaker without fulfilling a request for fabricated wording. This uses the same model and is not independent factual verification. Accepted factual statements, actors, epistemic kinds and immutable source spans are copied unchanged from the human-reviewed ledger. No zero-overlap fallback or generated factual prose is admitted.

Explicit other-proposal and later-event cases get a useful application-composed boundary explanation. Unknown personal cost remains unknown, never zero. Runtime matches do not inherit human approval. The original bounded Gate certificate and experimental native v8 matcher remain unchanged.

## Proof and limits

The final real Public AI Apertus v1.5 8B run passed 38/38 known development questions, including all four prior failures and the original 13 AHV questions. This is not a blind accuracy estimate, a new source-extraction run, second-case validation or local MLX parity. Full requests, responses, failures and deployment/browser observations are retained in the [evidence packet](../evidence/matching-v10-2026-10-15/REVIEW.md).

No quota namespace was replaced or reset. During Worker/Durable Object propagation, mismatched execution hashes withhold publication. Diagnostics expose expected/observed public contract hashes and honestly retain whether the old instance performed inference. No secret, question or note is added to production logs. Existing credit caps, server-side token, private-field rejection and global-hosting disclosure remain. Video and submission assets are outside this change.
