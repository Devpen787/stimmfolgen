# Live Apertus development evidence — 15 October 2026

**Status: local browser-to-model happy path observed; public hosting and full live QA acceptance NOT cleared.** This supplements the prior bounded, human-reviewed Gate 0. It does not replace that gate, edit its approvals, or establish general civic-analysis accuracy.

The user requested real, use-time Apertus answers accessible to other people's browsers, without model downloads, and explicitly excluded their Mac as a host for other people. They subsequently required zero payment from both owner and visitors. No hosting purchase, API charge, public deployment or organiser submission has been performed.

## Actual local experiments

Pinned `swiss-ai/Apertus-v1.5-8B`, text-only community MLX 4-bit conversion, existing M3 Pro 18 GiB Mac, literal loopback port 8766. See the established Gate 0 identity contract for exact conversion and weight hashes. A fresh identity inspection authenticated the local weights before these calls. Every local generation and checking call reauthenticates the model and original PDF.

Twenty question trials across four prompt revisions are retained in this folder. Both successful and failed outputs remain. `manifest.json` hashes the path-redacted files. Only the absolute repository path is replaced with `<REPO>`; raw prompts and completions remain unchanged. These are public test questions, not actual voter questions/notes. The generator uses the five human-reviewed propositions as its bounded evidence; it does not independently ingest arbitrary votes.

The first prompts produced irrelevant summaries, copied an uncertainty placeholder, omitted required uncertainty fields, misread later-event questions and produced malformed JSON. A separate pass by the **same model** sometimes rejected valid uncertainty explanations and sometimes accepted irrelevant information. This is not an independent semantic oracle or proof of accuracy. Deterministic checks reject malformed structures and invented evidence IDs; the model check is an additional imperfect filter. Rejected answers are withheld.

Final v4 local set: one supported answer, four withheld answers. This is **not five passing answers**. The supported answer preserves the proposal and attributed national cost estimate, but includes an extra cost fact not necessary for the question. Better relevance and useful refusal coverage remain open work, followed by testing the actual selected hosted model. Changing from local 8B to hosted 70B requires new evidence; no equivalence is assumed.

## Observed browser journey

Agent-operated usability walkthrough, not an independent human user study or physical-phone test:

- Search AHV and track the vote.
- Open What it means and submit an explicit public question through `/api/live/question`.
- Receive a fresh real Apertus answer in **30.38 seconds**, with human-reviewed source and date drawers and explicit AI/unreviewed labelling.
- Navigate dated official Updates, sourced Related votes, and the worker Perspective with financing uncertainty.
- Save a synthetic visit-only note; create a disposable encrypted QA vault; reload locks it; unlock restores the note and tracked vote.
- Actual mobile CSS viewport approximately **389 × 845**, no horizontal document overflow. Browser zoom required adjusting the viewport override; dimensions were read from the DOM. Desktop was also inspected. No app warnings/errors were observed.

The [local mobile answer screenshot](local-mobile-answer.png) contains only the public test question and answer. Other screenshots are stored locally under `.local/rigor-pass/`; no real user's notes or credentials are included. This is loopback browser proof, **not a remotely reachable demo**.

## Deterministic checks

100 Python tests passed after integration, including provider model mismatch, truncation, redirects, private payload and cross-origin rejection, persisted daily quotas, busy service, actual-case citation resolution and separate-check withholding. Node WebCrypto tests passed. Docker image build and offline Gate 0 check passed; hosted Compose syntax was validated with synthetic non-secret settings. No authenticated hosted API call, public HTTPS certificate, remote browser or physical phone has been verified.

## Privacy and model boundaries

Only `{question: ...}` from the public question form is accepted. Choices, notes, history and salary fields are rejected. The UI warns not to put sensitive information in a question. Runtime questions/answers are not persisted; an explicit evaluation callback records only these synthetic/public development trials. Saved choices and notes remain in the existing browser vault. Same-model checking does not grant human-reviewed publication status. Citations resolve from the authenticated case, never generated quotation text or model URLs.
