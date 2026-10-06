# CONT-P v0.4 — controles de stabilite et profondeur de memoire

## Statut
Calcul fini exploratoire. Aucun theoreme asymptotique, aucune memoire intrinseque et aucun lien RH ne sont revendiques.

## Resultat A — dependance a la taille d echantillon
Le signal residuel modulo 30030 est tres grand sur des fenetres de largeur 10 millions, mais chute fortement lorsque la fenetre augmente. Sur [10M,20M], [20M,40M], [50M,100M], l exces au-dessus du temoin markovien vaut respectivement environ 0.01663, 0.00583 et 0.00157 bit. Sur cinq sous-fenetres independantes de largeur 10M entre 50M et 100M, il reste proche de 0.020–0.022 bit.

Cette combinaison — stabilite a largeur fixe, forte baisse avec N — est un diagnostic fort d un effet de sparsity / estimation finie. Elle affaiblit nettement l interpretation d un rebond structurel propre a Q=30030.

## Resultat B — profondeur predictive hors echantillon
Sur [50M,100M], l ajout du passe au present modulo 30 ameliore la log-loss pour h=1 puis encore legerement pour h=2. A partir de h=3, la performance se degrade. Pour Q=210, 2310 et 30030, l ajout de X_(n-1) degrade deja la prediction hors echantillon avec le modele discret lisse utilise ici.

Lecture provisoire : modulo 30, une petite profondeur historique est predictivement utile; quand le present est enrichi modulo 210 ou davantage, ce benefice disparait dans ce protocole. Cela est compatible avec l hypothese qu une part importante de la memoire apparente modulo 30 provient d une projection trop pauvre du present.

## Limites
- Le temoin markovien est estime sur les memes fenetres et les triplets se chevauchent.
- Les z sont descriptifs, pas des p-values theorematiques.
- Les modeles d histoire sont des tables discretes avec lissage de Jeffreys; ils penaliseront fortement les contextes rares.
- A Q=30030 et h=4, environ 75.45 % des contextes de test n ont jamais ete vus en apprentissage : cette profondeur n est pas identifiable correctement a cette taille de donnees.

## Decision scientifique provisoire
Le signal le plus robuste a poursuivre n est plus le rebond Q=30030. Le resultat le plus propre est la dissociation suivante :
1. mod 30 : le passe court apporte un gain predictif hors echantillon ;
2. mod 210 et au-dela : ce gain disparait dans le modele actuel ;
3. le rebond apparent a 30030 est fortement dependant de la taille d echantillon.

Prochaine etape recommandee : controler cette dissociation par un modele hierarchique/backoff qui compare les representations a complexite effective comparable, puis etudier la loi de decroissance du gain historique avec la richesse du present.
