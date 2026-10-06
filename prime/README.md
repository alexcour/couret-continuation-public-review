# Prime continuation experiments through v0.11

CURRENT model: v0_11. v0_2 through v0_10 are historical supporting snapshots.
The unweighted pair comparator in v0.9 is superseded by the frequency-weighted
quadratic analysis in v0.10. Do not use the old pair share as a current result.

v0.11 predicts 73.5450% suppression in the finite 180/210 model, compared with
80.8932% in the frozen empirical comparison. The 90.92% figure concerns the drop
after calibration to G(180); it is not an out-of-sample prediction of both levels.
The singular-series factor calculations are finite. The Poissonized consecutivity
weight is a heuristic approximation, not a theorem about prime distributions.

The observed comparison is an input constant in MODEL_SCRIPT.py. Replaying that
script reproduces the model, not an independent new prime-data collection.
No general non-Markovianity, RH, twin-prime or priority claim is made.
The overlap with Lemke Oliver--Soundararajan and Murray 2026 remains material.

Run from the repository root: python3 scripts/replay_prime_v011.py --output /tmp/cont-prime-v011
Requires NumPy. The historical script remains byte-identical; its output directory
is redirected in memory by the wrapper. New outputs never overwrite the snapshots.
