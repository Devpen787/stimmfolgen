# StimmFolgen

**Follow a Swiss vote, understand its dated evidence, and keep your own reflections private.**

Hack Apertus 2026 · Track 2B · On-premise prototype. My votes, Upcoming votes and Search lead to a short explanation, original sources, later official updates, related votes and perspectives for Me, Others and Switzerland. No voting recommendation or inferred Yes/No choice.

![Actual desktop tracker — synthetic tracked AHV example](track_2b/docs/evidence/tracker-v2-2026-10-14/desktop-final.png)

[Actual mobile view](track_2b/docs/evidence/tracker-v2-2026-10-14/mobile-final.png). Screenshots show synthetic tracking, not the owner’s political choices.

## Run it

With Docker and make installed, from a clean checkout:

```sh
make run
```

Open http://127.0.0.1:8770. Use `make run PORT=8772` if that port is occupied. The build fetches dependencies and the hash-pinned official booklet; a mismatch fails closed. No credentials, model weights or paid API are needed for the reviewed publication journey. The container runs as a non-root user with a read-only filesystem and loopback-only host binding.

## A 90-second judge journey

1. Search AHV and track **13th AHV pension**. Return to My votes, then Explore my vote.
2. Read What it means; open Source and dates for original passages, actor, page and historical frame.
3. Open Perspectives. A working-age person gets an honest unknown personal charge, not a fabricated CHF calculation.
4. Inspect separately dated official updates and the related financing proposal.
5. Add a **synthetic** private note. Keep it only for this visit or create an optional encrypted local vault. Reload locks saved data; encrypted backup/recovery stays local.

## Where Apertus is used

Actual local Apertus v1.5 8B inference selected immutable source spans, extracted candidate values and identified attribution. Independent controls and five accepted source statements produced the published AHV explanation. Seven bounded trials passed using eight real model completions. Earlier failures are retained.

The web app serves **reviewed recorded results**; clicking Explore does not perform new inference. P03 is reviewed reference context, not an extraction from the final trial. The other four selected proposals have official references but no reviewed Apertus explanation. Catalogue search, update metadata and encryption are application functions.

```text
Official booklet -> immutable spans -> local Apertus candidates
                 -> independent checks + human review -> reviewed public case
Browser -> Docker publication API -> explanation, citations and updates
Browser-only choices/notes -> optional encrypted vault and encrypted backup
```

Native inference uses the pinned community text-only MLX 4-bit conversion of swiss-ai/Apertus-v1.5-8B on Apple Silicon. Linux Docker runs publication/evidence replay, not Mac GPU inference. [Judge instructions](track_2b/docs/JUDGE_RUN.md) provide the separate native reproduction commands.

## Verify and review

```sh
make check
python -m unittest discover -s track_2b/tests -p 'test*.py'
node track_2b/tests/test_private_vault.mjs
```

Python tests require PyMuPDF 1.28.2; vault tests require Node 22+. Docker `make check` uses its pinned environment. The synthetic blueprint validator is separate from real-model evidence.

- [Current technical report](track_2b/StimmFolgen_Report.pdf) · [editable source](track_2b/technical_report.md)
- [Current 98-second demo](track_2b/demo/StimmFolgen_Tracker_Demo.mp4) · [transcript](track_2b/demo/TRACKER_DEMO.md) · [captions](track_2b/demo/StimmFolgen_Tracker_Demo.srt)
- [Submission preparation and remaining owner actions](track_2b/docs/SUBMISSION_READINESS.md)
- [Exact judge run](track_2b/docs/JUDGE_RUN.md) · [API contract](track_2b/docs/APP_CONTRACT.md)
- [Real Apertus release evidence](track_2b/docs/evidence/APP_RELEASE_2026-10-14.md) · [tracker evidence](track_2b/docs/evidence/tracker-v2-2026-10-14/REVIEW.md)
- [Privacy limits](track_2b/docs/PRIVATE_TRACKER_THREAT_MODEL.md) · [third-party rights review](THIRD_PARTY_NOTICES.md)
- [Official Track 2B instructions](track_2b/README.md) · [historical design blueprint](track_2b/docs/blueprint-v0.1/README.md)

## Scope and limits

One reviewed historical AHV development case; five selected proposals, not a complete registry. No second-case or unseen-ballot accuracy proof, current-law personal calculator, comprehension study, exhaustive accessibility audit, account/sync or independent security audit. Encryption protects stored ciphertext, not an unlocked/compromised device. A lost passphrase cannot be recovered. External official-source visits remain visible to their publishers.

The required submission is through the organisers' website, not Devpost. A prepared video/PDF or passing CI does not mean the project has been submitted. The older reader demo and evidence remain historical artifacts.
