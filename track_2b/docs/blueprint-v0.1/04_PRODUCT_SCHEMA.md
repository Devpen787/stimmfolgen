# 04 — The Entire Product as a Schema (Smallest Pieces → Whole System)

## 0. What "schema" means here
Not merely database tables. This is the **product circuit board**: entities, relations, events, states, public vs private boundaries, UI view models, evidence rules, and test ownership. The goal is that one can inspect a small source span and trace it forward to a user-facing statement—or start at a visible statement and trace it all the way back to exact bytes in a dated official document.

## Layer map
```
L0 Raw source: Publisher → DocumentSnapshot (bytes/hash/version) → Page → PassageSpan
L1 Meaning: Jurisdiction → BallotEvent → Proposal → Provision / Claim / Forecast
L2 Reasoning: Claim → MechanismStep / EvidenceLink / Counterclaim / Uncertainty
L3 Applicability: AffectedGroup → ApplicabilityRule → ImpactStatement → Perspective
L4 Experience: CaseVersion → Answer / ImpactView → SourceDrawer → UnderstandingBrief
L5 Private: LocalVault → SavedCase / ScenarioSelection / UserNote / OptionalVoteMemory
L6 Operations: PipelineRun → ModelTrace → ReviewDecision → EvaluationCase → ReleaseGate
```

## Entity registry and source of authority
| Entity | Key fields (not exhaustive) | Authority / relationship | Public/private |
|---|---|---|---|
| `Jurisdiction` | id, level, country/canton/municipality codes, available languages | canonical registry | public |
| `BallotEvent` | id, jurisdiction_id, vote_date, status | official ballot authority | public |
| `Proposal` | id, ballot_event_id, position, official_title_i18n, description, ballot_choice_labels | one distinct legal question; never conflated with other items in same booklet | public |
| `Publisher` | id, official_name, type, website | organization identity; not guarantee of truth | public |
| `DocumentSnapshot` | id, proposal_ids[], publisher_id, doc_role, final_url, sha256, retrieved_at, published_at, editorial_cutoff, lang, licence, source_type, status | immutable version; multiple ballot issues may share physical file | public |
| `SourceSpan` | id, document_id, pdf_page_index, printed_page, start/end offsets, excerpt, excerpt_sha256, extraction_method, quality, available_at | exact support location; source of citation UI | public |
| `Actor` | id, name, role_at_date, institution, source | who wrote/argued/recommended, role is time-specific | public |
| `Provision` | id, proposal_id, legal_effect, applicability_conditions[], source_span_ids[], temporal_scope | text establishing what the proposal says, not prediction of outcome | public |
| `Claim` | id, proposal_id, actor_id, text, kind, assertion_type, source_span_ids[], as_of | explicitly attributed political/projection/factual assertion | public |
| `MechanismStep` | id, proposition, relation_kind, upstream_ids[], downstream_ids[], assumption_ids[], status | candidate causal or conditional link; *not presumed true* | public |
| `ImpactStatement` | id, proposal_id, impacted_group_ids[], mechanism_ids[], statement, horizon, epistemic_type, applicability_rule_ids[], evidence_link_ids[], uncertainty_ids[] | unit displayed in UI; must not exist without classification | public |
| `AffectedGroup` | id, neutral_label, fact_tags[], scope_self_others_nation_beyond | generic factual situation, **not a user segment for persuasion** | public |
| `ApplicabilityRule` | id, rule_type, operands, required_facts[], missing_facts_behavior | deterministic predicates for selected scenario | public |
| `EvidenceLink` | id, from_id, source_span_id, relationship (`STATES`,`SUPPORTS_PREMISE`,`DISPUTES`,`CONTEXT_ONLY`), reviewer_status | a reference does NOT prove causal validity | public |
| `Uncertainty` | id, kind, reason, missing_fact_or_assumption, mitigation/next_source | explicit gap; optionally blocks personal number | public |
| `CaseVersion` | id, proposal_id, mode, as_of, document_hashes[], analysis_version, reviewed_at, status, generated_by_model_id | immutable assembled public record for one proposal at one knowledge frame | public |
| `ModelTrace` | id, case_version_candidate_id, model_family/revision, runtime, prompt_version, decoding_config, input_hash, output_hash, status, latency, request_time | restricted operational artifact; published only after redaction | operations |
| `ReviewDecision` | id, item_id, reviewer, decision, evidence, reason, reviewed_at | acceptance/rejection, not magical truth certification | operations/public audit |
| `Answer` | id, case_version_id, input_question_id, conclusion_ids[], citations[], outcome/status | dynamic or reviewed response; no invented sources | public interaction |
| `UnderstandingBrief` | id, case_version_id, saved_statement_ids[], question_refs[], note_refs[], created_at, mode | generated on device; references immutable public case | private |
| `LocalVault` | id, cipher_version, salt/kdf, entries_enc, schema_version | local ciphertext only by default | private |
| `ScenarioSelection` | id, case_id, selected_group_ids, temporary_factual_flags, save_opt_in | local, generic factual applicability | private/ephemeral |
| `UserNote` | id, case_id, case_version, text, created_at, updated_at | user's own words, never model-edited silently | private |
| `OptionalVoteMemory` | id, proposal_id, self_recorded_choice, user_timestamp, explicit_opt_in | private, default disabled | private |
| `UpdateNotice` | id, from_case_version, to_case_version, change_type, affected_ids, rationale | public diff; privately link to saved case | mixed |
| `EvaluationCase` | id, source_frame, task, gold_reference, rubric, withheld_from_dev | benchmark provenance | operations |
| `EvaluationRun` | id, model_version, prompt_version, evaluation_case_ids[], output_paths, raw_metrics, errors | reproducibility | operations |

