# CONT 03 Extrait mathématique général pour relecture

Version éditoriale du 6 octobre 2026. Les sections sont conservées avec leur numérotation de source. Les exemples et raccords FCI, ainsi que les liens internes, ont été retirés. Ces extraits chronologiques doivent être lus avec le statut actuel du README.

0. Statut et résultat directeur
Objet : déterminer quand le quotient de continuation Ω_Q défini dans CONT-01/CONT-02 est une véritable mémoire opérationnelle, c’est-à-dire quand son état suivant peut être calculé depuis son état courant et la nouvelle interaction, sans relire l’histoire complète.
Résultat directeur : l’existence d’une mise à jour récursive sur un quotient est équivalente à une propriété de stabilité de la relation d’équivalence par prolongement de l’histoire. Dans le cas déterministe, il s’agit exactement d’une congruence à droite. Dans le cas stochastique, il faut en plus traiter l’admissibilité et les observations de probabilité nulle.
Garde bibliographique : la récursivité des états prédictifs ou d’information est classique. Les causal states sont récursivement calculables ; les information states sont précisément conçus pour être récursivement actualisables. CONT-03 fixe donc le langage interne et isole les conditions exactes adaptées au programme, sans revendiquer ce principe comme nouveau.

1. Histoires et prolongement
Soit H un ensemble d’histoires admissibles. Une interaction élémentaire est notée e=(a,o), où a est une action/intervention et o une nouvelle observation. On note h·e l’histoire prolongée lorsqu’elle est admissible.
Pour éviter toute ambiguïté, le prolongement peut être partiel : certains couples (a,o) peuvent être impossibles après une histoire donnée. Dans un modèle stochastique, l’admissibilité pertinente sera souvent « o appartient au support de la loi de la prochaine observation sous a ».

2. Congruence de prolongement
Définition 2.1. Une relation d’équivalence ≈ sur H est stable par prolongement si, dès que h≈h′, tout prolongement élémentaire commun e satisfait
h·e ≈ h′·e.
Si toutes les interactions élémentaires sont syntaxiquement définies, cette propriété est la congruence à droite usuelle. Dans un système partiellement défini ou stochastique, elle est comprise sur les prolongements communément admissibles.

3. Théorème U1 — caractérisation de la mise à jour quotient
Théorème U1. Soit η:H→Ω=H/≈ la projection canonique. Il existe une application de mise à jour F telle que
η(h·e)=F(η(h),e)
pour tout prolongement admissible si et seulement si ≈ est stable par prolongement.
Preuve. Si F existe et h≈h′, alors η(h)=η(h′). Pour tout e admissible des deux côtés, η(h·e)=F(η(h),e)=F(η(h′),e)=η(h′·e), donc h·e≈h′·e. Réciproquement, si ≈ est stable, définir F([h],e)=[h·e]. La stabilité garantit que le résultat ne dépend pas du représentant choisi. CQFD.
Interprétation : une statistique suffisante pour le futur n’est pas automatiquement une mémoire exploitable ; elle doit également permettre de calculer sa propre évolution à partir de l’information conservée.

4. Version pour une représentation quelconque
Soit Φ:H→Z. Une transition réduite F_Φ vérifiant Φ(h·e)=F_Φ(Φ(h),e) existe exactement lorsque les fibres de Φ sont stables par prolongement :
Φ(h)=Φ(h′) ⇒ Φ(h·e)=Φ(h′·e)
pour tout prolongement commun admissible. Cette condition est plus forte que la seule suffisance Q si Φ contient des distinctions redondantes qui évoluent différemment.
Ainsi deux questions doivent être séparées : (a) Φ conserve-t-elle toutes les distinctions pertinentes pour Q ? (b) Φ peut-elle être actualisée sans l’histoire complète ?

5. Définition — état opérationnel exact
Une représentation Φ est appelée état opérationnel exact pour Q lorsqu’elle satisfait simultanément :
Suffisance : L_Q(Φ)=0.
Actualisabilité : il existe F_Φ tel que Φ(h·e)=F_Φ(Φ(h),e).
La première condition empêche de perdre des distinctions qui modifient les continuations ; la seconde empêche de dépendre de distinctions déjà oubliées pour calculer l’état suivant.

