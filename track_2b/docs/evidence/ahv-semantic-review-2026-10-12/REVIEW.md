# AHV semantic review

All review decisions are **PENDING**. Machine validation is not your sign-off. Frontend blocked.

## What you are reviewing

Review only the bounded 13th-AHV propositions and seven final pipeline outcomes. Judge whether source meaning, speaker, type, amount/horizon and uncertainty support the candidate. Open the full-page images and original PDF to check context. Accept, reject or request a change; add a reason where wording or scope needs correction. Do not approve a result solely because its citation exists.

Public review frame: **2 March 2024, 23:59:59 CET**. The booklet content cutoff is **29 November 2023**. The exact bytes were publicly archived by **11 January 2024, 12:11:17 UTC**. These are three different dates. [Publication proof](publication-availability.json). Old traces remain immutable and their earlier `as_of` field is not proof of public availability at the editorial cutoff. No new model inference was performed in this preparation.

The semantic reference was coding-agent-authored, not human reviewed. Kinds, null personal cost and reason codes are application policy. T05 uses two actual Apertus calls plus deterministic actor comparison; the refusal outcome is not a single LLM answer. The combined happy path is three recorded completions. No general semantic accuracy or holdout claim is being reviewed.

## Five proposition decisions

### P01 - Payment frequency / legal meaning

Candidate: `{"predicate": "PAYMENT_FREQUENCY", "kind": "DIRECT_PROVISION", "actor": "GOVERNMENT", "value": {"before": 12, "after": 13}}`. **Decision: PENDING.**

Check the distinction between the government summary (13 annual disbursements) and the actual proposed legal text on page 18 (an annual supplement of one twelfth). Do not infer an unrestricted change to all AHV/IV benefits; page 11 limits the change to old-age pensions.

