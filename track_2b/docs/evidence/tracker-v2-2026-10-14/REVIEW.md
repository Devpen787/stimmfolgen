# Tracker v2 release evidence — 14 October 2026

Implemented the user-selected option 3 for desktop/mobile on PR #4 after the bounded AHV Gate passed. My votes, Upcoming votes and local Search lead to a progressively disclosed Explore journey. Tracking never infers a political choice. Choices and notes are private browser state, optionally encrypted on this device; Apertus performs public analysis, not encryption.

## Source and analysis boundary

Five selected proposals, not a complete vote registry. Only AHV has reviewed recorded Apertus analysis; other entries explicitly say it is unavailable. No fresh model completion was performed for this UI change or a web click. The original reviewed P01–P05 wording, immutable spans, Gate certificate, all failed traces and original packet remain unchanged. P03 remains reviewed reference context, not a final-trial extraction.

The official November ballot list and October AHV implementation page were checked on 14 October through the successful official web-page reader. Direct HTTP snapshot retrieval returned 403. The committed excerpts are therefore explicitly MANUAL_PRIMARY_WEB_EXCERPT with excerpt hashes and null original HTML hash, not authenticated raw HTML. Updates and relationships never enter the historical pre-vote inference frame.

Primary references: https://www.admin.ch/de/volksabstimmung-vom-29-november-2026 and https://www.bsv.admin.ch/de/umsetzung-13-ahv-rente. No-recorded-update means no verified item in this snapshot, not proof nothing happened.

## Verification

- 86 Python tests pass: original evidence/semantic/HTTP controls plus catalogue/date/source boundary tests.
- Actual native WebCrypto tests pass: ciphertext-only persistence, random nonces, wrong password, tampering, reload/lock, concurrent saves, backup recovery and lock-race cancellation. CI runs these tests with Node 22.
- Actual local browser: find/track AHV; query retained after tracking; default choice Not recorded; source/actor/date dialog; keyboard tab switching; Me/Others/Switzerland; separate dated update; related financing navigation; unavailable analysis and empty-update states; encrypted download, local recovery, private save, wrong password rejection and reload locking. Timed inactivity produced the five-minute lock message during QA.
- Synthetic recovery/save audit: 33 public GET requests and zero POST requests. No private note, choice, search query or passphrase sent. Only aggregate evidence is committed.
- No browser console errors/warnings in the tested mobile journey. Desktop and mobile show no horizontal page overflow. Mobile tab strip scrolls intentionally; bottom navigation remains available with content padding.
- Offline Docker Gate check: PASS_BOUNDED_AHV, seven previously recorded control trials/eight actual completions authenticated. Five deliberate mutations fail closed (source bytes, missing/rejected approval, premature date, substituted checkpoint).

Screenshots depict synthetic tracking on isolated QA origins, never real user choices or notes: [mobile](mobile-final.png), [Explore](mobile-explore.png), [desktop](desktop-final.png), [selected design comparison](option3-comparison.png). See root design-qa.md. The old report is preserved byte-for-byte in historical-report-v1 for its historical manifest; the old demo remains unchanged and describes the previous interface.

Limits: no independent security audit, user comprehension study, exhaustive accessibility audit, second reviewed case, live per-click inference, cross-device sync or deployed public service. Encryption protects stored ciphertext, not an unlocked/compromised device. A lost passphrase has no recovery service. Fresh local cold-clone and remote check results are recorded separately when complete.

## Cold delivery result

Clean committed checkout 6bb0368 launched using root make run, with no model endpoint or local working files. Real HTTP journey, offline Gate replay and all five deliberate failures passed. Exact image/commit and certificate: cold-clone.json. Current file hashes: artifact-hashes.json. This is publication replay, not a fresh inference run.
