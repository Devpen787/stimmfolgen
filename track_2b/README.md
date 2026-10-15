# Track 2 B: Own Project

Bring your own idea and build a working Apertus prototype that tackles a problem you care about — any domain, any use case. The project must be new, started within the hackathon period.

Submissions must use the Apertus model family.
For Track 2 this means that submitted solutions must be built with Apertus. Other open-weights models can be used to support development, e.g. as automatic judges during evaluation. Their role must be clearly described in the submission report.

💬 In case you have questions, join the conversation on [Discord](https://discord.gg/hack-apertus) or send an email to “hello@hackapertus.ch”

---

## 🔧 Resources & Tools

Check our resources & tools page for detailed information:
https://hackapertus.notion.site/resources-tools

| Models           | URL                                      |
|------------------|------------------------------------------|
| Apertus v1.5 8B  | [huggingface.co/swiss-ai/Apertus-v1.5-8B](https://huggingface.co/swiss-ai/Apertus-v1.5-8B)  |
| Apertus v1.5 70B | [huggingface.co/swiss-ai/Apertus-v1.5-70B](https://huggingface.co/swiss-ai/Apertus-v1.5-70B) |


## Target architecture (mandatory)

Whatever you build in Track 2B must be deployable in one of these three architectures:

- **a) On-premise** — on the organisation's own infrastructure, under its own administration.
- **b) Air-gapped** — with no external network connection at runtime.
- **c) Sovereign Swiss cloud** — on a cloud platform operated in Switzerland, under Swiss jurisdiction, with Swiss data residency.

---

## Data

The `data/` directory must not exceed 100 MB.

---

## 📦 Submission Requirements & Deliverables

❗️ Submissions are not handled on Devpost but via this URL only:
http://hackapertus.ch/online-hack/submissions

The submission must: 
1. follow the template repo and include all prerequisite files and definitions
2. follow the specified input/output formats
3. run in a Docker container, launched with `make run` from the root of the project
4. run end-to-end when judges try to run it

### Git repo (URL)
- Create your repo from this template (**Use this template**) and work in the `track_2b/` challenge directory. Delete the other track challenge directories.
- Keep `track_2b/` as it is: don't rename it or move its files.
- Set the repo to PUBLIC (Settings --> Collaborators --> Manage Visibility)
- Submit the URL of YOUR Git repo.

### Technical Report (pdf)
- Update [technical_report.md](technical_report.md) in this repository with all the details for your submission.
- Upload a pdf of your technical report to this directory, named as `TeamName_Report.pdf`.
- Format: pdf, max. 6 pages w/o references
- Submit the pdf of the technical report.

### Demo video (URL)
- Max. 2 min demo video of your prototype

### Dataset (URL) - optional, depending on your project
Submitted datasets must comply with our guidelines for responsibly sourced datasets.

- Create a user account on Hugging Face
- Clone our dataset template on Hugging Face: https://huggingface.co/datasets/HackApertus/online_hack_template
- Complete the dataset card with all required information
- Upload your dataset. It should consist of the following components:
    - evaluation dataset (i.e. individual test cases)
    - model response dataset (i.e. the model response to each test case)
    - metadata file (i.e. additional information about each test case; where relevant, this file must contain instance-level licensing information) 
- Make sure your dataset access control is set to PUBLIC
- Provide the URL of _your_ data set


---

## ⚖️ Judging Criteria

1. Purposeful use of AI
2. Technical rigour
3. Value, cost & scalability
4. Sovereign deployability
5. Implementation feasibility

Judges use a Scale 0–5 per dimension.

---

## Support

**Licensing requirements**
Please check our Terms & Conditions (6. What you build is open source):
https://hackapertus.ch/terms-and-conditions

## FAQ
💡 https://hackapertus.ch/faq

## Contact
💬 In case you have questions, join the conversation on Discord or send an email to “hello@hackapertus.ch”

## StimmFolgen: private vote tracker

Run `make run` from the repository root (or this directory), then open http://127.0.0.1:8770. See [judge instructions](docs/JUDGE_RUN.md).

