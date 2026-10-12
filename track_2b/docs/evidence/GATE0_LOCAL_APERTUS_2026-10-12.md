# Gate 0 — historical legacy Apertus phase, 12 October 2026

**Historical phase only.** The subsequent [actual v1.5 run](GATE0_APERTUS_V15_2026-10-12.md) supersedes this phase for current project status.

**Outcome at this phase: BLOCKED for the required v1.5 checkpoint; FAIL for the installed legacy model's structured AHV diagnostic. Actual local inference and the official source are verified. No frontend work began.**

Branch started from `feat/gate0-source-and-apertus-probe` at `10fc09fbd7a896ebc37b7830083f8477899b1f56`. This is a single-case development experiment, not held-out accuracy, human semantic approval, or a completed submission.

## Machine, assets and runtime

Observed Mac: Apple M3 Pro, arm64, 12 CPU cores, 18 GPU cores, 18 GiB RAM, macOS 26.6.2. Disk space was about 254 GiB free before this work. The installed model is **not Apertus v1.5**:

- Conversion: `mlx-community/Apertus-8B-Instruct-2509-4bit`.
- Backing checkpoint: `swiss-ai/Apertus-8B-Instruct-2509`.
- Conversion revision: `c5e6ae2e52c4149f36cb8e47b7ab1489ef885fed`.
- Model path: `~/.cache/bml-models/apertus-8b-instruct-2509-mlx-4bit`.
- MLX safetensors, affine 4-bit / group 64; 839 tensors, packed U32 weights and BF16 auxiliary tensors. Weight SHA-256: `bcde62001035dd38e9a8b2642f29e0d7b98ef7a6e69b50a6e55be26a8b1c0a9a`.
- Existing runtime: MLX 0.32.0, mlx-lm 0.31.3, Transformers 5.15.0. Model weights are approximately 4.53 GB. This is compatible with short-context inference on this 18 GiB machine; it does not establish maximum-context capacity.
- Source tooling: repo-local Python 3.14.6 and PyMuPDF 1.28.2.

Identity was checked through the cached card, configuration, safetensors header, download revision and complete weight hash. A dedicated `mlx_lm.server` process served these weights at `http://127.0.0.1:8766/v1`, with the actual MLX alias `default_model`. The endpoint advertised the inspected resolved model path. The installed server's source maps that alias to its `--model` argument. This is a locally controlled runtime binding, not signed remote attestation.

Standard model locations (`~/.cache`, Ollama and local runtime directories) contained this conversion and a symlink to it, with no v1.5 weights found. Ollama's model list contained Gemma and Qwen, not Apertus. No additional model weights were downloaded. The separate service did not modify AutoBots code, registries, runtime environment or KG state. The unrelated Open Source AI checkout was left alone during this run.

## Actual inference and source

The loopback smoke request `Rechne 2 + 2. Antworte nur mit der Zahl.` returned **`Die Antwort lautet 4.`**, 7 completion tokens, in 2.30 seconds. This verifies generation, but fails the exact number-only instruction.

The original adapter then rejected the genuine local alias before a model request. This failure is retained in `original-adapter-failure.json`. The revised guard admits the alias only with freshly rechecked pinned local bytes and an endpoint/path binding; it does not accept arbitrary names beginning with `swiss-ai/apertus`.

The actual Federal Chancellery PDF was downloaded again on the Mac: **759,783 bytes**, **32 pages**, SHA-256 **`53c7cc72c28f80969ed56d7813ad8c05e505b1817923418d0dfa45368a6bd07e`**. The printed editorial cutoff on PDF page 2 is **29 November 2023**. PDF pages **4, 9, 11, 14 and 16** were extracted. All model requests use the PRE_VOTE knowledge frame `2023-11-29`; later implementation or financing decisions are not part of that source frame.

The official source is [the March 2024 voting booklet](https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf). Model output and public excerpts are retained for inspection, with original requests and response bytes represented as UTF-8 text. The PDF itself remains in ignored `.local/`, not Git.

## Results and failure analysis

The first unmodified prompt was sent directly to the verified local server after observing the alias rejection. It produced two invented quotations, wrong actor labels and no required direct/projection coverage. It took 34.46 seconds. This is a genuine failed model response, not a fixture.

The stricter v2 suite produced eight actual responses. **All eight failed the structured diagnostic.**

| Trial | Observed failure | Seconds |
| --- | --- | ---: |
| Full extraction | Prose instead of the required JSON | 51.98 |
| Direct provision | Missing contract fields; existing-rent quote did not support the requested 13th-payment statement | 10.07 |
| Cost projection | Missing fields; quoted five-year cost while labelling introduction cost | 9.10 |
| Financing refusal | Correct general abstention in prose, but no valid structured/cited answer | 6.05 |
| Fake page quote | Repeated the fake quote; completion also hit its token limit | 26.78 |
| Actor mix-up | Attributed the government's budget argument to the initiative committee; prose instead of JSON | 15.97 |
| Unsupported CHF | No valid refusal contract, fabricated quote/role metadata | 9.02 |
| Temporal leakage | No valid refusal, invented quote/role and missing date metadata | 8.31 |

Three additional focused German templates also failed the JSON contract. These supplied expected kind/outcome/metadata, so they are **not independent classification tests**. Their full inputs are recorded and should not be pooled into an accuracy percentage.

There is useful narrower evidence: the focused provision response copied an exact contiguous paragraph from **PDF page 9** about paying the monthly old-age pension 13 rather than 12 times a year. The exact source offset is recorded in `focused-provision-source-check.json`. It still failed JSON output and is **WITHHELD**. This demonstrates actual source-backed extraction, not a passing product pipeline.

