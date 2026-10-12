# Gate 0 — Real official source / real Apertus experiment

**State:** SOURCE TEST ready. Model call prepared, but not yet executed. Never claim a completed Apertus inference until an actual model trace and semantic human check exist.

## Why this is the first gate

In the official March 2024 booklet, the 13th AHV provision is defined but its financing is not. Payroll and VAT changes are hypothetical alternatives, not enacted financing decisions. A model must not invent a person's precise CHF burden.

## Get the source (public document)

The official source URL is hard-coded/allowlisted in `source_probe.py`. It downloads the bytes, SHA-256 hashes them and extracts 5 pages with PyMuPDF. The editorial cutoff is **29 November 2023** as printed on PDF page 2. `gate0-source.json` contains page-level extracts and source metadata. It is labelled `SOURCE`, not model-generated evidence.

```bash
pip install 'pymupdf>=1.24,<2'
python track_2b/src/gate0/source_probe.py --out /tmp/gate0-source.json
python -m unittest discover -s track_2b/tests -p 'test_gate0.py' -v
```

For an externally obtained, trusted exact PDF, specify `--pdf /path/to/booklet.pdf` instead of download.

## Only when real model access is configured

```bash
export LLM_NAME='swiss-ai/Apertus-v1.5-8B'
export LLM_BASE_URL='https://api.inference.cscs.ch/v1' # example; requires authorisation
# Set LLM_API_KEY securely in your runner or secret manager. Do not commit credentials.
python track_2b/src/gate0/model_probe.py --source-report /tmp/gate0-source.json --out /tmp/gate0-model.json
```

The output records actual response, provenance, model ID and mechanical quote-presence checks. **A matching quotation proves only that the words appear on the PDF page; it does not prove the claim or prediction is true.** All model findings remain `CANDIDATE_UNREVIEWED` until a human checks meaning, attribution and dates.

## Limits and next decision

- This is a small experiment, **not** the final `make run` end-to-end application.
- Network access is required to acquire the official PDF; offline/on-prem deployment must use vetted cached sources.
- No local private voter notes are collected.
- No source text is assumed neutral just because it appears inside the official booklet.
- Negative findings and inability to access the model must be recorded without simulating a pass.
