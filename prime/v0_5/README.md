# CONT-P v0.5 — backoff hiérarchique

## Objet
Tester si l'histoire courte reste prédictivement utile lorsque les contextes rares sont régularisés vers le modèle du présent seul.

## Protocole
Fenêtre: 50M–100M. Split par blocs en trois ensembles disjoints: apprentissage, validation, test.
Pour chaque Q dans {30,210,2310,30030}, on compare:
- base: P(X_{n+1}|Y_n),
- histoire: P(X_{n+1}|Y_n,X_{n-1}),
régularisée par backoff hiérarchique vers la base.
Le poids de backoff tau est choisi sur validation puis figé avant l'évaluation test.

## Résultats test
- Q=30: gain historique +0.002181 bit/symbole.
- Q=210: gain historique +0.000277 bit/symbole.
- Q=2310: gain historique +0.000014 bit/symbole.
- Q=30030: gain historique -0.000010 bit/symbole.

## Lecture provisoire
Le signal historique utile décroît de façon très nette lorsque la représentation du présent est enrichie. Avec régularisation hiérarchique, le petit bénéfice historique observé modulo 30 subsiste faiblement à 210, devient pratiquement nul à 2310 et n'est plus détectable à 30030.

Ce résultat est compatible avec l'hypothèse suivante: une part substantielle de la « mémoire » observée modulo 30 est un effet de projection, c'est-à-dire une compensation par le passé d'information absente de la représentation présente.

Il ne s'agit pas d'une preuve asymptotique ni d'une preuve d'absence de mémoire intrinsèque. Il s'agit d'un résultat prédictif fini, hors échantillon.