**Gate 0 PASS for the bounded AHV case.** P01-P05 have the user's recorded statement approval. A fresh local Apertus v1.5 suite passes seven control trials using eight real completions, with authenticated immutable spans and an admitted historical public frame. Old failures and the original pending packet remain unchanged. [Release evidence](docs/evidence/APP_RELEASE_2026-10-14.md) and [ADR 0005](docs/adr/0005-bounded-gate-clearance-and-reviewed-case.md) disclose exactly what this clears.

The frontend was built after the backend Gate check passed. The overview serves **reviewed recorded results**; configured installations also provide a separate Ask Apertus form for live question-to-source matching against reviewed wording. The responsive desktop/mobile journey offers My votes, Upcoming votes and Search. Explore shows dated sources, official updates, related votes and Me/Others/Switzerland perspectives. Tracking does not infer a Yes/No choice. Visit-only tracking is the default; an optional passphrase vault encrypts saved choices and notes on this device, with encrypted backup/recovery. P03 is reviewed reference context rather than a final-trial extraction. There is no account or cross-device sync, no independent security audit and no broader policy accuracy claim. The catalogue contains six selected proposals; reviewed Apertus analysis currently covers AHV only. [Tracker evidence](docs/evidence/tracker-v2-2026-10-14/REVIEW.md) documents the checks.

Apertus inference is fully local and separate from Docker-contained publication: pinned text-only community MLX conversion of `swiss-ai/Apertus-v1.5-8B` on the user's Mac. These original Gate runs used no inference API. The later public demo uses finite Public AI starter credit, with no owner/visitor payment. Cloud CI authenticates evidence and tests delivery; it does not invoke the Mac's model. [Runtime contract](docs/APP_CONTRACT.md) and [technical report](technical_report.md) describe this boundary.

## Live hosted and optional local modes - 15 October

The [public demo](https://stimmfolgen-demo.stimmfolgen-hosted.workers.dev/) now makes actual Public AI Apertus v1.5 8B requests through a Cloudflare Worker. No visitor download or payment is required. It is a finite starter-credit demo, not permanent free compute or Swiss-sovereign hosting. The owner's Mac is not exposed. `make local-download` then `make local-run` provides optional loopback-only Apple Silicon inference with pinned weights and no API key. Default `make run` remains reviewed Docker publication. [Current proof and limitations](docs/evidence/hosted-local-2026-10-15/REVIEW.md) supersede older no-live descriptions above.


Product reliability continuation: live Apertus now selects reviewed source IDs; a separate relevance call checks the selection and the server displays accepted wording unchanged. The public journey was retested from fresh desktop and phone-sized browser origins, including sources, updates, perspectives and encrypted note reload/unlock. Matching remains bounded and fallible, especially locally; no general accuracy or physical-device claim is made. See [the exact results and preserved failures](docs/evidence/product-reliability-2026-10-15/REVIEW.md). Video files were not changed.

Hosted matching v9 interprets questions into neutral English source queries, ranks immutable reviewed statements and checks candidates against the original question. It does not generate public factual prose. Actual final testing: original AHV 13/13; combined development sets 34/38 exact matches, with four no-answer failures retained. Attribution recovery is verified on desktop and responsive phone, including source dates and private note recovery. Local 4-bit matching remains experimental. See [current matching evidence and limitations](docs/evidence/matching-continuation-2026-10-15/REVIEW.md) and [ADR 0008](docs/adr/0008-query-retrieval-and-original-question-check.md). Video unchanged.

Matching continuation (15 October): hosted scoped-query v10 passed 38/38 known AHV development questions, including useful uncertainty corrections and explicit other-proposal boundaries. This is bounded development evidence, not general accuracy or local MLX parity. [Latest proof and retained failures](docs/evidence/matching-v10-2026-10-15/REVIEW.md); [product and Track 2B limits](docs/evidence/matching-v10-2026-10-15/PRODUCT_ASSESSMENT.md).