The focused refusal began: “Die Frage, wie viele zusätzliche CHF eine angestellte Person definitiv pro Jahr bezahlen müsste, wenn die Finanzierung nicht beschlossen ist, kann nicht beantwortet werden”. It then discussed the missing financing formula and hypothetical alternatives, but repeated text and exhausted its token budget. It remains a failed structured answer, despite the useful initial refusal.

These semantic observations were made by the coding agent against the actual booklet. **No human semantic reviewer has approved any model output.** Exact substring matches prove copied words, not supported interpretation or the truth of forecasts. The tests explicitly demonstrate that a matching quote can accompany an unsupported interpretation.

## Fixes and validation

- Verify the pinned PDF edition and printed editorial cutoff; retain page text hashes, offsets and links. Require original PDF bytes when running inference and compare re-extracted pages, so an edited JSON report cannot substitute fabricated source text.
- Admit the inspected MLX alias using explicit local provenance. Record that the backing model is legacy; require opt-in diagnostic mode and return a nonzero exit status. Do not relabel it v1.5.
- Check the URL hostname rather than searching for the word `localhost`; reject embedded credentials and unverified aliases.
- Preserve raw public request/response, hashes, timings and parsing failures. Reject truncated responses, empty supported answers, missing claim coverage, wrong roles/dates and non-null personal-financing numbers.
- Keep every candidate unreviewed or withheld. No code claims that these mechanical checks establish semantic entailment. No automatic publication or frontend gate is implemented.
- Update the manual CI recorder to cache source bytes and retain failed-run traces; it has not been dispatched and cannot access this Mac's model.

**31 deterministic unit tests PASS**, including synthetic adversarial controls for fake quotes, actor swaps, unsupported CHF and temporal/source mutations. These unit inputs are explicitly synthetic and are not model results. The official source probe passes locally. The prior six tests passed before changes. CI results and design-contract checks are recorded separately in the PR; no clean Docker application, held-out benchmark, second referendum, or human comprehension test was run.

## Reproduce locally

From a checkout of this PR, with the existing model and runtime:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install 'pymupdf==1.28.2'
mkdir -p .local/gate0
.venv/bin/python track_2b/src/gate0/source_probe.py \
  --out .local/gate0/source.json --pdf-out .local/gate0/booklet.pdf

APERTUS_MODEL_DIR="$HOME/.cache/bml-models/apertus-8b-instruct-2509-mlx-4bit"
APERTUS_PYTHON="$HOME/.local/share/autobots/apertus-mlx-runtime/venv/bin/python"
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 \
  PYTHONDONTWRITEBYTECODE=1 "$APERTUS_PYTHON" -m mlx_lm server \
  --model "$APERTUS_MODEL_DIR" --host 127.0.0.1 --port 8766 \
  --temp 0 --max-tokens 1800 --chat-template-args '{"enable_thinking":false}' \
  --decode-concurrency 1 --prompt-concurrency 1 --prompt-cache-size 1 \
  --prefill-step-size 512
```

In a second terminal in the same checkout, after the server is ready:

```sh
.venv/bin/python track_2b/src/gate0/local_model.py \
  --model-dir "$HOME/.cache/bml-models/apertus-8b-instruct-2509-mlx-4bit" \
  --base-url http://127.0.0.1:8766/v1 --out .local/gate0/local-model.json
.venv/bin/python track_2b/src/gate0/evaluate_local.py \
  --source-report .local/gate0/source.json --source-pdf .local/gate0/booklet.pdf \
  --local-model-report .local/gate0/local-model.json --allow-legacy-diagnostic \
  --out-dir .local/gate0/repeat
.venv/bin/python -m unittest discover -s track_2b/tests -p 'test_gate0.py' -v
```

The evaluator intentionally exits **2** for this legacy checkpoint, regardless of mechanical results. Stop the dedicated server with Ctrl-C afterward. Prompts, budgets and observed outputs are in `local-apertus-2026-10-12/`; exact previous requests can also be resent to this loopback endpoint. Output/latency need not be byte-identical across hardware/runtime versions. The focused templates are preserved as raw requests, not represented as the default suite.

Inference used local weights and Hugging Face offline modes. Network was used for public-source, dependency and metadata acquisition; the OS was not air-gapped. No paid API, private voter context, credential, protected GitHub secret, or personal-file upload was used. Absolute model paths are redacted in published metadata; raw HTTP prompts/responses are unchanged.

## Concrete next decision

A candidate no-paid-API route is the publisher's text-only [v1.5 MLX 4-bit conversion](https://huggingface.co/tokimoa/apertus-v1.5-8b-mlx-4bit), revision **`f08ed532a657bef7d322bd0cbca43dac13a9d0a3`**, declared upstream revision **`a411d838600baf0e3635a3daf66fb7c55fc97bb6`**. Its weight file is **4,530,491,646 bytes (~4.22 GiB)**; the inspected config uses `model_type=apertus`, the same 4-bit affine/group-64 format supported by the existing MLX runtime. This is a plausible memory-compatible next experiment, not verified inference or independent conversion-equivalence proof. The official [v1.5 model card](https://huggingface.co/swiss-ai/Apertus-v1.5-8B) confirms a separate checkpoint family; the current cached weights cannot satisfy that identity.

Only small public metadata was fetched for this option (`v15-option.json`), not weights. The initially stated download-permission requirement was read too broadly: the explicit permission condition concerns a hardware-infeasible model replacement; the separate inspection-before-download condition was satisfied here. The feasible pinned v1.5 conversion was subsequently acquired and tested locally. See the current v1.5 report for the actual FAIL result; frontend work remains stopped.
