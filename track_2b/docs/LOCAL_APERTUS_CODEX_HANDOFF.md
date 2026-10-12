# Codex handoff — Run the user's **local** Apertus model first

**Created:** 2026-10-12  
**Branch:** `feat/gate0-source-and-apertus-probe`  
**Status:** Instructions for execution on the user's Mac. No inference has yet been run.

## User's immediate objective

The user has ALREADY downloaded Apertus onto their local Mac. The next job is to **discover the existing files and runtime, prove real local inference, and connect those results to the source-grounded 13th-AHV Gate 0 test**. Prefer local inference. Do NOT ask the user to purchase an API key before trying the local model. Do NOT download an additional 8B/70B model without first inspecting what is already installed. Do not assume that a download by itself implies a runnable model.

## Codex's environment and permissions

Work locally on the user's machine. Use existing GitHub repo [Devpen787/stimmfolgen](https://github.com/Devpen787/stimmfolgen) and checkout branch `feat/gate0-source-and-apertus-probe`, the head of draft PR #3 based on the design setup PR #2. Verify that the branch contains `track_2b/src/gate0/source_probe.py`, `track_2b/src/gate0/model_probe.py`, `AGENTS.md` and `track_2b/docs/blueprint-v0.1`. Keep changes focused and open reviewable pull requests. Do not merge or use protected GitHub secrets.

## Step 1 — Observe the machine, do not guess

Inspect **without uploading any personal files**:

1. Mac CPU architecture (Apple Silicon arm64 vs Intel), physical RAM, free disk, macOS version.
2. Whether Ollama, LM Studio, MLX, llama.cpp, Python/transformers, or another compatible runtime is already installed.
3. The ACTUAL location, format and size of Apertus assets the user downloaded: Ollama model/tag, GGUF, MLX repository, Hugging Face safetensors shard set, or something else. Ask the user for the folder location only if discovery cannot find it. Do not traverse or share unrelated private folders.
4. Exact checkpoint version (Apertus v1.5 **8B or 70B**) and quantization, verifying model metadata rather than inferring identity from a filename alone.
5. Estimate memory compatibility; if 70B or unquantized weights cannot realistically fit, document that and propose the least costly feasible 8B option, with explicit user permission before downloading.

Expected output: a compact factual environment report and one selected **local inference** strategy.

## Step 2 — Serve Apertus locally

Preferred: the already-installed runtime compatible with the existing model format.

- Existing Ollama model: inspect `ollama list` and model metadata; consider its OpenAI-compatible `http://localhost:11434/v1`.
- Existing GGUF: check local llama.cpp compatibility and serve an OpenAI-compatible endpoint, or import into installed Ollama if supported.
- Existing MLX model on Apple Silicon: use the compatible MLX serving mode if installed.
- Hugging Face safetensors: assess transformer/runtime support and hardware limits; do NOT rename safetensors to GGUF or assume any format will work in Ollama.
- If model is genuinely unavailable locally, stop and report precise blocker rather than substituting a cloud model or mocked completion without permission.

Make a tiny real test generation first (`2+2`, or another deliberately trivial probe), recording the model identity, serving command, model size/quantization, response, hardware and latency. This proves **inference happened**, not reasoning quality.

## Step 3 — Connect the repo's reproducible Gate 0 test

Run the existing source probe over the actual 2024 Federal Chancellery PDF:

```sh
python3 -m pip install 'pymupdf>=1.24,<2'
python3 track_2b/src/gate0/source_probe.py --out /tmp/stimmfolgen-gate0-source.json
```

Prior GitHub Actions source evidence **has passed**: public official PDF, SHA-256 `53c7cc72c28f80969ed56d7813ad8c05e505b1817923418d0dfa45368a6bd07e`, 32 pages and five extracted. Reverify the local bytes and exact source edition.

To run the actual model adapter, use the **local** endpoint:

