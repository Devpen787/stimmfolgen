# 0007 — Live source matching with immutable reviewed wording

15 October 2026. Product continuation on PR #4; supersedes the live prose/audit publication design, not the original Gate evidence or human approvals.

## Problem and evidence

The same Apertus model wrote an explanation and judged it. Real trials rejected useful uncertainty explanations because the judge tested the user's demand for certainty rather than the response. Actor corrections were also lost. Changing the audit instructions reduced false rejections, but authored negative controls then exposed approvals of a wrong speaker and denial of a known source. A second call to the same model is not an independent factual authority. All attempts, including rejected fixes, remain in the [product evidence](../evidence/product-reliability-2026-10-15/REVIEW.md).

## Decision

Live Apertus interprets the public question and selects IDs from the authenticated, human-reviewed AHV ledger. A separate call filters the selected IDs for relevance. The server alone resolves those IDs to the exact accepted statement, epistemic kind, speaker, original source span and dates. Model output has no factual-text field. Unknown IDs, generated text, duplicate references, malformed completions, model mismatch and truncation fail closed.

The factual checks are independent of runtime model agreement: source-byte authentication, bound statement approvals, immutable composition, and deterministic comparison against separately authored evaluation references. The second relevance call uses the same model and remains fallible. It cannot confer human approval on the question match. The model may miss a statement or select extra/unrelated reviewed context; these are measured separately from factual integrity.

Voting-advice and no-match messages are application policy/scope messages, explicitly labelled. They contain no invented factual claims. A no-match, withheld or unavailable response offers all reviewed source statements as a clearly labelled browsing alternative, not a substituted live answer. Later events link to separately dated Updates.

Local 4-bit inference uses additional fictional library examples to teach the output contract and individual-versus-aggregate distinction. These examples contain no AHV expected IDs or answers. Local matching remains experimental because its full relevance evaluation does not pass. No downloaded weights/tokenizer were changed and no new model was downloaded.

## Product and deployment consequences

The UI says “Powered by Apertus v1.5” and explains that live matching uses reviewed wording. Private choices and notes are never attached. Mobile Explore sections wrap so all five are discoverable. Static assets pass through the Worker to receive no-store/CSP headers; versioned module/style URLs replace already cached builds.

The public demo retains its finite free-credit caps, exact provider model allowlist and server-side secret. Global Cloudflare/Public AI hosting is disclosed; the owner's Mac is not a visitor host. This does not claim general accuracy, new facts from arbitrary documents, independent human usability research, a physical-phone test or permanent free hosting. Video files are unchanged.
