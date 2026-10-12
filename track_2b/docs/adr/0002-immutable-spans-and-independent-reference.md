# ADR 0002 — immutable source spans and an independent semantic reference

Date: 2026-10-12. Status: adopted for Gate 0 diagnostics; release blocked.

Generated quotes failed faithful-source reproduction, and a matching quote did not establish the meaning of a claim. The active probe now accepts source IDs and a small typed answer. It never accepts model-written quotes, explanatory prose, URLs or timestamps. The application resolves citations from a catalog rebuilt from the pinned original PDF. Identity binds document bytes, extractor/segmenter version, page, block, offsets, exact text hash, role and editorial cutoff. This is a content-addressed reference to normalized extracted text, with raw block/bounding-box provenance; it is not a byte offset in the PDF or proof of publication availability.

A separately authored evaluation-only primary-source reference checks payment direction, cost amount and horizon, actor, epistemic kind and refusal outcomes. It is never sent to Apertus. This reference is coding-agent-authored and not human reviewed; it is independent of extraction logic and model output, not an independent human adjudication or general natural-language entailment system.

Initial nested protocols failed. The final, narrower protocol uses task-specific lexical retrieval and flat fields. An explicit adapter preserves all model values and IDs, rejects extra fields and never repairs a wrong answer. Kind comes from the typed task; positive actor comes from cited source metadata; null personal cost and refusal reason codes come from application policy. These fields are not independently generated classification/refusal explanations. Budget attribution explicitly asks the model for the actor. The full extraction result combines three recorded completions and requires each component to qualify; it is not a single full-extraction completion. No generalisation, holdout or classification accuracy is claimed.

Two unchanged final local v1.5 runs pass six of seven live checks and reproduce the actor-attribution failure. The semantic checker withholds the otherwise mechanically valid committee selection. Preserve every attempted protocol, raw prompt/request/response, at-run reference and verdict, and separate final revalidation. Historical generated-quote probes remain baseline diagnostics; they are not the active path.

Cloud CI verifies source authenticity, reference resolution, evidence integrity and synthetic adversarial safeguards. It does not host Apertus. The optional manual inference workflow requires an explicitly provisioned self-hosted Mac and pinned loopback server; it has no paid endpoint fallback. No such runner was provisioned or dispatched here. Gate 0 remains FAIL, with human semantic review and public availability verification also outstanding. Frontend work remains blocked.

Evidence: [observed span report](../evidence/GATE0_SPANS_2026-10-12.md).
