# CONT 05 Extrait mathématique général pour relecture

Version éditoriale du 6 octobre 2026. Les sections sont conservées avec leur numérotation de source. Les exemples et raccords FCI, ainsi que les liens internes, ont été retirés. Ces extraits chronologiques doivent être lus avec le statut actuel du README.

0. Statut et question directrice
Objet : relier le programme Continuation–Provenance aux travaux sur curiosité artificielle, learning progress, agents autotéliques, information gain et active learning, sans confondre ces littératures ni revendiquer comme nouveau le principe général d’exploration informative.
Question : si Ω_Q et L_Q(Φ) décrivent quelles distinctions du passé doivent être conservées pour prédire les continuations pertinentes, quelles expériences faut-il choisir pour découvrir ces distinctions avec le moins d’interactions possible ?
CONT-05 déplace donc le problème de la représentation vers celui de l’identification active : non plus seulement « quelle mémoire est suffisante ? », mais « quelle intervention réduit le plus vite notre incertitude sur la suffisance de la mémoire ? ».

1. Audit du rapport sur la curiosité artificielle
Le rapport fourni contient un socle correct : les récompenses basées uniquement sur l’erreur de prédiction peuvent être attirées par des sources de variabilité difficilement apprenables ; le learning progress vise au contraire les régions où la compétence ou le modèle s’améliore ; les architectures autotéliques choisissent des objectifs en fonction de leur intérêt d’apprentissage.
Cependant, le learning progress ne doit pas être présenté comme le principe universel ou unique de la curiosité artificielle. La littérature comprend aussi nouveauté, pseudo-comptages, information gain, désaccord d’ensembles, empowerment, exploration optimiste et autres objectifs intrinsèques.

2. Noisy TV : formulation corrigée
Pathak et al. (ICML 2017) définissent une récompense intrinsèque par erreur de prédiction dans un espace de caractéristiques appris par dynamique inverse, ce qui évite déjà une partie des variations incontrôlables des pixels. Le problème noisy-TV reste néanmoins un problème général pour les bonus de prédiction lorsque l’erreur est dominée par une variabilité irréductible ou par de l’information manquante.
Random Network Distillation (2018) a précisément été proposé pour réduire certaines causes du noisy-TV en utilisant une cible déterministe conditionnelle à l’observation. Il ne faut donc pas classer RND comme intrinsèquement aussi vulnérable qu’un prédicteur direct du prochain état ; sa robustesse dépend du type de stochasticité de l’observation et de la représentation.
Learning Progress Monitoring (Hou, An, Du ; prépublication 2025, ICLR 2026) récompense l’amélioration du modèle plutôt que l’erreur brute et annonce des propriétés de zéro-équivariance et de monotonie vis-à-vis d’un gain d’information sous les hypothèses de son modèle. Cette relation ne doit pas être généralisée à toute définition du learning progress.

3. Learning progress et cognition humaine
Ten et al. (Nature Communications, 2021) fournissent des résultats expérimentaux selon lesquels les humains suivent leur progrès d’apprentissage pendant une exploration motivée par la curiosité.
Molinaro, Colas, Oudeyer et Collins (NeurIPS 2024, N=175) montrent qu’un modèle de latent learning progress contribue à expliquer la sélection autonome des buts dans une tâche hiérarchique. Le résultat soutient l’influence du LLP dans ce paradigme ; il ne démontre pas que tout comportement humain de curiosité obéit à un unique principe de dérivée de l’erreur.

4. Agents autotéliques et LLM : correction chronologique
LMA3 — Language Model Augmented Autotelic Agent — est une contribution PMLR de 2023. Le LLM y sert notamment à représenter des buts, générer des buts et sous-buts et fournir des fonctions de récompense.
MAGELLAN a été publié à ICML 2025. Il apprend à prédire en ligne compétence et learning progress dans de grands espaces de buts sémantiques afin de prioriser les objectifs d’apprentissage.
SELFGOAL est publié à NAACL 2025 et construit/adapte un arbre de sous-buts pour atteindre des objectifs de haut niveau sous feedback limité ou retardé. Il est pertinent pour la décomposition de buts, mais ne doit pas être présenté comme une méthode de learning progress sauf démonstration spécifique.
À supprimer du rapport : les formulations « manifestation thermodynamique », « loi de conservation de l’information » et « heuristique universelle de l’intelligence » ; elles ne sont pas supportées par les résultats cités.

