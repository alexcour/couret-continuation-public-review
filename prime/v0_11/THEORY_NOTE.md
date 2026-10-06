# CONT-P v0.11 — condition de consécutivité dans un modèle semi-analytique

## Modèle
Pour Q in {180,210}, on conditionne sur le présent y appartenant aux unités modulo Q.
Les gaps g1,g2 sont pondérés par

  w_Q(g1,g2) = exp(-(g1+g2)/log x) * S_Q({0,g1,g1+g2}),

où S_Q est la série singulière conditionnelle dont on retire les facteurs premiers divisant Q, déjà observés par le présent.

Le facteur exponentiel est la version Poissonisée de la condition de consécutivité mise en avant dans l'heuristique de Lemke Oliver–Soundararajan.

## Résultat canonique
- x milieu = 75,000,000
- Hmax = 180
- premiers locaux jusqu'à 199
- suppression modèle 180->210 = 73.545032%
- suppression observée = 80.893198%
- G210 prédit après calibration du seul niveau sur G180 = 0.000378306398809
- G210 observé = 0.000273227529
- fraction de la baisse observée reproduite = 90.916213%

## Lecture
Ce modèle incorpore explicitement deux ingrédients absents du proxy v0.10 :
1. l'admissibilité conditionnelle modulo Q ;
2. une pénalisation de consécutivité exp(-(g1+g2)/log x).

Il reste heuristique : la véritable inclusion-exclusion de LOS contient des termes secondaires plus fins, et l'indépendance Poisson n'est pas une identité pour les nombres premiers.
