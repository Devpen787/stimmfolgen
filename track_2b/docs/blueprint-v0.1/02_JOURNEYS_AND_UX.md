# 02 — User Journeys, Information Architecture and UX

## Jobs to be done
1. **First-time voter**: "I need to know what this changes, without reading 40 pages at once." 
2. **Conscientious returning voter**: "I want to understand the important trade-offs, check claims and revisit my questions later." 
3. **Person affected differently than others**: "I need to know which provisions apply to my circumstances and who might experience different effects." 
4. **Historical investigator**: "I remember an issue returning. What's changed in the proposal, and what happened after an earlier vote?" 
5. **Accessibility/language needs**: "Help me understand the original terms at different depth, without changing their meaning." 

## Information architecture: only three top-level locations
- **Votes** (default): current/archived federal referendum list, jurisdiction/date, search; one issue is the central object.
- **My understanding** (optional): locally saved brief per issue, questions, notes, selected perspectives, optional self-recorded prior vote, source version alerts.
- **About evidence & privacy**: explain evidence classes, sources, historical frame, update history, private data controls and limitations.

Not top-level menus: pro/contra, national/global impacts, chat, timelines, scoring, claims taxonomy, AI settings; these are progressively revealed **within a vote**. There is **no ballot recommendation screen**.

## The main five screen states

**S01: Vote picker**: Heading "What are you voting on?" Current federal ballot cards + archive search. Each card shows title, jurisdiction, date, available language, source status. User can upload a booklet only in later version after source and copyright controls.

**S02: Vote overview (the wow moment)**: Heading "What could change?" One-sentence official-scope description, three cards maximum: `What the proposal actually changes`, `Who might be affected`, `What remains uncertain`. Source date and speaker attribution present but subordinate. Prominent `Explore what this means` and `View original booklet`.

**S03: Impact explorer**: First question: "Explore one situation" with neutral preset scenario chips (e.g. receiving an old-age pension, working-age contributor, public finances). No birthdate, salary, party affinity, personal address or political belief required. For each selected lens show 1–3 validated consequences and unknowns, with `Why?` → evidence. "Others affected" opens separate stakeholder scenarios—not a ranked recommendation.

**S04: Evidence walkthrough**: A single selected consequence expands into the minimum causal chain: *proposal provision → hypothesised/conditional mechanism → possible effect*. Every step labelled with its epistemic status and author; `See source` opens exact excerpt and original document/page. Opposing claim is available where sourced, **not forced into false balance**. "Not established" is a useful answer.

**S05: My understanding**: User can save a brief: "Here's what the proposal would do / what might vary by situation / what remains open / sources checked / my own questions." This is *not* automatically a vote decision. Optional notes encrypted locally. Show source-version timestamp; future updates display delta, not silently rewriting.

## Complete journey and state register
| Journey | Trigger → successful outcome | Essential exception / trust state | screens/modules |
|---|---|---|---|
| J00 Understand trust & privacy | Arrive → clear promise without sign-up | explanation of what app cannot prove | S01, About; M08 |
| J01 Choose referendum | Search or pick issue → exactly one ballot item | source absent, wrong canton, several ballot items | S01; M01/M04 |
| J02 First understand | Open proposal → 60–90 sec digest | content in review, ambiguous translation | S02; M07/M08 |
| J03 Explore personal applicability | Select factual scenario → conditional explanation | insufficient scenario facts → explicitly conditional | S03; M06/M08 |
| J04 Explore other people | Switch scenario → different valid effects | no evidence for that group | S03; M06/M08 |
| J05 Explore wider effects | Open Switzerland/beyond → sourced claims/limits | national consequences uncertain; skip irrelevant international lens | S03/S04; M06 |
| J06 Challenge a claim | Tap claim → mechanism/evidence/assumptions | only attribution proven, not outcome | S04; M05/M06/M07 |
| J07 Ask in own words | Ask question → bounded passage-linked response | no answer / missing model / false premise / vote recommendation request | S04; M05/M07 |
| J08 Compare arguments | See actual speakers and evidence quality | one-sided source or unequal evidence | S04; M06/M07 |
| J09 Source inspection | Tap citation → original PDF page and quoted span | source removed/version mismatch/text OCR confidence | S04; M02/M03 |
| J10 Save/resume | Add own question/brief → opens next visit | vault locked/forgotten key; no server rescue | S05; M09/M10 |
| J11 Revisit old ballot | Search historical case → choose pre-vote or 'what happened later' | avoid future leakage when replaying old booklet | S01/S05; M04/M07 |
| J12 Receive factual update | Reopen saved case → review documented change | source retraction/correction; no automatic edits to notes | S05; M02/M07/M09 |
| J13 Delete/export | Export/delete local data → verifiable local operation | failed export must not trigger delete | Settings; M09 |
| J14 Accessibility/language | Switch language and text size → consistent explanation | verified cross-language passage unavailable → disclose | all; M03/M08 |
| J15 No model service | Revisit pre-reviewed case → usable source-backed static view | no simulated AI replies | S02-S05; M07/M08 |

## A representative first-run journey (no ceremony)
```
Open site (no login)
     ↓
Choose "13th AHV pension — March 2024 [historical]"
     ↓
What changes? → defined additional pension payment; financing not specified in original initiative
     ↓
Who would you like to understand? [Pension recipient] [Working-age person] [Switzerland]
     ↓
Tap [Working-age person] → Financing effect: not established by proposal alone
     ↓
Why? → booklet passage + initiative vs later financing distinction
     ↓
Tap [Other people] → compare pension-recipient condition
     ↓
Save [1 short understanding brief] optional; no account
```
This is a designed flow using the verified general policy scope, **not a run of the app** or a promise of exact personal effect.

## Screen density and the Surface Clarity Gate
- One primary action/screen, maximum three first-level content cards, max 2–3 lines per consequence until expansion.
- Never show four perspective panels simultaneously by default. Progressive expansion: `Me / Others / Switzerland`, and `Beyond Switzerland` only when relevant evidence exists.
- Show verdict distinctions in ordinary language, not seven coloured truth labels. Use `Established in proposal`, `Claim by X`, `Depends on ...`, `We can't determine this` with optional definitions.
- Every insight must answer an implicit user question: "What changes? For whom? Why? How do we know?" Delete any content that answers none.
- AI chat is *a follow-up control*, not the homepage. Source inspection is one tap away, not a PDF dump.
- Avoid both "equal columns = truth" and confidence percentages unsupported by calibration.
- Accessible desktop/mobile: WCAG 2.2 AA target; 44px touch targets, readable typography, keyboard/focus, language tag, non-colour-only status, print-friendly brief.

## UX copy examples (illustrative)
- Good: "The proposal would add an annual pension supplement. Its financing was not decided in this text."
- Good: "The Federal Council argues this would increase financing pressure. See why and what assumptions this depends on."
- Good: "We can't calculate your exact salary contribution from this booklet."
- Bad: "This reform saves you CHF 1,200." (without validated inputs/model)
- Bad: "For people like you, YES makes sense." (personalised political recommendation)
- Bad: "Supporters are 80% correct." (invented evidence score)

## UX validation with humans
Ask the voter to explain **in their own words**: (a) one direct policy change, (b) one major uncertainty, (c) why a claim is disputed, (d) a difference between two contexts, (e) where the answer comes from. Compare with official booklet and conventional summariser on comprehension **and time/effort**. Blindly score answers where feasible. Track confusion, scrolls, source opens, unsupported-confidence comprehension. Do **not** measure success by whether the user votes differently or develops a preferred party view.