5. Le raccord mathématique avec CONT
Dans CONT-02, une représentation Φ est évaluée par
L_Q(Φ)=sup_{Φ(h)=Φ(h′)} d_Q(h,h′).
Mais dans un système inconnu, les noyaux de continuation K_h^π et donc d_Q sont eux-mêmes inconnus. Un agent doit apprendre ces objets à partir d’expériences choisies séquentiellement.
La question d’exploration devient donc : quelle action, politique ou expérience fournit le plus d’information sur les distinctions de continuation encore non résolues à l’intérieur des fibres de Φ ?

6. Modèle d’incertitude sur les continuations
Soit D_t l’ensemble des observations disponibles au temps t. On considère une famille de modèles possibles θ∈Θ avec posterior p_t(θ)=p(θ|D_t), ou dans un cadre non bayésien un ensemble de confiance M_t de modèles compatibles avec les données.
Chaque θ définit des noyaux K_{h,θ}^π, une distance d_{Q,θ}, une équivalence ~_{Q,θ} et éventuellement un quotient Ω_{Q,θ}. L’incertitude pertinente n’est pas toute l’incertitude du modèle : c’est l’incertitude qui peut changer les distinctions de continuation utiles pour Q.

7. Définition de travail — risque de suffisance non certifiée
Pour une représentation candidate Φ, définir par exemple
B_t(Φ)=sup_{Φ(h)=Φ(h′)} sup_{θ∈M_t} d_{Q,θ}(h,h′).
B_t(Φ) est une borne pessimiste de perte compatible avec les données. Si B_t(Φ)=0, la représentation est certifiée Q-suffisante relativement à la classe de modèles considérée. Si B_t(Φ)>0, il reste soit une insuffisance réelle, soit une incertitude expérimentale à résoudre.
Cette définition est une proposition interne ; son originalité n’est pas établie et doit être comparée à l’active model learning, au robust RL, à l’identification de systèmes et à l’active automata learning.

8. Progrès de continuation
Pour une expérience candidate e, comprenant éventuellement une politique d’intervention et un protocole d’observation, on peut définir un progrès de continuation attendu :
CP_t(e;Φ)=B_t(Φ)−E[B_{t+1}(Φ) | D_t,e].
L’expérience la plus intéressante est celle qui réduit le plus la borne d’incertitude sur la perte de continuation, et non celle qui produit simplement l’observation la plus surprenante.
Cette définition est l’analogue CONT du learning progress : l’objet dont on suit le progrès n’est pas l’erreur brute du monde, mais notre capacité à décider si les collisions créées par Φ sont réellement sans conséquence future.

9. Version bayésienne — gain d’information ciblé
Une formulation plus canonique consiste à définir une variable aléatoire Θ_Q qui ne retient du modèle θ que les caractéristiques pertinentes pour la question Q : classes de continuation, valeurs de d_Q au-dessus d’un seuil, transitions de Ω_Q, ou témoins d’insuffisance.
La valeur intrinsèque d’une expérience peut alors être
IG_Q(e)=I(Θ_Q ; O_e | D_t),
c’est-à-dire l’information mutuelle attendue entre le résultat de l’expérience et la structure de continuation qui reste inconnue.
Cette formulation appartient conceptuellement au Bayesian experimental design et à l’exploration par information gain. Le delta CONT réside seulement dans le choix de Θ_Q : apprendre la structure minimale nécessaire aux continuations pertinentes plutôt que l’ensemble du modèle génératif.

10. Pourquoi cette formulation résiste au noisy-TV
Une source irréductiblement aléatoire peut avoir une grande entropie observationnelle tout en apportant très peu d’information sur Θ_Q. Une fois connue comme aléatoire et Q-non pertinente, répéter son observation ne réduit ni B_t(Φ) ni l’entropie de Θ_Q.
Ainsi, dans le cas idéal, CP_t et IG_Q deviennent faibles même si l’erreur de prédiction instantanée reste élevée. C’est le mécanisme précis recherché par les approches de learning progress et d’information gain.
Garde : cette robustesse n’est garantie que si le modèle d’incertitude sépare correctement incertitude épistémique et variabilité aléatoire ; un estimateur mal spécifié peut encore être attiré par le bruit.

