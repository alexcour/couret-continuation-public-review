# COD-H-01 — G0.4: documentary gate and validation record (2026-10-13)

**Status:** research work-in-progress, no peer review; GA015 direct Greek rubrics **0/6** authenticated. The six-row ledger contains **three non-diplomatic source reports** (K1, K5, K6) and **three unknown entries** (K2–K4).

## Verification executed locally

Replayed the original `check_evidence.py` against the six-row CSV: **PASS**. Subsequently tested a stricter validator against the CSV and ran **9/9 unit tests PASS** with Python 3. The enhanced validator rejects duplicate rubric identifiers, missing source attribution, invented text for an unverified row, source-layer conflation and any premature GA015 certification. This does not verify Greek source accuracy.

The branch now includes a path-scoped GitHub Actions workflow `codh01-documentary-gate.yml` using Python 3.12. **GitHub-hosted CI conclusion must be checked separately**; passing local tests is not proof that remote CI ran successfully.

## Source acquisition outcome

- Primary *manuscript* transcriptions K1–K6 are **not yet directly extracted and independently collated**.
- Pinakes CPG 3642 supplies a *tradition-level* first and sixth entry; neither should be labelled GA015.
- The F.1 catalogue lists *chapter lists*, numbered kephalaia and quotation markers, not an exhaustive folio-level Greek transcription. The absence of a feature from a catalogue should not be used as a universal argument of absence.
- Available digitized and indexed sources consulted did not yield a fully checked Greek diplomatic text of K2–K4. **Do not infer these lines from modern section boundaries.**
- We did not rely on OCR to claim an independent ancient reading.

## Correct protocol order

G0 image-level provenance and six readings -> G1 two independent transcriptions with variant apparatus -> G2 controlled comparison of authentic historical titles and navigation marks -> G3 preregistered randomized reading study. **G0 still open**. Keep PR as draft; do not merge or publish this packet as an established historical result.

Working Drive report: https://docs.google.com/document/d/1RymbUPoyMzJCJqGvsEAo2E9joEtMmlFZMrIK9-JYfZ0/edit

Review request: inspect actual facsimile/edition of GA015, confirm for each K1–K6 the *witness*, *folio*, *ink/material layer*, *Greek spelling*, *corresponding body-text position*, and *variant status*. Where any field is absent use **unknown**, not an imputed value.
