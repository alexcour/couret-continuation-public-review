# CONT-P v0.10 — quadratic information expansion and Euler-factor prediction

## 1. Exact information identity
For finite variables C (present), H (history), Z (future), the history gain under the true law is

G = I(H;Z|C) = E_{C,H} D_KL(P(Z|C,H) || P(Z|C)) / ln 2.

This identity is exact when G is defined as the population log-loss improvement from conditioning on H in addition to C.

## 2. Perturbative theorem
Assume, for fixed P(H|C), an exponential perturbation around a history-free baseline P0(Z|C):

P_e(Z=z|C=c,H=h) = P0(z|c) exp(e s(c,h,z)) / Z_{c,h}(e).

Define the score centered in z,

t(c,h,z)=s(c,h,z)-E_{P0(Z|c)} s(c,h,Z),

and its history mean m(c,z)=E[t(c,H,z)|C=c]. Then as e→0,

I_e(H;Z|C) = e^2/(2 ln 2) E[(t(C,H,Z)-m(C,Z))^2] + O(e^3),

where Z is drawn from P0(.|C) in the quadratic term.

Thus the leading information gain is a Fisher/KL quadratic form: a conditional variance of the history-dependent score.

## 3. Additive local-prime model
Suppose the score decomposes over unresolved sieve primes,

s = sum_ell s_ell,

and cross-covariances between distinct local scores vanish under a CRT-style null. Then

G(Q) ≈ K * sum_{ell not visible in rad(Q)} W_ell,

with W_ell the corresponding quadratic score variance and K common to the comparison. Revealing a new prime ell predicts

[G(Q)-G(Q ell)]/G(Q) ≈ W_ell / sum_{r unresolved} W_r.

For q=180 versus q=210 this is not literally a nested refinement; rather, rad(180)=30 while rad(210)=210. The model treats prime-power refinements as carrying no new Euler prime at this order and interprets 180/210 as an equal-cardinality radical-substitution control.

## 4. Correct quadratic weights
### Pair
For d uniform modulo ell, the proper quadratic pair weight is

W2_ell = ((ell-1)/ell^2) * log((ell-1)/(ell-2))^2.

As ell→∞,

W2_ell = ell^-3 + 2 ell^-4 + O(ell^-5).

The normalized ell=7 share over unresolved primes ell>=7 is 0.657526078 (65.75%).

### Triplet
For H={0,h1,h1+h2} with h1,h2 uniform modulo ell,

P(nu=1)=1/ell^2,
P(nu=2)=3(ell-1)/ell^2,
P(nu=3)=(ell-1)(ell-2)/ell^2,

F_ell(nu)=(1-nu/ell)(1-1/ell)^(-3),

and

W3_ell = Var(log F_ell(nu)).

As ell→∞,

W3_ell = 3 ell^-3 + 7 ell^-4 + O(ell^-5).

The normalized ell=7 share is 0.671783551 (67.18%).

## 5. Correction to v0.9
v0.9 compared the triplet variance to an unweighted squared pair contrast. That pair quantity was not the actual KL/Fisher quadratic form. With correct frequency weighting, the pair share is 65.75% rather than 47.16%, very close to the triplet share 67.18%.

Therefore the claim that the triplet model is markedly superior to the pair model is withdrawn. The robust conclusion is narrower: both proper local quadratic models predict a dominant contribution from the first unresolved prime 7.

## 6. Calibrated 180/210 prediction
Frozen empirical values:
- G(180) = 0.00143000134896 bit/symbol
- G(210) = 0.000273227528942
- observed delta = 0.00115677382002
- observed suppression fraction = 0.808931978 (80.89%)

Calibrating the overall scale K to G(180):
- pair model predicts delta = 0.00094026317897, hence G(210) = 0.000489738169993;
- triplet model predicts delta = 0.000960651384106, hence G(210) = 0.000469349964857.

The triplet quadratic prediction captures 83.05% of the observed delta; the pair model captures 81.28%.

The remaining empirical suppression is larger than the simple independent-local model predicts. At point calibration, the triplet model leaves a predicted G(210) about 1.72 times the observed residual.

## 7. Uncertainty caution
The v0.6 blockwise descriptive intervals were computed separately for q=180 and q=210, not as paired block differences. A conservative rectangle from their marginal intervals gives a delta range [0.000879981337688, 0.00143356630235], which contains the quadratic prediction. This is only a sensitivity band, not a confidence interval for the arithmetic sequence and not evidence that the model is statistically validated.

## 8. What remains missing
The second-order formula is derived, but the prime-specific score s is still modeled heuristically by local Euler factors. Missing ingredients include:
- the consecutiveness condition (no intervening prime),
- finite-x Lemke Oliver–Soundararajan secondary terms,
- correlations between successive gaps,
- dependence between local-prime scores after conditioning on the observed residue state,
- the exact effect of the hierarchical backoff estimator used in finite samples.

## 9. Novelty boundary
Murray (2026) already studies coarse mod-30 apparent memory recovered by primorial hidden state with Markov, dimension-matched and held-out controls, and his September follow-up establishes exact refinement covariance for a Hardy–Littlewood functional. Thus v0.10 does not claim novelty for projection-induced memory or primorial recovery.

The candidate contribution remains the explicit continuation-gain functional G(Q), equal-cardinality radical-substitution controls such as 180/210, and the calibration of a derived KL/Fisher quadratic expansion against local Euler-factor weights. Novelty remains N = NON ÉTABLIE pending manuscript-level comparison.
