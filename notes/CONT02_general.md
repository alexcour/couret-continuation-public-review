# CONT 02 Extrait mathématique général pour relecture

Version éditoriale du 6 octobre 2026. Les sections sont conservées avec leur numérotation de source. Les exemples et raccords FCI, ainsi que les liens internes, ont été retirés. Ces extraits chronologiques doivent être lus avec le statut actuel du README.

0. Statut
Objet : donner un cadre minimal rigoureux à l’équivalence de continuation, à la distance d_Q, à la perte par quotient L_Q(Φ) et à la provenance minimale Ω_Q. Les résultats T1 et T2 ci-dessous sont des conséquences directes des propriétés d’une métrique sur les lois de probabilité et de la factorisation par fibres. Ils constituent un socle formel du programme, mais ne sont pas revendiqués comme nouveaux dans la littérature.
Frontière : la proximité avec les predictive state representations, les information states, les ε-transducers, les métriques de bisimulation et l’équivalence de Nerode est explicite. La nouveauté éventuelle doit être cherchée dans des extensions ou articulations non couvertes par ces cadres, pas dans T1/T2 eux-mêmes.

1. Cadre
Pour chaque histoire h∈H et chaque π∈Π, on suppose donnée une loi de continuation K_h^π sur Y. On suppose d’abord K_h^π∈P₁(Y), l’ensemble des lois à premier moment fini, de sorte que la distance de Wasserstein W₁ est définie.
On note Q=(Π,Y,ρ) la spécification de continuation. Un horizon fini ou d’autres paramètres peuvent être incorporés à Y ou à Π.

2. Définition de l’équivalence de continuation
Définition 2.1. Deux histoires h,h′ sont Q-équivalentes si elles induisent la même loi future sous toute intervention admissible :
h ~_Q h′  ⇔  K_h^π = K_h′^π pour tout π∈Π.
Cette relation est immédiatement une relation d’équivalence. Elle est relative à Q : modifier les interventions admissibles, les observables futurs ou l’horizon peut modifier les classes.

3. Distance de continuation
Définition 3.1. Posons
d_Q(h,h′)=sup_{π∈Π} W₁(K_h^π,K_h′^π).
Sans hypothèse supplémentaire, d_Q peut prendre la valeur +∞. Si ρ est bornée, ou si les familles de lois satisfont une borne uniforme adaptée sur leurs premiers moments, d_Q est finie.

4. Théorème T1 — pseudométricité
Théorème T1. La fonction d_Q est une pseudo-distance étendue sur H. Sous une hypothèse assurant sa finitude uniforme, c’est une pseudo-distance finie. De plus :
d_Q(h,h′)=0  ⇔  h ~_Q h′.
Preuve. La positivité, la symétrie et d_Q(h,h)=0 suivent de celles de W₁. Pour h,h′,h″ et tout π, l’inégalité triangulaire de W₁ donne W₁(K_h^π,K_h″^π)≤W₁(K_h^π,K_h′^π)+W₁(K_h′^π,K_h″^π)≤d_Q(h,h′)+d_Q(h′,h″). En prenant le supremum sur π, on obtient l’inégalité triangulaire pour d_Q. Enfin W₁(P,Q)=0 si et seulement si P=Q ; donc d_Q(h,h′)=0 exactement lorsque toutes les lois K_h^π et K_h′^π coïncident. CQFD.

5. Corollaire — espace métrique des états de continuation
Soit Ω_Q=H/~_Q et η_Q:H→Ω_Q la projection canonique. La formule
d̄_Q([h],[h′])=d_Q(h,h′)
est bien définie et donne une vraie distance sur Ω_Q. Ainsi la provenance minimale, au sens prédictif/interventionnel fixé par Q, n’est pas seulement un quotient ensembliste : elle porte naturellement la géométrie induite par d_Q.
Garde : cette « géométrie » est métrique. Elle ne fournit pas à elle seule une variété, une connexion, une courbure ou une holonomie.

6. Perte de continuation d’une représentation
Soit Φ:H→Z une représentation déterministe. On définit son diamètre maximal de continuation sur les fibres par
L_Q(Φ)=sup{d_Q(h,h′) : Φ(h)=Φ(h′)}.
Si l’ensemble considéré est vide dans un cas dégénéré, on adopte la convention appropriée au domaine ; dans les applications présentes, chaque fibre est non vide par définition sur Im(Φ).

7. Théorème T2 — suffisance par factorisation
Théorème T2. Les assertions suivantes sont équivalentes :
(i) L_Q(Φ)=0.
(ii) Pour tous h,h′, Φ(h)=Φ(h′) implique h~_Qh′.
(iii) Pour chaque π∈Π, la loi K_h^π est constante sur chaque fibre de Φ.
(iv) Pour chaque π∈Π, il existe une application unique K̄^π:Im(Φ)→P₁(Y) telle que K_h^π=K̄^π(Φ(h)) pour tout h∈H.
Preuve. (i)⇔(ii) vient de d_Q(h,h′)=0⇔h~_Qh′. (ii)⇔(iii) est la définition de ~_Q. (iii)⇒(iv) : définir K̄^π(z)=K_h^π pour n’importe quel h tel que Φ(h)=z ; la constance sur la fibre assure que cette définition est indépendante du représentant. L’unicité est immédiate sur Im(Φ). Enfin (iv)⇒(iii) est directe. CQFD.

