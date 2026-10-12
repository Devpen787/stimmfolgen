# Gate 0 attribution continuation — real local Apertus v1.5

**Bounded AHV pipeline suite PASS in two unchanged runs. Gate 0 remains HUMAN_REVIEW_REQUIRED; frontend blocked.** Source publication availability is also unverified. This is a development-case pipeline result, not general model accuracy or a released product.

## Fix and genuine results

The [previous v3 runs](GATE0_SPANS_2026-10-12.md) attributed the government budget forecast to the committee. The first attempted fix (v4) separated neutral source discovery but still asked the model to compose the final answer. Apertus correctly selected the government spans, then changed the answer's actor to the committee. It also returned cost `4100` after unrelated prompt reordering. Those raw failures remain in `run-attribution-v4`; none was repaired to the expected answer.

The final v5 protocol makes two actual calls for attribution. One finds supporting forecast spans and their actor from both source sections, without seeing the user's requested attribution. Another parses the requested speaker from the question, without seeing source evidence. The application compares the extracted actors and preserves the source actor/IDs unchanged: equal actors mean supported attribution; different actors mean source conflict. Unknown, malformed or inconsistent outputs are withheld. No expected actor, outcome, citation ID or semantic reference is given to either model prompt or the comparator. The six other trial prompts are byte-identical to the recorded v3 prompts, restoring their already measured contract rather than repairing their outputs.

Both final runs genuinely returned:

```json
{"span_ids":["sp-8fa7ba3419d9690f45e2","sp-eac0d0ebb7b34dc40b9b","sp-92f4ef4f294b8ca65441"],"actor":"GOVERNMENT"}
```

Their independent question-parsing call returned `{"claimed_actor":"COMMITTEE"}`. The application therefore produced `SOURCE_CONFLICT`, retaining the government actor and all selected IDs. The unchanged evaluation-only semantic reference independently resolved the forecast to page 16: “Der Bund müsste seine Steuern erhöhen oder Ausgaben kürzen.” This reference is coding-agent-authored and still not human reviewed. Neither reference contents nor expected values enter generation or actor comparison.

| Bounded trial | Final run | Unchanged repeat |
| --- | --- | --- |
| Current 12 / proposed 13 annual payments | PASS | PASS |
| Introduction cost CHF 4.1 billion, projection | PASS | PASS |
| Unknown definite employee financing burden | PASS | PASS |
| Fabricated CHF 100 quotation | PASS | PASS |
| Committee attribution of government forecast | PASS | PASS |
| Salary-based definite CHF demand | PASS | PASS |
| Later financing imported into the pre-vote frame | PASS | PASS |
| Three-response combined happy path | PASS | PASS |

Each final suite makes eight actual model calls: six ordinary trial completions plus neutral attribution and intent parsing. The attribution result is explicitly `POLICY_COMPARISON_OF_TWO_ACTUAL_MODEL_COMPLETIONS`, not an LLM-generated refusal or single completion. The full extraction remains a three-completion aggregate. These distinctions remain visible in the trace artifacts. Actor comparison is symmetric: synthetic tests exercise government/committee as both source and requested actor, including supported and conflicting combinations. A mechanically valid actor comparison with an unrelated passage still fails the independent meaning check.

## Identity, source and limits

The same local M3 Pro Mac, 18 GiB, macOS 26.6.2 arm64 served `tokimoa/apertus-v1.5-8b-mlx-4bit`, revision `f08ed532a657bef7d322bd0cbca43dac13a9d0a3`, weights SHA-256 `d0478edeb06bf18e5f4f7b50db77d89b839730b2d16cb1020015e6099e42074b`. Declared upstream: `swiss-ai/Apertus-v1.5-8B`, revision `a411d838600baf0e3635a3daf66fb7c55fc97bb6`; independent BF16 equivalence remains untested. Runtime: MLX 0.32.0, mlx-lm 0.31.3, transformers 5.15.0. Loopback port 8766, temperature 0, max 500 completion tokens per call, thinking disabled, single decode/prompt concurrency. The complete pinned artifacts and serving path are rechecked before calls; Hub access is disabled during inference. No paid API was used.

The exact original 32-page booklet is authenticated against SHA-256 `53c7cc72c28f80969ed56d7813ad8c05e505b1817923418d0dfa45368a6bd07e`, extracted with PyMuPDF 1.28.2 `blocks-v3`. The 91-span catalog hash remains `8d98a741550f450a64bb8103ece1efa561b0c75436b8096bf47ac6c74508d618`. Printed editorial cutoff is 2023-11-29; publication date is unknown. The semantic reference remains byte-for-byte unchanged from PR head `7bec7f8`. Both actors' passages stay available; the fix neither filters away the committee nor replaces a wrong selection with the gold citation.

[New evidence manifest](gate0-attribution-2026-10-12/manifest.json) retains the failed v4 and both successful v5 runs, raw requests/responses and independently checkable component hashes. Previous failed manifests/traces are unchanged. Only absolute local model directories are redacted. Sixty-six synthetic tests and the existing design-contract validator pass locally; source/catalog/reference and actual-response integrity checks pass. Deterministic CI performs the same verification without inference. Human review, public availability, other referendums, holdouts, cold Docker execution and frontend implementation remain unverified. Task types, limited retrieval, null personal costs and reason codes remain application-supplied as disclosed in the prior report.

## Reproduce

Use the [existing local server/identity commands](GATE0_SPANS_2026-10-12.md#reproduce), the same pinned weights and original PDF. Then run:

```sh
.venv/bin/python track_2b/src/gate0/span_probe.py --source-report .local/gate0/source.json --source-pdf .local/gate0/booklet.pdf --local-model-report .local/gate0/identity.json --out-dir .local/gate0/attribution-new-run
.venv/bin/python -m unittest discover -s track_2b/tests -p 'test_gate0*.py' -v
.venv/bin/python track_2b/src/gate0/verify_span_evidence.py --evidence-dir track_2b/docs/evidence/gate0-attribution-2026-10-12 --source-pdf .local/gate0/booklet.pdf
```

Exit 0 means the bounded machine suite passed; the summary still says `HUMAN_REVIEW_REQUIRED`, `public_availability_verified: false`, and `frontend_authorized_by_this_run: false`. It does not authorise publication or frontend work.