11. Curiosité dirigée vers les fibres de Φ
CONT suggère une stratégie d’exploration très ciblée. Au lieu d’explorer uniformément l’espace des états, on cherche d’abord des collisions de représentation Φ(h)=Φ(h′). Pour chacune, on recherche une intervention π susceptible de maximiser la divergence prédite entre K_h^π et K_h′^π.
Schématiquement :
(h,h′) ← collision de Φ ;   π* ← argmax_π E[d_Q(h,h′)|D_t,π] ou gain d’information associé ;   exécuter π* ;   raffiner Φ ou certifier la fibre.
Cette boucle transforme la curiosité en procédure de falsification active de la suffisance d’une représentation.

12. Raccord direct à CONT-04
CONT-04 définit les tests d’ordre AB/BA comme sondes de L_Q. CONT-05 permet de choisir activement quels couples A,B tester.
On peut définir une valeur d’expérience d’ordre
IG_comm(A,B|h)=I(Θ_Q ; O_{AB},O_{BA} | D_t,h),
ou un progrès attendu sur la borne C_Q(Φ)≤L_Q(Φ). L’agent privilégie alors les commutateurs les plus susceptibles de révéler une distinction Q-pertinente cachée dans une fibre de Φ.
Ce principe donne une interprétation opérationnelle au « mouvement » : l’ordre n’est pas contemplé comme propriété abstraite ; il devient une expérience choisie pour découvrir ce que la représentation oublie.

15. Raccord à HOL-01
Sur HOL-01, une exploration active pourrait choisir des lacets dans Γ_7 afin d’apprendre l’action de monodromie sur la fibre. Le problème est alors classique d’identification de groupe/action sous requêtes.
Pour CONT, l’objectif additionnel serait de sélectionner les lacets non seulement parce qu’ils génèrent une grande action de fibre, mais parce qu’ils sont susceptibles de produire un résidu qui soit d_Q-pertinent pour une tâche Q explicitement choisie.
Cela distingue « apprendre la monodromie » de « apprendre la partie de la monodromie qui compte pour les continuations ».

16. Learning progress sur la représentation elle-même
Si Φ_t évolue pendant l’apprentissage, on peut mesurer un progrès de représentation par la diminution d’une perte certifiée ou estimée :
RP_t = B_{t−Δ}(Φ_{t−Δ}) − B_t(Φ_t).
Mais ce signal mélange deux phénomènes : nouvelles données et changement de représentation. Pour l’analyse scientifique, il faut séparer progrès d’identification à Φ fixe et progrès d’architecture lorsque Φ est modifiée.

17. Une alternative plus proche de MAGELLAN
Dans de grands espaces d’expériences, il est impossible d’estimer CP_t(e) séparément pour chaque e. Une architecture de type MAGELLAN suggère d’apprendre un méta-modèle qui prédit le progrès de continuation d’expériences ou de familles d’expériences à partir de leur description.
Dans le programme CONT, le méta-modèle pourrait prendre comme entrée : type d’intervention, fibre de Φ ciblée, statistiques de séparation observées, profondeur du mot, coût expérimental et contexte ; il prédirait la réduction attendue de B_t ou l’information sur Θ_Q.
Cette idée est une application/adaptation, pas une nouveauté théorique acquise.

18. SELFGOAL et décomposition hiérarchique
SELFGOAL est surtout pertinent lorsque l’expérience ou la question de continuation elle-même est trop complexe. Une requête « distinguer ces deux histoires à horizon 20 » peut être décomposée en sous-tests de plus faible horizon, puis raffinée en fonction des observations.
Cela rejoint la hiérarchie Ω_{T+1}→Ω_T de CONT-03 : les sous-buts peuvent être indexés par horizon ou profondeur de séparation.

19. Définitions candidates à tester
CLP — Continuation Learning Progress : réduction empirique ou attendue d’une mesure d’incertitude sur les lois de continuation ou sur L_Q.
RIG — Representation Information Gain : information acquise sur les distinctions de continuation à l’intérieur des fibres d’une représentation Φ.
ACS — Active Continuation Separation : procédure qui choisit adaptativement des interventions afin de séparer ou certifier les classes candidates de Ω_Q.
Ces noms sont provisoires et aucune revendication d’originalité ne doit être faite avant audit bibliographique ciblé.

