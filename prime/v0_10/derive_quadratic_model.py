from pathlib import Path
import math, csv, json, hashlib, zipfile
import numpy as np
from sympy import primerange

OUT=Path('/mnt/data/CONT_PRIME_MEMORY_v0_10')
OUT.mkdir(exist_ok=True)

# Frozen empirical values from v0.6
G180=0.0014300013489627617
G210=0.0002732275289423214
CI180=(0.0012279044436102594,0.0016320982543161027)
CI210=(0.0001985319519622952,0.0003479231059219035)
obs_delta=G180-G210
obs_frac=obs_delta/G180

# Quadratic local weights, primes >=7 to 1e6
primes=list(primerange(7,1_000_001))
rows=[]
pair_ws=[]; trip_ws=[]
for l in primes:
    # Pair: d uniform mod l; two factor states, weighted variance exactly p(1-p)*contrast^2
    contrast=math.log((l-1)/(l-2))
    wp=(l-1)/(l*l)*contrast*contrast
    pair_ws.append(wp)

    # Triplet H={0,h1,h1+h2}; h1,h2 uniform mod l
    p1=1/(l*l)
    p2=3*(l-1)/(l*l)
    p3=(l-1)*(l-2)/(l*l)
    def logF(nu):
        return math.log(1-nu/l)-3*math.log(1-1/l)
    us=[logF(1),logF(2),logF(3)]
    ps=[p1,p2,p3]
    mu=sum(p*u for p,u in zip(ps,us))
    wt=sum(p*(u-mu)**2 for p,u in zip(ps,us))
    trip_ws.append(wt)
    rows.append([l,wp,wt,contrast,p1,p2,p3,*us])

Sp=sum(pair_ws); St=sum(trip_ws)
share_pair=pair_ws[0]/Sp
share_trip=trip_ws[0]/St
pred_delta_pair=G180*share_pair
pred_delta_trip=G180*share_trip
pred_G210_pair=G180-pred_delta_pair
pred_G210_trip=G180-pred_delta_trip

# conservative rectangle for difference from marginal descriptive intervals
rect_delta=(CI180[0]-CI210[1], CI180[1]-CI210[0])

