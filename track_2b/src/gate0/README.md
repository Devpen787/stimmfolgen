# Gate 0 — official source and actual local Apertus

The [current observed run](../../docs/evidence/GATE0_APERTUS_V15_2026-10-12.md) verifies genuine local v1.5 text-model inference. **The real AHV diagnostic FAILS; the frontend remains stopped.** The report includes hardware, pinned model/source hashes, exact commands and genuine failure traces. The existing 2509 checkpoint was also tested; its historical diagnostic is retained separately.

`source_probe.py` acquires/checks the pinned official PDF, editorial cutoff and five pages. Block extraction preserves sidebar order and soft-hyphen continuations. Raw block geometry and hashes are recorded. Publication date/availability remain unknown; editorial cutoff is only the knowledge basis.

`local_model.py` verifies one of two explicitly pinned MLX conversions and the local endpoint/path binding. `model_probe.py` requires original PDF bytes, records every actual attempt and performs mechanical validation. Unverified local aliases and arbitrary Apertus-like names are rejected. Legacy inference requires `--allow-legacy-diagnostic` and cannot pass the checkpoint gate.

`evaluate_local.py` runs actual extraction and the fake-quote, actor, CHF and hindsight controls. `--full-booklet-baseline` adds a same-model, same-generation-budget baseline; the extractive baseline is explicitly not model output. `focused_probe.py` reproduces template-guided trials whose metadata/type/outcome are supplied, so their results are not independent classification accuracy.

All actual outputs remain candidate/unreviewed or withheld. Exact quotes and role identifiers do not prove interpretation. No human semantic reviewer approved this run. A wrong source-grounded interpretation is explicitly demonstrated and tested. A zero CLI exit code means mechanical success only.

Start the loopback server and run the commands in the evidence report. A configured real hosted endpoint is also supported via `LLM_NAME`, `LLM_BASE_URL`, and securely supplied `LLM_API_KEY`; none was used in this session. `.local/` keeps weights, raw PDFs and temporary logs ignored. Never commit credentials or private voter notes.

This probe is not the final Docker `make run` application, an encrypted vault, or a held-out policy-reasoning benchmark.
