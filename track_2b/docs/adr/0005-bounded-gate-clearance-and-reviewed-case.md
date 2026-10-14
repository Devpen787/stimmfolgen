# ADR 0005 — Bounded Gate 0 clearance and a reviewed recorded case

Date: 14 October 2026. Status: implemented for the AHV development case.

The user accepted P01/P02 with revised wording and explicitly accepted P03/P04/P05, authorising backend completion, Gate 0 checks and frontend construction afterwards. Five immutable-packet-bound decision records preserve those authorisations. This is human statement review, not human approval of the seven raw trial outcomes.

Gate 0 combines those five approvals with authenticated booklet/span provenance, verified pre-vote availability, a public case frame of 2 March 2024 23:59:59 CET, actual pinned local Apertus v1.5 inference, and independently rechecked mechanical and bounded semantic controls. A fresh release run performs eight real completions and passes seven trials. The certificate was obtained by running the backend release check before creating frontend files. Older failures and the pending fields in the prepared review packet remain unchanged.

`release_guard.py` re-extracts and authenticates the source catalogue, rechecks the prepared packet and release-trace manifest, enforces five bound approvals, and independently evaluates final candidates. A missing approval, changed source/model/frame or failing control blocks backend startup. The frontend therefore cannot quietly replace unavailable evidence with generated prose.

The frontend and Docker application serve **REVIEWED_RECORDED_CASE**. Their answers are deterministic publication of reviewed wording; web clicks do not run a fresh LLM. Apertus supplied extraction and intent candidates in the genuine recorded pipeline. The application supplies retrieval, refusal policy and comparison of independently extracted actors. P03 is explicitly reviewed reference context rather than a final-trial model extraction. No expected actor or gold span ID enters model generation or actor comparison.

The ephemeral understanding brief lives only in tab memory and exports plaintext on explicit action. There is no production encrypted vault, account, analytics or cross-device storage. The API accepts only a topic enum-style request and rejects additional notes/salary fields.

This clears the **bounded AHV Gate 0** and authorises its frontend, not general policy accuracy, an unseen ballot, language parity, the second referendum, encrypted storage, BF16 conversion equivalence or overall submission readiness. The historical design blueprint remains a larger target; this smaller runtime view has an explicit contract and does not pretend to implement the full vault/public-case schema.
