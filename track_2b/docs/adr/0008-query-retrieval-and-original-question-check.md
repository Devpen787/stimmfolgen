# ADR 0008 — Interpret the public question before source retrieval

Date: 2026-10-15. Scope: hosted AHV question matching on PR #4.

## Problem

Apertus sometimes missed the reviewed attribution statement when the user asked whose argument taxes/spending cuts were. Selecting opaque statement IDs twice compounded relevance failures. More verbose source-index prompts regressed routing; lexical retrieval alone also matched unsupported retirement-age and climate questions through shared generic words.

## Decision

Hosted Apertus produces a schema-constrained neutral English retrieval query, scope, intent and requested result count. This call has no statement IDs or expected answers. BM25F ranks authenticated reviewed titles/statements. A separate Apertus call checks each candidate against the original question and its untrusted translated focus; only a strict boolean can pass. No lexical overlap produces no candidate. A model-only fallback scan was tested and rejected after it matched a benefit statement to a worker-charge question. A refusal’s unused retrieval metadata is discarded without changing its scope decision. Other invalid/truncated responses fail closed.

The application copies accepted statement wording, epistemic type, speaker, dates and immutable spans unchanged. Model judgments can reject candidates but cannot create factual text, add source IDs or change their actors. Retrieval scores are neither truth nor confidence scores. A small fictional library example teaches comparison cardinality without prescribing any AHV answer. No question-to-answer map or special attribution ID exists in runtime code. Tests rename every ID, reverse card order and use an unrelated fictional ledger.

The semantic relevance check uses the same model and is fallible; it is not independent truth verification. Source/wording integrity is checked deterministically against the human-reviewed ledger. Runtime matches do not inherit human approval. The original bounded Gate 0 certificate is unchanged. The optional local 4-bit path retains its existing experimental disclosure; unsuccessful native reasoning-template experiments were preserved rather than shipped.

## Evidence and limits

See [matching continuation evidence](../evidence/matching-continuation-2026-10-15/REVIEW.md), including rejected prompts, unsupported-topic false matches and interrupted experiments. No model weights or vendor tokenizer files changed. No paid service was activated. Existing aggregate quotas and server-side secret remain in place. This change does not broaden the five-statement historical AHV corpus, certify arbitrary questions, or establish physical-device/human-user usability. Video files are outside this change.