## Graph edges: types are important
```
BallotEvent 1 ── N Proposal
Proposal N ── N DocumentSnapshot  (via document_proposal_scope)
DocumentSnapshot 1 ── N SourceSpan
Proposal 1 ── N Provision
Proposal 1 ── N Claim
Actor 1 ── N Claim
Claim/Provision N ── N EvidenceLink ── 1 SourceSpan
Claim/Provision N ── N MechanismStep ── N ImpactStatement
ImpactStatement N ── N AffectedGroup
ImpactStatement 0..N ── N Uncertainty
Proposal 1 ── N CaseVersion
CaseVersion 1 ── N Answer
CaseVersion 1 ── N UpdateNotice
User's private SavedCase N ── 1 PUBLIC CaseVersion (reference only)
```
**Never** use source PDFs as input where one ballot event is presumed to contain one issue. Several ballot items share the same official booklet. All claims and provisions must point to exactly one `proposal_id` or explicitly mark a justified cross-proposal comparison.

## Enumerations and epistemic contract
- `claim_kind`: `OFFICIAL_PROPOSAL_TERM`, `GOVERNMENT_ARGUMENT`, `COMMITTEE_ARGUMENT`, `OTHER_ATTRIBUTED_ARGUMENT`, `OFFICIAL_PROJECTION`, `EXTERNAL_EMPIRICAL_FINDING`, `MODEL_HYPOTHESIS`.
- `epistemic_type`: `DIRECT_PROVISION`, `CONDITIONAL_APPLICABILITY`, `ATTRIBUTED_PREDICTION`, `EVIDENCE_BACKED_ESTIMATE`, `POST_VOTE_OBSERVATION`, `UNRESOLVED`, `DISPUTED`.
- `evidence_relationship`: `STATES`, `SUPPORTS_PREMISE`, `DISPUTES`, `CONTEXT_ONLY`, `CONTRADICTS`.
- `review_status`: `CANDIDATE`, `MECHANICALLY_VALID`, `HUMAN_REVIEWED`, `CONTESTED`, `WITHHELD`.
- `case_mode`: `PRE_VOTE`, `RETROSPECTIVE`.
- `answer_outcome`: `SUPPORTED`, `CONDITIONAL`, `ATTRIBUTED_ONLY`, `INSUFFICIENT_EVIDENCE`, `SOURCE_CONFLICT`, `SERVICE_UNAVAILABLE`, `USER_DATA_NOT_SHARED`.
- `scope`: `PERSONAL_SCENARIO`, `PEOPLE_AROUND`, `SWITZERLAND`, `CROSS_BORDER`.

Do NOT create a single `truth_score` number or classify political interests as positive/negative per person. A statement's provenance, epistemic class, assumptions and conflicting evidence are necessary and not compressible to '87% true'.

## Core schema and invariants
1. Every published `ImpactStatement` has `proposal_id`, `epistemic_type`, a human-readable `statement`, `horizon` and **either a valid EvidenceLink or the explicit `UNRESOLVED`/`MODEL_HYPOTHESIS` treatment**.
2. Only `DIRECT_PROVISION` can be labelled "The proposal says/changes"; an actor's prediction is never promoted to direct effect by citation alone.
3. Every quoted passage resolves to `(DocumentSnapshot.sha256, page, offsets, quoted_hash)` and has a visible actor or publisher.
4. `SourceSpan.available_at` must precede `CaseVersion.as_of` in PRE_VOTE mode; otherwise link is invalid. Missing `available_at` requires review before inclusion.
5. A provisional estimate of money/benefit requires a reviewed calculation with unit, formula, variables, verified sources and input-completeness checks. If any required variable is missing, respond conditionally or abstain.
6. A person-specific applicability predicate runs locally on neutral factual scenario values. Do not send user notes, vote memory, political affiliation or profile to shared model.
7. `POST_VOTE_OBSERVATION` may establish that an indicator changed; it cannot assert causal attribution without separately identified research and valid limitations.
8. A `HUMAN_REVIEWED` label means *reviewed according to a published rubric*, not that competing economics are settled.
9. Corrections append a version and diff; they never rewrite previous dated answers or private briefs in place.
10. No `Answer` is allowed to contain a vote recommendation, covert argument prioritisation or comparative political utility score.

