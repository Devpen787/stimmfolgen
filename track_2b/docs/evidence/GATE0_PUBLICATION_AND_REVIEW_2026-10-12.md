# Gate 0 publication availability and pending AHV review

**Pre-vote availability PASS. Human semantic review PENDING. Frontend blocked.** No new model inference was performed in this continuation, and no historical source report, span identity, model output or semantic reference was changed.

The exact pinned German booklet was served from the original official government URL and archived by **11 January 2024, 12:11:17 UTC**, before the 3 March vote. The current BSV download, current pinned Federal Chancellery file and historical archived payload are identical: 759,783 bytes, SHA-256 `53c7cc72c28f80969ed56d7813ad8c05e505b1817923418d0dfa45368a6bd07e`. The archive CDX record reports HTTP 200/application-PDF and payload SHA-1 base32 `2LBTYX6NDQ3A2M6J4YY24CSQQBORBQWU`; that digest also matches the downloaded bytes. Memento and archived origin HTTP dates match the capture timestamp. This is an observed availability upper bound, not a signed timestamp or proof of the first publication instant.

Primary document witness: [archived original government PDF](https://web.archive.org/web/20240111121117id_/https://www.admin.ch/dam/gov/de/Dokumentation/Abstimmungen/Marz2024/marzo_DE.pdf.download.pdf/marzo_DE.pdf). Publisher corroboration: [BSV document listing](https://www.bsv.admin.ch/de/renteninitiative-ahv-2024), which dates the German attachment to 11 January 2024, and [its current PDF](https://www.bsv.admin.ch/dam/de/sd-web/3ulVVyBoZ99F/erlaeuterungen-20240303.pdf). The BSV page itself is dated 26 March 2024; it is not being presented as a pre-vote page snapshot. Current HTTP modification dates and the booklet's printed editorial cutoff were not used as publication evidence.

## Three different temporal facts

| Fact | Date | What it establishes |
| --- | --- | --- |
| Booklet editorial cutoff | 29 November 2023 | Printed content/knowledge boundary |
| Exact-byte public archive observation | 11 January 2024, 12:11:17 UTC | Booklet was available by this time |
| Proposed public review frame | 2 March 2024, 23:59:59 CET | A pre-vote frame after the verified availability witness |

The original diagnostic reports used `as_of: 2023-11-29` for content knowledge. They remain immutable and do not prove that the document was public on that date. A public frame at that cutoff fails the new availability guard. The proposed March review frame passes. The sidecar record is bound to the document hash and does not mutate content-addressed span IDs or relabel earlier model traces. Active runtime adoption of the public-frame/content-cutoff distinction and a final Gate 0 decision remain necessary after human review; preparation is not admission.

## Ready for the user's semantic review

Open the [review packet](ahv-semantic-review-2026-10-12/REVIEW.md). It contains five proposition decisions (P01-P05), seven actual-trial decisions (T01-T07), exact normalized spans and hashes, candidate outputs copied from the immutable final-repeat traces, eight unannotated source page images, and a [blank response template](ahv-semantic-review-2026-10-12/review-response.template.json).

Important review distinctions: page 18 defines an annual supplement of one twelfth; page 9 explains the payment-frequency change. Page 11 concerns old-age pensions, forecasts and hypothetical financing options. The five-year cost is a reference-only entry, not a returned final extraction answer. Page 16 is jointly labelled Federal Council and Parliament; `GOVERNMENT` is the pipeline's coarse enum for that section. The actor-conflict outcome is a policy comparison of two real Apertus completions; the full happy path is a three-response aggregate. These distinctions are surfaced for acceptance, rejection or correction rather than pre-approved by the packet author.

Every decision, reviewer name/date and overall outcome remains PENDING or blank. The coding-agent-authored reference is still not human reviewed. No private political preferences are requested. The packet verifier checks source/candidate/hash binding and refuses to treat preparation as approval. Seventy-three deterministic tests and design contracts pass locally. Cloud CI verifies the stored archive witness against pinned source bytes without making a new archive request or running Apertus. Broader release gates, licensing/generalisation, cold Docker execution and private-data security are not certified by this review.

## Reproduce acquisition and verification

Run from the repository root. Keep downloaded complete PDFs and raw headers in ignored `.local/`.

```sh
mkdir -p .local/gate0/publication
curl -L --fail 'https://www.bsv.admin.ch/de/renteninitiative-ahv-2024' -o .local/gate0/publication/bsv-de.html
curl -L --fail 'https://www.bsv.admin.ch/dam/de/sd-web/3ulVVyBoZ99F/erlaeuterungen-20240303.pdf' -o .local/gate0/publication/bsv-booklet.pdf
curl -L --fail 'https://web.archive.org/cdx/search/cdx?url=www.admin.ch/dam/gov/de/Dokumentation/Abstimmungen/Marz2024/marzo_DE.pdf.download.pdf/marzo_DE.pdf&output=json&filter=statuscode:200&to=20240302' -o .local/gate0/publication/cdx.json
curl -L --fail -D .local/gate0/publication/archive-headers.txt 'https://web.archive.org/web/20240111121117id_/https://www.admin.ch/dam/gov/de/Dokumentation/Abstimmungen/Marz2024/marzo_DE.pdf.download.pdf/marzo_DE.pdf' -o .local/gate0/publication/archived-booklet.pdf
shasum -a 256 .local/gate0/booklet.pdf .local/gate0/publication/bsv-booklet.pdf .local/gate0/publication/archived-booklet.pdf
.venv/bin/python -m unittest discover -s track_2b/tests -p 'test_gate0*.py' -v
.venv/bin/python track_2b/src/gate0/verify_semantic_review_packet.py --packet-dir track_2b/docs/evidence/ahv-semantic-review-2026-10-12 --source-pdf .local/gate0/booklet.pdf
```

The packet's [availability record](ahv-semantic-review-2026-10-12/publication-availability.json), [CDX response](ahv-semantic-review-2026-10-12/cdx-response.json) and [manifest](ahv-semantic-review-2026-10-12/manifest.json) retain the observed source chain. Archive record length describes compressed WARC storage, not the uncompressed PDF length. Page images were rendered from the authenticated original with Poppler at 1400-pixel maximum dimension, inspected for legibility and left unannotated. Full source PDFs remain local.
