# COD-H-01 — MSI synthetic bench v0.1

**18 October 2026: synthetic software testing only, NO acquired raw Glasgow MSI, NO K1 reconstruction, G0 partial.** Grounded in COD-H-01 addenda G0.12/G0.13, University of Glasgow DOI 10.5525/gla.researchdata.1865 and existing documentary PR #3. Existing TEI and documentary tests are unchanged.

## Reproduction (Python 3.12, repository root)

    python3 -m venv .venv
    . .venv/bin/activate
    python -m pip install -r case-studies/codex-h/msi_lab/requirements.txt
    export PYTHONPATH=case-studies/codex-h
    python -m unittest discover -s case-studies/codex-h/msi_lab/tests -v
    python -m msi_lab.bench generate --scenario signal --out /tmp/msi-signal
    python -m msi_lab.bench analyze --input /tmp/msi-signal --out /tmp/msi-report
    python -m msi_lab.bench generate --scenario artifact --out /tmp/msi-artifact
    python -m msi_lab.bench analyze --input /tmp/msi-artifact --out /tmp/msi-artifact-report

Use fresh paths, or remove your own old temporary outputs first. The original ten adversarial tests passed locally on 18 October. Four additional tests now cover a held-out PCA band, a coherent multiband stain, seeded reproducibility and excessive registration displacement; their remote status must be checked at the new head. Reports contain hashes, software versions, orientation and alignment, PCA explained fractions, and synthetic holdout contrast. Output images: false_color.png and pc1.png. UTC log timestamp varies; fixed seeded fixture contents are reproducible.

## What the tests DO and DO NOT show

- Inputs are invented four-band 128x128 arrays, with invented wavelength labels 450/550/650/750 nm (NOT actual Glasgow wavelengths), asymmetric registration fiducials, a mirrored band, translations and fake bar-shaped target.
- SHA-256 verification rejects tampering; strict manifest requires source, rights, per-band details, and rejects path traversal and real-origin labels.
- Orientation enumerates 8 rotate/mirror candidates; translation alignment searches integer shifts up to five pixels using pre-planted artificial fiducials OUTSIDE the content ROI; fails closed on weak scores.
- Unsupervised centered PCA and percentile RGB composites are pictures, not evidence of letters.
- Negative fixtures test blank regions, a one-band false positive, a shared multiband stain, held-out last-band rejection, missing metadata, no fiducials, and no overwrites.
- Limitations: NO dark/flat correction, physical radiometric calibration, 16-bit TIFF/RAW parser, lens distortion, nonrigid registration, measured uncertainty, or paleographic verification. Pre-set fixture target and thresholds MUST NEVER be used as real manuscript evidence.

## Strict approval and real-image gate (NOT YET IMPLEMENTED)

1. Await explicit data-holder permission for 86v / Coislin 202 11rT; verify exact file/folio/capture mapping and access/derivative/crop terms. The notice's CC BY-NC 4.0 does not replace individual access conditions. Do not place restricted pixels in a public repository.
2. Make a private intake ledger with supplier ID, immutable original hash, bytes, role, surface, dates, source, band/filter/wavelength if documented, dimensions, bit depth, orientation/mirror, dark/flat frame metadata, rights and credits. Missing metadata must be reported as NOT SUPPLIED.
3. Implement a separate permission-gated real-image loader after inspection of actual image formats. Do not spoof origin=SYNTHETIC_ONLY. Establish material orientation from reference markers rather than expected Greek text.
4. Pre-register region of interest, blank zones, independent held-out raw bands and parameter sensitivity. Check registration margins, interpolation artifacts, substrate texture, noise, saturation and multiband consistency before considering signs.
5. Require TWO independent blind readers and explicit alternative transcriptions with coordinates, orientation, source bands and disagreements. Only then seek external review from Allen, without claiming K1 is reconstructed.

**No automatic merge.** No synthetic output is a manuscript transcription. No OCR, generative character completion or Greek phrase prompting in this software.

## v0.2 review gate — 18 October 2026

The fourth band is kept entirely outside PCA fitting and retained for separate known-fixture contrast checks; this is a **software holdout**, not physical independence. Reports now say `band_support_at_fixture_threshold` instead of implying statistically independent observations. A deliberately shared multiband stain generates four-band support but remains `NOT_RECONSTRUCTED`, demonstrating that even spatial and spectral coherence cannot authenticate characters. Radiometric response, genuine exposure independence and historical ink attribution require the restricted originals, calibration metadata and approval from data holders. The previous wording suggesting independent bands was withdrawn. The new tests should not be considered successful until the latest GitHub CI completes.
