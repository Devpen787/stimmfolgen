# Gate 0 — First observed source evidence (2026-10-12)

**Status:** official-source retrieval and five-page extraction verified in GitHub Actions. **Apertus inference NOT run.** This is not a demonstration of policy reasoning accuracy.

## Exact source

- Official title: Swiss Federal Chancellery, *Volksabstimmung vom 3. März 2024 — Erläuterungen des Bundesrates*.
- Source URL: https://www.bk.admin.ch/dam/de/sd-web/In9i5Kp4p64r/2024-03-03_erlaeuterungen_des_bundesrates.pdf
- Booklet referendum date: 2024-03-03.
- Printed editorial cutoff: 2023-11-29 (PDF page 2).
- Download and PDF extraction were independently executed by GitHub Actions on 2026-10-12.
- Actual downloaded PDF byte count: **759,783**.
- Actual downloaded PDF SHA-256: **53c7cc72c28f80969ed56d7813ad8c05e505b1817923418d0dfa45368a6bd07e**.
- Observed PDF page count: **32**.
- Extracted and labelled PDF pages (1-indexed): **4, 9, 11, 14, 16**.
- Source verifier status: **PASS**.
- Unit test and provenance workflow status: **PASS**.
- Reproducible GitHub Actions source run: https://github.com/Devpen787/stimmfolgen/actions/runs/38222222624
- Downloadable source extraction JSON: workflow artifact `gate0-real-official-source`. This retains the actual selected-page text (not embedded in Git).
- Source run commit: `ae0c7d55a9657667f4ab0e86a50263815143e8cd`.

## Trust boundaries

The source PDF discusses (i) a defined 13th AHV payment, (ii) financial cost projections and possible financing alternatives, and (iii) the initiative not specifying financing. These are *different epistemic classes*. Existing-source content is not proof that a projection will occur.

The verifier only checks PDF bytes, page availability, minimum text presence, and expected anchor terms. It does **not** verify semantic interpretation, competing claims, legal consequences, or the truth of political predictions.

## Next experiment (PENDING)

- Authorise a genuine Apertus 1.5 8B or 70B endpoint.
- Run `model_probe.py --source-report gate0-source.json` with `LLM_NAME`, `LLM_BASE_URL` and securely provided `LLM_API_KEY`.
- Retain raw model response and mechanical grounding outcomes.
- Have a reviewer check whether the interpretation truly follows from its quoted pages and preserves actor/date. Then assess false certainty and missing evidence.
- Do not claim `LIVE/INTEGRATED` or model evidence until the recorded run exists.
