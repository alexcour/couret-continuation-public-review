# CONT 04 Extrait mathématique général pour relecture

Version éditoriale du 6 octobre 2026. Les sections sont conservées avec leur numérotation de source. Les exemples et raccords FCI, ainsi que les liens internes, ont été retirés. Ces extraits chronologiques doivent être lus avec le statut actuel du README.

0. Statut et objectif
Objet : transformer l’intuition « A puis B n’est pas nécessairement B puis A » en un outil mathématique précis pour le programme Continuation–Provenance. Le but n’est pas de présenter la non-commutativité comme nouvelle, mais de distinguer la non-commutativité brute d’un système de la non-commutativité qui reste pertinente pour les continuations définies par Q.
Résultat directeur : une paire d’ordres AB/BA qui est fusionnée par une représentation Φ mais reste séparée par d_Q constitue un témoin explicite de perte de continuation. Ce témoin fournit une borne inférieure sur L_Q(Φ).

1. Cadre déterministe minimal
Soit H un espace d’histoires ou d’états opérationnels et soit T_a:H→H l’opérateur associé à une intervention élémentaire a. Pour deux interventions a,b et une histoire h, on note
h_ab = T_b(T_a(h))   et   h_ba = T_a(T_b(h)).
L’ordre des indices décrit l’ordre temporel : h_ab signifie a puis b.
On conserve la spécification de continuation Q et sa pseudo-distance d_Q de CONT-02. Soit également Φ:H→Z une représentation candidate.

2. Trois notions qu’il faut séparer
Non-commutativité structurelle : T_b∘T_a ≠ T_a∘T_b comme applications sur H, ou au moins h_ab≠h_ba pour une histoire h.
Non-commutativité représentée : Φ(h_ab)≠Φ(h_ba). L’ordre est alors visible dans la représentation choisie.
Non-commutativité de continuation : d_Q(h_ab,h_ba)>0. L’ordre modifie alors une distinction pertinente pour les futurs spécifiés par Q.
Ces trois propriétés ne sont pas équivalentes. Une différence microstructurale peut être future-équivalente ; une représentation peut distinguer des différences sans conséquence ; et une représentation peut au contraire fusionner deux états dont les continuations diffèrent.

3. Tableau des quatre régimes représentation/continuation
Régime I — Φ(h_ab)=Φ(h_ba) et d_Q(h_ab,h_ba)=0 : l’ordre est invisible pour Φ et sans conséquence pour Q.
Régime II — Φ(h_ab)=Φ(h_ba) et d_Q(h_ab,h_ba)>0 : mémoire d’ordre cachée par Φ. C’est le régime critique pour le programme.
Régime III — Φ(h_ab)≠Φ(h_ba) et d_Q(h_ab,h_ba)=0 : effet d’ordre visible mais redondant pour Q.
Régime IV — Φ(h_ab)≠Φ(h_ba) et d_Q(h_ab,h_ba)>0 : effet d’ordre à la fois visible et pertinent.

4. Définition — défaut de commutation de continuation
Pour une histoire h et deux interventions a,b, on définit
κ_Q(a,b|h)=d_Q(h_ab,h_ba).
κ_Q mesure uniquement la différence qui subsiste au niveau des continuations pertinentes. Il ne dépend pas d’une métrique arbitraire sur l’état brut.
Si κ_Q=0, les deux ordres peuvent être structurellement différents mais sont identiques pour la tâche Q. Si κ_Q>0, l’ordre a une conséquence future mesurable dans la géométrie de continuation.

5. Définition — défaut caché par une représentation
Pour une représentation Φ, on définit le défaut d’ordre caché global
C_Q(Φ)=sup { d_Q(h_ab,h_ba) : Φ(h_ab)=Φ(h_ba), h∈H, a,b admissibles }.
Le supremum porte uniquement sur les commutateurs dont les deux endpoints sont fusionnés par Φ. C_Q(Φ) mesure donc la part de non-commutativité future-pertinente qu’un test AB/BA peut révéler à l’intérieur des fibres de Φ.

6. Théorème C1 — borne par la perte de continuation
Théorème C1. Pour toute représentation Φ,
C_Q(Φ) ≤ L_Q(Φ).
Preuve. Toute paire (h_ab,h_ba) intervenant dans le supremum de C_Q(Φ) vérifie Φ(h_ab)=Φ(h_ba). Elle appartient donc à une même fibre de Φ. Or L_Q(Φ) est le supremum de d_Q sur toutes les paires appartenant à une même fibre. Le supremum sur la sous-famille des paires générées par échange de deux interventions ne peut excéder le supremum sur toutes les paires de fibre. CQFD.
Corollaire. Si un seul témoin vérifie Φ(h_ab)=Φ(h_ba) et d_Q(h_ab,h_ba)=δ>0, alors
L_Q(Φ) ≥ δ > 0.
Un test d’ordre fournit donc un certificat constructif d’insuffisance de représentation.

