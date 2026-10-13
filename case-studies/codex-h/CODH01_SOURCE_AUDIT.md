# COD-H-01 — Codex H, Titus, and the observability of paratext

**Status (2026-10-13): documentary working note / NOT PEER-REVIEWED / NO NEW THEOREM / NO EXPERIMENT PERFORMED.**  
Scope: Greek manuscript cataloguing, document reconstruction and an *unimplemented* protocol for studying present-day reading behaviour. This case is outside the stable mathematical claims of this repository. No theological inference or claim concerning historical reader cognition is made.

**Current source acquisition: G0.5.** [Detailed witness-specific collation](CODH01_G05_COLLATION.md) and [structured six-slot record](CODH01_COLLATION.json). The Glasgow TEI of reconstructed **87r**, explicitly mapped to **Paris, BnF, Coislin 202, 11r**, now supplies Greek edition entries **K2–K6**, with uncertainty and Omont-derived restorations retained. K1 is absent from this acquired page and remains tradition-level only. Five edition entries acquired does **not** mean five independently certified diplomatic readings. The older G0.4 record is a historical acquisition snapshot.

**G0.7 source coverage supplement:** [Source coverage and unresolved foliation discrepancies](CODH01_G07_SOURCE_COVERAGE.md). All **ten indexed Titus transcriptions** are preserved and hash-checked: five list-level rubric numbers, one body-level γ, and 26 modern verse labels, which do not certify complete recovered verses. The 86v image yielded no secure K1 reading in this inspection. Allen–Fowler (2025), pp. 195–196, differs from the current index for **88v/88r** and the start of **89v**. Separately, the article and index identify the colophon as **96r**, while catalogue F.1 reports **95r**. Keep source versions and material shelfmarks attached. **G0 remains partial.**

**Printed comparator acquired in G0.7:** [Six source-bounded PG records](CODH01_PG85_TITUS_COLLATION.json). Visual inspection of the public PG85 scan places the Greek Titus list at **788B–C, PDF page 394**; 785 concerns 2 Timothy. K1 has **πρὸς** in this print versus **εἰς** in Pinakes. Printed start references and notes belong to the edition and its named witnesses, not GA015. Preserve the source spellings; no K1 Codex H reading or complete rubric span is certified. The older G0.5/G0.6 statement that the scan had only been located is superseded by this acquisition.

## 1. What is actually attested?

The Codex H of the Pauline Epistles is Gregory–Aland **015** (GA 015), catalogued as **F.1** by Allen, Fowler, Scieri and Venetskov, *The Euthalian Tradition of the New Testament: A Catalogue of Greek Manuscripts* (2025), printed pp. **324–325** (PDF pages 334–335). The entry enumerates distributed fragments, **chapter lists**, **kephalaia numbers [P]** and **quotation markers [P]**. It does **not** explicitly list **in-text kephalaia titles** among the attested in-text features in that entry. Absence from the catalogue inventory is not proof of historical absence.

The IRHT/CNRS Pinakes **work-level notice** for *In Tit.: capitula* (CPG 3642) reports **six capitula** and points to PG **85.785B–C** (with a title reference to 85.788B). It records the first and sixth rubric of the **Euthalian tradition**. This is **not an independently transcribed reading from GA 015**.

A report of information supplied by Garrick Allen associates rubric **K5** with **Titus 3:1–9**, reporting an English title; it does not supply a directly audited Greek GA 015 reading in the source examined for this note.

The Pinakes explanation states that Titus has no *subdivisions* of chapters and therefore no red-ink numbering for such subdivisions. Do not confuse absence of subchapter marks with absence of the six rubric entries. Nor does the existence of six entries alone prove that they partition the entire continuous letter into six mutually exclusive spans.

## 2. Evidence ledger: do not fill blanks by inference

Machine-readable current snapshot: [CODH01_EVIDENCE.csv](CODH01_EVIDENCE.csv). A nonempty string under `reported_text` is **only** attributed to the `source_layer` stated in that row. No row has completed this dossier's independent diplomatic validation. The flag does not deny the existence of the scholarly GA015 edition. Braces mark `unclear`, square brackets `supplied`, parentheses `ex`; original XML controls exact encoding.