```sh
export LLM_BASE_URL='http://localhost:11434/v1' # example only, use chosen runtime
export LLM_NAME='<exact SERVED Apertus model identifier>'
unset LLM_API_KEY # no hosted token needed for unauthenticated loopback endpoints
python3 track_2b/src/gate0/model_probe.py --source-report /tmp/stimmfolgen-gate0-source.json --out /tmp/stimmfolgen-gate0-model.json
```

**Important model identity guard:** the current `model_probe.py` only accepts IDs beginning `swiss-ai/apertus`. A genuine local Ollama or GGUF model may expose a short alias like `apertus:8b`. Do not simply disable the guard; verify the model's provenance and installed runtime metadata, then extend the guard for *verified* local aliases and capture the real backing checkpoint/quantization. The model parameter sent to `/v1/chat/completions` must be the actual served alias.

The probe's quote check proves only that quote text appears on the selected page. It does NOT prove the interpretation is supported or that projected downstream impacts will happen.

## Step 4 — Test the risky promise, with deliberate failure

Ask the model to extract:

1. One direct provision about the 13th AHV pension.
2. One projected cost or actor-attributed political claim, labelled as a projection/claim.
3. One explicit unresolved issue: **the original initiative did not settle financing**. Refuse a precise employed person's future CHF financing impact when no enacted financing formula exists.

Preserve **raw request and response**, source hashes, page links, local hardware/model metadata and prompt revision. Run targeted negative controls: fake page quote, attributed actor mix-up, unsupported CHF calculation, and temporal leakage from post-2024 information. Fail closed and mark uncertain rather than emitting unreviewed statements as established facts.

Have human reviewer check **meaning**, not only substring matches. Never insert a fake 'success' into README or technical report.

## Step 5 — Convert to a first vertical slice, AFTER model gate passes

Only after successful local inference:

- Connect verified/candidate claims through the v0.1 JSON schema to ONE public case screen.
- Implement one complete user path: choose 2024 AHV → what changes → affected people → why/how → sources & unknowns → user understanding brief.
- Keep personal context optional and local. Do not imply encryption is complete without implementation/security verification.
- Make failure, empty-state and model-offline handling visible.
- Align Docker `make run` with the actual supported inference architecture, including how a judge can run the system with available Apertus service, weights and dependencies. A working developer localhost setup is NOT automatically an end-to-end clean Docker submission.
- Add a second referendum only when the same pipeline works without manual hardcoding.

## Explicit non-claims

Until verified, DO NOT claim the app is live, that public data is neutral just because it's in the official booklet, that any causal inference is proven, that the private vault is encrypted, that any configured hosted model is Swiss-sovereign, or that GitHub Actions can reach a model running on the Mac.

## Definition of done for current Codex session

Give the user a link to the focused PR, a plain-English outcome of the real local model test (PASS / FAIL / BLOCKED), exact evidence and commands, environment/hardware facts, at least one real model response tied to booklet provenance if available, and the next issue. If local serving fails, diagnose it rather than launching a large frontend build.
## Current continuation: immutable spans (12 October 2026)

Use `src/gate0/span_probe.py` for the active local test, not the historical generated-quote diagnostic. [Latest evidence and reproduction commands](evidence/GATE0_SPANS_2026-10-12.md) preserve all four span runs and independently revalidate their source-grounded typed propositions. Two unchanged final Apertus v1.5 runs pass six of seven live trials but fail actor attribution. Gate 0 and the frontend remain blocked; do not promote coding-agent-authored reference results to human review. CI validates source/trace integrity only; no cloud model runtime or self-hosted Actions runner was provisioned.

## Latest attribution continuation (12 October 2026)

[The corrected local v1.5 pipeline](evidence/GATE0_ATTRIBUTION_2026-10-12.md) passes all seven bounded trials and the combined happy path in two unchanged runs. Apertus extracts the source actor and separately parses the requested actor; application comparison returns source conflict when they differ. No expected actor or gold ID enters generation or comparison. All prior failures, including the failed first fix, remain preserved. The composed refusal is not a single model answer. Human semantic review and publication availability remain outstanding; frontend work stays blocked.
