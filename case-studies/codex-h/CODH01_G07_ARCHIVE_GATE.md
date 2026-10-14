# COD-H-01 — G0.7: public Glasgow TEI archive acquisition gate

Date: 2026-10-13. **K1 remains unverified in GA 015. G0 PARTIAL / G1 not begun.**

## Data and provenance

The Glasgow research data archive *Codex H (GA 015) TEI/XML Transcription* is deposited under DOI **10.5525/gla.researchdata.2105**, at https://researchdata.gla.ac.uk/2105/, downloadable as `2105_data.zip` (about 55 KB, CC BY 4.0). This collection must not be confused with the independent large multispectral dataset DOI **10.5525/gla.researchdata.1865** (approximately 241 GB, access-on-request, CC BY-NC 4.0). The latter is not held locally, and the availability of TEI data is not equivalent to an independent examination of multispectral images.

## Reproduction

The branch includes [inspect_glasgow_2105.py](inspect_glasgow_2105.py), a stdlib tool to scan all contained XML pages after a bounded, safe ZIP inspection, listing page identifiers, Titus divisions and `num type="chapNum"` values. It prints its source ZIP SHA-256 so an independent researcher can tie results to exact bytes. It **never** infers the missing K1 from a tradition-level incipit, a neighbouring witness or an image-only metadata entry. It performs no automatic OCR or palaeographic identification.

Command:
```bash
python3 case-studies/codex-h/inspect_glasgow_2105.py --download --output /tmp/codh01_2105_manifest.json
```
The output manifest, and not the full ZIP, is the proposed traceable result. A numerical `1` in an unrelated XML element does not certify the first rubric. The tool reports **candidates for human philological review**, not manuscript readings.

**Execution disclosure:** source archive retrieval did not succeed from the current container network (name resolution failed), and this new acquisition script has not yet been run against the real ZIP during this turn. Do not describe K1 as located or the ZIP as inspected. Keep PR in draft and require the resulting review of exact source entries before G0 can advance.

## Next gate

Verify the ZIP member list and hashes; inspect pages adjoining Titus 87r, especially folio 86v (image known, transcription not confirmed); if the absence of K1 persists in edited data, inquire with the editorial team about its manuscript status and any transfers. Keep full source screenshots and images subject to their own rights.
