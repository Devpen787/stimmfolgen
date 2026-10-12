# StimmFolgen — Context, Decisions and Non-Claims (12 October 2026)

**Status:** User-approved project direction and design blueprint; still a concept, not a verified working application. This is a handoff artifact summarising decisions made in conversation. It must not be cited as independent empirical evidence.

## User observation and problem

A Swiss voter receives large referendum booklets, takes voting seriously, reads summaries and detailed arguments, remembers some past votes, and occasionally encounters related issues in later referendums. This requires considerable time and mental synthesis, even when concise official information exists.

The essential job is **not** "summarise my booklet" or "tell me how to vote." It is **help me understand what could change, how it could affect my situation, people around me, Switzerland and others interacting with Switzerland, why opposing sides predict different consequences, what assumptions their arguments require, and where uncertainty remains**. People may reasonably value personal, community and societal effects differently. No model should decide or optimize that trade-off for them.

## Product thesis

Working name: **StimmFolgen**, pending trademark/name availability review.

Promise: **Understand what a vote could change, who it could affect, why, and what remains uncertain—without receiving a voting recommendation.**

Public source-grounded reasoning + a private local deliberation space. Public evidence and personal understanding must remain explicitly separated.

## Features deliberately NOT in v0.1

- AI recommendation on voting yes or no, propensity scoring or persuasion.
- Claims that the system can *prove* complex future policy effects or exact personal impact when assumptions/financing are unresolved.
- Whole-Switzerland municipal coverage or a claim that Swissvotes contains cantonal/municipal voting histories.
- Private cross-device accounts/sync, production encryption or silent training on personal reflections.
- A massive chat-first homepage or feature dashboard.
- Automatic acceptance of an LLM's source reference as proof that its explanation is correct.

## Selected cases / purposes

1. **13th AHV (March 2024):** directly defined benefit vs historically unresolved funding; must preserve pre-vote knowledge boundary when retrospectively analysing the 2024 booklet.
2. **Homeownership tax reform (September 2025):** circumstances matter (renter/owner/second home, implementation, mortgage deductions); no unjustified personal CHF predictions.
3. **National highways expansion (November 2024):** competing congestion, environmental and local/community effects; separate projections from observed outcomes.
4. **Federal e-ID (2021 rejected and 2025 accepted):** show how a related issue returns with changed design; compare laws and documented changes rather than asserting proposals are identical.

Prioritise the first two deeply. Cases 3–4 are coverage targets if supported. One truly unprepared fifth case is the extensibility/holdout check, **not** a promise of completion.

## Engineering approach drawn from ETHGlobal finalist studies

A strong demo has: real user problem → one hard/falsifiable promise → an enforceable boundary independent of model prose → successful and intentional uncertain/refusal paths → reproducible evidence → complete user consequence.

Proposed hard invariant: **No predicted or disputed consequence may be published as an established fact. If a personal effect is not computable from actual provisions and known inputs, the user sees the missing facts and uncertainty, not a fabricated number.**

Apertus supplies candidate extraction and interpretation; the verifier controls provenance, type/status, temporal integrity and publication. Human review is necessary for selected samples and ambiguous claims. Source citations alone do not prove causal claims.

## Scope and quality gates

- Prove real Apertus v1.5 inference **before** ambitious product UI work. Local inference is now observed, but its failed AHV quality gate remains a blocker; see the current evidence report.
- Preserve exact model IDs/configuration, prompts, document version/hashes, outputs and human ground truth.
- Compare against direct-booklet and extractive baselines; report failures, unanswered cases and omissions.
- Enforce a single schema through public evidence → published explanations → private brief and render no raw unreviewed answer as established.
- Add a second distinct referendum with the same pipeline; test an unseen import and cold-start Docker `make run`.
- Expose no invented vote dates, result claims or unsupported calculations.
- Use the official Hack Apertus **Track 2B** repository template. Final public repo/submission should remain separate from this temporary Build OS archive.

## Intended five design pillars

1. Architecture and stable sources/adapters (government booklets, Federal Chancellery/VoteInfo, Swissvotes, official results and Fedlex).
2. End-to-end user journeys plus failures and 'what changed?' return visits.
3. Local-first private voter understanding, explicitly versioned public-source updates.
4. Full circuit-board product schema from immutable passages to exposed UI fields and saved briefs.
5. Surface Clarity: front page starts with **What changes? Who is affected? What remains uncertain?**; progressively disclose deeper evidence.

## Evidence and delivery status

The October 12 v0.1 architecture ZIP contained documentation, JSON schemas, a synthetic fixture, a validation script, a clickable HTML concept and two screenshots. This GitHub staging branch includes text documentation and the HTML UX concept. The schema JSON, fixture, script, manifest and screenshots still need verbatim migration from the original ZIP before they can be claimed to be on GitHub.

This material represents **designed**, not **implemented** or **validated**, work. The subsequent [actual local Apertus v1.5 run](evidence/GATE0_APERTUS_V15_2026-10-12.md) records a FAIL result and genuine traces. It does not establish policy-reasoning accuracy or a secure personal-data vault.

## Current Gate 0 continuation

The [immutable span diagnostic](evidence/GATE0_SPANS_2026-10-12.md) replaces generated quotations with authenticated source IDs, adds a separate bounded semantic reference, and records two unchanged real local v1.5 runs. Six of seven live checks pass; actor attribution fails both times. The reference is coding-agent-authored, not human reviewed. Types/retrieval and refusal policy are supplied by the application. Full extraction is a recorded three-response aggregate. Gate 0 remains FAIL and frontend implementation is blocked. Cloud CI verifies sources and safeguards; cloud Apertus inference is not configured.
