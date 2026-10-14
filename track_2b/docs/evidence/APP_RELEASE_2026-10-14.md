# AHV Gate clearance and working prototype - 14 October 2026

**PASS_BOUNDED_AHV.** The user explicitly accepted P03, P04 and P05 after previously accepting P01/P02 with revised wording, and authorised backend/Gate completion followed by frontend construction. Their three new bound records preserve the exact authorisation. No acceptance of T01-T07 raw traces is invented.

The backend certificate was obtained before frontend files were created. [ADR 0005](../adr/0005-bounded-gate-clearance-and-reviewed-case.md) describes the release boundary: five human-approved statements plus independently rechecked engineering controls, actual pinned local model inference, authenticated source and verified public temporal admission. The prepared review packet and all earlier failed traces are unchanged. The new run is deliberately still marked unreviewed at raw-generation level; the separate release certificate controls publication.

## New real inference

The same existing local M3 Pro/18 GiB Mac and pinned v1.5 text-only 4-bit MLX weights were used, without a paid API. Exact revision, backing checkpoint, weights/tokenizer/config hashes, requests and responses are in [the release run](gate0-release-2026-10-14/run-release-v6/). A fresh official PDF download matches the pinned source. The availability witness admits 2 March 2024 23:59:59 CET as the public frame; the printed 29 November 2023 content cutoff stays separate. Each actual request now contains the public-frame restriction.

| Trial | Result | Observed seconds |
| --- | --- | --- |
| Direct annual supplement / 12 to 13 summary payments | PASS | 31.763 |
| Approximate CHF 4.1bn introduction cost, projection | PASS | 8.487 |
| Unresolved definite employee financing | PASS | 11.218 |
| Fabricated CHF 100 quotation | PASS | 6.898 |
| False committee attribution of Council/Parliament forecast | PASS | 19.394 (two calls) |
| Definite salary-based CHF demand | PASS | 13.140 |
| Later financing leaked into pre-vote frame | PASS | 10.904 |
| Three-response combined happy path | PASS | Derived aggregate, not another completion |

Eight actual completions, seven bounded trials. No response was repaired. Actor refusal is application comparison of two independently extracted actors. The evaluation-only oracle is separate from generation; reviewed published statements are not general ground truth. P03 remains reviewed reference context, visibly disclosed in the UI.

## Implemented journey and checks

Python backend publishes the reviewed case only after authenticating its source, prepared packet, trace manifest, pinned recorded identity, semantic controls, temporal frame and five bound approvals. Plain HTML/CSS/JavaScript preserves the approved design and provides overview, recipient/working-person/national situations, source dialog and original PDF, attribution, personal-cost abstention and a private ephemeral brief.

- 83 deterministic tests PASS. The new HTTP tests use explicit routing fixtures, never labelled model evidence. Approval/identity negative tests reject missing/rejected/stale decisions and checkpoint or weight substitution. Existing independent semantic mutant tests remain.
- Design-contract validator PASS on its original synthetic fixture, with its non-claims retained.
- Real Docker HTTP smoke PASS: five approved cards, actual PDF, recorded-mode fields, unknown personal CHF amount, unsupported-question abstention and private-field rejection.
- Offline Docker certificate check PASS with `--network none`, non-root user and read-only filesystem. No LLM endpoint needed for this reviewed publication mode.
- Browser smoke: all four sections, source actor and page/hash display, personal-cost answer, keyboard Escape dismissal, synthetic note export and empty note after reload. Browser console warn/error list was empty. Native browser zoom makes requested viewport differ from CSS dimensions; measured widths were 1280x898 and 388x840, with no horizontal document overflow.
- Approved concept comparison preserves colours, typography, layout, four sections and source-first interaction. Content changed to approved statements and truthful evidence/mode labels; no arbitrary visual score or human comprehension claim.
- [Actual browser captures](app-release-2026-10-14/) show overview, benefit, financing abstention, attribution, source and brief. Only a clearly synthetic QA note was entered/exported; no private user note is committed.

## Delivery artifacts and limits

[Judge launch/re-inference instructions](../JUDGE_RUN.md), [runtime contract](../APP_CONTRACT.md), [technical report](../../technical_report.md), [five-page report PDF](../../StimmFolgen_Report.pdf), and [102-second narrated walkthrough](../../demo/StimmFolgen_Demo.mp4). The video is assembled from actual browser captures with local synthetic narration; it is not a continuous screen recording or fresh click-time inference.

Cold clone/run results are added below after testing the committed implementation. No hosted deployment, external video upload, merge or submission is claimed. One AHV case is cleared; second-case/holdout/language validation and production encrypted storage remain unverified. Government source availability is not an open reuse licence; no full source PDF or model weights are committed.

Primary links: [official booklet](https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf), [exact historical archive](https://web.archive.org/web/20240111121117id_/https://www.admin.ch/dam/gov/de/Dokumentation/Abstimmungen/Marz2024/marzo_DE.pdf.download.pdf/marzo_DE.pdf), [conversion model card](https://huggingface.co/tokimoa/apertus-v1.5-8b-mlx-4bit), [declared official upstream](https://huggingface.co/swiss-ai/Apertus-v1.5-8B), [government conditions of use](https://www.admin.ch/fr/conditions-utilisation).
