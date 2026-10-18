# COD-H-01 — G0.10, audit TEI multi-corps (14 octobre 2026)

## Périmètre vérifié
La PR #3 demeure **ouverte, en brouillon**. La note G0.9 signalait pour le ZIP DOI 10.5525/gla.researchdata.2105 un seul `pb[@n]` dans le premier `body` analysé, aucune référence 86v/87r et aucun `chapNum n=1` dans ce sous-arbre. **Limitation importante mise au jour :** le script `probe_combined_tei.py` opère `next(...body...)`, donc ne parcourt que le PREMIER `body` et non nécessairement tous les `body` du document. Le premier inventaire affichait 12 noms de pages et 25 numéros au maximum : ce n'est pas une preuve d'exhaustivité.

Le nouveau `audit_combined_tei_global.py` examine **tous les TEI, text, body, pb, div, head, title et num**, même dans un `teiCorpus` possédant plusieurs `TEI`. Chaque valeur candidate est associée à son contexte de `body`, division et TEI ; les attributs de foliation et les mentions de Titus sont indexés ; les nombres 1 et références modernes du type `B17K1V5` ne deviennent jamais des lectures de la rubrique antique K1. La sortie JSON contient dénombrements globaux, inventaires par corps, empreintes SHA-256 du ZIP et du XML, et textes de rubriques potentielles limités à des extraits d'identification. Le script fonctionne avec `--download` et `--zip`. Deux tests synthétiques de corps TEI multiples et de séparation numéros anciens/références modernes ont été exécutés localement (**2/2 PASS**).

## Acquisition et reproductibilité
Source attendue : https://researchdata.gla.ac.uk/2105/1/2105_data.zip ; DOI 10.5525/gla.researchdata.2105.
Empreinte ZIP issue des workflows GitHub 38427473252 et 38428339654 : `c2c04b62d2f88171fd1805a5d4b41cb14da8138a7b0305acd30e118b93165d1f`.
Le runtime de calcul local a échoué à résoudre `researchdata.gla.ac.uk` (erreur DNS). Les journaux antérieurs attestent un téléchargement réussi depuis GitHub Actions ; la nouvelle exécution doit être validée en consultant sa CI et son artefact JSON, non présumée réussie. Le nouveau workflow `codh01-global-tei-audit.yml` lance les tests, télécharge le ZIP public, effectue l'analyse globale puis dépose un inventaire JSON en artefact 30 jours. **Aucune conclusion supplémentaire sur le contenu XML n'est prononcée avant examen du nouvel artefact.**

## Tri critique des leçons
- **Observation dans l'édition numérique GA 015 :** K2–K6 transcrites sur le TEI 87r = BnF Coislin 202, 11r ; K3 possède en outre un γ du corps encodé à 90r au voisinage de Tite 2,1/2,2. Deux segments K2/K5 comportent un sigma `supplied` attribué à Omont ; `unclear` et abréviations doivent demeurer distinctes des lectures sûres. Ces transcriptions sont des données d'édition, non deux lectures philologiques indépendantes de notre équipe.
- **Attestation éditoriale externe, non GA 015 :** la rubrique K1 de Pinakes emploie `εἰς` ; l'imprimé PG 85, 788B–C, donne `πρὸς`. Ni l'un ni l'autre ne certifie la leçon de GA 015. Le témoin imprimé indique des repères de départ variables pour certaines rubriques, sans étendue biblique complète certifiée dans GA 015.
- **Comparaison Allen–Fowler :** 2025 donne Coislin 11vT comme 88v et début Tite 1,11b en 89v ; les TEI/index actuels donnent 88r et début 1,12. L'écart 95r (catalogue F.1) / 96r (article/index) pour le colophon reste ouvert. L'état de transfert de 86v décrit comme non récupérable à cette étape ne fixe pas K1 sur cette page.
- **Donnée négative strictement limitée :** K1 non présente parmi les cinq entrées K2–K6 du TEI 87r ; sur l'image 86v examinée auparavant, aucune lecture sûre de K1 ; la place matérielle, la formule et les bornes GA 015 demeurent **INCONNUES**.

## Gate
G0 documentaire **PARTIEL** ; G0 diplomatique **NON FRANCHI** ; G1 collation indépendante **NON ENGAGÉE** ; G2/G3 bloqués. Aucun intervalle de six unités, aucune reconstitution K1, aucune étude cognitive, aucune revendication de découverte. Le courrier envoyé à Garrick Allen le 13 octobre ne doit PAS être renvoyé. Le dossier reste **DRAFT**.

## Suites
1. Lire le journal et surtout l'artefact complet de la nouvelle CI ; comparer son empreinte ZIP à celle du 13 octobre.
2. Déterminer le nombre global de `TEI`, `body`, `pb`, les balises et conventions pour la page et la rubrique, y compris dans les en-têtes.
3. Séparer explicitement *absence de codage*, *absence de transcription*, *perte du support*, *illisibilité* et *absence historique de rubrique*.
4. En cas de nouvelle absence de 86v/87r, établir la couverture réelle du corpus déposé, indépendamment des dix XML Titus de l'édition en ligne.


## G0.11 — confirmed global inventory, 14 October 2026
GitHub Actions global workflow [run 38529032636](https://github.com/alexcour/couret-continuation-public-review/actions/runs/38529032636), job `115736157135`, **SUCCESS** after fixing test import path at commit `8dd79994af32ec656dae49110b92c695a5a5e9e2`. Its two synthetic tests PASS, archive download PASS, full 125-body scan PASS, JSON artifact upload PASS. Previous workflow 38528501206 had failed *before acquisition* with ModuleNotFoundError, so no palaeographic interpretation of that earlier failure.

Parsed log observation: archive root `teiCorpus`, 125 TEI, 125 `text`, 125 `body` and 125 `pb`. **Folio 87r is present** as the page break in body #112, carrying five ancient `chapNum` values **2, 3, 4, 5, 6**. **Folio 86v is absent from the 125 `pb@n` values**, not evidence it was absent from the ancient manuscript. Folio 90r occurs in body #116 and includes a `chapNum` 3, consistent with the previously archived separately acquired TEI. All `num type=chapNum` number 1 records in this corpus are elsewhere: body #62 (no inscribed text in this emitted record) and body #89 (`α`, `inscriptio`). **Neither is a Titus K1 claim**. Titus-labelled chapter divisions occur in bodies #113, #116 and #120; these are `div type=chapter` for modern biblical references and must not be mistaken for six ancient kephalaia.

**Important correction to G0.9:** that older script operated only on the *first* `body` of a multi-TEI corpus and therefore incorrectly suggested one page and no 87r as if those were corpus-wide. The G0.11 full scan supersedes those purported global counts, while retaining G0.9 as an auditable historical record. The result does NOT authenticate or locate K1. Absence of an encoded `pb@n=86v` means merely that this deposited TEI corpus does not index such a page by that identifier. The earlier inspected image of 86v still lacks a defensible reading. Do not silently import PG85/Pinakes K1 into GA015.

The JSON inventory is a GitHub Actions artifact `codh01-global-tei-structure` (30-day retention). Preserve the output SHA-256 and page index in the archive of the review, and do not publish a historical reconstruction from automatic keyword matches. The relevant historical foliation discrepancies with Allen–Fowler, the Omont dependencies, and editorially supplied letters remain as stated in G0.7. G0 documentary partial, G1 not undertaken, G2/G3 blocked, PR #3 DRAFT; editor already contacted 13 October, no duplicate email.