8. Théorème T2bis — propriété universelle de Ω_Q
Théorème T2bis. Ω_Q est la représentation déterministe la plus grossière qui soit Q-suffisante, au sens suivant : si Φ:H→Z vérifie L_Q(Φ)=0, alors il existe une unique application g:Im(Φ)→Ω_Q telle que
η_Q = g ∘ Φ.
Preuve. Si Φ(h)=Φ(h′), la suffisance donne h~_Qh′ ; donc η_Q(h)=η_Q(h′). La projection η_Q est ainsi constante sur les fibres de Φ et se factorise de façon unique à travers Im(Φ). CQFD.
Corollaire. Une représentation suffisante Φ est minimale à isomorphisme près exactement lorsque ses fibres coïncident avec les classes de ~_Q. Dans ce cas Im(Φ) est en bijection canonique avec Ω_Q.

9. Première borne quantitative
Soit u:Y→R une fonction 1-Lipschitz. Par dualité de Kantorovich-Rubinstein, pour toute π et toutes histoires h,h′,
|E_{K_h^π}[u]−E_{K_h′^π}[u]| ≤ W₁(K_h^π,K_h′^π) ≤ d_Q(h,h′).
Donc, si Φ(h)=Φ(h′),
|E_{K_h^π}[u]−E_{K_h′^π}[u]| ≤ L_Q(Φ).
Pour une fonction C-Lipschitz, le membre de droite devient C·L_Q(Φ). Ce lemme donne un sens opérationnel immédiat à la perte L_Q, sans prétendre encore fermer T3 sur le regret de contrôle optimal.

11. Raccord à l’équivalence de Nerode
Dans un automate déterministe à sorties de type Mealy, deux états sont classiquement équivalents lorsqu’ils produisent les mêmes sorties pour tout mot d’entrée futur. La minimisation quotient alors l’automate par cette équivalence comportementale. La spécialisation déterministe précédente est donc de nature Nerode/Mealy.

12. Raccord à la littérature contrôlée
Predictive State Representations : Littman, Sutton et Singh représentent l’état par des prédictions multi-étapes conditionnelles aux actions futures. Cela recouvre déjà une part importante de l’idée d’état défini par ses continuations contrôlées.
ε-transducers : Barnett et Crutchfield étendent les causal states aux processus entrée-sortie avec mémoire, donnant un autre cadre voisin pour les équivalences de comportements conditionnés par les entrées.
Information states : Subramanian, Sinha, Seraj et Mahajan donnent des conditions de suffisance d’une fonction de l’histoire pour la programmation dynamique et des versions approchées avec bornes de sous-optimalité.
Bisimulation metrics : Ferns, Panangaden et Precup construisent des métriques comportementales pour les MDP et les relient aux différences de fonctions de valeur.
Conclusion bibliographique : T1 et T2 doivent être présentés comme fondations et normalisation du vocabulaire interne, non comme claims de nouveauté.

13. Ce qui reste réellement ouvert
O1 — Choisir Q de manière non arbitraire : quelles familles d’interventions et quels futurs doivent définir l’équivalence dans une application donnée ?
O2 — T3 : obtenir des bornes de regret ou de viabilité à partir de L_Q(Φ) pour des systèmes contrôlés sous hypothèses explicites.
O3 — T4 : construire des témoins d’ordre AB/BA qui certifient L_Q(Φ)>0 lorsque Φ fusionne les deux résultats, sans inférer abusivement l’existence d’un latent.
O4 — Étudier quand Ω_Q admet une mise à jour récursive fermée Ω_{t+1}=F(Ω_t,a_t,o_{t+1}); cette propriété est essentielle pour une mémoire réellement exploitable.
O5 — Étudier les liens précis entre Ω_Q, états prédictifs minimaux, PSR, bisimulation et information states afin d’isoler une contribution qui ne soit pas une simple reformulation.
O6 — Tester une géométrisation sur HOL-01 uniquement après avoir défini explicitement le foncteur ou le transport qui relie classes de continuation et fibres congruentielles.

14. Proposition de prochain théorème
Le prochain résultat utile n’est pas une abstraction supplémentaire. Il faut traiter la mise à jour récursive de Ω_Q : donner des conditions nécessaires et suffisantes pour qu’il existe une transition réduite F telle que la classe de continuation après une observation/action nouvelle soit calculable depuis la classe courante, sans relire l’histoire complète.
Dans le cas déterministe, cela conduit naturellement à une congruence à droite ; dans le cas stochastique contrôlé, cela rejoint la notion d’état d’information actualisable. C’est le point où le programme peut passer de « quotient prédictif » à « mémoire opérationnelle ».
