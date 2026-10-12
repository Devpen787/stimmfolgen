# Technical report — StimmFolgen (DRAFT; NOT SUBMITTED)

- **Track:** Hack Apertus Online, Track 2B — Own Project
- **Event:** October 2026
- **Team:** To be confirmed by the entrant
- **Demo:** Not recorded
- **Status:** Design baseline only. No live Apertus results or completed evaluation.

## 1. Summary

StimmFolgen is a proposed Swiss referendum understanding tool. It helps users explore the likely and uncertain consequences of a proposal for defined factual situations, other groups, Switzerland and cross-border stakeholders; every displayed statement should show whether it is a provision, an attributed prediction, an evidence-backed estimate, an observation, or an unresolved claim. The product does **not** recommend voting choices.

## 2. Architecture

**Proposed:** Official booklet + versioned source adapters → immutable passages → Apertus-generated candidate structured claims/impacts → schema, attribution, temporal and source-reference gates → human-reviewed explanations → citizen-facing four-scope explainer → separate local private notes vault.

The architecture/design files in [docs/blueprint-v0.1/](docs/blueprint-v0.1/) are **plans only**, not implemented services.

### Target architecture (mandatory)

**Proposed target:** on-premise or sovereign Swiss cloud with a local-first user vault. Neither deployment has been proven. External source collection may use internet during ingestion; model serving/dependency paths and runtime restrictions must be disclosed and tested before the project claims compliance. Hosted inference is acceptable only if it satisfies the declared architecture requirements.

## 3. Use of Apertus

- **Intended model:** `swiss-ai/Apertus-v1.5-8B` (unverified access).
- **Intended role:** source-grounded extraction of provisions, attributed claims, causal assumptions and impact categories; candidate generation, NOT independent authority.
- **Environment/endpoint:** not configured or tested.
- **Prompts, latency, model outputs:** none yet; do not invent.

## 4. Data

Planned primary sources: Swiss Federal Chancellery archived voting booklets, official vote information, Swissvotes historical metadata and Fedlex legislation. Verify availability, provenance, temporal cutoffs and redistribution licences before adding corpus files. A synthetic library-vote fixture used for schema validation is **fictional** and not an Apertus output. No personal voting information may enter repository datasets.

## 5. Evaluation

**Not run.** Planned questions include correct direct effect, unresolved funding, source provenance, actor attribution, period leakage, scope sensitivity, absent information and deliberate abstention. Baselines: official booklet short summary, extractive source passage and plain direct Apertus prompt. Report per-case accuracy, unsupported assertions, abstention, missing-source rates and human review agreement. Never substitute a JSON-schema pass for semantic evaluation.

| Setup | Metric | Result |
| --- | --- | --- |
| Official source baseline | TBD | NOT RUN |
| Plain Apertus source-prompt | TBD | NOT RUN |
| StimmFolgen pipeline | TBD | NOT RUN |

## 6. Limitations and safety

- Causal and economic predictions are not guaranteed or provable from booklet text alone.
- Official booklets have attributed government and committee positions; they are not pure apolitical reference material.
- Balanced pro/con presentation does not guarantee neutral coverage or equal evidentiary standing.
- Private context must be voluntary, minimal and purpose-limited; the planned local encryption implementation is **not complete**.
- No individual voting recommendations, political persuasion or voter propensity inference.

## 7. Reproducibility and delivery

- **Current `make run`:** template placeholder fails; unresolved.
- **Apertus inference:** unresolved.
- **Data lineage and tests:** authored design and synthetic contract checks only.
- **Video/PDF:** not produced.

This report is intentionally a transparent starting point for Codex to update *with verifiable real evidence*. Generate the final PDF after the implementation has been tested.
