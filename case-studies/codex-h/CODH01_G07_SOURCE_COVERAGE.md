# COD-H-01 — G0.7 : couverture des sources de Tite et écarts de localisation

13 octobre 2026. **G0 partiel ; K1 non acquise pour GA 015 ; double validation philologique non effectuée ; aucune expérience sur lecteurs.** Ce complément poursuit G0.5 sans ajouter de titre antique ni d'intervalle biblique inféré.

## 1. Recherche de K1 et examen des transferts

L'index numérique acquis fournit **dix transcriptions étiquetées Tite** : une liste, huit pages du corps et une souscription. Les dix fichiers TEI ont été téléchargés, archivés sans modification et contrôlés par empreinte. Les numéros de rubriques de la liste sont seulement **2 à 6**. Aucune K1 n'est acquise dans ce corpus ; la formulation de Pinakes demeure au niveau de la tradition.

La fiche **86v = Coislin 202, 11rT** indique une image mais aucune transcription. L'image traitée a été examinée au niveau 11 : elle juxtapose des traces concurrentes et des caractères en miroir. Aucune chaîne attribuable avec assurance à K1 n'en a été extraite. La présence d'une image ne vaut pas récupération du texte transféré ; la couche du support ne doit pas être prise pour une nouvelle rubrique. Cela ne démontre ni l'absence historique de K1 ni son impossibilité de récupération.

Allen et Fowler (2025), *JBL* 144(1), annexe p. **195** (PDF p. **29**), décrivent 86v comme un transfert non récupérable dans l'état de leur relevé. Cette indication et l'absence de transcription dans l'index actuel sont compatibles ; elles ne localisent pas, à elles seules, K1 sur 86v. L'emplacement et le statut de K1 restent à demander aux éditeurs ou à établir sur des sources nouvelles.

## 2. Numérotation ancienne et références modernes : inventaire séparé

Le contrôle du TEI relève **cinq numéros dans la liste** et **un seul numéro dans le corps**, γ sur 90r. Il se trouve, dans l'encodage, à la fin du bloc `Titus.2.1`, immédiatement avant `Titus.2.2` ; les derniers mots avant la marque sont `ὑγιαινούση διδασκαλία`. Le relevé G0.5 d'un ancrage près de Tite 2,2 est ainsi confirmé à l'échelle du corpus numérique acquis. La vue d'ensemble de l'image 90r a été examinée, mais aucun arbitrage philologique indépendant n'est déclaré.

Les blocs `B17K1V5` et `Titus.1.5` sont des **références éditoriales modernes**, pas des preuves d'une rubrique ancienne K1. Le script ne compte comme numéro ancien que les éléments `num` portant `type="chapNum"`. Il n'invente pas de marques à partir des divisions XML ni des thèmes du texte.

Le corpus porte **26 références modernes distinctes**. Certaines ne couvrent que des fragments de versets, avec lectures incertaines et restaurations. Ce nombre n'est donc ni un nombre de versets intégralement récupérés ni un indicateur de certitude historique.

| Page de l'édition actuelle | Support de conservation | Contenu indiqué par l'index | Numéros de rubrique encodés |
|---|---|---|---|
| 87r | Coislin 202, 11r | Liste de Tite | β, γ, δ, ε, ϛ |
| 87v | Coislin 202, 11v | Tite 1,1–3 | Aucun |
| 88r | Coislin 202, 11vT | Tite 1,3–6 | Aucun |
| 89v | Coislin 202, 12rT | Tite 1,12–15 | Aucun |
| 90r | Coislin 202, 12r | Tite 1,15–2,2 | γ, entre les mots de 2,1 et ceux de 2,2 |
| 90v | Coislin 202, 12v | Tite 2,2–5 | Aucun |
| 91r | Coislin 202, 12vT | Tite 2,5–8 | Aucun |
| 92v | Coislin 202, 13rT | Tite 3,9–12 | Aucun |
| 93r | Coislin 202, 13r | Tite 3,13–15 | Aucun |
| 93v | Coislin 202, 13v | Souscription de Tite | Aucun |

« Aucun » signifie **aucun élément correspondant dans le TEI acquis**. Ce n'est pas une constatation d'absence sur tous les états ou toutes les images du manuscrit. Les bornes de l'index décrivent des pages, pas les intervalles K1–K6.

## 3. Écarts entre les sources de 2025 et l'édition numérique

Les pages imprimées 195 et 196 de l'article ont été rendues et inspectées pour vérifier les caractères et les références, sans s'en tenir à l'OCR. La cote et la face de conservation permettent de comparer les descriptions malgré des numéros reconstitués différents.

