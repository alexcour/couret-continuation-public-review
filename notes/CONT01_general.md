# CONT 01 Extrait mathématique général pour relecture

Version éditoriale du 6 octobre 2026. Les sections sont conservées avec leur numérotation de source. Les exemples et raccords FCI, ainsi que les liens internes, ont été retirés. Ces extraits chronologiques doivent être lus avec le statut actuel du README.

1. Question directrice
Pour une histoire h, une famille d’interventions admissibles U, une famille d’observables futurs Y et un horizon T, on regroupe les continuations pertinentes dans une spécification Q=(U,Y,T). Deux histoires sont équivalentes relativement à Q lorsqu’aucune intervention admissible ne permet de distinguer leurs lois de continuation.
h ~_Q h′  ⇔  K_h^π = K_h′^π pour toute politique π ∈ U.
Le programme vise ensuite quatre objets : l’équivalence ~_Q ; une pseudo-distance de continuation d_Q ; la perte de continuation d’une représentation L_Q(Φ) ; et la provenance minimale Ω_Q = H / ~_Q.

2. Objets de travail
Distance de continuation : d_Q(h,h′)=sup_{π∈U} W₁(K_h^π,K_h′^π), sous les hypothèses nécessaires pour que les lois de continuation soient comparables.
Perte par quotient : L_Q(Φ)=sup_{Φ(h)=Φ(h′)} d_Q(h,h′). Ainsi L_Q(Φ)=0 signifie que Φ ne fusionne aucune distinction pertinente pour Q.
Provenance minimale : Ω_Q est définie d’abord comme le quotient des histoires par l’équivalence de continuation. Une interprétation géométrique en termes de fibres, connexion, holonomie ou monodromie ne sera introduite que lorsqu’une structure supplémentaire la justifie.

3. Raccord avec l’ARC DE RECHERCHE CURRENT
Le document pose déjà la chaîne observation → fibres → perte d’information → reconstruction → transport et définit l’observabilité temporelle O_L=(A,A∘T,…,A∘T^{L−1}). CONT-01 prolonge cette grammaire en remplaçant la seule séparabilité d’états par l’équivalence des continuations sous interventions.
Statut : SOCLE CONCEPTUEL DÉJÀ PRÉSENT. La nouveauté éventuelle ne réside pas dans les fibres, les quotients ou l’observabilité en eux-mêmes.

7. TRI-002 : présent observable insuffisant, trajectoire séparante
Source CURRENT : « CU — Quotient (b,c) et perte d’orientation 2-adique — CURRENT » ; le registre épistémique identifie ce résultat comme TRI-002.
Le quotient observable satisfait Q_r(k)=Q_r(−k−1) et perd exactement un bit d’orientation relativement au compteur complet. Pour r≥3, deux observations successives déterminent à nouveau l’orientation.
Lecture CONT-01 : Φ(s)=Φ(s′) n’implique pas Φ(Ts)=Φ(Ts′). C’est un prototype déterministe exact où l’état instantané est insuffisant mais la trajectoire restaure la distinction.
Statut : THÉORÈME FINI / ARITHMÉTIQUE DÉJÀ ÉTABLI ; prototype de dépendance au chemin, non preuve d’un phénomène cognitif général.

8. Barning–Hall : endpoint contre trajectoire
L’endpoint modulo 30 sature à 48 états alors que les trajectoires observables continuent de distinguer une quantité croissante de mots. Des mots différents peuvent avoir le même endpoint modulo 30 tout en ayant des trajectoires différentes.
Lecture CONT-01 : ce document fournit un laboratoire combinatoire de compression de l’histoire et de collisions induites par une représentation finale.
Statut : PROTOTYPE DYNAMIQUE FINI ; excellent banc d’essai pour des versions déterministes de d_Q et L_Q.

9. HOL-01 : prototype géométrique de mémoire sur les fibres
Le revêtement Γ_49→Γ_7 possède 24 sommets en base, 1176 au niveau 49 et des fibres de cardinal 49. Des lacets de la base peuvent agir non trivialement sur la fibre.
Lecture CONT-01 : HOL-01 fournit un modèle exact où un retour au même observable de base peut coexister avec une transformation interne de la fibre. Il peut servir de laboratoire pour une éventuelle géométrisation de Ω_Q.
Garde : monodromie non triviale ≠ non-markovianité générale ; holonomie triviale ≠ markovianité ; Ω_Q n’est pas défini par la monodromie.
Statut : PROTOTYPE GÉOMÉTRIQUE FINI. HOL-01U reste une annexe classique / banc de contrôle, non une revendication de nouveauté.

10. Cayley 10A6 / 10C3 : suffisance relative au domaine et à la tâche
Dans le corpus U(210), certaines fibres spectrales contiennent plusieurs classes de digraphes : le spectre n’est donc pas suffisant pour la tâche générale « déterminer l’isomorphisme ». Dans la famille structurée de 10A6 pour p≥5, le document CURRENT énonce au contraire l’équivalence cospectralité ⇔ critère h ⇔ isomorphisme explicite.
Lecture CONT-01 : la suffisance doit toujours être indexée par un domaine et une tâche. Une même représentation peut être insuffisante sur un grand domaine et suffisante sur une sous-famille structurée.
Statut : ILLUSTRATION STRUCTURELLE. Aucun L_Q numérique n’est encore calculé pour cette branche.

11. Corrections de notation
Réserver désormais Ω_Q ou Ω_min à la provenance minimale définie par le quotient de continuation.
L’ancien défaut de transport noté Ω=A U_Q−U_q A dans certains documents sera renommé Δ_tr afin d’éviter toute collision de notation.

12. Théorèmes réellement ouverts
T1 — Pseudométricité : donner des hypothèses suffisantes pour que d_Q soit une pseudo-distance et identifier précisément son quotient métrique.
T2 — Suffisance par fibres : caractériser L_Q(Φ)=0 en termes de factorisation des noyaux de continuation à travers Φ.
T3 — Compression approchée : relier L_Q(Φ)≤ε à une borne explicite de regret, de valeur ou de décision pour une classe d’interventions spécifiée.
T4 — Défaut de commutation observable : si deux ordres d’intervention sont identiques sous Φ mais restent séparés par d_Q, prouver que Φ est insuffisante pour Q. La non-commutativité seule ne doit jamais être interprétée comme preuve d’un état latent.
T5 — Provenance minimale : établir existence, minimalité et éventuellement unicité de Ω_Q dans des catégories de systèmes précis, sans réinventer les causal states, predictive state representations ou information states.
T6 — Viabilité sous compression : borner la différence entre un noyau de viabilité calculé sur l’histoire complète et celui calculé à partir d’une représentation Φ en fonction de L_Q(Φ), sous hypothèses régulières explicites.

14. Frontière de nouveauté
Ne pas revendiquer comme nouveaux : états causaux minimaux, predictive state representations, information states, métriques de bisimulation, predictive rate-distortion, mémoire dans la théorie de la viabilité, ou non-commutativité en général.

15. Critère directeur
Question de recherche : quand peut-on oublier le chemin sans changer les futurs pertinents ?
Version quantitative : quelle est la représentation la moins complexe Φ telle que L_Q(Φ)≤ε ?
