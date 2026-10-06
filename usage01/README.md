# CONT-USAGE-01 — Diagnostic de permissions et témoins rejouables

Un démonstrateur utilisable, fondé sur des méthodes classiques d'apprentissage
d'automates. Son objectif est de convertir une différence pertinente de passé en
un test concret : préparer deux histoires, appliquer la même suite d'actions,
observer les deux résultats et rejouer cette comparaison après une modification.

## Démarrage en une commande

Python 3.10 ou plus récent, sans dépendance externe. Décompresser l'archive, ouvrir
un terminal dans le dossier `CONT_USAGE01`, puis exécuter :

```bash
python3 run_demo.py
```

Le programme lance le service de test dans un **processus séparé**, apprend son
comportement par HTTP, génère les témoins, les rejoue et les oppose à un mutant.
Il arrête ensuite les services. Ouvrir `results/reference/report.html` dans un
navigateur : le rapport fonctionne hors ligne, permet de choisir un témoin et
de télécharger son test JSON. Les données déjà produites sont incluses dans
l'archive ; on peut consulter le rapport sans exécuter Python.

## Cas d'usage effectivement démontré

Le service gère un document avec un verrou et une approbation de validation.
L'écran ne présente que `READY` et `LOCKED`. Les actions déclarées sont :

| Action | Effet de la politique de référence |
| --- | --- |
| APPROVE | Une approbation devient disponible, même pendant un verrouillage. |
| EDIT | La modification invalide toute approbation précédente. |
| FAULT | Le document est verrouillé. |
| REARM | Le verrou est levé ; l'approbation est conservée. |
| COMMIT | Refus si verrouillé, refus sans approbation, validation sinon ; une validation consomme l'approbation. |

Témoin central, trouvé automatiquement :

| Branche | Statut à l'arrivée | Même action suivante | Résultat |
| --- | --- | --- | --- |
| APPROVE → EDIT | READY | COMMIT | BLOCKED_REVIEW |
| EDIT → APPROVE | READY | COMMIT | COMMITTED |

Les deux histoires donnent aussi les mêmes réponses `ACK, READY` pendant leurs
deux actions de préparation. Le statut courant et la dernière réponse échouent
donc tous deux à préserver la distinction utile. Une seconde collision, dans le
statut `LOCKED`, exige `REARM → COMMIT` pour être révélée. Une action seule ne
sépare pas les deux états verrouillés.

La mémoire générée compte quatre états de continuation. `monitor.py` fournit
`PredictiveMonitor` : il prédit la réponse, valide l'observation reçue et actualise
l'état sans relire le passé. Un désaccord laisse l'état inchangé et signale un
écart au modèle. La mémoire ne remplace pas les contrôles d'autorisation du service.

## Résultats inclus et vérification

