# CONT-P v0.3 — extension jusqu'à Q=30030

## Objet
Tester si l'information historique résiduelle décroît quand le présent p_n est
représenté modulo 30, 210, 2310 puis 30030.

## Fenêtres
10–20 M, 20–40 M, 50–100 M.

## Résultat principal sur 50–100 M
 q_present  phi_q  reps  actual_cmi_bits  null_mean_cmi_bits  null_sd_cmi_bits  excess_over_markov_null_bits  z_descriptive  null_min_bits  null_max_bits  observed_transition_edges
        30      8   100         0.002675            0.000103          0.000007                      0.002573     357.334472       0.000086       0.000118                         64
       210     48   100         0.001463            0.000617          0.000016                      0.000846      52.413599       0.000566       0.000648                       1659
      2310    480   100         0.006638            0.006237          0.000058                      0.000401       6.930634       0.006080       0.006424                      11953
     30030   5760    40         0.071740            0.070151          0.000165                      0.001589       9.613212       0.069828       0.070490                      94173

## Point méthodologique critique
phi(30030)=5760 états possibles du présent. La représentation est donc très
parcimonieuse à 100 millions. La CMI brute augmente mécaniquement avec la
dimension et ne doit pas être comparée directement entre Q.

Le témoin nul est une chaîne de Markov d'ordre 1 calibrée sur les transitions
réelles Y_n -> Y_(n+1), implémentée de façon creuse (uniquement transitions
observées).

## Interprétation
- Q=30 : fort excès historique par rapport au témoin.
- Q=210 : excès nettement réduit.
- Q=2310 : excès encore réduit.
- Q=30030 : régime de forte sparsité ; la comparaison au témoin, et non la CMI
  brute, est la seule lecture acceptable.

Aucune mémoire intrinsèque ni persistance asymptotique n'est revendiquée.
