# CONT-P v0.8 — confrontation théorique et contrôle de complexité

## Correction méthodologique apportée à v0.7
Comparer q=30 à q=30*l confond deux effets : l'ajout du facteur premier l et l'augmentation du nombre d'états φ(q). v0.8 construit donc une baseline avec des moduli 2,3,5-lisses et compare, à complexité comparable, le gain historique obtenu après ajout d'un nouveau facteur premier.

## Contrôle exact pour le facteur 7
q=180 et q=210 ont tous deux φ(q)=48. Dans la grande fenêtre 50M–100M, les gains historiques v0.6 sont environ 0.001430 et 0.000273 bit/symbole respectivement. À complexité exactement identique, la présence du facteur 7 absorbe donc environ 80.9% du gain qui subsiste dans le raffinement 2,3,5-lisse.

Ce contrôle est plus fort que la comparaison q=30 -> 210, car il ne confond pas l'effet arithmétique de 7 avec la dimension de l'état.

## Stabilité en échelle
Le fichier q180_vs_q210_factor7_effect.csv répète le même contrôle sur cinq fenêtres entre 10M et 100M. Fraction moyenne supprimée par le passage 180 -> 210 : 0.889; min 0.839; max 1.032.

## Lien avec Hardy–Littlewood / Lemke Oliver–Soundararajan
Pour un nouveau premier l ne divisant pas le modulus de base, le facteur local de la série singulière d'une paire diffère selon que l divise ou non l'écart. Le rapport local entre les cas l|h et l∤h vaut (l-1)/(l-2), soit un excès 1/(l-2). Le premier nouveau facteur possible, l=7, possède donc le contraste local le plus fort.

Le papier LOS 2016 va plus loin : son terme principal de biais c1 pénalise les répétitions adjacentes, tandis que c2 contient une structure arithmétique plus fine. Pour r>=3, le c2 du motif contient aussi un terme portant sur les égalités à distance supérieure à 1; le papier en déduit explicitement que les premiers modulo q ne sont pas markoviens d'ordre 1. Le suivi 2020 montre que c2 est lui-même un objet arithmétique complexe, relié à des sommes de Dedekind.

## Ce que v0.8 permet de dire
1. La non-markovianité des motifs de premiers n'est pas nouvelle : elle est déjà prédite par LOS.
2. Notre courbe G(Q), qui mesure combien d'information historique reste utile quand on raffine uniquement la représentation du présent, est une autre question.
3. Après contrôle de complexité, le facteur 7 reste un effet exceptionnellement fort dans les données testées. Pour 11, 13, 17, 19, 23, une grande partie de la baisse brute de v0.7 est expliquée par l'augmentation de φ(q).
4. Le contraste local Hardy–Littlewood explique qualitativement pourquoi 7 doit être le nouveau facteur le plus influent, mais il ne fournit pas directement la valeur de notre gain conditionnel en bits. Une dérivation spécifique à notre observable serait nécessaire pour une comparaison quantitative.

## Statut
EXPÉRIENCE FINIE ET REPRODUCTIBLE. Interprétation théorique prudente. Aucune revendication de nouveauté tant qu'une recherche bibliographique ciblée n'a pas exclu une formulation antérieure de la courbe de suffisance sous raffinement de l'état.

## Audit de nouveauté ciblé — correction importante
Une recherche web ciblée en octobre 2026 montre que l'usage de la CMI d'ordre 2 sur les triplets de résidus premiers n'est pas inédit : un préprint annoncé en mai 2026 étudie explicitement la CMI2 de (p_{n-1},p_n,p_{n+1}) modulo q jusqu'à 10^9. Un autre préprint de septembre 2026 étudie des défauts markoviens de noyaux de résidus jusqu'à 10^8. Ces travaux s'ajoutent naturellement à la non-markovianité déjà conjecturée par Lemke Oliver–Soundararajan en 2016.

Par conséquent, CONT-P ne doit revendiquer ni la découverte de la non-markovianité, ni l'introduction de la CMI appliquée aux résidus premiers. La piste de nouveauté à auditer est plus étroite : la courbe de suffisance sous raffinement du présent

G(Q) = gain prédictif hors échantillon apporté par X_{n-1}=p_{n-1} mod 30 pour prévoir X_{n+1}=p_{n+1} mod 30, conditionnellement à Y_n=p_n mod Q,

avec comparaison de moduli à complexité effective égale et ablation contrôlée des facteurs premiers.

## Correction du diagnostic v0.7
Après contrôle de complexité, le rôle attribué à 11,13,17,... doit être fortement atténué. Sur les facteurs testés jusqu'à 23, seul 7 produit un effet arithmétique massif qui survive au contrôle de dimension. Le contrôle exact q=180 versus q=210 est particulièrement propre car φ(180)=φ(210)=48.

Sur la grande fenêtre v0.6, le gain historique passe de ~0.001430 bit/symbole à q=180 à ~0.000273 à q=210, soit environ 80.9% de suppression à complexité exactement identique. Le test v0.8 répété sur cinq fenêtres entre 10M et 100M retrouve une suppression de l'ordre de 84% à 103% selon la fenêtre (la valeur >100% correspond à un gain q=210 légèrement négatif dans la plus petite fenêtre).

## Lecture Hardy–Littlewood
Pour un premier l absent du modulus de base, le facteur local de la série singulière d'une paire distingue l|h de l∤h. Le rapport des facteurs locaux vaut (l-1)/(l-2); l=7 est donc le nouveau petit premier donnant le contraste local le plus fort après 2,3,5. Cela rend qualitativement plausible son rôle exceptionnel. Toutefois notre observable est conditionnelle et à trois temps : les formules LOS de paires ne prédisent pas directement le gain G(Q) en bits. Une dérivation spécifique reste à faire.