L'exécution de référence identifie quatre états derrière deux statuts et examine
les 40 couples (état appris, paire d'actions distinctes non ordonnée). Elle génère
14 cas de régression : deux collisions du statut courant et douze divergences
liées à l'ordre. Les 14 sont rejoués avec succès sur la référence. Le mutant qui
conserve l'approbation après `EDIT` échoue sur quatre cas.

Les coûts exacts et les répartitions par phase figurent dans `summary.json`.
Il s'agit d'appels réellement exécutés sur le serveur HTTP local. Les préparations,
actions, libérations de session et requêtes servies par le cache sont distinctes.
Le coût de la mutation et celui des tests de développement sont séparés du coût
de l'expérience de référence ; les mesures ne prouvent aucun avantage de vitesse
par rapport à un outil existant.

```bash
python3 verify_results.py
python3 -m unittest discover -s tests -v
```

Le vérificateur n'importe ni le serveur cible, ni l'apprenant, ni le diagnostic.
Il reformule les règles sur une paire de booléens, vérifie toutes les transitions
du modèle, sa minimalité, les 40 paires d'ordre, les séparateurs minimaux des
témoins, l'ensemble du journal HTTP et le résultat du mutant. Les tests vérifient
aussi les refus de conclusion, les observations instables, les erreurs HTTP,
l'actualisation de la mémoire et la différence entre un ordre visible redondant
et un ordre pertinent.

## Raccorder une autre cible de test

Le diagnostic n'importe aucun état interne du service. Le contrat d'interface est :

1. `POST /prepare {}` crée une instance indépendante dans l'état initial convenu
   et renvoie `{"session": "identifiant", "view": "statut"}`.
2. `POST /step {"session": "identifiant", "action": "ACTION"}` renvoie
   `{"decision": "résultat", "view": "statut"}` après l'action.
3. Facultatif : `POST /release {"session": "identifiant"}` libère l'instance.

`interface.json` configure l'adresse, les chemins, l'alphabet et la borne d'états.
Ajouter `"token_env": "CONT_TEST_TOKEN"` si une authentification Bearer est
nécessaire ; la valeur est lue dans l'environnement et n'est pas journalisée.
Pour une API de forme différente, adapter `HttpAdapter.post/query` ou fournir
une passerelle qui expose ce contrat. Une URL et un fichier de configuration ne
suffisent pas à garantir que toute API est directement compatible.

Exemple avec le serveur de test inclus, dans deux terminaux :

```bash
python3 protocol_server.py --port 8765
```

```bash
python3 diagnose.py --config interface.json --out results/custom
python3 replay.py --config interface.json --cases results/reference/regression_cases.json --out results/regression
```

Le diagnostic apprend toujours depuis une préparation fraîche. Il ne suppose
aucun mot de remise à zéro dans le protocole testé. La préparation est une capacité
de la cible de test ou de sa passerelle ; elle n'est pas inventée par l'analyseur.
Les actions sont réellement exécutées sur les instances préparées.

## Sens exact des garanties

- L'alphabet et la projection observée sont explicitement déclarés. Ici chaque
  sortie contient `decision` et le statut `view` après l'action. Les identifiants
  de session et les temps d'exécution sont exclus.
- La cible doit être déterministe, stationnaire, complète sur cet alphabet,
  préparée fiablement dans le même état initial et posséder au plus `max_states`
  états prédictifs. Les tests W sont classiques et la certification est
  **conditionnelle** à ces hypothèses.
- La borne quatre vient des deux booléens des règles du service contrôlé, avant
  l'apprentissage. Elle ne vient pas de la taille du candidat appris. Pour une
  cible réelle, l'utilisateur doit apporter une borne justifiée. Une borne fausse
  peut invalider la garantie sans être toujours détectable.
- Une profondeur de découverte insuffisante ne devient pas une certification.
  Une erreur HTTP, une sortie non conforme, un changement lors d'une répétition
  ou un témoin non confirmé entraîne `INCONCLUSIVE` et un code de sortie 2.
  Le rejeu de régression renvoie 0 pour PASS, 1 pour FAIL, 2 pour INCONCLUSIVE.
- Les séparateurs sont les plus courts dans le modèle appris. Ici un vérificateur
  indépendant confirme leur minimalité sur le service fini de référence.
- Pour les continuations déterministes avec métrique discrète sur les traces,
  chaque témoin présentant le même `view` et des suites observables différentes
  donne une borne inférieure de 1 sur la perte de cette représentation. Le rapport
  ne prétend pas estimer des lois stochastiques par ces observations déterministes.
- Un statut différent peut être sans conséquence sur le futur. L'atlas examine
  le statut effectivement observé de chaque branche et la classe de continuation
  séparément ; il n'assimile pas un changement d'affichage à une mémoire utile.

## Ce qui est livré, ce qui reste à établir

Livré : une interface HTTP, un moteur générique de table d’observation, un diagnostic de projection,
un atlas d'ordre, une mémoire opérationnelle, des tests JSON, leur rejeu, un rapport
interactif autonome et des contrôles indépendants. La cible est différente du
modèle d’autorité conservé en privé et tourne de l'autre côté d'une frontière de processus HTTP.

Le service est un **banc contrôlé**, pas un connecteur déjà déployé chez un client.
La prochaine étape est un protocole réel en environnement de test, avec une
préparation sûre et une borne documentée. Il faudra comparer à LearnLib, AALpy
et ALEX sur la même cible, le même alphabet et les mêmes hypothèses : temps de
raccordement, opérations nécessaires, clarté des témoins et détection de régressions.
Cette comparaison et la validation d'un usage novateur ne sont pas encore faites.

## Provenance

`active_learner.py` et `conformance.py` sont repris à l'identique du moteur générique de CONT-04E. Les composants HTTP, diagnostic, mémoire, rejeu, rapport, serveur de
test et vérification sont ajoutés pour CONT-USAGE-01. Les méthodes classiques
ne sont pas revendiquées comme de nouveaux théorèmes.

- LearnLib : https://github.com/LearnLib/learnlib
- AALpy : https://github.com/DES-Lab/AALpy
- ALEX : https://learnlib.de/pages/alex

`SHA256SUMS` assure l'intégrité du paquet, à l'exclusion du manifeste lui-même,
des fichiers temporaires et des caches Python. Les résultats inclus sont figés ;
une nouvelle exécution les remplace et demande de recalculer le manifeste avant
de distribuer une nouvelle version.

## Préparation de diffusion du 6 octobre 2026

Les liens vers les dossiers privés ont été retirés. Le code et les résultats scientifiques
sont conservés. Le démonstrateur n’importe aucun modèle industriel ni aucun modèle
d’autorité privé. Le dossier parent porte les licences et le statut de relecture.