7. Théorème C2 — critère de sûreté pour une représentation suffisante
Théorème C2. Si L_Q(Φ)=0, alors tout couple d’ordres AB/BA que Φ fusionne est Q-équivalent :
Φ(h_ab)=Φ(h_ba) ⇒ d_Q(h_ab,h_ba)=0.
C’est simplement la spécialisation de la suffisance par fibres de CONT-02. Sa valeur opérationnelle est sa contraposée : un seul commutateur caché de continuation strictement positif réfute la suffisance de Φ.

8. Le test AB/BA n’est pas complet
C_Q(Φ)=0 n’implique pas nécessairement L_Q(Φ)=0. Les collisions les plus graves d’une représentation peuvent provenir de chemins plus longs, de bifurcations qui ne sont pas obtenues par simple échange de deux actions, ou de différences de provenance sans paire commutée correspondante.
Ainsi C_Q est une sonde et une borne inférieure, non une caractérisation générale de L_Q.
Programme naturel : étendre le test à des relations de mots w≈w′, à des boucles et à des commutateurs itérés.

9. Non-commutativité pertinente sur le quotient minimal
Supposons Ω_Q opérationnel au sens de CONT-03 et supposons que les interventions a,b induisent des applications F_a,F_b sur Ω_Q. La distance quotient d̄_Q de CONT-02 permet de définir
κ̄_Q(a,b|ω)=d̄_Q(F_b(F_a(ω)), F_a(F_b(ω))).
Cette quantité est la version intrinsèque du défaut d’ordre : toutes les distinctions Q-inutiles ont déjà été quotientées.
On a κ̄_Q(a,b|[h])=κ_Q(a,b|h) lorsque les opérateurs sont compatibles avec la projection H→Ω_Q.

10. Théorème C3 — commutation sur Ω_Q
Théorème C3. Les interventions a et b commutent sur l’état de continuation Ω_Q si et seulement si κ̄_Q(a,b|ω)=0 pour tout ω∈Ω_Q.
Dans ce cas, l’ordre a puis b ou b puis a ne modifie aucune continuation pertinente définie par Q, même si les deux séquences peuvent produire des micro-états différents dans un espace plus fin.
Inversement, κ̄_Q>0 pour un état ω signifie que l’ordre transforme réellement l’état de continuation minimal.

13. Rapport avec l’intuition « l’acte transforme celui qui agit »
Mathématiquement, l’intervention a ne se contente pas de produire une sortie : elle transforme l’état depuis lequel b sera appliquée. L’expression
F_b(F_a(ω))
signifie que b agit sur l’état déjà transformé par a. Inverser l’ordre signifie donc appliquer les mêmes transformations à des états intermédiaires différents.
Le contenu scientifique de cette idée n’est pas une doctrine philosophique de l’identité ; c’est la dépendance compositionnelle de l’état opérationnel et de son espace de continuations.

14. Relation avec les effets d’ordre en sciences cognitives
Les effets d’ordre des questions et jugements sont documentés en sciences cognitives et ont notamment été modélisés par des opérations non commutatives dans la quantum cognition. Wang et Busemeyer ont développé un modèle quantique des effets d’ordre de questions et testé une égalité quantitative sur plusieurs jeux de données.
CONT-04 n’adopte pas pour autant un modèle quantique. Son objet est plus abstrait : comparer les continuations après deux séquences d’interventions et mesurer ce qui reste pertinent après quotient par ~_Q.
La présence d’un effet d’ordre empirique ne suffit donc pas à conclure à une structure quantique, à une variable cachée ou à une provenance minimale particulière.

15. Ne pas confondre avec le do-calculus statique
Les symboles a,b de CONT-04 représentent des interventions séquentielles qui transforment l’état du système entre deux temps. Ils ne doivent pas être identifiés sans précaution à une simple composition formelle de do-opérateurs statiques dans un modèle causal structurel.
Le phénomène étudié ici vient précisément du fait que la seconde intervention agit sur un système déjà modifié par la première. Le cadre causal exact devra donc expliciter le temps, l’état et la règle de transition.

16. HOL-01 : non-commutativité structurelle déjà établie
HOL-01 contient deux lacets γ₁ et γ₂ de Γ_7 dont les transports sur la fibre de 49 points ne commutent pas. Dans les coordonnées affines F_7², leur commutateur est calculé comme une translation non triviale. Le sous-groupe engendré est compatible avec UT_3(F_7).
Cela fournit un exemple exact de non-commutativité de transport sur une fibre. Mais CONT-04 impose une garde supplémentaire : cette non-commutativité n’est un défaut de continuation que relativement à une spécification Q qui distingue effectivement les conséquences futures des différents points de fibre.

