# Verification evidence

This directory contains source/model verification and selected reproducible results, not a development task journal. Original submitted source: [9e1c608](https://github.com/Devpen787/stimmfolgen/tree/9e1c60845c64bbe2b810a08be67fe39d47e96904). Full original evidence is preserved in that commit and in a verified private Git bundle/file archive. No Git history was rewritten by cleanup.

## Authenticated AHV packets — unchanged

| Directory | Purpose |
| --- | --- |
| `gate0-release-2026-10-14` | Eight actual local release completions, seven bounded controls, source and span/reference hashes |
| `ahv-semantic-review-2026-10-12` | Original source/context/review packet and pre-vote availability witness |
| `ahv-human-review-2026-10-12` | Five later accepted statement decisions bound to the original packet |
| `gate0-attribution-2026-10-12` | Actual failed/fixed attribution protocols and repeat run used by the review packet |
| `gate0-spans-2026-10-12` | Earlier failed immutable-span protocols and repeat-run trace verification |
| `local-apertus-v15-2026-10-12` | Original actual local v1.5 baseline diagnostics, including failures |

These packets are byte-for-byte preserved. The original prepared review packet still says PENDING; that historical record does not override the subsequent bound acceptance decisions. The runtime release guard checks the resulting bounded Gate. No raw trial human approval or general accuracy claim is inferred.

## Current local/hosted verification

[Selected local and hosted evidence](local-hosted-verification/README.md) includes complete final 20-question native and 45-question hosted development runs, earlier local matching failures, rejected second-source extraction, fresh-install identity/dependency observations, production HTTP checks and three representative synthetic browser captures. Source-record hashes identify exactly which already-redacted original records were retained. Internal scripts, deployment account logs, duplicate captures and transient working output are archived outside the current public tree.

The 20 native questions include 16 real model-invoking questions and four application-policy refusals without model calls. Hosted results are known inspected development cases, not blind held-out accuracy. Native/hosted protocol equivalence and broad language/ballot generalisation are not established.

[Second-source candidate](property-tax-2026-10-15/README.md): actual 2025 homeownership booklet, four source-bound statements and engineering tests. It remains unpublished pending human wording review. Editorial cutoff is not an exact-byte pre-vote archive witness.

Run the source and release verifiers described in [JUDGE_RUN](../JUDGE_RUN.md). Unit/provider fixtures are explicitly synthetic; authenticating recorded inference never performs new model inference. Browser captures show synthetic records, not personal political choices. Third-party rights remain described in [notices](../../../THIRD_PARTY_NOTICES.md).

[Cleanup verification and preservation](cleanup-verification.md) records what was checked after curation.
