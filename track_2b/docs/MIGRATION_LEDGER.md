# Documentation migration ledger — 2026-10-12

**Source:** `Devpen787/ethglobal-build-os` branch `archive/stimmfolgen-blueprint-v0.1`, itself originating in the conversation attachment `StimmFolgen_Product_Blueprint_v0.1.zip` (dated 12 Oct 2026).

## Imported

- Nine authored Markdown documents: README; 01–05; BUILD_HANDOFF; INGEST_RUNBOOK; and CONTEXT_AND_DECISIONS.
- SOURCE_REGISTRY.csv
- UX_CONCEPT.html (interactive demonstration **only**, not an implementation)
- JSON Schemas: `schemas/public_case.schema.json`, `schemas/private_vault.schema.json` (same intended object model; reserialised as formatted JSON on import)
- Synthetic fixture: `fixtures/synthetic_case.json` (fictional; reserialised on import)
- Design schema validator: `tools/validate_design.py`
- Codex AGENTS.md, initial status file and this technical report draft.

## Not yet imported

- Original `UX_PREVIEW_desktop.png` and `UX_PREVIEW_mobile.png` (binary images from the source ZIP; screenshots can be regenerated from the HTML prototype).
- Original ZIP `MANIFEST.json` containing byte hashes for the original ZIP. Because schemas/fixture were reserialised, the original archive hashes should not be treated as hashes of this branch's files. Preserve the ZIP separately until binary assets are recovered.

## Trust note

Only structural contracts are tested by the schema validator. Live Apertus inference, document acquisition, semantics, security, privacy encryption, source page offsets and `make run` are **not** verified. A passing CI design validation is not a functioning product.
