# COD-H-01 — G0.9: full combined-XML structural audit, 13 October 2026

Public Glasgow archive DOI 10.5525/gla.researchdata.2105. ZIP SHA-256 `c2c04b62d2f88171fd1805a5d4b41cb14da8138a7b0305acd30e118b93165d1f`. GitHub-hosted source scan [run 38428339654](https://github.com/alexcour/couret-continuation-public-review/actions/runs/38428339654), job 115403573443: **SUCCESS**.

The new `probe_combined_tei.py` scans all TEI `pb` elements throughout the `text/body` tree of the one XML member instead of truncating a folio list to the first 12 entries. It yields:
- Member: `combined-xml.xml`
- Explicit TEI page breaks `pb[@n]` in this file: **1**
- Exact `pb n=86v`: **no**; `pb n=87r`: **no**
- Titus-labelled `div` in the scanned body: **0**
- `num type=chapNum` with `n=1`: **0**
- Title-related lexical matches on folios 85r–88v: **0**

**Scope warning:** these are results for the identified TEI structural conventions only. A combined XML source may encode manuscript segmentation through other elements/attributes or may be a different text subset. The parser's zero counts are *not* proof that Titus K1 was absent in the sixth-century manuscript; nor do they negate the previously acquired Glasgow website GA015 folio-87r TEI with K2–K6. Inspect the XML root, nested element types, full header, data coverage and provenance before treating this deposited ZIP as evidence about manuscript foliation.

Confirmed from prior independent source report: GA015 86v has an image but no acquired transcription. Earlier 2025 research reports its transfer as presently unrecoverable; **this does not itself locate K1 on that image**.

Next action: seek clarification from Glasgow editors on whether the DOI 2105 combined XML contains precisely the same witness/page corpus as the web edition and, independently, where K1 was expected and what imaging evidence survives.

**G0 incomplete. G1 not started. No claim of K1 found, no six-way partition, no cognitive experiment. PR draft.**
