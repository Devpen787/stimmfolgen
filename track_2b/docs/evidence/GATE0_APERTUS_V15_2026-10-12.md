# Gate 0 — actual local Apertus v1.5, 12 October 2026

**Overall outcome: FAIL. Actual local v1.5 text-model inference is verified; the AHV extraction is not reliable enough to proceed to the frontend.** The source and deterministic safeguards pass. No output is human approved or promoted to a verified policy effect.

## Runtime and provenance

The existing model on this M3 Pro / 18 GiB Mac was `mlx-community/Apertus-8B-Instruct-2509-4bit`, not v1.5. Its actual failed experiment is retained in [the legacy report](GATE0_LOCAL_APERTUS_2026-10-12.md). After inspecting hardware, existing assets and a feasible conversion, a separate local v1.5 model was acquired; no paid API was used.

- Actual conversion: [`tokimoa/apertus-v1.5-8b-mlx-4bit`](https://huggingface.co/tokimoa/apertus-v1.5-8b-mlx-4bit).
- Conversion revision: `f08ed532a657bef7d322bd0cbca43dac13a9d0a3`.
- Publisher-declared backing checkpoint: [`swiss-ai/Apertus-v1.5-8B`](https://huggingface.co/swiss-ai/Apertus-v1.5-8B), upstream revision `a411d838600baf0e3635a3daf66fb7c55fc97bb6`.
- Actual weights: **4,530,491,646 bytes (4.22 GiB)**. Full SHA-256 independently computed locally: **`d0478edeb06bf18e5f4f7b50db77d89b839730b2d16cb1020015e6099e42074b`**, matching the pinned repository's LFS metadata and cached download metadata.
- Local path: `.local/models/apertus-v1.5-8b-mlx-4bit`, ignored by Git.
- Format: MLX safetensors, affine 4-bit quantization / group 64. The cached card, configuration, complete weight hash, tokenizer/chat-template hashes and safetensors header were inspected.
- Dedicated loopback server: `http://127.0.0.1:8766/v1`, actual served alias **`default_model`**, bound to the inspected path through MLX's CLI/default-model mapping and `/v1/models` response.
- Existing runtime: **MLX 0.32.0 / mlx-lm 0.31.3 / Transformers 5.15.0**; macOS 26.6.2 arm64, 12 CPU cores, 18 GPU cores. Source tooling: Python 3.14.6 / PyMuPDF 1.28.2.

This is the converter's **text-only extraction** of the v1.5 checkpoint, not the original multimodal distribution. Provenance and artifact identity were verified; an independent equivalence test against official BF16 weights was not performed. No new runtime packages were installed into AutoBots. Its existing runtime executable was used read only; all project changes, cached weights, source files and logs are in StimmFolgen. Source/dependency/model acquisition used the network; inference used explicit local paths with Hugging Face offline modes. The OS was not air-gapped.

The new model returned exactly **`4`** to `Rechne 2 + 2. Antworte nur mit der Zahl.` in **2.21 seconds**, 2 completion tokens. Raw request and response are published in the evidence folder. This is real generation proof, not policy-quality proof.

## Exact official source and parser correction

The actual [Federal Chancellery March 2024 booklet](https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf) was retrieved on this Mac: **759,783 bytes, 32 PDF pages**, SHA-256 **`53c7cc72c28f80969ed56d7813ad8c05e505b1817923418d0dfa45368a6bd07e`**. Selected PDF/printed pages are **4, 9, 11, 14, 16**. The printed editorial cutoff on page 2 is **29 November 2023**.

The original line-sorted extraction inserted left sidebar headings into body sentences and split soft-hyphen words. For example, a provision became `nicht nur 13. AHV-Rente 12 Mal`, while `Einführung` became `Ein der Initiative führung`. This made reasonable quotations fail exact matching. The parser now preserves whole text blocks and joins actual soft-hyphen line continuations. Raw text blocks, bounding boxes and normalized text hashes are retained. Old extraction modes remain available to authenticate earlier failed traces. The PDF bytes are unchanged.

The editorial cutoff is a **knowledge basis**, not a verified public-release date. The final report (`blocks-v3`) records `published_at=null`, `available_at=null` and `public_availability_verified=false`. Earlier experimental `available_at` values were editorial-cutoff proxies, not independent publication evidence. Public temporal availability still needs review before admission to a published product case. All model prompts use the historic booklet knowledge frame and exclude later financing decisions.

## Actual experiment and candid result

There were **22 v1.5 local responses**: one smoke response, two nine-trial suites and three focused template probes. These repeat one development case; they are not 22 independent evaluation cases or an accuracy benchmark. Each preserves the exact public request/response, model/source identity, prompt revision, decoding settings, latency and failures.

The initial nine-trial suite failed all mechanical checks. Failures included translated actor identifiers, glued/non-exact quotes, missing dates and output contract mistakes. The source parser and prompt schema were corrected without replacing raw model outputs or weakening exact citation checks.

The corrected nine-trial suite had three mechanically valid responses at run time. A subsequent final validator check also enforces the prompt's 240-character quote limit, reducing this to **two of nine**. **Neither count establishes semantic correctness.**

| Corrected trial | Final mechanical result | Meaning/limitation observed by coding agent |
| --- | --- | --- |
| Full extraction | FAIL | Reversed 13 vs 12 payments; omitted prediction/unknown coverage; returned personal financing `0` |
| Direct provision | FAIL | Concatenated two nonadjacent sentences; used an insufficient-evidence outcome for a stated provision |
| Cost projection | FAIL | Classified a pension-scope provision as a cost projection |
| Financing refusal | PASS, unreviewed | Correct cited financing gap and no exact personal CHF amount |
| Fake page quote | FAIL / WITHHELD | Repeated the invented CHF 100 quote; rejected by source comparison |
| Actor mix-up | FAIL / WITHHELD | Still attributed the government's budget argument to the committee; a matching committee quote did not support that interpretation. Also exceeded quote-length limit |
| Unsupported CHF | FAIL / WITHHELD | Returned personal financing `0`, which is a specific unsupported amount, not unknown |
| Temporal leakage | PASS mechanically, unreviewed | Did not use later decisions, but misclassified a pension-scope provision as COST_PROJECTION |
| Full-booklet baseline | FAIL | Non-exact citation/role, missing coverage and personal financing `0` |

The actor trial is a concrete demonstration that a source substring, matching page role and valid JSON **cannot establish interpretation**. It must not be accepted as a successful E03 attribution test. A unit test explicitly preserves this distinction. No model or coding agent is represented as a human reviewer.

A genuine successful narrower response is the financing refusal in `corrected/financing_refusal.json`:

> The initiative does not specify how the additional costs for the 13th AHV pension will be financed.

Its exact [page 11](https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf#page=11) quote is `Die Initiative macht keine Angaben dazu, wie die zusätzlichen Ausgaben für die 13. AHV-Rente finanziert werden sollen. Das müsste vom Parlament bestimmt werden.` The response uses `UNRESOLVED`, correct source role/date, explicit missing financing facts, `INSUFFICIENT_EVIDENCE` and `personal_financing_chf=null`.

The focused cost-projection template also passed mechanical checks and generated the **4.1-billion-CHF projected introduction cost** with an exact page-11 quote and `COST_PROJECTION`. Its statement additionally mentions the five-year figure, which is elsewhere on the same page but outside its selected quotation; that detail still needs its own reviewed support span. The three focused templates supplied kind/outcome/metadata, so they are **not independent classification or refusal-choice tests**. The focused provision failed because it glued separate sentences; the focused refusal omitted required unknowns.

## Baselines and evidence limits

Both suites include the actual v1.5 full-booklet baseline, using the same model, temperature 0, 1,400-token generation budget and task as the selected-page extraction. Initial full-booklet latency: **61.42 seconds**; corrected: **54.95 seconds**. Selected-page full extraction: **40.71 / 47.90 seconds**. The larger prompt was slower in these particular observations; no universal speed or quality conclusion follows. Both paths failed.

An extractive baseline separately retrieves three exact provision/cost/financing passages through authored AHV search cues. It is labelled **EXTRACTIVE_BASELINE_NO_MODEL**. It does not produce a generated interpretation or prove new-case generalisation. The traces, baseline passages and raw block geometry are in [the evidence directory](local-apertus-v15-2026-10-12/). `MANIFEST.json` pins the published artifacts; absolute model paths are redacted, while raw HTTP prompts/responses are unchanged.

## Software fixes and verification

- Bind supported local aliases to explicitly pinned, rechecked conversion bytes and endpoint paths. Distinguish the legacy and v1.5 artifacts; never upgrade identity from a filename or alias alone.
- Require the original pinned PDF when invoking the model; compare source-role/date/text metadata with independently re-extracted bytes. Separate publication-date unknowns from editorial cutoff.
- Preserve text blocks and soft-hyphen continuations, with reproducible old extraction versions.
- Clarify JSON fields/role enums; retain both failed prompt revisions and final outputs.
- Keep parse failures, truncation, invalid/missing fields, empty supported answers, coverage failures and unsupported financing values. Validate exact quotes, offsets, hashes, roles, dates, kinds and quote lengths. Do not publish mechanically valid but semantically unreviewed candidates.
- Use actual loopback hostname checks and reject credentials embedded in endpoint URLs, unverified aliases and fabricated Apertus model names.
- Retain failed-run evidence in the manual workflow without invoking any hosted service during this session.

**38 deterministic unit tests PASS**, including source mutation, sidebar-ordering, soft-hyphen, wrong checkpoint, fake quote, actor swap, CHF value, date and truncation controls. The official source re-extraction, artifact/request/response hashes, and existing synthetic design-contract validator pass locally. CI outcomes are separate and linked in the PR. No frontend, Docker application, unseen referendum, encryption implementation, held-out accuracy study or human review was completed.

## Reproduce this local test

From the PR checkout:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install 'pymupdf==1.28.2'
mkdir -p .local/gate0
.venv/bin/python track_2b/src/gate0/source_probe.py \
  --out .local/gate0/source.json --pdf-out .local/gate0/booklet.pdf

APERTUS_MODEL_DIR="$PWD/.local/models/apertus-v1.5-8b-mlx-4bit"
APERTUS_PYTHON="$HOME/.local/share/autobots/apertus-mlx-runtime/venv/bin/python"
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1 \
  PYTHONDONTWRITEBYTECODE=1 "$APERTUS_PYTHON" -m mlx_lm server \
  --model "$APERTUS_MODEL_DIR" --host 127.0.0.1 --port 8766 \
  --temp 0 --max-tokens 1800 --chat-template-args '{"enable_thinking":false}' \
  --decode-concurrency 1 --prompt-concurrency 1 --prompt-cache-size 1 \
  --prefill-step-size 512
```

After the server is ready, in a second terminal in that checkout:

```sh
.venv/bin/python track_2b/src/gate0/local_model.py \
  --model-dir .local/models/apertus-v1.5-8b-mlx-4bit \
  --base-url http://127.0.0.1:8766/v1 --out .local/gate0/local-model.json
.venv/bin/python track_2b/src/gate0/evaluate_local.py \
  --source-report .local/gate0/source.json --source-pdf .local/gate0/booklet.pdf \
  --local-model-report .local/gate0/local-model.json --full-booklet-baseline \
  --out-dir .local/gate0/repeat
.venv/bin/python track_2b/src/gate0/focused_probe.py \
  --source-report .local/gate0/source.json --source-pdf .local/gate0/booklet.pdf \
  --local-model-report .local/gate0/local-model.json --out-dir .local/gate0/focused
.venv/bin/python -m unittest discover -s track_2b/tests -p 'test_gate0.py' -v
```

The failing suite exits **2** and still saves every attempt. Exit 0 means mechanical checks succeeded, never human semantic approval. Stop the dedicated server with Ctrl-C after use. Fresh source reports now explicitly leave publication dates unknown; the rendered source text is unchanged from the corrected model run. Earlier prompts and extraction versions can be reproduced from their preserved raw requests/reports. Outputs and latency may vary by runtime/hardware.

Weights already exist on this Mac. A different machine must acquire the pinned conversion explicitly; the exact original acquisition was `huggingface_hub.snapshot_download('tokimoa/apertus-v1.5-8b-mlx-4bit', revision='f08ed532a657bef7d322bd0cbca43dac13a9d0a3', local_dir='.local/models/apertus-v1.5-8b-mlx-4bit')`. Model weights and raw PDF files are not in Git. This is a disclosed local runtime prerequisite, not a cold Docker submission.

## Next issue

Fix citation construction through immutable source-span selection rather than asking the model to retype/concatenate quotes. Add an independent semantic reference/review for the provision direction, actor attribution and cost classification. Re-run the same adverse controls before claiming Gate 0 passed. **The frontend remains stopped.**
