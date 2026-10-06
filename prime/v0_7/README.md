# CONT-P v0.7 — ablation des facteurs premiers

## Question
La disparition de la mémoire historique dépend-elle seulement du nombre d'états du présent, ou surtout de certains facteurs premiers nouvellement introduits dans le modulus ?

## Protocole
Même fenêtre, split et backoff que v0.6. On part de q=30 puis on ajoute un seul premier r, q=30r, pour r=7,11,...,97. On teste aussi plusieurs paires et triplets.

## Référence
Gain historique mod 30 : 0.002180472 bit/symbole.

## Ajout d'un seul petit premier (r<=47)
 added_prime  q_present  phi_q  test_gain_bits  block_ci95_low_bits  block_ci95_high_bits  fraction_memory_removed_vs_mod30
           7        210     48        0.000273             0.000199              0.000348                          0.874693
          11        330     80        0.001077             0.000944              0.001209                          0.506189
          13        390     96        0.000976             0.000777              0.001176                          0.552290
          17        510    128        0.001043             0.000880              0.001207                          0.521516
          19        570    144        0.000902             0.000734              0.001070                          0.586475
          23        690    176        0.000827             0.000676              0.000978                          0.620685
          29        870    224        0.000500             0.000396              0.000604                          0.770796
          31        930    240        0.000504             0.000397              0.000612                          0.768727
          37       1110    288        0.000475             0.000367              0.000584                          0.782075
          41       1230    320        0.000419             0.000275              0.000564                          0.807640
          43       1290    336        0.000455             0.000404              0.000505                          0.791517
          47       1410    368        0.000354             0.000214              0.000494                          0.837815

## Lecture
Si deux représentations ont une complexité comparable mais des gains très différents, la nature arithmétique de l'information ajoutée compte davantage qu'une simple dimension d'état.

Les intervalles par blocs sont descriptifs et ne sont pas des p-values arithmétiques asymptotiques.
