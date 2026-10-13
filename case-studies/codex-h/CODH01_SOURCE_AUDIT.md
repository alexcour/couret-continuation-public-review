# COD-H-01 — Codex H, Titus, and the observability of paratext

**Status (2026-10-13): documentary working note / NOT PEER-REVIEWED / NO NEW THEOREM / NO EXPERIMENT PERFORMED.**  
Scope: Greek manuscript cataloguing, document reconstruction and an *unimplemented* protocol for studying present-day reading behaviour. This case is outside the stable mathematical claims of this repository. No theological inference or claim concerning historical reader cognition is made.

**Current source acquisition: G0.5.** [Detailed witness-specific collation](CODH01_G05_COLLATION.md) and [structured six-slot record](CODH01_COLLATION.json). The Glasgow TEI of reconstructed **87r**, explicitly mapped to **Paris, BnF, Coislin 202, 11r**, now supplies Greek edition entries **K2–K6**, with uncertainty and Omont-derived restorations retained. K1 is absent from this acquired page and remains tradition-level only. Five edition entries acquired does **not** mean five independently certified diplomatic readings. The older G0.4 record is a historical acquisition snapshot.

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
