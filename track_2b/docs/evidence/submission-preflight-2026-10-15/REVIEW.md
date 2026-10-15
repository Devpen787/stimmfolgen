# Submission preflight — 15 October 2026

**Technical package prepared; no submission or main merge performed.** Official requirements were checked against the live Track 2B form, current upstream template and Devpost deadline. See SUBMISSION_READINESS.md and submission-draft.md. No participant personal fields, terms checkbox or Submit action were sent.

## Review findings and changes

1. Public default main lacks the working Makefile/app, while implementation is in a three-PR chain. PR #4 is prepared for direct review against main; final default-branch delivery remains an owner decision. The stale root README was replaced with actual setup, model use, current report/video and limits.
2. The old demo described obsolete ephemeral-only notes. The current 98.052-second walkthrough uses actual captures of search, track, original source, uncertainty, dated update, encrypted synthetic note, lock and Apertus disclosure. It has H.264/AAC, 1280x720, local synthetic voice, captions and reproducible script. It is a narrated sequence of captures, not continuous recording or fresh model generation. All private content is synthetic on isolated port 8777.
3. Code review found that a sufficiently large vault could be saved above the import/unlock size limit, producing a backup that could not be reopened. Persist now enforces its own envelope/import limits before writing. An actual WebCrypto regression checks rejected oversize writes preserve the previous backup and remain unlockable. No user data was used.
4. Report pagination briefly produced a one-word sixth page. Text was tightened and the final report is five complete pages. Original historical reports/manifests are preserved; current artifacts have a new hash record.
5. Rights review: the immutable source packet contains eight full-page PNGs, not only small quotations. No blanket open licence is established for every component. THIRD_PARTY_NOTICES.md records the actual source notice, possible official-text exclusion and the unresolved rights warranty. Original evidence is retained rather than silently removed or relicensed. PyMuPDF AGPL and icon MIT terms are disclosed.

## Verification performed

- 86 Python source, semantic, model identity, approval, temporal, routing and catalogue controls pass.
- Actual native WebCrypto tests pass, including wrong passwords/tampering, nonce freshness, concurrent writes, lock races, backup recovery and the new oversize preservation test.
- Synthetic blueprint validator passes, separately labelled as not real model/semantic proof.
- Actual reviewed-case HTTP happy path, unknown personal cost, unsupported question and private-extra-field rejection pass.
- Browser desktop loop passed against real case: search -> track -> My votes -> meaning/source dates -> working-age perspective unknown -> update -> related vote -> encrypt synthetic note -> lock. Browser console has no errors/warnings. Earlier mobile QA remains applicable to unchanged layout; no new mobile claim from this run.
- Video streams/duration verified with ffprobe; representative frames inspected. Transcript matches reviewed case limits; no actual personal choice or private user note is shown. Caption timings are approximate chunks, not forced-aligned speech transcription.
- PDF rendered and inspected; max six-page requirement passes at five pages.
- Targeted secret scan of tracked files found no private-key blocks, GitHub token shapes or AWS access-key shapes. Local secrets/model paths are excluded. This is a targeted check, not exhaustive security certification.

No new Apertus inference is performed for this release preparation; prior real eight-completion run remains authenticated and clearly recorded. No failed trace, approval or original source ledger was modified. This is one AHV development case, not general policy accuracy. No comprehensive accessibility, comprehension or independent security audit.

Final Docker cold-clone replay/negative-control results and remote CI are appended as they complete. Remaining nontechnical gates: accurate participant/team/eligibility fields, approved accessible video URL, reviewed main integration and source/terms clearance.

## Cold clone result

Committed app 1fd283d: a new local Git clone built and launched with root make run, actual HTTP journey passed, offline Gate replay authenticated PASS_BOUNDED_AHV and all five deliberate mutations blocked. No model endpoint or private local files were needed for publication replay. Exact certificate and image: cold-clone.json. This does not prove a bare default-main checkout before PR integration. A reload/unlock browser check restored the synthetic note using the current vault fix.
