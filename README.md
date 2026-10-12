# StimmFolgen — Swiss voting-impact explorer

A Track 2B project for [Hack Apertus 2026](https://hackapertus.ch/): **understand what a vote could change, who it could affect, why, and what remains uncertain—without receiving a voting recommendation.**

**Current status (12 October 2026):** design baseline imported. This repository does **not** yet contain working Apertus inference, evaluated causal claims, a deployed application, or verified encrypted user storage. All demonstration content should be marked as synthetic or sourced and reviewed.

## Read first

- [Track 2B official instructions](track_2b/README.md) — preserved from the official template.
- [Architectural baseline](track_2b/docs/blueprint-v0.1/01_SYSTEM_AND_SOURCES.md)
- [Full product schema — circuit board](track_2b/docs/blueprint-v0.1/04_PRODUCT_SCHEMA.md)
- [User journeys and UX](track_2b/docs/blueprint-v0.1/02_JOURNEYS_AND_UX.md)
- [Privacy & updates](track_2b/docs/blueprint-v0.1/03_PRIVACY_AND_UPDATES.md)
- [Codex build handoff](track_2b/docs/blueprint-v0.1/BUILD_HANDOFF.md)
- [Context, user observation and decisions](track_2b/docs/CONTEXT_AND_DECISIONS.md)
- [Illustrative clickable UX concept](track_2b/docs/blueprint-v0.1/UX_CONCEPT.html) (non-functional mockup)
- [Status and blockers](track_2b/docs/PROJECT_STATUS.md)

## Mandatory next step

Get one **real Apertus 1.5 inference** over a verified official referendum passage and retain the exact prompt, response, model/version, source/page and human checked expectations. The official template's `make run` currently exits with a placeholder error; it must be implemented and cold-run before submission.

## Safety and trust boundary

The model may generate candidate explanations, not factual authority. Attribution, verifiable exact passages, valid as-of dates, evidence types and human-review flags are structured and auditable. Do not claim a policy has a predictable personal impact from a source that leaves that impact undetermined. Do not recommend voting choices, infer voter preferences, or publish personal deliberations.

## Submission

Keep `track_2b/` intact. Docker `make run`, source-licensed documentation, technical report PDF (up to six pages), maximum 2-minute demo video and public repository are required. The technical report template is still a placeholder, not a submitted result.
