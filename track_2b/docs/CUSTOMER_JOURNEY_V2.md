# StimmFolgen customer journey v2

14 October 2026. Implemented option 3 journey, based on the user's clarification and the current running-app audit. The responsive private tracker was implemented after the bounded AHV Gate passed; no additional model capability is claimed.

## Purpose

Help someone understand past and upcoming Swiss votes, the proposal and its analysis, and possible or documented effects on themselves, other people and Switzerland. Give the reader the information and uncertainty needed to form their own view. Do not recommend a vote.

User clarification: “Understand past votes, see votes, see analysis of votes and affects of vote in general, for the direct user and for others.”

## Latest user brief: a very simple private vote tracker

The user clarified the primary product: track votes, browse upcoming votes and search; open My votes to revisit what they voted on, its meaning with dated sources, then Explore my vote for updates (or an explicit no-update state), related votes and perspectives.

Primary navigation: **My votes / Upcoming votes / Search**. Tracking is distinct from optionally recording a personal vote choice. The app never infers a choice from a saved or read case. Private tracking, notes and choices require an implemented and tested on-device storage boundary; Apertus performs public-source analysis, not encryption. The selected option 3 implements this workflow with optional encrypted persistence and encrypted backup recovery.

Core path: find vote -> track it -> open My votes -> understand the proposal -> explore me/others/Switzerland -> view dated updates or no recorded updates -> explore a related vote -> keep personal notes privately.

“None” means no verified updates in the app's current source snapshot, not proof that nothing happened. Each update carries a source publication date when known plus checked-at date; related proposals have a stated, sourced relationship. Original historical analysis remains separately dated and immutable.

## Three entry needs

- Preparing: “There is a vote coming up. What would it change, and who could be affected?”
- Looking back: “What was this past vote about, what was decided, and what happened afterwards?”
- Understanding a connection: “Why does this matter for me or someone else, and how does it relate to another vote?”

The first screen is a vote explorer, not the inside of a preselected case. It offers clear past/upcoming categories, plain-language titles, date/topic search and explicit analysis availability. Catalogued, analysed, reviewed, and post-vote evidence available are different states. A plausible ballot card must never imply that its model analysis exists.

## End-to-end journey

| Step | Reader question | Experience | Completion signal | Current support |
| --- | --- | --- | --- | --- |
| 1. Discover | Which vote do I want to understand? | Browse past/upcoming votes; search date/topic; open a vote | The reader has chosen a specific proposal and date | Implemented: My votes, Upcoming votes and local search; five selected proposals |
| 2. Understand | What was/is being proposed? | Short overview with the change, scope and status; progressively reveal detail | The reader can describe the proposal in their own words | Implemented: two central statements with other accepted statements progressively disclosed |
| 3. Explore effects | What could it mean for me, for others, for Switzerland? | Explicit perspective selector; neutral factual situations; effect, condition, horizon and unknown | The reader knows which effects apply conditionally and which cannot be established | Implemented: Me, Others and Switzerland, with explicit factual situations |
| 4. Examine analysis | Why might this happen, and who says so? | Show proposed mechanism, assumptions, competing attributed arguments and limits; tap to inspect source | The reader can distinguish a provision, prediction and disagreement | Source/actor checks work for the bounded AHV case; current analysis page mostly repeats statements |
| 5. Look back or connect | What was decided, what later happened, or what changed from another vote? | Historical result and implementation timeline, separately labelled documented observations; related vote comparison where independently sourced | Expectations are not mistaken for later outcomes or proven causation | Implemented: separately dated official AHV update and sourced financing relationship; no causal inference |
| 6. Keep understanding | What have I learned and what do I still need to know? | Optional private brief with selected case/perspective, remaining questions, sources and personal notes | The reader keeps a useful reference without sharing personal deliberation | Implemented: visit-only default, optional AES-GCM encrypted local vault and encrypted backups |

Effects for “me” depend on facts, not political profiling. For “others,” select a factual situation such as an AHV old-age pension recipient rather than inferring family circumstances. National effects are independently sourced macro claims, not a sum of invented personal predictions. Unsupported effects should say what is missing.

## Historical integrity

A past-vote page separates three questions: what was proposed and predicted before the vote; what the official result was; and what later sources document about implementation or outcomes. A later outcome does not alone prove that the vote caused it. These views require separate source snapshots and knowledge frames.

The cleared AHV Gate 0 covers the original pre-vote booklet interpretation only. It does not certify the official result, current pension law, observed later impacts, another ballot or retrospective causal analysis. Broader views need appropriate official sources and independent checks before being published.

## Apertus's visible role

Use a visible, restrained “Prepared with Apertus v1.5” identifier on an analysed case, plus a short explanation of what it did. Lead with user questions, not a generic AI marketing promise.

Verified current role: local Apertus selected relevant original-booklet passages and typed candidate values, extracted a source actor, and separately parsed the requested actor. The application resolves verbatim quotations, compares the actors, applies independent bounded checks and refusal policy. Human review accepted the five published statement wordings. P03 is reviewed reference context, not a final-trial model extraction.

Publication should make this chain inspectable: original evidence -> Apertus candidates -> independent checks -> reviewed explanation. Current web clicks read the recorded reviewed case; do not use a typing animation, “thinking” status or “live AI answer” label to disguise this. New causal explanations, free-form chat, automatic real personal-impact predictions or every-ballot analysis are not verified capabilities.

## What changes in the experience

- Make the entry point “My votes,” with the vote and its status visible before analysis.
- Give each view one main question and one obvious next action.
- Present the short answer first. Keep the approved full wording and its source readily accessible. New policy paraphrases need meaning review; shortening labels must not rewrite the substantive claim.
- Use an impact view that makes “me / others / Switzerland” explicit and shows applicability, uncertainty and time horizon.
- Show evidence and attribution beside the question they support instead of repeating all five claims as another page of paragraphs.
- Keep the historical frame visible in plain language. Put technical hashes and diagnostic detail inside source detail, not the main reading path.
- Treat the existing design as implementation context, not a selected visual target for this redesign. Choose the new visual direction around this journey before rebuilding.

## Success criteria to test

A first-time reader can find a vote, identify the proposed change, select a perspective, distinguish a forecast from a defined provision, identify who made an argument, inspect an original passage and state an unresolved question. Measure comprehension and completion with an actual reader; do not call it “100x better” or equate a passing code test with understanding.

The backend Gate and raw evidence remain unchanged during this journey review. Browser audit evidence and current gaps are recorded in the local UX audit packet. The user selected option 3 before implementation. Browser and privacy evidence is recorded in the tracker v2 release packet.
