# 01 — System Architecture & Reliable Sources

## Bounded context: what we build, and what we do NOT build
We build a **versioned, source-backed consequence explorer** for specific Swiss referendum propositions. We do not build a general-purpose political chatbot, a policy-outcome causal estimator, an electronic voting tool, a ballot choice recommender, or a voter microtargeting engine.

The *public source system* and *personal reflection tool* are independent. Source records have editorial provenance, immutable snapshots, temporal windows and correction history. User context never becomes part of shared inference or dataset training.

```
                        PUBLIC / REUSABLE                                   PRIVATE / LOCAL
  official source feeds + manually curated source list
                       |
     [M01 DISCOVER] → [M02 FETCH & SNAPSHOT] → [M03 EXTRACT/OCR]
                             |                   |
                             v                   v
                      checksum manifest     page/span index
                             \                   /
                              [M04 NORMALISE REFERENDUM]
                                          |
                      [M05 RETRIEVE/ANALYSE WITH APERTUS]
                          provisions • claims • mechanisms
                                          |
                       [M06 LINK IMPACTS & COUNTERCLAIMS]
                                          |
                       [M07 VALIDATE, REVIEW, PUBLISH]
                                          |
                        IMMUTABLE VERSIONED CASE API
                                          |
                           [M08 UX / SCENARIO EXPLORER] <── [M09 LOCAL VAULT]
                                          |
                                    [M10 PERSONAL BRIEF]
```

## Module contract register
| ID | Input | Output | Error/fallback | Essential test |
|---|---|---|---|---|
| M01 source discovery | referendum id + jurisdiction/date | source candidates w/ publisher, URL | human-entered source manifest | cannot confuse two ballot items |
| M02 fetch/snapshot | source candidate | immutable bytes + SHA256 + retrieval time + licence metadata | `FETCH_FAILED` / old snapshot retained | bytes match stored digest |
| M03 extract/OCR | document snapshot | paginated text, bounding coordinates if available, language, OCR quality | `EXTRACTION_UNVERIFIED`, require review | source passage maps to actual PDF page |
| M04 normalise | labelled spans + metadata | stable ballot issue/proposal IDs, valid date/source linkage | `NEEDS_REVIEW` | no mixing AHV and retirement-age proposals in same booklet |
| M05 Apertus | retrieved passages + validated scope + question | typed candidate provisions/claims/mechanisms/answers | timeout, no source = abstain | real-model trace, attributed speaker and source IDs |
| M06 analysis | typed items | impacted-group relations, claimed mechanisms, counterclaims, caveats | unsupported edges marked `UNSUPPORTED` | does not invent financing or causal effect |
| M07 quality | candidate output + source graph + tests | reviewed/published case version + audit trail | block publication / label experimental | referenced span exists AND meaning reviewed; no future leakage |
| M08 user experience | published case + question + neutral scenario | progressive evidence views | source missing/unavailable display | shows unknown without fake answer; no recommender |
| M09 local vault | user-entered selections/notes | encrypted local entries | no saving unless opted in; export supported | shared API never receives private data by default |
| M10 brief | currently viewed evidence + explicit user saves | locally generated, reference-locked brief | stale sources flagged at next open | brief never silently rewritten after updates |

