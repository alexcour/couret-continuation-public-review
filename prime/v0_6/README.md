# CONT-P v0.6 — courbes denses de raffinement du présent

## But
Remplacer les quatre seuls points 30 → 210 → 2310 → 30030 par plusieurs chaînes de représentations emboîtées, afin de distinguer :
1. l'effet général de la richesse du présent ;
2. l'effet du type d'information arithmétique ajoutée.

## Données et protocole
- nombres premiers dans [50 000 000, 100 000 000] ;
- X_n = p_n mod 30 ; futur prédit : X_(n+1) ;
- présent Y_n = p_n mod q ;
- historique ajouté : X_(n-1) ;
- split par blocs de 50 000 triplets : train / validation / test cycliques ;
- backoff hiérarchique vers P(X_(n+1)|Y_n) ;
- tau choisi exclusivement sur validation puis figé sur test ;
- dispersion calculée sur les blocs test retenus.

## Chaînes testées
- primoriale : [30, 210, 2310, 30030]
- raffinement 2-adique : [30, 60, 120, 240, 480, 960, 1920, 3840, 7680, 15360, 30720]
- raffinement 3-adique : [30, 90, 270, 810, 2430, 7290, 21870]
- raffinement 5-adique : [30, 150, 750, 3750, 18750]
- mixte : [30, 60, 180, 360, 2520, 27720]

## Gains historiques test (bit/symbole)
- primorial_new_primes: 30:+0.002180, 210:+0.000273, 2310:+0.000020, 30030:+0.000098
- 2_adic_refinement: 30:+0.002180, 60:+0.001945, 120:+0.001594, 240:+0.001269, 480:+0.000839, 960:+0.000530, 1920:+0.000313, 3840:+0.000208, 7680:+0.000145, 15360:+0.000167, 30720:+0.000608
- 3_adic_refinement: 30:+0.002180, 90:+0.001808, 270:+0.001154, 810:+0.000532, 2430:+0.000175, 7290:+0.000078, 21870:+0.000208
- 5_adic_refinement: 30:+0.002180, 150:+0.001502, 750:+0.000498, 3750:+0.000157, 18750:+0.000183
- mixed_refinement: 30:+0.002180, 60:+0.001945, 180:+0.001430, 360:+0.000972, 2520:+0.000030, 27720:+0.000171

## Contrôle par blocs
Les colonnes block_ci95_low_bits / block_ci95_high_bits donnent un intervalle descriptif construit à partir des gains moyens par bloc test. Il ne s'agit pas d'un p-value ni d'un intervalle de confiance arithmétique asymptotique.

## Comparaison à complexité voisine
 q_present factorization  phi_q  test_history_gain_bits  block_ci95_low_bits  block_ci95_high_bits
       150       2*3*5^2     40                0.001502             0.001299              0.001705
       180     2^2*3^2*5     48                0.001430             0.001228              0.001632
       210       2*3*5*7     48                0.000273             0.000199              0.000348

## Statut
Expérience finie et reproductible. Aucun théorème asymptotique, aucune implication RH et aucune revendication de nouveauté ne sont formulés à ce stade.