## Public response contract example
`schemas/public_case.schema.json` is an executable JSON Schema *for the public case exchange format*, not the exhaustive conceptual ERD above. An MVP response may be smaller, but must still meet all trust invariants. It includes `source_spans`, `impacts` and `uncertainties` with source linkage and temporal basis. Complex semantic correctness remains a separate evaluation obligation.

## Private contract
`schemas/private_vault.schema.json` describes data **inside** encrypted payload, not stored plaintext. The on-disk object should only expose algorithm/KDF/nonces/ciphertext/tag and version—not notes or voting history. It is not legitimate to call an unencrypted JSON file private merely because it is saved in the user's browser.

## View model mapping: same truth everywhere
| UI control | Derived from schema | Must expose |
|---|---|---|
| Vote card | Proposal + BallotEvent + CaseVersion | jurisdiction/date/mode/version |
| "What changes" | Provision → EvidenceLink → SourceSpan | direct legal scope, quote |
| "Who may be affected" | ImpactStatement + AffectedGroup + ApplicabilityRule | conditions and missing facts |
| "Why?" | MechanismStep + EvidenceLink + Uncertainty | each assumption + attribution |
| "Others" | AffectedGroup + matching impacts | no value-based ranking |
| "What's uncertain" | Uncertainty + omitted-data summary | missing information without invented answer |
| Source drawer | SourceSpan + DocumentSnapshot | exact page, publisher, version, language |
| Personal brief | CaseVersion + selected facts and local UserNotes | frozen basis, no vote recommendation |
| Update banner | UpdateNotice from old to new CaseVersion | exactly what changed, no silent overwrite |

## Crosswalk: user → interaction → engine → persisted facts → verification
| Requirement | Main journey | Core objects/modules | Gate |
|---|---|---|---|
| Understand proposal simply | J01/J02 | Proposal, Provision, Span; M01–M08 | E01–E03 |
| Explain personal applicability | J03 | Impact, Group, Rule; M06/M08 | E04, E07 |
| Consider other people/Switzerland | J04/J05 | Impact, Scope; M06 | E05, E08 |
| Dissect competing claims | J06/J08 | Claim, Actor, Mechanism, Evidence; M05–M07 | E03, E06 |
| Trace every important conclusion | J09 | Snapshot, Span, Evidence; M02/M03/M07 | E02 |
| Historical/time integrity | J11/J12 | CaseVersion, UpdateNotice; M04/M07 | E09 |
| Save privately | J10/J13 | Vault, Brief, Note; M09/M10 | P01–P04 |
| Accessible low-friction UI | J00–J15 | Screens S01–S05 | UX01–UX05 |
| Reuse on new ballot | J01 + backoffice | PipelineRun, SourceAdapter, CaseVersion | E10 |

## Example trace in reverse, the 'circuit board' exercise
User sees "We cannot establish your exact additional salary contribution from this original booklet."
→ S03 impact card `impact:ahv-financing-unknown`
→ `ImpactStatement(epistemic_type=UNRESOLVED)`
→ `Uncertainty(missing_fact=financing_method_and_rate)`
→ `Proposal(2024-03-03/AHV13)`
→ referenced `SourceSpan(printed_page=11; exact PDF bytes/hash)`
→ `DocumentSnapshot` editorial cutoff/retrieval/hash
→ `CaseVersion(mode=PRE_VOTE, as_of <= vote date)`
→ E07 test asking for precise annual worker cost must abstain.
The forward trace from the actual PDF passage must land on the *same* impact card. If any edge is missing, the card is not ready to publish.

## State machines
**Source:** `DISCOVERED → FETCHED → EXTRACTED → SEGMENTED → ANALYSED → MECHANICALLY_CHECKED → HUMAN_REVIEWED → PUBLISHED`; any stage may lead to `FAILED` / `NEEDS_REVIEW`, never jump from `ANALYSED` directly to `PUBLISHED` for sensitive causal assertions.

**Case:** `NOT_AVAILABLE → DRAFT → REVIEW_REQUIRED → PUBLISHED → SUPERSEDED`; `WITHHELD` permitted at any pre-publication state. `SUPERSEDED` versions remain addressable for historical briefs.

**Private brief:** `EPHEMERAL → USER_SAVED → USER_EDITED → EXPORTED` or `USER_DELETED`, with pinned case version. Updates create notices, not mutations of note text.

**Answer:** `QUESTION_RECEIVED → SOURCE_SCOPE_FIXED → SOURCES_RETRIEVED → MODEL_CANDIDATE → VERIFIED/ABSTAINED → DISPLAYED`. On provider outage: `SERVICE_UNAVAILABLE`, not a fabricated `VERIFIED` response.