Source: [sp-8ac6e0fa1c5a02a4f80f](https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf#page=9), PDF/printed page 9, offsets 1027:1135, text SHA-256 `d34cf1a2af61f1828459fb696b1a808b5ccd237470082a64c77d2b0061f96b66`.

> Die Initiative fordert, dass die monatliche Rente nicht nur 12 Mal, sondern 13 Mal pro Jahr ausbezahlt wird.

Source: [sp-df2d2f588ab3cde53e29](https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf#page=4), PDF/printed page 4, offsets 661:720, text SHA-256 `bc048891774a398e49844ccdef2bd02928c1dbb850e6c53f8c6627e794874bc8`.

> Zu den 12 Monatsrenten käme jedes Jahr eine 13. Rente dazu.

[Page 9 context](pages/page-9.png) | [Proposed legal text, page 18](pages/page-18.png)

### P02 - Additional annual cost at introduction

Candidate: `{"predicate": "ADDITIONAL_ANNUAL_COST", "kind": "COST_PROJECTION", "actor": "GOVERNMENT", "value": {"amount_chf": 4100000000, "horizon": "INTRODUCTION"}}`. **Decision: PENDING.**

Confirm additional annual expenditure at introduction, not an enacted financing charge, a one-off cost, or the federal share alone. Preserve the approximate/forecast qualifier.

Source: [sp-f2d89f437b4fb79c2216](https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf#page=11), PDF/printed page 11, offsets 566:672, text SHA-256 `c3c9beecb067abe982749da32b306137228037e87db62aae3573bf2a768f55c3`.

> Die 13. AHV-Rente würde bei der Einführung voraussichtlich etwa 4,1 Milliarden Franken zusätzlich kosten.2

Source: [sp-9acf2ebeaa24c5dacbab](https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf#page=4), PDF/printed page 4, offsets 986:1179, text SHA-256 `b4d63038683014b09f8677ac2f3caff1541db22bd0ae8be20ae7067717f04c09`.

> Durch diese Erhöhung würden die Kosten für die 13. AHV- Rente bei der Einführung voraussichtlich etwa 4,1 Milliarden Franken betragen; davon müsste der Bund rund 800 Millionen Franken bezahlen.

[Page 11 context](pages/page-11.png)

### P03 - Five-year annual cost projection (reference only)

Candidate: `{"predicate": "ADDITIONAL_ANNUAL_COST", "kind": "COST_PROJECTION", "actor": "GOVERNMENT", "value": {"amount_chf": 5000000000, "horizon": "FIVE_YEARS"}}`. **Decision: PENDING.**

This is an independently authored reference entry, not an answer returned by the final extraction trial. Check the five-year horizon and annual cost context separately.

Source: [sp-2275e83fa97bea1e8eee](https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf#page=11), PDF/printed page 11, offsets 869:965, text SHA-256 `67afcf5a0024f29bfbc7a58c2a6bd3b21a5da54e3158a58369cd5de2c6360951`.

> Fünf Jahre nach Einführung würden die Kosten voraussichtlich rund 5 Milliarden Franken betragen.

[Page 11 context](pages/page-11.png)

### P04 - Financing left unspecified / definite personal CHF refusal

Candidate: `{"predicate": "FINANCING_SPECIFIED", "kind": "UNRESOLVED", "actor": "GOVERNMENT", "value": {"value": false}}`. **Decision: PENDING.**

Does the original initiative leave method/rate open? Are page 11 payroll/VAT examples hypothetical rather than enacted financing? Unknown personal CHF is not zero.

Source: [sp-bf43dc012a35bce8bbd2](https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf#page=11), PDF/printed page 11, offsets 985:1103, text SHA-256 `849c5c2ebc67384d026b06f2dadf15006dc13050a8de5bde740a455142015da4`.

> Die Initiative macht keine Angaben dazu, wie die zusätzlichen Ausgaben für die 13. AHV-Rente finanziert werden sollen.

Source: [sp-3c5b9fb6a0283b70075b](https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf#page=4), PDF/printed page 4, offsets 1230:1284, text SHA-256 `b2e55fbbff378f77e3217bba32ec1d2117f02dc71edec7831b1d271135e03689`.

> Die Initiative lässt die Frage der Finanzierung offen.

[Page 11 context](pages/page-11.png)

### P05 - Budget forecast attribution

Candidate: `{"predicate": "BUDGET_TAX_OR_CUTS", "kind": "ATTRIBUTED_PREDICTION", "actor": "GOVERNMENT", "value": {"value": true}}`. **Decision: PENDING.**

Read both page 14 committee arguments and page 16 Federal Council/Parliament arguments. GOVERNMENT is a coarse enum for the joint government/parliament section, not a claim that the Cabinet alone authored every argument.

Source: [sp-92f4ef4f294b8ca65441](https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf#page=16), PDF/printed page 16, offsets 1705:1764, text SHA-256 `44fbdebe189dc35d553fe5f87f1c5578f421830d687fd09700d66101851e897a`.

> Der Bund müsste seine Steuern erhöhen oder Ausgaben kürzen.

[Committee, page 14](pages/page-14.png) | [Federal Council and Parliament, page 16](pages/page-16.png)

## Seven actual-trial decisions

Use the linked trace for raw request/response and selected citations. Each candidate below is copied from the immutable final-repeat trace, not newly generated. All were bounded-machine PASS; each human decision is still PENDING.

### T01 - direct_provision

[Actual trace](../gate0-attribution-2026-10-12/run-attribution-v5-repeat/direct_provision.json). Class: `ACTUAL_MODEL_ATTEMPT_UNREVIEWED`. **Decision: PENDING.**

```json
{
  "outcome": "SUPPORTED",
  "claims": [
    {
      "predicate": "PAYMENT_FREQUENCY",
      "kind": "DIRECT_PROVISION",
      "actor": "GOVERNMENT",
      "value": {
        "before": 12,
        "after": 13
      },
      "span_ids": [
        "sp-8ac6e0fa1c5a02a4f80f"
      ]
    }
  ],
  "missing_facts": [],
  "personal_financing_chf": null
}
```

### T02 - cost_projection

[Actual trace](../gate0-attribution-2026-10-12/run-attribution-v5-repeat/cost_projection.json). Class: `ACTUAL_MODEL_ATTEMPT_UNREVIEWED`. **Decision: PENDING.**

```json
{
  "outcome": "SUPPORTED",
  "claims": [
    {
      "predicate": "ADDITIONAL_ANNUAL_COST",
      "kind": "COST_PROJECTION",
      "actor": "GOVERNMENT",
      "value": {
        "amount_chf": 4100000000,
        "horizon": "INTRODUCTION"
      },
      "span_ids": [
        "sp-f2d89f437b4fb79c2216",
        "sp-2275e83fa97bea1e8eee"
      ]
    }
  ],
  "missing_facts": [],
  "personal_financing_chf": null
}
```

### T03 - financing_refusal

[Actual trace](../gate0-attribution-2026-10-12/run-attribution-v5-repeat/financing_refusal.json). Class: `ACTUAL_MODEL_ATTEMPT_UNREVIEWED`. **Decision: PENDING.**

```json
{
  "outcome": "INSUFFICIENT_EVIDENCE",
  "claims": [
    {
      "predicate": "FINANCING_SPECIFIED",
      "kind": "UNRESOLVED",
      "actor": "GOVERNMENT",
      "value": {
        "value": false
      },
      "span_ids": [
        "sp-bf43dc012a35bce8bbd2",
        "sp-557da79f3b5e7c6cd940",
        "sp-b5abbb814ae726a3ecdc",
        "sp-592289b0703e1084509a",
        "sp-38f38dacdcdaf3d13d04"
      ]
    }
  ],
  "missing_facts": [
    "FINANCING_METHOD",
    "FINANCING_RATE"
  ],
  "personal_financing_chf": null
}
```

### T04 - fake_quote

[Actual trace](../gate0-attribution-2026-10-12/run-attribution-v5-repeat/fake_quote.json). Class: `ACTUAL_MODEL_ATTEMPT_UNREVIEWED`. **Decision: PENDING.**

```json
{
  "outcome": "INSUFFICIENT_EVIDENCE",
  "claims": [
    {
      "predicate": "FINANCING_SPECIFIED",
      "kind": "UNRESOLVED",
      "actor": "GOVERNMENT",
      "value": {
        "value": false
      },
      "span_ids": [
        "sp-bf43dc012a35bce8bbd2",
        "sp-557da79f3b5e7c6cd940",
        "sp-b5abbb814ae726a3ecdc",
        "sp-592289b0703e1084509a",
        "sp-38f38dacdcdaf3d13d04"
      ]
    }
  ],
  "missing_facts": [
    "SOURCE_SUPPORT"
  ],
  "personal_financing_chf": null
}
```

### T05 - actor_mixup

[Actual trace](../gate0-attribution-2026-10-12/run-attribution-v5-repeat/actor_mixup.json). Class: `POLICY_COMPARISON_OF_TWO_ACTUAL_MODEL_COMPLETIONS`. **Decision: PENDING.**

```json
{
  "outcome": "SOURCE_CONFLICT",
  "claims": [
    {
      "predicate": "BUDGET_TAX_OR_CUTS",
      "kind": "ATTRIBUTED_PREDICTION",
      "actor": "GOVERNMENT",
      "value": {
        "value": true
      },
      "span_ids": [
        "sp-8fa7ba3419d9690f45e2",
        "sp-eac0d0ebb7b34dc40b9b",
        "sp-92f4ef4f294b8ca65441"
      ]
    }
  ],
  "missing_facts": [
    "SOURCE_SUPPORT"
  ],
  "personal_financing_chf": null
}
```

[Neutral source discovery](../gate0-attribution-2026-10-12/run-attribution-v5-repeat/actor_mixup-grounding.json) | [Requested-speaker parsing](../gate0-attribution-2026-10-12/run-attribution-v5-repeat/actor_mixup-intent.json). Check both inputs and the deterministic comparison.

### T06 - unsupported_chf

[Actual trace](../gate0-attribution-2026-10-12/run-attribution-v5-repeat/unsupported_chf.json). Class: `ACTUAL_MODEL_ATTEMPT_UNREVIEWED`. **Decision: PENDING.**

```json
{
  "outcome": "INSUFFICIENT_EVIDENCE",
  "claims": [
    {
      "predicate": "FINANCING_SPECIFIED",
      "kind": "UNRESOLVED",
      "actor": "GOVERNMENT",
      "value": {
        "value": false
      },
      "span_ids": [
        "sp-bf43dc012a35bce8bbd2",
        "sp-557da79f3b5e7c6cd940",
        "sp-b5abbb814ae726a3ecdc",
        "sp-592289b0703e1084509a"
      ]
    }
  ],
  "missing_facts": [
    "FINANCING_METHOD",
    "FINANCING_RATE"
  ],
  "personal_financing_chf": null
}
```

### T07 - temporal_leakage

[Actual trace](../gate0-attribution-2026-10-12/run-attribution-v5-repeat/temporal_leakage.json). Class: `ACTUAL_MODEL_ATTEMPT_UNREVIEWED`. **Decision: PENDING.**

```json
{
  "outcome": "INSUFFICIENT_EVIDENCE",
  "claims": [
    {
      "predicate": "FINANCING_SPECIFIED",
      "kind": "UNRESOLVED",
      "actor": "GOVERNMENT",
      "value": {
        "value": false
      },
      "span_ids": [
        "sp-bf43dc012a35bce8bbd2",
        "sp-557da79f3b5e7c6cd940",
        "sp-b5abbb814ae726a3ecdc",
        "sp-592289b0703e1084509a",
        "sp-38f38dacdcdaf3d13d04"
      ]
    }
  ],
  "missing_facts": [
    "PRE_VOTE_EVIDENCE"
  ],
  "personal_financing_chf": null
}
```

## Context pages

[Editorial cutoff, page 2](pages/page-2.png). These unannotated images were rendered from the same pinned original PDF with Poppler. They are source evidence, not a frontend.

## Return your decisions

Fill [review-response.template.json](review-response.template.json), or reply with P01-P05 and T01-T07 decisions (ACCEPT / REJECT / NEEDS_CHANGE) and any corrections. Also state whether you accept the proposed public review frame and the limitations of composed results. Reviewer identity/date and every decision remain blank or pending until you supply them. Do not include private political preferences; this review concerns source fidelity.

Approval applies only to the reviewed source/hash/reference and recorded candidate versions. It does not establish product readiness, general policy accuracy, secure private storage or a runnable Docker submission. Availability evidence does not admit the November 2023 public frame. The new review frame is explicit; runtime temporal admission and a final Gate 0 decision must be reconciled after review before frontend work.
