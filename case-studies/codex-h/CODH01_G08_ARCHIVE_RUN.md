# COD-H-01 — G0.8: bounded archive acquisition outcome (13 October 2026)

GitHub Actions **run 38427473252**, job **115400525076**, completed SUCCESS on commit `20ef12c5fbfdf921baac3cbc3fd2fef54d9f7f19`. The public Glasgow research archive DOI **10.5525/gla.researchdata.2105** was downloaded and parsed by `inspect_glasgow_2105.py` on a GitHub runner. Log data:
- ZIP SHA-256: `c2c04b62d2f88171fd1805a5d4b41cb14da8138a7b0305acd30e118b93165d1f`
- XML members enumerated: **1**
- Files matched by this script's `86v`/`87r` member-name or direct page-break filter: **0**

**Do not infer that K1 is absent.** The script's matching method was designed primarily for folio-specific XML documents. Because the ZIP has *one* XML member, the single XML could contain several pages or a different organisational structure, and the filter must be adapted to inspect all elements/metadata inside that member before any K1 presence claim. This is a structural discovery about the archive, not a reading of GA015.

Independent source observations carried over:
- GA015 TEI 87r directly acquired separately on the project's scholarly website: K2–K6, with editorial uncertainty preserved.
- GA015 86v: image listed, no transcription in the previously acquired project's page index; earlier inspected transfer image yielded no defensible K1 reading.
- Allen–Fowler 2025 describe the 86v transfer as not recoverable at that stage; this does **not** locate K1 on 86v.
- Pinakes and PG85 788B–C have different work-level K1 variants (`εἰς` / `πρὸς`); **neither establishes the wording of GA015 K1**.

Next independent gate: inventory the root node and all TEI elements inside the unique XML member, distinguishing `pb` manuscript page identifiers, `div` structural annotations, apparatus entries and quotations. Save a structured file-level report with no speculative reconstruction. Do not merge PR or mark G0 complete; no cognitive study.