17. HOL-01 montre aussi pourquoi Q est indispensable
Prenons comme représentation Φ la réduction modulo 7. Deux relèvements d’une même fibre ont le même observable modulo 7. Si Q ne regarde que les trajectoires futures modulo 7 sous les mêmes mots de générateurs, alors les relèvements restent projetés sur la même trajectoire de base : la différence de fibre peut être invisible à Q malgré la monodromie non triviale.
Ainsi une monodromie non triviale ne force pas automatiquement d_Q>0 pour toute tâche.
Pour que HOL-01 devienne un témoin CONT-04, il faut choisir un Q sensible à une conséquence de la fibre — par exemple une observation fine, une décision ou une fonction future qui varie avec le relèvement — puis exhiber explicitement un séparateur.
Ce point est conceptuellement important : la provenance n’est pas « tout ce qui diffère dans le passé », mais ce qui ne peut être oublié sans modifier les continuations pertinentes.

18. Boucles, commutateurs et résidu de chemin
Le test AB/BA se généralise naturellement aux boucles. Si deux chemins γ,γ′ partent du même état représenté et reviennent au même observable Φ, on peut mesurer
R_Q(γ,γ′|h)=d_Q(T_γ(h),T_γ′(h)).
Lorsque γ′ est le chemin trivial, R_Q mesure un résidu de chemin pertinent pour Q. Lorsque γ et γ′ sont les deux ordres ab et ba, on retrouve κ_Q.
Cette formulation relie CONT-04 à la note « holonomie, Berry et résidu de chemin » sans identifier abusivement tout résidu à une holonomie géométrique.

19. Commutateur de groupe : seulement lorsque les inverses existent
Si les interventions sont bijectives et possèdent des inverses, on peut considérer la boucle de commutateur
[a,b]=a^{-1}b^{-1}ab
ou la convention inverse selon l’ordre adopté. Un résidu non trivial de cette boucle constitue un témoin plus intrinsèque de non-commutation.
Mais de nombreuses interventions réelles sont irréversibles — consommation d’un permis, dommage, apprentissage, décision administrative. Dans ce cas, la comparaison AB/BA est plus fondamentale que le commutateur de groupe, car les inverses n’existent pas.

20. Petite-boucle et crochet de Lie — piste conditionnelle
Si Ω_Q possède ultérieurement une structure de variété différentiable et si a,b sont les petits temps de flots lisses engendrés par des champs X,Y, la différence entre les deux ordres est gouvernée au premier ordre croisé par le crochet de Lie [X,Y].
Cette piste pourrait relier le défaut de continuation à une géométrie locale. Elle reste conditionnelle : CONT-04 ne démontre ni structure différentielle sur Ω_Q ni relation de courbure.

21. Hiérarchie des témoins d’ordre
Niveau O0 — différence brute : h_ab≠h_ba.
Niveau O1 — différence représentée : Φ(h_ab)≠Φ(h_ba).
Niveau O2 — différence de continuation : d_Q(h_ab,h_ba)>0.
Niveau O3 — différence de continuation cachée : Φ(h_ab)=Φ(h_ba) et d_Q(h_ab,h_ba)>0.
Niveau O4 — boucle observable fermée avec résidu Q-pertinent.
Niveau O5 — structure de transport/monodromie certifiée et résidu Q-pertinent compatible avec cette structure.
Cette hiérarchie évite de passer directement d’un simple effet d’ordre à une revendication géométrique ou causale forte.

22. Questions de recherche ouvertes
R1 — Caractériser les classes de systèmes où les transpositions adjacentes AB/BA suffisent à reconstruire toute la perte L_Q(Φ).
R2 — Généraliser C_Q(Φ) aux relations entre mots, puis déterminer un ensemble minimal de tests de chemins qui certifie L_Q(Φ)=0 dans les systèmes finis.
R3 — Définir une version stochastique où AB et BA induisent des distributions de classes Ω_Q plutôt que des endpoints déterministes.
R6 — Sur HOL-01, choisir un Q explicite et déterminer si le commutateur de monodromie produit une divergence de continuation mesurable ou reste invisible pour le Q choisi.

24. Positionnement bibliographique
Les effets d’ordre et les opérations non commutatives sont classiques en physique, en théorie des opérateurs, en systèmes dynamiques et dans certains modèles cognitifs. Wang et Busemeyer (2013) donnent un exemple majeur d’effet d’ordre en jugement modélisé par probabilité quantique.
Les graphes de Schreier, la monodromie et les commutateurs de groupes sont également classiques. HOL-01 apporte un objet arithmétique spécifique, mais sa nouveauté reste séparée de la nouveauté éventuelle de CONT.

25. Résultats de CONT-04
C1 : FERMÉ — C_Q(Φ)≤L_Q(Φ).
C2 : FERMÉ — une représentation Q-suffisante ne peut cacher aucun commutateur de continuation positif.
C3 : FERMÉ — sur Ω_Q, κ̄_Q mesure exactement la non-commutation pertinente des interventions induites.
HOL-01 : fournit une non-commutativité de monodromie, mais son statut comme défaut de continuation dépend encore du choix explicite de Q.