6. Application au quotient minimal Ω_Q
Le quotient Ω_Q=H/~_Q de CONT-02 est toujours minimal parmi les représentations déterministes Q-suffisantes. Il devient en plus un état opérationnel minimal exactement lorsque ~_Q est stable par prolongement.
Dans ce cas, il existe une transition canonique
F_Q([h],e)=[h·e],
et toute mémoire Q-suffisante qui s’actualise exactement contient au moins l’information nécessaire pour déterminer Ω_Q, à isomorphisme près lorsque ses fibres sont exactement celles de ~_Q.

7. Quand l’équivalence de continuation est-elle automatiquement récursive ?
La réponse dépend du choix de Q. Si Q ne regarde qu’un futur tronqué ou une famille d’interventions non fermée par concaténation, la stabilité peut échouer. Pour obtenir une récursivité canonique, il faut que Q soit continuation-complet : après une première action et une première observation, les questions futures utilisées pour définir l’équivalence doivent encore appartenir à la famille décrite par Q.

8. Définition — spécification continuation-complète
On dira qu’une spécification Q est continuation-complète lorsque :
(i) elle contient l’information sur la prochaine observation nécessaire pour conditionner la suite ;
(ii) sa famille de politiques/interventions est fermée par préfixation d’une action admissible et par poursuite après une observation ;
(iii) l’objet futur contient suffisamment de trajectoire pour que l’égalité des lois futures entraîne l’égalité des lois conditionnelles après toute observation de probabilité positive.
Cette définition est volontairement structurelle ; ses versions mesurables précises dépendront du modèle considéré.

9. Théorème U2 — stabilité sur les événements de probabilité positive
Théorème U2, forme contrôlée. Supposons Q continuation-complet, que des probabilités conditionnelles régulières soient disponibles, et que h~_Qh′. Fixons une action a. Alors les lois de la prochaine observation sous a coïncident. Pour toute observation o ayant probabilité strictement positive sous cette loi commune, les histoires prolongées h·(a,o) et h′·(a,o) sont encore Q-équivalentes.
Idée de preuve. L’égalité des lois de continuation pour toutes les politiques incluant le préfixe a donne d’abord l’égalité de la loi de la prochaine observation. En choisissant ensuite arbitrairement la politique de continuation après o, l’égalité des lois jointes « prochaine observation + futur restant », puis le conditionnement par l’événement o de probabilité positive, imposent l’égalité de toutes les lois futures conditionnelles. On obtient donc h·(a,o)~_Qh′·(a,o).
Garde : sur un événement de probabilité nulle, la loi conditionnelle n’est pas déterminée de manière intrinsèque par la loi jointe ; l’état après un tel événement doit être laissé hors support, fixé par convention, ou traité avec une structure supplémentaire.

10. Conséquence — unifilarité relative
Sous les hypothèses de U2, la classe suivante Ω_{t+1} est déterminée par la classe courante Ω_t, l’action a_t et l’observation effectivement reçue o_{t+1}, sur le support du processus :
Ω_{t+1}=F_Q(Ω_t,a_t,o_{t+1}).
C’est l’analogue contrôlé de l’unifilarité : la mémoire latente minimale n’a pas besoin d’être réinférée depuis l’historique complet après chaque étape.

11. Correction importante : horizon fini
Une équivalence définie seulement par les T prochaines étapes n’est pas, en général, stable à horizon T après prolongement. Deux histoires peuvent être identiques pour une question à horizon court tout en révélant une différence après une étape supplémentaire.
La relation correcte est plutôt : l’équivalence à horizon T+1 avant l’observation entraîne, sous les mêmes hypothèses de positivité, l’équivalence à horizon T après l’observation.
Schématiquement :
Ω_{T+1}  --(a,o)-->  Ω_T.
Pour disposer d’un état stationnaire Ω→Ω, il faut soit travailler avec un futur complet/invariant par décalage, soit inclure le temps ou l’horizon restant dans l’état.
Cette remarque interdit de confondre « suffisance pour une décision à horizon T » et « état récursif autonome ».

