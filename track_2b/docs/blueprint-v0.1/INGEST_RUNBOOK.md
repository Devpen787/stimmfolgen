# Ingestion Runbook — One More Referendum, Same System

This is a **design-level operations runbook**, not evidence that a working CLI exists yet. Implement it on the project template and retain run logs for each new issue.

## Required human inputs
- Canonical federal/cantonal/municipal jurisdiction and vote date.
- Exact ballot item (ordinal/title; multiple items can share a PDF).
- German/French/Italian source URLs as available, source roles and declared publisher.
- Original content cutoff date and pre-vote/retrospective context.
- Source licensing, appropriate attribution and whether raw bytes can be republished.

## Repeatable processing steps and acceptance artifacts
| Step | Planned command / API operation | Artifact | Gate |
|---|---|---|---|
| 1 | `discover --jurisdiction CH --date YYYY-MM-DD --item N` | `source_manifest.json` | verified exact issue |
| 2 | `fetch --manifest source_manifest.json` | immutable PDF/hash manifest | hashes recorded, fetch failures visible |
| 3 | `extract --document DOCUMENT_SHA` | paginated JSONL with printed/page mapping | page QA |
| 4 | `segment --case CASE_ID` | span registry + speaker role | cross-item contamination blocked |
| 5 | `analyse --model Apertus-v1.5-8B --case CASE_ID` | raw structured candidate + prompt/model traces | actual model provenance |
| 6 | `validate --case CASE_ID` | mechanical report + abstention flags | no invented citations, dates/IDs valid |
| 7 | `review --case CASE_ID` | reviewer approval/blocked items + reasons | human checks central claims and omission |
| 8 | `publish --case CASE_ID --version V` | immutable public case snapshot | reviewed semantics only labelled reviewed |
| 9 | `regression --suite heldout` | case matrix, raw traces, compared baselines | published reliability claims backed by results |
| 10 | `diff --from OLD --to NEW` | source/case changes and citizen-readable update | historical pinned brief intact |

These are **proposed CLI names**, not implemented commands. The actual first deliverable can be a `make ingest-case` wrapper around fewer scripts as long as the module boundaries and outputs remain explicit.

## New-case standard acceptance checklist
- [ ] All source bytes stored/hash recorded or external reference with licensed storage.
- [ ] One canonical proposal, no leakage from an adjacent ballot issue.
- [ ] Printed pages resolve to source text and original PDF.
- [ ] All visible claims classified as provision / attributed claim / forecast / observation / unknown.
- [ ] Every inference contains mechanism assumptions or explicitly no established mechanism.
- [ ] Two different affected groups reviewed, with honest absence of evidence where relevant.
- [ ] Pre-vote as-of boundary tested.
- [ ] Unsupported personal monetary question correctly abstains.
- [ ] At least one adverse test (conflicting source, irrelevant evidence, missing value, no model) run.
- [ ] Same UI used without case-specific display code.
- [ ] Update manifest can be refreshed without overwriting user's own notes.

## Source integrity / licensing
Raw public website access is not blanket permission to republish all its files. Store/check rights per document version. Prefer linking to official PDFs and only redistributing content allowed under verified terms. The Swissvotes **dataset** is published under CC BY 4.0; that does not automatically license unrelated PDFs shown by Swissvotes or other publishers.

## Example acceptance narrative
"New canton source not supported" is an honest adapter failure. "The German source supplies no international implications" is an honest epistemic gap. Neither should result in a green 'completed' card pretending the content was fully analysed.