20. Premier théorème candidat
Dans un modèle bayésien fini correctement spécifié, si une expérience e est conditionnellement indépendante de Θ_Q sachant D_t, alors IG_Q(e)=0. Une source de bruit indépendante de la structure de continuation pertinente ne reçoit donc aucune valeur intrinsèque par IG_Q.
Ce résultat est élémentaire par définition de l’information mutuelle ; son intérêt est de fixer le critère que tout bonus de curiosité CONT devrait approximer.

22. Troisième problème — apprentissage approximatif
Dans les systèmes stochastiques continus, il faut remplacer la séparation booléenne par un test statistique de d_Q(h,h′)>ε avec risque contrôlé. Le problème actif devient une allocation adaptative d’échantillons entre fibres, politiques et horizons.
Objectif : obtenir avec probabilité au moins 1−α une borne supérieure B_t(Φ)≤ε, ou exhiber un contre-exemple avec d_Q>ε.
Ce problème relie CONT aux tests séquentiels, bandits, active hypothesis testing, identification de systèmes et experimental design.

23. Critère d’arrêt
Un agent d’exploration CONT ne doit pas apprendre indéfiniment. Un critère naturel est : arrêter l’exploration dédiée à Φ lorsque B_t(Φ)≤ε au niveau de confiance requis, ou lorsque le coût marginal attendu des expériences dépasse la valeur opérationnelle d’une réduction supplémentaire de B_t.
Cela fournit une version mathématique du passage curiosité → suffisance : on cesse d’explorer non parce que le monde est devenu prévisible, mais parce que les incertitudes restantes ne changent plus les continuations qui comptent pour Q.

24. Nouvelle articulation du programme
CONT-02 : définir ce qu’une représentation perd.
CONT-03 : déterminer quand cette représentation peut se mettre à jour récursivement.
CONT-04 : utiliser l’ordre des interventions comme sonde de pertes cachées.
CONT-05 : choisir activement les sondes qui réduisent le plus vite l’incertitude sur ces pertes.
La chaîne devient : représentation → continuation → test → apprentissage actif → certification.

26. Positionnement de nouveauté
Non nouveau : learning progress, intrinsic motivation, Bayesian information gain, active learning, active automata learning, PSR, identification active de systèmes.
Potentiellement distinctif : cibler explicitement l’exploration sur la certification de la perte de continuation L_Q(Φ), sur les collisions des fibres de Φ et sur les tests d’ordre C_Q(Φ), puis relier le critère d’arrêt à une notion de suffisance relative à Q.
Originalité : NON ÉTABLIE. Un audit bibliographique dédié est nécessaire avant toute revendication.

27. Références externes de cadrage
Pathak et al., Curiosity-driven Exploration by Self-supervised Prediction, ICML 2017.
Burda et al., Exploration by Random Network Distillation, 2018.
Baranes & Oudeyer, Active learning of inverse models with intrinsically motivated goal exploration in robots, Robotics and Autonomous Systems 2013.
Colas et al., CURIOUS: Intrinsically Motivated Modular Multi-Goal Reinforcement Learning, ICML 2019.
Ten et al., Humans monitor learning progress in curiosity-driven exploration, Nature Communications 2021.
Colas et al., Augmenting Autotelic Agents with Large Language Models (LMA3), CoLLAs/PMLR 2023.
Molinaro et al., Latent Learning Progress Drives Autonomous Goal Selection in Human Reinforcement Learning, NeurIPS 2024.
Gaven et al., MAGELLAN: Metacognitive predictions of learning progress guide autotelic LLM agents in large goal spaces, ICML 2025.
Yang et al., SELFGOAL: Your Language Agents Already Know How to Achieve High-level Goals, NAACL 2025.
Hou, An & Du, Beyond Noisy-TVs: Noise-Robust Exploration Via Learning Progress Monitoring, ICLR 2026.

29. Verdict
Le rapport sur la curiosité artificielle apporte une piste utile à condition de renverser son interprétation : CONT n’a pas besoin d’une théorie générale de la curiosité. Il a besoin d’une théorie de sélection active des expériences capables de réduire l’incertitude sur les distinctions futures pertinentes.
Le candidat le plus propre est IG_Q ou CP_t : une expérience vaut par la réduction attendue de l’incertitude sur la structure de continuation, et non par la surprise qu’elle produit. Cette formulation est compatible avec le learning progress, avec l’information gain et avec l’active automata learning, tout en restant directement connectée à L_Q, C_Q et Ω_Q.