12. Exemple conceptuel de l’échec à horizon court
Considérons deux histoires qui donnent exactement la même loi de la prochaine observation, mais des lois différentes pour l’observation suivante conditionnellement au même premier résultat. Elles sont équivalentes pour Q_1 mais pas pour Q_2. Après la première observation, leurs prolongements peuvent donc ne plus être Q_1-équivalents. La classe Q_1 courante ne suffit pas à calculer la classe Q_1 suivante.
Ce contre-exemple abstrait montre que la récursivité ne découle pas de la seule égalité d’une prédiction locale.

14. Défaut d’actualisation pour une représentation candidate
Pour une représentation Φ qui prétend résumer l’histoire, on peut définir un défaut qualitatif d’actualisation : il existe une collision d’update si l’on trouve h,h′,e tels que
Φ(h)=Φ(h′) mais Φ(h·e)≠Φ(h′·e).
Une telle collision prouve qu’aucune fonction F_Φ de la seule représentation courante et du nouvel événement ne peut reproduire exactement Φ à l’étape suivante.

15. Défaut d’actualisation pertinent pour la continuation
Lorsque la représentation Φ contient des détails redondants, une divergence de Φ(h·e) et Φ(h′·e) n’est pas forcément importante. On définit donc un défaut plus directement lié à Q :
U_Q(Φ)=sup d_Q(h·e,h′·e),
où le supremum porte sur les couples Φ(h)=Φ(h′) et les prolongements communs admissibles e.
Si U_Q(Φ)=0, l’état de continuation canonique après l’événement est déterminé par Φ(h) et e, même si la valeur exacte de Φ à l’étape suivante peut contenir des distinctions supplémentaires. Cette quantité est une proposition de travail ; son positionnement bibliographique reste à auditer avant toute revendication d’originalité.

16. Lien entre perte statique et défaut d’update
L_Q(Φ) et U_Q(Φ) mesurent deux défauts différents. L_Q(Φ)>0 signifie que Φ a déjà fusionné au présent des histoires aux continuations différentes. U_Q(Φ)>0 signifie qu’une collision présente peut devenir pertinente après un seul prolongement.
Dans une spécification continuation-complète, si L_Q(Φ)=0, alors les prolongements issus d’une même fibre de Φ restent dans une même classe Ω_Q sur les observations de probabilité positive ; ainsi U_Q(Φ)=0 au niveau du quotient canonique. En revanche Φ elle-même peut ne pas être récursivement actualisable si elle conserve des distinctions redondantes instables.

18. Positionnement bibliographique
Shalizi et Crutchfield, Computational Mechanics: Pattern and Prediction, Structure and Simplicity, Journal of Statistical Physics 104 (2001) : les causal states sont des statistiques prédictives minimales et possèdent une dynamique récursive/unifilaire.
Subramanian, Sinha, Seraj et Mahajan, Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems, JMLR 23 (2022) : une information state peut être définie comme une fonction de l’histoire récursivement actualisable et suffisante pour la prédiction pertinente à la programmation dynamique.
Conséquence : U1 est une caractérisation structurelle élémentaire du quotient ; U2 rapproche le cadre CONT des états prédictifs/information states. La contribution potentielle du programme doit résider dans des objets ou bornes supplémentaires, pas dans la simple existence d’une mise à jour récursive.

19. Résultats de CONT-03
U1 : FERMÉ — existence d’une mise à jour quotient ⇔ stabilité par prolongement.
U2 : FERMÉ sous les hypothèses explicitement déclarées de continuation-complétude, conditionnement régulier et probabilité positive.
Horizon fini : CORRECTION STRUCTURELLE — une famille Ω_T est naturellement graduée ; un update stationnaire exige une fermeture temporelle ou l’ajout de l’horizon restant.
U_Q(Φ) : NOUVEL OBJET DE TRAVAIL INTERNE ; originalité non auditée.

20. Prochaine étape
La prochaine étape la plus productive est CONT-04 : définir et analyser le défaut d’ordre des interventions comme témoin expérimental de perte de continuation. Il faudra distinguer trois phénomènes : non-commutativité réelle du système, non-commutativité visible sous Φ, et retour au même observable avec divergence des continuations.
Le résultat recherché ne sera pas « AB≠BA implique mémoire cachée », qui est faux, mais un critère du type : si Φ(ABh)=Φ(BAh) alors que d_Q(ABh,BAh)>0, la représentation Φ a effacé une distinction créée par l’ordre et pertinente pour le futur.
