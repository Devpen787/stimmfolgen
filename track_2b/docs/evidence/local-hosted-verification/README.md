# Local and hosted Apertus verification

## Recorded results

- `local/`: 20/20 known development questions on actual native Apertus v1.5 8B MLX. Sixteen questions invoke the model; four intentional advice/later-event refusals are application policy with no model call.
- `hosted/`: 45/45 known development questions on real Public AI `swiss-ai/apertus-v1.5-8b`, including seven second-source candidate questions.
- `failures/`: initial 11/13 native matching run, invalid native query adapters, rejected source extraction, transport/source acquisition failures. These remain failures.
- `installation/`: clean-checkout/runtime observations, real updated native HTTP response, privacy/unknown-case rejection, production execution-contract checks, second-source reproduction and owned-service shutdown observations.
- `browser/`: representative desktop/mobile public journeys and a labelled private second-case preview. All tracked notes are synthetic.
- `trace-provenance.json`: file hashes and original record locations in the immutable submitted commit's archives. Selected record content is unchanged; home paths were already redacted before publication.

These are inspected development cases, not independent held-out accuracy or local/hosted protocol equivalence. Factual wording is source-bound and separately reviewed. The same-model relevance check is fallible. Candidate evaluation is not human publication approval.

## Installation scope

Fresh public clone at `917e77c`, new Python environment, no-cache Docker app builds; then fast-forward/rebuild at `b9e4b27`. Existing downloaded weights were APFS-copied and reauthenticated on the same M3 Pro / 18 GiB Mac. This is not another physical machine, a new remote weight download or an air-gap proof. Model: community MLX 4-bit conversion of Apertus v1.5 8B; exact pins are in the records and local inspection code. Native GPU inference runs outside Linux Docker; the app uses Docker Desktop's host bridge and loopback-only bindings, without an API key or hosted fallback.

Recorded fresh-install AHV browser answer: 7.522 seconds. Responsive private-preview journeys used actual CSS 389x844 and 1280x800, including correct AHV attribution and second-source answers, source dates, updates, related/perspective states, encrypted backup recovery and cross-vote isolation. These are agent-operated browser tests, not physical-phone, independent-user or comprehensive accessibility studies. The public second-source entry has official information only; analysis was not admitted.

Recorded deterministic checks: 108 Python tests, 29 compiled Worker tests with no skips, actual WebCrypto tests, offline Docker Gate replay/failure mutations, cold HTTP smoke and authenticated export parity. These counts are the original observations, not new inference or a claim that cleanup itself reran the model.

## Reproduce matching

With the documented local model server running and a fresh output directory:

```sh
node track_2b/tools/evaluate_onprem.mjs track_2b/docs/evidence/local-hosted-verification/onprem-two-cases.json .local/new-local-run track_2b/docs/evidence/property-tax-2026-10-15/case-candidate.json
```

For hosted evaluation, use `hosted-two-cases45.json`, a private local token file and `tools/evaluate_hosted_matching.mjs`; the optional fourth argument supplies the unpublished candidate only to the explicit evaluator. Do not paste or commit credentials. Running these evaluators creates real inference requests; ordinary CI replays recorded checks or uses labelled synthetic provider fixtures.
