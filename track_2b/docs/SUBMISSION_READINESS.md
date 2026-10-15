# Submission preparation — 15 October 2026

Status: **TECHNICAL PACKAGE PREPARED; NOT SUBMITTED.** Owner details, public video URL, reviewed main integration and rights/terms confirmation remain. Recheck the actual form immediately before submission.

## Official requirements checked live

Deadline: **16 October 2026, 12:00 CEST (Zurich noon), no extensions**. Aim to finish submission by 11:00 to leave a buffer. Submission endpoint: https://hackapertus.ch/online-hack/submissions — not Devpost. One submission per project.

Track 2B form observed 15 October: first name, last name, Devpost email, GitHub username, team name, team members, project name, Swiss student team status, model, report PDF, repository URL and video URL are required. Hugging Face username/dataset URL and participant message are optional. A Terms acceptance checkbox precedes Submit. No form values or personal information have been submitted.

References: [Devpost overview](https://hackapertus.devpost.com/), [organiser form](https://hackapertus.ch/online-hack/submissions), [current template requirements](https://github.com/HackApertus/project-template/blob/main/track_2b/README.md), [report template](https://github.com/HackApertus/project-template/blob/main/track_2b/technical_report.md), [terms](https://hackapertus.ch/terms-and-conditions).

| Requirement | Current state | Final action |
| --- | --- | --- |
| New Apertus project in Track 2B | Public template-derived repo, other track folders removed | Owner confirms authorship/event eligibility |
| Model | Actual local v1.5 8B, community MLX 4-bit conversion disclosed | Choose 8B v1.5 in form |
| Required target architecture | On-premise, local MLX ingestion + Docker reviewed publication | Do not claim fresh inference inside Linux Docker |
| Root Docker make run | Clean release checkout tested; source hash authenticated | Main must receive reviewed app before submitting bare repo URL |
| Public repository | https://github.com/Devpen787/stimmfolgen | Review and integrate PR #4 into main |
| Report, <=6 pages | StimmFolgen_Report.pdf, five pages | Confirm team naming/credit and final PDF |
| Video, <=2 min | StimmFolgen_Tracker_Demo.mp4, about 98 seconds | Review narration, upload approved video, test public-view URL |
| data/ <=100 MB | Only small fixtures/manifests; no model weights or raw PDF | Automated preflight checks size |
| Dataset URL | Optional, no separate dataset submission prepared | Leave blank; do not call third-party source corpus open data |
| Terms and third-party material | Apache code, MIT icons; source licensing review documented | Owner must resolve source page/excerpt rights and accept actual terms |
| Personal fields | Not collected in public files | Owner supplies/enters accurate details |

## Ordered work plan

1. Freeze the bounded AHV scope. Preserve failed traces, approved meanings and the historical source frame. No speculative feature expansion.
2. Replace stale root documentation, update status and report, and prepare the current tracker video/captions from genuine browser captures.
3. Review source/model/private-data boundaries, run unit/crypto/blueprint checks, clean Docker launch, real HTTP path, offline Gate replay and all fail-closed mutations. Verify desktop/mobile browser flow and media/PDF rendering.
4. Commit/push to PR #4; retarget to main for review rather than leaving a three-PR dependency chain as the judges' default checkout. Do not merge without review.
5. Owner reviews the exact package, confirms rights/team/eligibility, selects a video host and approves final public-facing material. Publishing a video and accepting the organiser's terms are separate final actions.
6. After reviewed main integration, repeat a clone of the bare repository/default branch, verify the video URL without login, attach the correct PDF, complete required identity fields, then perform one authorised submission. Save the confirmation privately.

## Product and official judging fit

Primary category: AI x Data / Research; secondary: privacy-preserving civic information. Anchor user: a Swiss voter following a proposal over time. Primitive: immutable-source candidate extraction with reviewed publication and explicit uncertainty. Proof objects: real Apertus traces, span ledger, bound review decisions/Gate certificate and local encrypted envelope. Verifiers: release guard, semantic checks, failure mutations and crypto tests. Reusable surface: native ingestion CLI, public API and contracts. Live state change: track a vote and save/lock a synthetic note.

| Judging dimension | Demonstrable evidence | Limit to disclose |
| --- | --- | --- |
| Purposeful AI use | Local Apertus extracts source IDs/values/actors before checked publication | User-facing clicks replay reviewed results |
| Technical rigour | Preserved failures, independent semantic controls, temporal admission, cold start | One development case, not held-out accuracy |
| Value, cost, scalability | Search/track/explore/return flow, local inference, cached publication | No measured user benefit or scaling load test; human review remains per case |
| Sovereign deployability | Native on-premise MLX and loopback Docker publication | Build needs internet; native GPU inference separate from Linux Docker |
| Implementation feasibility | Working responsive flow, CI, tests, report and video | Generalisation, languages and production security remain untested |

Winner-grade checklist: named primitive, proof object, verifier, bounded system, reusable CLI/API, real private state change, real sponsor/model ingestion and sub-two-minute demo are present. Default-main delivery and rights confirmation are outstanding. This is a readiness review, not a claim of winning competitiveness.

## Owner actions only

Confirm team/member names, Devpost email, Swiss-student eligibility and project credit. Choose/approve narration and a video host. Review the ready PR and approve main integration. Read actual organiser terms (including output licences and third-party warranties); this agent has not accepted them. Complete source-material rights clearance described in THIRD_PARTY_NOTICES.md. The report and video can be fully prepared before any final submission permission is requested.