| Localisation de conservation | Tableau Allen–Fowler 2025 | Index / TEI acquis le 13 octobre 2026 | État |
|---|---|---|---|
| Coislin 202, 11vT | **88v**, Tite 1,3b–6a, p. 195 | **88r**, Tite 1,3–6 ; le TEI porte `pb n="88r"` | Écart r/v à clarifier ; aucune harmonisation silencieuse |
| Coislin 202, 12rT | **89v**, Tite 1,11b–15a, p. 195 | **89v**, Tite 1,12–15 ; premier bloc encodé `B17K1V12` | Écart de couverture initiale à clarifier ; ne pas ajouter 1,11 au TEI |
| Coislin 202, 14r | Article p. 196 : **96r** ; catalogue F.1, p. 324 : colophon à **95r** | **96r**, colophon dans l'index actuel | L'article et l'index concordent ; écart avec le catalogue à clarifier sans réassigner son 95r à la liste de Tite |

Aucune cause précise de ces écarts n'est démontrée. Ils peuvent relever d'une révision de la reconstruction, d'une différence de description ou d'une erreur ; le dossier ne tranche pas. L'écart 88r/v ne change pas la localisation matérielle de K2–K6 sur 11r.

## 4. Restaurations : portée réelle de l'observation

Le TEI de la liste contient **deux éléments `supplied` attribués à Omont** et **six éléments `unclear`**. Plusieurs pages transférées contiennent de nombreux éléments `supplied` attribués à **NA28**. Ces segments sont des restitutions explicitement documentées, pas des lettres matériellement lues avec certitude. Les comptes par page et par source sont conservés dans `CODH01_TITUS_SOURCE_INVENTORY.json`.

Ni un texte complété par une édition moderne ni la proximité thématique d'un passage ne peut fournir une limite de rubrique manquante. La correspondance secondaire K5 / Tite 3,1–9 conserve son statut ; K6 / Tite 3,10–15 ne devient pas une lecture vérifiée. Les six `complete_biblical_span` restent inconnus et les six indicateurs de validation diplomatique indépendante restent faux.

## 5. Sources encore à acquérir et questions philologiques précises

1. **K1 :** existe-t-il une lecture, une restauration déclarée ou seulement une reconstruction par analogie ? Sur quelle page, quelle bande ou quel transfert ? Le fichier actuel 87r ne comporte pas l'entrée α.
2. **Foliotation :** comment réconcilier 88v/88r pour 11vT et le 95r du catalogue F.1 avec le 96r de l'article et de l'index pour le colophon ? Quelle version doit être citée ?
3. **Couverture de 89v :** le segment 1,11b du tableau de 2025 est-il identifié dans l'état éditorial actuel ou exclu du TEI ?
4. **Ancrages :** quels numéros de rubriques sont matériellement attestés pour K1, K2, K4, K5 et K6 ? Une liste de thèmes ne suffit pas à fournir leurs intervalles complets.
5. **Lectures et couches :** arbitrer K5/K6 et les deux sigma restitués ; distinguer encre première, réencrage, diacritiques et transferts ; fournir deux transcriptions indépendantes et résolution des divergences.

Le téléchargement Google Books rencontré présente un CAPTCHA. Une autre copie publique de PG 85, déjà signalée dans G0.6 sur Wikimedia Commons, a ensuite été acquise : **113 582 035 octets, 957 pages**, empreinte conservée. Les pages physiques **393 et 394** ont été rendues et examinées. **La colonne 785 donne II Timothée ; la liste grecque de Tite est en 788B–C, face à la traduction latine 787B–C.** Le renvoi Pinakes à 785B–C est donc à distinguer de la localisation observée dans cet exemplaire ; nous corrigeons notre repérage bibliographique, sans modifier la notice officielle. Blomkvist p. 57 reste à consulter.

### Comparateur imprimé PG 85 : six rubriques, aucune nouvelle lecture de GA 015

Le relevé ci-dessous conserve les mots de l'imprimé ; les césures sont réunies et les appels de notes (31)/(32) sont séparés. C'est une **transcription de travail de l'édition imprimée**, sans double validation des diacritiques ni identification indépendante de chaque manuscrit de base. Elle complète la comparaison documentaire ; elle ne remplace aucune lecture du Codex H.

| Rubrique | Grec relevé dans PG 85, 788B–C | Ancrage de départ indiqué dans la colonne latine 787B–C |
|---|---|---|
| K1 | Περὶ διδασκάλων ἐπιτηδείων πρὸς διακονίαν, καὶ ἔλεγχον ἀπειθῶν. | Aucun renvoi explicite dans cette entrée |
| K2 | Κατὰ τῶν σαρκικὰς καθάρσεις πρεσβευόντων, καὶ ὑπὲρ πνευματικῆς ἀρετῆς. | 1,10 ; Palat. : 1,15 |
| K3 | Παραινέσεις, ὡς δεῖ παραινεῖν καθ’ ἡλικίαν ἐκάστοις. | 2,2 |
| K4 | Περὶ δούλων, ὡς ἂν καὶ αὐτοὶ τῆς Χριστοῦ χάριτος ἀξίως δουλεύοιεν. | 2,9 |
| K5 | Περὶ ἀρχόντων ὑπακοῆς πρεπούσης τῇ ἐπιεικείᾳ τοῦ Χριστοῦ. | 2,15 ; Cryp. : 3,1 |
| K6 | Παραίνεσις περὶ τοῦ ἐκκλίνειν τοὺς ἐριστικοὺς ζητητάς. | Cryptoferratensis : 3,10 ; Palatinus : 3,9 |