## Canonical, repeatable ingest sequence
1. **Identify**: user picks ballot by date/jurisdiction; canonical ID contains authority, date, ballot-item ordinal, language-independent identity. An exact ballot item must be selected even if the booklet covers multiple propositions.
2. **Acquire**: fetch from registry (or explicit user upload); capture final URL, publisher, publication/editorial cutoff dates when known, retrieved_at, HTTP metadata, licence and SHA256; never treat retrieval date as content validity date.
3. **Extract**: paginated PDF text using maintained PDF library; OCR only for image-only pages; record printed page vs PDF page index, language, characters and layout anomaly flags.
4. **Segment**: passage IDs linked to source hash and exact offsets; separately tag title, statutory text, proponents' arguments, government position, opponents' arguments, budget figures, caveats. Every segment requires attributed actor when identifiable.
5. **Normalise**: establish proposal metadata and chronology. Split propositions, even when physically in same PDF. Human checks confusing splits.
6. **Analyse**: Apertus v1.5 receives bounded retrieved passages and produces typed candidate `provisions`, `claims`, `mechanisms`, `affected_groups`, `uncertainties`, each with spans and explicit epistemic class. Retrieval and model inference are separate; no model call can invent source IDs.
7. **Validate mechanically**: JSON Schema, ID existence, quote/offset alignment, actor roles, source cutoff ≤ specified historical frame, valid transitions, deterministic scenario and arithmetic checks.
8. **Review semantically**: inspect central claims, omissions and attribution; check whether a passage supports the actual *interpretation*, not merely whether the quotation exists. Mark each conclusion `DRAFT`, `REVIEWED`, `DISPUTED`, or `WITHHELD`.
9. **Publish immutable case**: version ID and diff/manifest; show last-reviewed and evidence cutoff; ongoing cases can have staged changes, not silent replacements.
10. **Update**: poll metadata when revisited/on a scheduled server job, compare hashes, create replacement document version, run dependency and regression tests, publish delta; consumer explicitly chooses pre-vote vs retrospective mode.

### Historical frame rule
`source.published_at <= analysis.as_of` AND (`passage.available_at <= analysis.as_of` OR explicit UNKNOWN) must hold for an answer claiming to reflect pre-vote knowledge. Post-vote facts are shown only in a visibly distinct retrospective view. Editorial corrections to prior statements retain earlier source snapshot and show what changed.

### Official source adapters and their obligations
**Federal first**: FedChancery archive = canonical source of printed explanatory booklets (PDF; HTML index is not a guaranteed public API); official subject dossiers and Fedlex = additional law/explanation; Swissvotes = federal-history metadata (CC BY 4.0 dataset with attribution and version), FSO open results = outcome data. VoteInfo website/app can act as a *discovery/reference surface*; do not invent a public API for every detail without endpoint tests. Canton/municipal adapters are future modules with distinct jurisdiction, language, document form and rights.

**Trust hierarchy is contextual, not partisan**: official text establishes *what was formally proposed/decided*; attributed arguments establish *what someone claimed*; official projections are still projections; external research may support/contest empirical premises; observations are not automatically causal effects. Verified text extraction does not equal verified factual conclusion.

### Why use Apertus (not deterministic code alone)?
Needed for semantic tasks where straightforward parsers fail: claim/provision boundary, attribution, multilingual paraphrases, reasoning about conditional applicability, identifying unspoken assumptions and relationship candidates. Keep fetching, digesting, date checks, extraction coordinates, numerical calculation, source authorisation, encryption and audit logging deterministic. A simple search-and-quote baseline plus direct Apertus prompt should be compared on the same cases; if the structured pipeline adds no meaningful value, don't claim it does.

### Fail-closed contract
- No traceable supporting passage → `INSUFFICIENT_EVIDENCE` response, not confident explanation.
- Passage backs a politician's statement but not empirical truth → display `ATTRIBUTED_CLAIM`, never fact.
- Model proposes causal link without supporting evidence → labelled *hypothesis to investigate*, not outcome.
- Mixed or outdated source versions → refuse to join until version alignment/review.
- Hosted model unavailable → show pre-reviewed public case content with an explicit 'Ask unavailable' state; do not simulate a live Apertus answer.
- Unverified document parsing → user sees source and a warning, not fabricated full coverage.

### Evolution to production
Dedicated source adapters; human review queue; passage-level version diff; stats with evidence limits; multilingual alignment; local model availability; accessibility audit; legal assessment; verified cantonal/communal sources. These are roadmap items, not already built capabilities.