| Rubric | Available evidence | GA 015 Greek verified? |
|---|---|---|
| K1 | Greek incipit in the Pinakes *tradition-level* catalogue | **No** |
| K2 | GA015 digital edition 87r, lines 1–3; uncertain letters and Omont-supplied final sigma | **No** |
| K3 | GA015 digital edition 87r, lines 4–6; encoded marginal gamma at 90r between Titus 2:1 and 2:2 | **No** |
| K4 | GA015 digital edition 87r, lines 7–9; uncertain letters and unexpanded nomen sacrum | **No** |
| K5 | GA015 digital edition 87r, lines 10–12; Omont-supplied final sigma; Titus 3:1–9 remains a separate secondary report | **No** |
| K6 | GA015 digital edition 87r, lines 13–15: plural and αἱριστικοὺς; compared with witness-specific Pinakes reports | **No** |

The sixth rubric illustrates a transmission question: the acquired GA015 TEI gives `αἱριστικοὺς` and plural `παραινέσεις`; Omont p. 50 has the same distinctive letter sequence and plural. Pinakes gives `ἐριστικοὺς` at work level, `αἱρετικοὺς` for British Library Add. 28816 and `ἐριστηκοὺς` for Harley 5557. These forms are **not substituted** for the GA015 edition's wording. Semantic interpretation and independent paleographic review remain open. The sources cannot be counted as independent observations: Glasgow explicitly supplies two letters from Omont.

**Critical correction to earlier exploration:** an OCR corpus issued in 2026 for volumes of the *Patrologia Graeca* cannot by itself verify PG 85 here. At the time of this audit, the volume directories in `calfa-co/Patrologia-Graeca` **do not include PG085**. Its reported corpus-level character error rate is not a page-level verification, nor a direct copy of GA 015.

## 3. Formal separation of document layers

For witness `w`, represent an observation as `P_w = (B_w, L_w, M_w, R_w, S_w)`, where:

- `B_w`: extant body text, with uncertainty;
- `L_w`: list-level rubric strings and order;
- `M_w`: visible material markers (numbers, ink, marginal signs);
- `R_w`: documented links between rubric entries and positions in the body text, **a partial relation until verified**;
- `S_w`: source provenance, layer of inscription, transcription type and editorial interventions.

One may know `|L_w| = 6` while `R_w` remains unknown; therefore `|L_w| = 6` alone cannot certify a six-piece partition of the letter. This is a logical non-identifiability observation, **not a new mathematical theorem**.

In classical finite-observation language, a property `g` is identifiable relative to observation `O` and admissible reconstructions `X_H` only if `g` is constant on each fibre `O^{-1}(y) ∩ X_H`. Observing a chapter-list count is weaker than reconstructing the list-to-text alignment. This is a routine criterion of factorisation, not an original result.

## 4. Review gates

- **G0 documentary** — Catalogue F.1 and Pinakes source-level claim descriptions: **PARTIAL PASS**.
- **G0 diplomatic** — six GA 015 titles, folios, manuscript images and text boundary relationships: **OPEN**.
- **G1 philological** — two independent transcriptions and critical variant register: **NOT STARTED**.
- **G2 experimental material** — validated translations, presentation conditions, preregistration: **BLOCKED ON G0/G1**.
- **G3 cognitive study** — randomised participant study, blinded coding and statistics: **NOT STARTED**.

Conditional experimental question (once G0/G1 are satisfied): holding the words fixed, do *historically authenticated* headings change present-day navigation, recall or interpretation compared with length-matched neutral headings? Do **not** infer the cognition of sixth-century readers from any modern experiment.

## 5. Source references (no source PDF reproduced)

1. Allen, Fowler, Scieri & Venetskov (2025), *The Euthalian Tradition of the New Testament*, catalogue F.1, pp. 324–325, introduction on dating and scribal layers: https://eprints.gla.ac.uk/346002/1/346002.pdf ; https://doi.org/10.1163/9789004736917
2. Pinakes, IRHT/CNRS, *In Tit.: capitula*, CPG 3642 (tradition-level description): https://pinakes-dev.irht.cnrs.fr/notices/oeuvre/15355/
3. Lauren K. McCormick (2026-05-18), reporting Garrick Allen on the title attached to Titus 3:1–9: https://www.biblicalarchaeology.org/daily/ancient-cultures/daily-life-and-practice/pauls-lost-words-recovered/
4. Allen & Fowler (2025), *The Story of Codex H (GA 015): Manuscript Migration and Primary Sources in Biblical Studies*, *JBL* 144(1):167–196, https://doi.org/10.15699/jbl.1441.2025.9 ; https://eprints.gla.ac.uk/342036/
5. Allen et al. (2026, accepted/in press), *Codex H of the Pauline Epistles (GA 015): Introduction and Edition*: https://research.rug.nl/en/publications/codex-h-of-the-pauline-epistles-ga-015-introduction-and-edition/
6. Digital scholarly edition (manuscript transcription must be checked directly): https://codexh.arts.gla.ac.uk/
7. Vidal-Gorène & Kindt (2026), *The Patrologia Graeca Corpus*, LREC, https://aclanthology.org/2026.lrec-1.517/ ; data repository https://github.com/calfa-co/Patrologia-Graeca (PG085 absent from the inspected directory list).
8. Omont (1889), *Notice sur un très ancien manuscrit grec en onciales des Épîtres de Saint Paul*, printed p. 50 / PDF page 55, directly inspected typographic transcription K2–K6, Coislin 202, 11r: https://archive.org/details/noticesuruntrsa00omongoog/page/n54/mode/2up
9. Glasgow/INTF TEI 87r and metadata, acquired 2026-10-13, preserved with CC BY 4.0 attribution in `sources/`: https://codexh.arts.gla.ac.uk/data/G015-Images/87r/87r.xml ; https://codexh.arts.gla.ac.uk/data/output_data.json