Les renvois sont des **ancrages de l'édition et de témoins désignés par elle**, jamais des étendues complètes ni des localisations GA 015. On conserve les désignations historiques *Palat.*, *Cryp.*, *Cryptoferratensis* sans leur attribuer une cote moderne non vérifiée. Aucun intervalle de fin n'est déduit du titre suivant.

Différences attestées entre les sources consultées : K1 **πρὸς** dans cet imprimé / **εἰς** dans Pinakes ; K3 **ὡς** dans PG / **ἂς** dans le TEI de GA 015 ; K5 **τοῦ Χριστοῦ** dans PG / **τῶν χυ** dans le TEI ; K6 singulier et **ἐριστικοὺς** dans PG / pluriel et **αἱριστικοὺς** dans le TEI. Ce sont des différences de leçons attribuées, sans conclusion nouvelle sur leur origine ou leur sens.

L'apparat imprimé note (31) **δουλεύσειεν** pour le *Regio-Alexandrinus* et un manuscrit vatican n° 363 ; note (32) **αἱρετικοὺς** pour *Palatinus*, *Urbinas*, l'édition stéphanienne et Œcumenius. Les identités modernes et les images de ces témoins ne sont pas vérifiées ici. Ne pas les confondre avec les variantes BL Add. 28816 ou Harley 5557.

Le fichier `CODH01_PG85_TITUS_COLLATION.json` conserve les six leçons et chaque statut séparément. **K1 est mieux documentée dans la tradition imprimée ; son grec GA 015 reste inconnu.**

## 6. Vérifications et état du dossier

`audit_titus_sources.py` vérifie les empreintes, le format TEI, la concordance de foliation et l'inventaire des seuls fichiers disponibles. **24/24 tests locaux PASS**, y compris rejet d'un fichier source modifié ou manquant et séparation références modernes / numéros anciens. Le validateur des quatre notices de variantes K6 ajouté entre les deux phases a été conservé et rejoué : PASS. Les deux contrôles sont intégrés au workflow documentaire.

**G0 reste partiel ; G1 n'est pas engagé ; G2 et G3 ne sont pas engagés.** Les succès logiciels ne sont ni un examen philologique indépendant ni une preuve d'exhaustivité du manuscrit. Aucune découverte historique ni mesure cognitive nouvelle n'est revendiquée.

## Références et provenance

- Allen et Fowler, *The Story of Codex H (GA 015)*, *JBL* 144(1), 2025, 167–196 : https://eprints.gla.ac.uk/342036/ ; PDF effectivement consulté https://eprints.gla.ac.uk/342036/2/342036.pdf ; annexe pp. 195–196, PDF pp. 29–30.
- Index de l'édition : https://codexh.arts.gla.ac.uk/data/output_data.json ; empreinte du fichier complet acquise en G0.5 et conservée dans l'extrait de métadonnées.
- TEI : https://codexh.arts.gla.ac.uk/data/G015-Images/88r/88r.xml ; https://codexh.arts.gla.ac.uk/data/G015-Images/89v/89v.xml ; les dix fichiers et leurs empreintes sont conservés sous `sources/` avec les déclarations de licence CC BY 4.0 et les attributions de G0.5.
- Images inspectées : https://codexh.arts.gla.ac.uk/data/G015-Images/86v/86v.dzi ; https://codexh.arts.gla.ac.uk/data/G015-Images/90r/90r.dzi. Elles ne sont pas republiées dans la PR.
- Catalogue F.1 : https://eprints.gla.ac.uk/346002/1/346002.pdf ; pp. 324–325.
- Exemplaire PG 85 repéré, sans collation de ses colonnes : https://books.google.com/books?id=ZZLYAAAAMAAJ&printsec=frontcover
- Fac-similé PG 85 effectivement consulté : https://commons.wikimedia.org/wiki/File:Patrologia_Graeca_Vol._085.pdf ; PDF https://upload.wikimedia.org/wikipedia/commons/1/19/Patrologia_Graeca_Vol._085.pdf ; grec de Tite, page PDF 394, col. 788B–C ; comparateur II Timothée, page PDF 393, col. 785.

Le PDF de l'article et les images ne sont pas joints au dépôt. Les écarts relevés sont des observations documentaires attribuées, pas des corrections soumises ou approuvées par les éditeurs.
