# 03 — Private User State, Security, Updates and Continuity

## Data classification
| Class | Examples | Default residence | Server needs it? |
|---|---|---|---|
| PUBLIC_SOURCE | official PDFs, laws, campaign arguments when permitted, source snapshots, results | shared content cache/server | yes |
| PUBLIC_ANALYSIS | reviewed claims/mechanisms/effects, provenance and quality flags | shared case version | yes |
| USER_PUBLIC_INTERACTION | view case, choose neutral publicly named scenario | browser memory only | only case/scenario ID if required; minimise logs |
| USER_PRIVATE | local notes, optional self-reported previous vote, saved questions, personal choice of contexts | encrypted local vault | **no by default** |
| USER_SENSITIVE_FREE_TEXT | freeform circumstances/financial/political reflections | memory / encrypted local only | **never in ordinary public-analysis requests** |
| SYSTEM_TELEMETRY | errors, model calls, counts | aggregate/de-identified; no questions/identifiers | limited opt-in or no analytics |

## Architecture options and launch choice
**MVP = local-first, no account**, because a login makes private saving harder, increases political-data risk and damages first-run UX. Public case bundles are read over HTTPS from a Swiss/local service; browser stores user's optional notes and saved briefs encrypted. Basic session works without saving anything. Storage is per browser/device unless the user exports.

Proposed implementation: IndexedDB holds AEAD-encrypted records (AES-GCM per-record nonces, authenticated metadata), envelope schema version, random salt, KDF metadata and revision. Derive master key with audited Argon2id implementation using a user-set passphrase; keep key only in process memory when unlocked. HTTPS, CSP, dependency integrity and origin isolation are mandatory. Encryption at rest protects against casual disk access, **not a compromised page, browser extension, malware or unlocked session**. Neither source-case ID nor scenario IDs should become user-specific analytics profile.

**Cross-device sync** is post-hackathon, not pretend completed: optional E2EE ciphertext upload; encryption keys exclusively client-side; explicit opt-in, conflict strategy, recovery-key flow and deletion semantics. On a fresh device without key, no recovery from the service. Check authentication, metadata leakage and Swiss hosting before shipping. Do not claim Swiss hosting makes processing private by itself.

## Inference privacy boundary
- Proposed Apertus service receives **only public document snippets + question about a generic selected scenario** by default, no stored user profile or notes.
- Personal applicability ideally computed locally by deterministic predicates over selected scenario tokens and published, reviewed effects. Freeform private text must not automatically be passed to model or included in public prompts.
- A user may ask a question containing identifying or sensitive content. MVP should clearly label online model inference and warn before transmission; alternatively support template questions that avoid sending such text. An air-gapped/local model avoids remote transmission but must actually be tested and deployed to claim it.
- Do not persist prompts/responses on the server unless explicitly required for the opt-in evaluation corpus, with synthetic questions only. Strip request bodies from reverse-proxy/APM logs, disable third-party trackers, configure short-lived rate-limiting identifiers.
- Backend may observe which public cases a device requests; no user account or stored reading history, but IP/network correlation remains possible. Avoid blanket "100% anonymous" claims.

## What may be saved
- `vault_preferences`: UI language/text size and optionally reminder settings (language itself usually non-sensitive).
- `saved_cases`: case ID + **specific case version** and locally stored question/annotation IDs.
- `context_cards`: opt-in scenario values from a fixed factual schema; discard by default at end of session; user can choose to save them.
- `user_notes`: questions and personally written reflections, with timestamps, never rewritten by model.
- `optional_vote_memory`: manual prior choice ONLY if expressly enabled; defaults off; no side inferred from reading. No automatic election-ballot integration.
- `briefs`: dated source-linked snapshots; updating the source adds a notice, not new private content or overwritten personal opinions.

## Lifecycle and retention
```
not_saved → (user taps Save) → vault_encrypted → unlocked_locally → edited → re-encrypted
                                   ↘ export encrypted file ↗
                                   ↘ delete selected item / delete all local vault
```
- No registration needed to consume public information. Explain difference between browsing a public case and saving private reflections.
- `Delete all` removes app-owned IndexedDB/local keys and synced ciphertext if the user enabled sync; cannot guarantee removal from browser backups, external exports or OS snapshots. Document limitations.
- Export imports verify authenticated data and schema version; wrong passphrase fails closed. Exports containing optional vote memory must remain encrypted unless user explicitly requests a plaintext export with warning.
- Vault corruption recovers via previously exported encrypted backup, not plaintext fallbacks.

## Case and source updates: append-only time travel
A case version is an **immutable snapshot** referencing hashed source versions. Each new source or corrected analysis creates a new version with `change_type`:
- `SOURCE_NEW_VERSION` (booklet corrected/republished)
- `ANALYSIS_CORRECTION` (wrong attribution/incorrect mechanism fixed)
- `RESULT_PUBLISHED` (ballot result available)
- `IMPLEMENTATION_UPDATE` (later legislation or rollout documented)
- `EXTERNAL_STUDY_ADDED` (new evidence; with limitations)

Client startup checks a lightweight public manifest when online. If saved version differs, show: "New information since you last looked" with **what changed**, date and sources. Do not inject post-vote facts into a pre-vote exercise. `as_of` and `mode=PRE_VOTE|RETROSPECTIVE` control valid evidence. Saved notes stay pinned to their original source version; reopening can compare old vs new. Silent reanalysis is forbidden.

## Threat model & minimum controls
| Threat | Consequence | Mitigation / claim limit |
|---|---|---|
| Personal vote history leaks | political privacy harm | no server vote memory; encrypted opt-in local vault; no analytics |
| Prompt injection in uploaded/source PDF | model follows campaign commands | treat PDFs as untrusted data; bounded prompts; parser isolation; reject source-instruction obedience |
| Model creates fabricated source reference | false authority | server generates source IDs; validates span/hash/page; model only chooses existing IDs |
| Authentic quotation used to assert unsupported effect | misleading inference | semantic/human review + epistemic classes; citation alone insufficient |
| Later evidence contaminates historical ballot | hindsight bias | immutable case versions + `available_at/as_of` filters |
| Source silently changes | loss of provenance | SHA256 snapshots, diff, editorial audit and invalidation |
| Cross-language explanation drifts | misinterpreted rights | lang-specific evidence, reviewed translations, fall back to source language |
| Browser compromise / weak password | vault exposure | CSP, lock screen, passphrase strength, no absolute guarantee |
| Outage or no Apertus access | misleading demo | honest unavailable mode, previously reviewed published cases only |

## Privacy-by-design acceptance criteria
1. Fresh visitor can complete understand/explore/source inspection with **no login and no persistent storage**.
2. Turning off/save-disabled private mode leaves no saved questions or profile.
3. Network inspection confirms no private note/vote memory reaches public API under the default path.
4. Missing model service preserves the audited case and does not hallucinate fresh answers.
5. Vault is encrypted, locked after page reload until passphrase entered, and clear/delete/export flows tested.
6. When source is changed, a user's original note and brief remain intact; update is separately visible.
7. No vote choice recommendation is generated from contextual information.

**Status**: these are requirements. Not yet implemented, security-audited, or independently verified.