**Reuse constraint.** This note paraphrases source catalogues, gives short textual examples for identification, and preserves the intellectual property and image rights of the source institutions. It contains no third-party facsimile, book PDF, full edition or unlicensed experimental material.

## G0.5 — source-specific K6 apparatus (2026-10-13)

New files: [CODH01_K6_VARIANTS.csv](CODH01_K6_VARIANTS.csv), [validate_variants.py](validate_variants.py) and [tests/test_variants.py](tests/test_variants.py). They keep four **catalogue-derived**, source-attributed records separate: Pinakes work-level desinit, BL Add. 28816 f.113, BL Harley 5557 f.264v and BnF grec 237 f.196v. All have `ga015_diplomatic_verified=false`.

The program strips diacritics solely to compare character sequences mechanically. It does **not** classify etymology, determine historical dependence among witnesses, establish a chronology of changes, or certify a facsimile reading. The three witness-level strings are non-identical to the work-level baseline under this normalization. These are *textual string differences*, not three established independent historical innovations.

A complete scanned *Patrologia Graeca* vol. 85 is locatable at https://commons.wikimedia.org/wiki/File:Patrologia_Graeca_Vol._085.pdf . Its indicated columns 785B–C have **not** been independently transcribed and compared with K2–K4 in this audit. Do not promote those missing rows. The full 2026 Greek edition or a direct reading of GA015 folios is still required for diplomatic collation.

**Scientific gate remains G0 PARTIAL; 0/6 Codex H Greek titles directly verified.** The change is a traceable variant test corpus, not a discovery about GA015 or a validated psychological effect.

### G0.6 reconciliation — superseding source-state correction (2026-10-13)

**Important: [G0.5's Glasgow TEI collation](CODH01_G05_COLLATION.md) supersedes the earlier statement that zero rubric *texts* were available for GA015.** The TEI edition supplies **five attributed texts, K2–K6**, on reconstructed folio 87r (= Paris BnF Coislin 202, fol. 11r). **K1 remains unknown in GA015**. The status field `ga015_greek_diplomatic_verified=false` refers strictly to absence of independent philological *certification*, not absence of an edited transcription. Do not conflate these conditions.

The additional [four-record K6 notice-level variant file](CODH01_K6_VARIANTS.csv) is a **supplement to, not a replacement for**, G0.5's richer GA015-versus-other-witness apparatus. It does not contain the GA015 TEI reading `παραινέσεις ... αἱριστικοὺς`, which belongs to the primary [G0.5 collation record](CODH01_COLLATION.json). Keep witness-specific orthographic differences separate from semantic claims. K2–K6 are *edition-level acquisitions*, **not** five independently validated facsimile readings. K1 and the complete bibliographic alignments are still open.

Workflow: the 7 new tests validate the four-row notice-level file only; previously documented G0.5 source files and tests remain authoritative for TEI and collation. Neither suite supplies a stemma, historically independent witness count, exhaustive body-text partition, or evidence for effects on readers. G0 partial, G1 not undertaken, G2–G3 blocked. PR stays **DRAFT**.


## G0.7 archive acquisition gate

A public official Glasgow TEI/XML dataset is identified as DOI [10.5525/gla.researchdata.2105](https://researchdata.gla.ac.uk/2105/), distinct from the on-request multispectral images DOI [10.5525/gla.researchdata.1865](https://researchdata.gla.ac.uk/1865/). See [G0.7 note](CODH01_G07_ARCHIVE_GATE.md) and [bounded ZIP inspector](inspect_glasgow_2105.py). The full archive could not be retrieved in this session and **no new K1 reading has been authenticated**. K2–K6 continue to be acquired edition-level texts without independent palaeographic certification. G0 remains partial, PR draft.
