# CONT-P v0.2 — mémoire de continuation des nombres premiers

## Question
Avec X_n = p_n mod 30, le passé X_{n-1} apporte-t-il encore une information
sur X_{n+1} une fois le présent Y_n = p_n mod Q connu ?

Q testés : 30, 210, 2310.

## Ce que v0.2 ajoute
Un témoin nul paramétrique : pour chaque Q, on estime exactement la matrice
de transition empirique Y_n -> Y_{n+1}, puis on simule une chaîne de Markov
d'ordre 1 de même longueur. On reconstruit X_n = Y_n mod 30 et on mesure la
même information mutuelle conditionnelle.

Sous ce témoin, le présent Y_n est par construction un état markovien suffisant.
L'écart entre la CMI réelle et la CMI des simulations mesure donc un excès
historique qui n'est pas expliqué par une simple chaîne d'ordre 1 sur Y.

## Résultat exploratoire principal, fenêtre [50M,100M]
- Q=30  : CMI réelle ~0.002675 bit ; nul ~0.000103 ; excès ~0.002572.
- Q=210 : CMI réelle ~0.001463 bit ; nul ~0.000611 ; excès ~0.000852.
- Q=2310: CMI réelle ~0.006638 bit ; nul ~0.00623  ; excès ~0.00040.

La CMI brute à Q=2310 est dominée par le biais de dimension ; la comparaison
au témoin nul est donc plus informative que la valeur brute.

Interprétation prudente :
1. Une part importante du signal modulo 30 disparaît quand le présent est enrichi.
2. Un excès résiduel subsiste encore à Q=2310 dans cette fenêtre finie.
3. Cela ne prouve ni une « mémoire intrinsèque » des nombres premiers, ni une
   persistance asymptotique. Le phénomène peut encore provenir de termes
   arithmétiques secondaires, de non-stationnarité ou d'une représentation
   présente encore insuffisante.

## Prochaines étapes
- répéter le témoin nul sur plusieurs fenêtres ;
- tester Q=30030 si la taille d'échantillon le permet ;
- remplacer le maximum TV par des résumés robustes et des intervalles ;
- tester des historiques d'ordre 3, 4, ... ;
- comparer à des modèles arithmétiques théoriques de motifs consécutifs ;
- audit bibliographique avant toute revendication de nouveauté.

## Exécution
python cont_prime_memory_v0_2.py --max 100000000 --null-reps 100 --out-prefix cont_p

Dépendances : Python 3, numpy, pandas, numba.

## Statut
EXPÉRIENCE EXPLORATOIRE FINIE.
Pas de théorème asymptotique.
Pas de lien revendiqué avec RH.
