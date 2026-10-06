# CONT-P v0.9 — local Euler-factor null and novelty correction

## 1. Purpose
Build the simplest analytic null connecting the observed loss of historical predictive gain under state refinement to local Hardy–Littlewood / singular-series factors, while tightening the novelty claim after the 2026 literature audit.

## 2. Exact local factors used
For a pair of offsets {0,d}, the local singular-series factor at a prime ell is

F_ell^(2)(d) = (1 - nu_ell/ell) (1 - 1/ell)^(-2),

with nu_ell = 1 if ell divides d and nu_ell = 2 otherwise. Hence the divisible/non-divisible contrast is

F_div / F_nondiv = (ell-1)/(ell-2).

For a triplet H={0,h1,h1+h2},

F_ell^(3)(H) = (1 - nu_ell(H)/ell) (1 - 1/ell)^(-3),

where nu_ell is the number of distinct offsets modulo ell. Under the deliberately simple null h1,h2 uniform modulo ell,

P(nu=1)=1/ell^2,
P(nu=2)=3(ell-1)/ell^2,
P(nu=3)=(ell-1)(ell-2)/ell^2.

We define the local information-strength proxy

W_ell^(3) = Var[ log F_ell^(3) ].

This is not asserted to equal conditional mutual information. It is a second-order proxy motivated by the quadratic expansion of KL/log-loss around a weak perturbation.

## 3. Main numerical comparison
Normalizing over primes ell >= 7 up to 10^6 (the tail is already converged at displayed precision):

- pair squared-log-contrast share of ell=7: 0.471611 (47.16%)
- triplet log-factor variance share of ell=7: 0.671784 (67.18%)
- empirical complexity-matched suppression 180 -> 210: 0.808932 (80.89%)

Thus the triplet local-factor null is materially closer to the observed effect than the pair null, but it still underpredicts the empirical suppression by about 13.71 percentage points.

## 4. Structural interpretation of 180 vs 210
rad(180)=30, so q=180 refines powers of 2 and 3 but introduces no new Euler prime in the singular series. In contrast rad(210)=210 introduces the new prime 7. Because phi(180)=phi(210)=48, this comparison is unusually clean: same reduced-state cardinality, different local sieve content.

## 5. What the simple null explains — and what it does not
Explains qualitatively:
- why 7 should dominate later primes;
- why a triplet-based observable is more sensitive to 7 than a pair-only observable;
- why adding a genuinely new sieve prime can matter more than prime-power refinement at equal state cardinality.

Does not yet explain quantitatively:
- the full ~81% empirical suppression;
- the consecutive-prime condition (absence of intervening primes);
- finite-x secondary terms c2;
- correlations among successive gaps;
- estimation/backoff effects in G(Q).

## 6. Novelty correction after 2026 audit
The strongest overlap is Daniel John Murray's 2026 SSRN work. His projection-tomography paper already studies coarse mod-30 apparent memory under larger primorial CRT state, with Markov controls, held-out checks and dimension-matched controls, and concludes that hidden primorial state explains much of the apparent memory. His follow-up gives an exact Hardy–Littlewood-model refinement covariance statement for Q -> Q*ell.

Therefore CONT-P must NOT claim novelty for:
- apparent memory caused by coarse prime-residue projection;
- recovery by primorial refinement;
- Markov/lumpability framing in this setting;
- CMI2/non-Markov diagnostics themselves.

The remaining candidate contribution is narrower: a complexity-matched continuation-sufficiency experiment, especially the exact-cardinality contrast 180 vs 210, combined with a declared held-out log-loss functional G(Q), blockwise uncertainty, and an explicit comparison to local Euler-factor variance. Even this requires direct manuscript-level comparison before publication.

## 7. Epistemic status
[D] Exact algebra inside this note: local factor ratios and probability counts for nu under the stated uniform-gap null.
[C] Computed: normalized local-factor variance shares and frozen empirical G-values.
[H] Heuristic: W_ell^(3) as a proxy for information contribution to G(Q).
[O] Open: derivation of G(Q) itself from consecutive-prime asymptotics / LOS coefficients.
[N] Novelty: NOT ESTABLISHED. Significant 2026 overlap exists.