# Write weights
with open(OUT/'quadratic_local_weights.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['prime','pair_quadratic_weight','pair_share_tail','triplet_quadratic_weight','triplet_share_tail','pair_log_contrast','P_nu1','P_nu2','P_nu3','logF_nu1','logF_nu2','logF_nu3'])
    for row,wp,wt in zip(rows,pair_ws,trip_ws):
        l=row[0]
        w.writerow([l,wp,wp/Sp,wt,wt/St,*row[3:]])

# Summary prediction table
with open(OUT/'second_order_prediction_180_210.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['quantity','pair_model','triplet_model','observed_or_reference'])
    w.writerow(['fraction_of_hidden_local_quadratic_weight_at_7',share_pair,share_trip,obs_frac])
    w.writerow(['predicted_or_observed_delta_G_bits',pred_delta_pair,pred_delta_trip,obs_delta])
    w.writerow(['predicted_or_observed_G210_bits',pred_G210_pair,pred_G210_trip,G210])
    w.writerow(['predicted_delta_fraction_of_observed_delta',pred_delta_pair/obs_delta,pred_delta_trip/obs_delta,1.0])
    w.writerow(['residual_G210_prediction_minus_observed',pred_G210_pair-G210,pred_G210_trip-G210,0.0])
    w.writerow(['descriptive_rectangle_delta_low','','',rect_delta[0]])
    w.writerow(['descriptive_rectangle_delta_high','','',rect_delta[1]])

# Small-epsilon sanity check for theorem
p0=np.array([0.2,0.3,0.5],float)
ph=np.array([0.45,0.55],float)
s=np.array([[0.4,-0.3,0.1],[-0.2,0.5,-0.15]],float)
# Center scores within each h under p0
t=s-(s*p0).sum(axis=1,keepdims=True)
bar=(ph[:,None]*t).sum(axis=0)
coef=((ph[:,None]*p0[None,:])*(t-bar[None,:])**2).sum()/(2*math.log(2))

def cmi_eps(eps):
    P=[]
    for h in range(2):
        q=p0*np.exp(eps*s[h])
        q=q/q.sum(); P.append(q)
    P=np.array(P)
    marg=(ph[:,None]*P).sum(axis=0)
    val=0.0
    for h in range(2):
        val += ph[h]*np.sum(P[h]*np.log2(P[h]/marg))
    return val

with open(OUT/'quadratic_expansion_sanity.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['epsilon','exact_CMI_bits','quadratic_prediction_bits','ratio_exact_to_quad','abs_error'])
    for e in [0.2,0.1,0.05,0.02,0.01,0.005,0.002]:
        exact=cmi_eps(e); pred=coef*e*e
        w.writerow([e,exact,pred,exact/pred,abs(exact-pred)])

# Correction register
with open(OUT/'epistemic_corrections.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['version','previous_statement','status_v0_10','reason'])
    w.writerow(['v0.9','pair proxy gives ~47.2% and triplet ~67.2%, suggesting triplet is much closer','SUPERSEDED','pair proxy omitted frequency weighting; the correct KL/Fisher quadratic pair weight gives ~65.8%'])
    w.writerow(['v0.9','triplet-specific sensitivity to factor 7 is strongly established','WEAKENED','proper pair and triplet quadratic weights are close: ~65.8% vs ~67.2%'])
    w.writerow(['v0.9','local Euler null explains most of observed 80.9% suppression','RETAINED WITH QUALIFIER','second-order triplet prediction captures ~83.0% of observed delta, but leaves material residual and is conditional on additive/uncorrelated local scores'])

# Theory note
note=f'''# CONT-P v0.10 — quadratic information expansion and Euler-factor prediction

## 1. Exact information identity
For finite variables C (present), H (history), Z (future), the history gain under the true law is

G = I(H;Z|C) = E_{{C,H}} D_KL(P(Z|C,H) || P(Z|C)) / ln 2.

This identity is exact when G is defined as the population log-loss improvement from conditioning on H in addition to C.

## 2. Perturbative theorem
Assume, for fixed P(H|C), an exponential perturbation around a history-free baseline P0(Z|C):

P_e(Z=z|C=c,H=h) = P0(z|c) exp(e s(c,h,z)) / Z_{{c,h}}(e).

Define the score centered in z,

t(c,h,z)=s(c,h,z)-E_{{P0(Z|c)}} s(c,h,Z),

and its history mean m(c,z)=E[t(c,H,z)|C=c]. Then as e→0,

I_e(H;Z|C) = e^2/(2 ln 2) E[(t(C,H,Z)-m(C,Z))^2] + O(e^3),

where Z is drawn from P0(.|C) in the quadratic term.

Thus the leading information gain is a Fisher/KL quadratic form: a conditional variance of the history-dependent score.

## 3. Additive local-prime model
Suppose the score decomposes over unresolved sieve primes,

s = sum_ell s_ell,

and cross-covariances between distinct local scores vanish under a CRT-style null. Then

G(Q) ≈ K * sum_{{ell not visible in rad(Q)}} W_ell,

with W_ell the corresponding quadratic score variance and K common to the comparison. Revealing a new prime ell predicts

[G(Q)-G(Q ell)]/G(Q) ≈ W_ell / sum_{{r unresolved}} W_r.

For q=180 versus q=210 this is not literally a nested refinement; rather, rad(180)=30 while rad(210)=210. The model treats prime-power refinements as carrying no new Euler prime at this order and interprets 180/210 as an equal-cardinality radical-substitution control.

## 4. Correct quadratic weights
### Pair
For d uniform modulo ell, the proper quadratic pair weight is

W2_ell = ((ell-1)/ell^2) * log((ell-1)/(ell-2))^2.

As ell→∞,

W2_ell = ell^-3 + 2 ell^-4 + O(ell^-5).

The normalized ell=7 share over unresolved primes ell>=7 is {share_pair:.9f} ({100*share_pair:.2f}%).

### Triplet
For H={{0,h1,h1+h2}} with h1,h2 uniform modulo ell,

P(nu=1)=1/ell^2,
P(nu=2)=3(ell-1)/ell^2,
P(nu=3)=(ell-1)(ell-2)/ell^2,

F_ell(nu)=(1-nu/ell)(1-1/ell)^(-3),

and

W3_ell = Var(log F_ell(nu)).

As ell→∞,

W3_ell = 3 ell^-3 + 7 ell^-4 + O(ell^-5).

The normalized ell=7 share is {share_trip:.9f} ({100*share_trip:.2f}%).

## 5. Correction to v0.9
v0.9 compared the triplet variance to an unweighted squared pair contrast. That pair quantity was not the actual KL/Fisher quadratic form. With correct frequency weighting, the pair share is {100*share_pair:.2f}% rather than 47.16%, very close to the triplet share {100*share_trip:.2f}%.

Therefore the claim that the triplet model is markedly superior to the pair model is withdrawn. The robust conclusion is narrower: both proper local quadratic models predict a dominant contribution from the first unresolved prime 7.

## 6. Calibrated 180/210 prediction
Frozen empirical values:
- G(180) = {G180:.12g} bit/symbol
- G(210) = {G210:.12g}
- observed delta = {obs_delta:.12g}
- observed suppression fraction = {obs_frac:.9f} ({100*obs_frac:.2f}%)

Calibrating the overall scale K to G(180):
- pair model predicts delta = {pred_delta_pair:.12g}, hence G(210) = {pred_G210_pair:.12g};
- triplet model predicts delta = {pred_delta_trip:.12g}, hence G(210) = {pred_G210_trip:.12g}.

The triplet quadratic prediction captures {100*pred_delta_trip/obs_delta:.2f}% of the observed delta; the pair model captures {100*pred_delta_pair/obs_delta:.2f}%.

The remaining empirical suppression is larger than the simple independent-local model predicts. At point calibration, the triplet model leaves a predicted G(210) about {pred_G210_trip/G210:.2f} times the observed residual.

## 7. Uncertainty caution
The v0.6 blockwise descriptive intervals were computed separately for q=180 and q=210, not as paired block differences. A conservative rectangle from their marginal intervals gives a delta range [{rect_delta[0]:.12g}, {rect_delta[1]:.12g}], which contains the quadratic prediction. This is only a sensitivity band, not a confidence interval for the arithmetic sequence and not evidence that the model is statistically validated.

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
'''
(OUT/'THEORY_NOTE.md').write_text(note,encoding='utf-8')

readme=f'''# CONT-P v0.10

## Main advance
Derived the second-order expansion of conditional mutual information / population log-loss gain around a history-free baseline, and connected it to additive local Euler-factor scores.

## Key correction
v0.9's pair comparator was not frequency-weighted and is superseded. The proper quadratic pair share of ell=7 is {100*share_pair:.2f}%, close to the triplet share {100*share_trip:.2f}%.

## 180/210 prediction
Observed suppression: {100*obs_frac:.2f}%.
Second-order pair prediction: {100*share_pair:.2f}%.
Second-order triplet prediction: {100*share_trip:.2f}%.

The triplet model predicts G(210)≈{pred_G210_trip:.6g} vs observed {G210:.6g}; the remaining discrepancy is material and points to finite-x/consecutiveness/gap-correlation structure beyond the independent local null.

## Status
[D] perturbative information expansion under the stated finite exponential-family model.
[D] exact local-factor combinatorics and quadratic weight formulas.
[C] numerical Euler-weight sums and frozen empirical comparison.
[H] identification of prime local factors with the perturbative score of actual consecutive-prime patterns.
[N] novelty NOT ESTABLISHED.
'''
(OUT/'README.md').write_text(readme,encoding='utf-8')

manifest={
  'name':'CONT-P','version':'0.10','date':'2026-10-06',
  'status':'perturbative theorem + finite calibration; novelty not established',
  'frozen':{'G180':G180,'G210':G210,'observed_suppression_fraction':obs_frac},
  'quadratic':{'pair_share_7':share_pair,'triplet_share_7':share_trip,'predicted_G210_triplet':pred_G210_trip},
  'supersedes':['v0.9 unweighted pair comparator'],
}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

# standalone script snapshot
Path(OUT/'derive_quadratic_model.py').write_text(Path('/tmp/build_v010.py').read_text(encoding='utf-8'),encoding='utf-8')

# zip
zip_path=Path('/mnt/data/CONT_PRIME_MEMORY_v0_10.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.iterdir()):
        z.write(p,arcname=f'{OUT.name}/{p.name}')
sha=hashlib.sha256(zip_path.read_bytes()).hexdigest()
Path('/mnt/data/CONT_PRIME_MEMORY_v0_10.zip.sha256.txt').write_text(f'{sha}  {zip_path.name}\n',encoding='ascii')
print(json.dumps({
 'pair_share7':share_pair,'triplet_share7':share_trip,'obs_fraction':obs_frac,
 'pred_G210_pair':pred_G210_pair,'pred_G210_trip':pred_G210_trip,'obs_G210':G210,
 'pred_delta_trip_fraction_obs':pred_delta_trip/obs_delta,'sha256':sha
},indent=2))
