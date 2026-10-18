# COD-H-01 — Sas d'admission des MSI réelles, v0.1

**État au 18 octobre 2026 : demande acceptée pour instruction, AUCUN fichier restreint reçu ni autorisation spécifique retrouvée.** Le présent code est un *contrôleur de métadonnées et d'empreintes* pour des fichiers locaux dont l'accès aura été **préalablement** autorisé ; ce n'est pas un chargeur d'images réelles, ni un outil de déchiffrement. Il ne comporte aucune donnée originale de Glasgow.

Références : dossier scientifique COD-H-01, addenda G0.12/G0.13 ; dépôt MSI [10.5525/gla.researchdata.1865](https://researchdata.gla.ac.uk/1865/), à ne pas confondre avec dépôt TEI 2105. La notice donne une licence générale CC BY-NC 4.0 mais celle-ci n'autorise pas automatiquement un transfert ni un partage des fichiers ou des produits dérivés. Les droits supplémentaires et les institutions détentrices doivent être examinés manuellement.

## Exécuter sans accès à Glasgow (Python 3.12, bibliothèque standard)

Depuis la racine du dépôt :

```bash
export PYTHONPATH=case-studies/codex-h
python -m unittest discover -s case-studies/codex-h/msi_intake/tests -v
python -m msi_intake.gate evaluate --manifest case-studies/codex-h/msi_intake/pending_request.example.json
# Code de sortie 2 ATTENDU : dossier BLOQUÉ, et rien n'est lu sur disque à part le JSON public.
```

Le `pending_request.example.json` est volontairement vide d'inventaire et de droits ; il **doit** échouer à franchir les portes. Les tests fabriquent des octets fictifs dans un répertoire temporaire : **aucune image multispectrale ni lettre grecque**. Les tests de réussite des empreintes sont des essais de logiciel avec une fausse autorisation explicitement fictive ; ils ne doivent jamais être cités comme approbation de Glasgow.

## Étapes à la réception éventuelle d'un lot

1. **Droits** : lire le courrier officiel complet hors dépôt public, vérifier identité du grantor, cotes et folios couverts, `inspect`, `process`, crops, dérivés, partage privé à des philologues, publication. Ne jamais mettre le courrier de droit, les liens de téléchargement ou les originaux dans la PR. Inscrire seulement une référence opaque au registre privé et une validation humaine nominative. Si incertain : `pending`.
2. **Correspondance** : obtenir du fournisseur la relation précise entre folio reconstruit `86v`, lieu de conservation `Coislin 202, 11rT`, capture, transfert et rôle des témoins. Documenter la source de cette relation ; ne jamais forcer par proximité avec 87r.
3. **Réception en coffre privé** : conserver les originaux en lecture seule, sans conversion ni renommage destructive. Enregistrer l'identifiant fournisseur, la taille, son SHA-256 communiqué, le rôle, les dates, les crédits, la licence et les exceptions. Indiquer `non fourni` pour toute information absente (pas `sans objet` par facilité).
4. **Métadonnées physiques** : relever, seulement lorsqu'ils existent réellement, filtre / bande / longueur d'onde, dimensions, profondeur, orientation/mirroir, gain/exposition, frame dark/flat, ordre d'acquisition et éventuelle recette de reconstruction publiée. L'absence de dark/flat limite toute interprétation radiométrique ; ne pas les simuler.
5. **Audit des empreintes** : uniquement après autorisation documentée *et* confirmation humaine de celle-ci, créer un manifeste privé conforme au schéma et exécuter `python -m msi_intake.gate verify-local --manifest /chemin/prive/manifest.json --source-root /chemin/prive/originaux --output /chemin/prive/rapport.json`. Sortie `HUMAN_REVIEW_REQUIRED` si toutes les empreintes et tailles fournisseur disponibles correspondent ; `HOLD_REFERENCE_UNAVAILABLE` si une référence fournisseur manque. Le rapport privé (mode 0600) conserve les nouvelles empreintes de réception. Cela signifie **intégrité locale uniquement**, et non analyse autorisée ou qualité spectrale.
6. **Validation séparée** : habilitation à la recherche, préenregistrement des ROI et zones témoins, contrôle du canal tenu à l'écart, estimation des erreurs de recalage et calibration, double lecture aveugle, communication à l'équipe d'Allen avec respect des droits. Aucune activation automatique du moteur synthétique sur les images réelles.

## Portes et interdictions

| Statut | Sens |
|---|---|
| `HOLD` | Permission, correspondance ou inventaire insuffisant. Aucun fichier local n'est ouvert. |
| `HOLD_ERROR` | Manifeste invalide ou preuve locale inaccessible. Rejet. |
| `HOLD_INTEGRITY` | Au moins un fichier local ne correspond pas à la taille ou empreinte fournisseur déclarée. |
| `HOLD_REFERENCE_UNAVAILABLE` | Empreinte/taille locales calculées, mais aucune comparaison complète au fournisseur n’est possible. |
| `MANUAL_EVIDENCE_REVIEW_REQUIRED` | Métadonnées autodéclarées présentes ; il faut revoir les preuves de droits hors logiciel avant de lire quoi que ce soit. |
| `HUMAN_REVIEW_REQUIRED` | Tests taille/SHA réussis localement, mais toujours aucune certification d'accès ou de lecture. |

L'outil **n'authentifie pas la signature du titulaire des droits** et ne transforme jamais un champ `granted` en autorisation juridique. Le statut doit être validé par une personne habilitée à partir des pièces originales avant exécution sur les données. Aucune image réelle, crop, rapport de pixels, fichier de droits ou token ne doit entrer dans les workflows publics de GitHub.

Le projet documentaire PR #3, le laboratoire synthétique PR #4 et la branche principale restent inchangés. **K1 = NON RECONSTRUITE ; G0 = PARTIEL.**