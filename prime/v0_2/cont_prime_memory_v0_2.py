#!/usr/bin/env python3
"""
CONT-P v0.2 — Prime residue continuation memory experiment.

Question:
Does X_{n-1}=p_{n-1} mod 30 contain predictive information about
X_{n+1}=p_{n+1} mod 30 after conditioning on the present
Y_n=p_n mod Q, Q in {30,210,2310}?

Adds to v0.1:
- a first-order Markov surrogate calibrated on the observed Y_n transition matrix.
- deterministic null simulations for the conditional mutual information (CMI).

Exploratory finite computation only. No asymptotic theorem is claimed.
"""
import argparse, math
import numpy as np
import pandas as pd
from math import gcd
from numba import njit

def primes_upto(n):
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    if n >= 4:
        sieve[4::2] = False
    for p in range(3, int(n**0.5) + 1, 2):
        if sieve[p]:
            sieve[p*p::2*p] = False
    return np.flatnonzero(sieve)

def units_mod(q):
    return np.array([a for a in range(q) if gcd(a, q) == 1], dtype=np.int32)

def encode_residues(vals, q):
    units = units_mod(q)
    mp = np.full(q, -1, dtype=np.int32)
    mp[units] = np.arange(len(units), dtype=np.int32)
    codes = mp[vals % q]
    if np.any(codes < 0):
        raise ValueError("Window contains a prime dividing the modulus.")
    return codes, units

def empirical_cmi(prev, cond, nxt, na, nb, nc):
    idx = (prev.astype(np.int64)*nb + cond.astype(np.int64))*nc + nxt.astype(np.int64)
    counts = np.bincount(idx, minlength=na*nb*nc).reshape(na, nb, nc)
    n = counts.sum()
    pabc = counts / n
    pab = counts.sum(axis=2) / n
    pbc = counts.sum(axis=0) / n
    pb = counts.sum(axis=(0,2)) / n
    nz = np.nonzero(counts)
    cmi = float(np.sum(
        pabc[nz] * np.log2(
            (pabc[nz] * pb[nz[1]]) /
            (pab[nz[0], nz[1]] * pbc[nz[1], nz[2]])
        )
    ))
    df = 0
    for b in range(nb):
        sub = counts[:, b, :]
        r = np.count_nonzero(sub.sum(axis=1))
        c = np.count_nonzero(sub.sum(axis=0))
        if r and c:
            df += (r-1)*(c-1)
    bias = df / (2*n*math.log(2))
    return cmi, bias, df

def tv_stats(prev, cond, nxt, na, nb, nc, min_context=200):
    idx = (prev.astype(np.int64)*nb + cond.astype(np.int64))*nc + nxt.astype(np.int64)
    counts = np.bincount(idx, minlength=na*nb*nc).reshape(na,nb,nc)
    ctx = counts.sum(axis=2)
    vals = []
    for b in range(nb):
        valid = np.where(ctx[:,b] >= min_context)[0]
        for i,a in enumerate(valid):
            pa = counts[a,b] / ctx[a,b]
            for ap in valid[i+1:]:
                pap = counts[ap,b] / ctx[ap,b]
                d = 0.5*np.abs(pa-pap).sum()
                vals.append((float(d), int(min(ctx[a,b],ctx[ap,b]))))
    if not vals:
        return np.nan, np.nan, 0
    ds = np.array([x[0] for x in vals])
    ws = np.array([x[1] for x in vals], dtype=float)
    return float(ds.max()), float(np.average(ds, weights=ws)), len(vals)

def block_split(n, block=50000):
    train = ((np.arange(n)//block) % 2 == 0)
    return train, ~train

def fit_probs(prev, cond, nxt, na, nb, nc, alpha=0.5, augmented=False):
    if augmented:
        idx = (prev.astype(np.int64)*nb + cond.astype(np.int64))*nc + nxt.astype(np.int64)
        c = np.bincount(idx, minlength=na*nb*nc).reshape(na,nb,nc).astype(float)
        return (c+alpha)/(c.sum(axis=2, keepdims=True)+alpha*nc)
    idx = cond.astype(np.int64)*nc + nxt.astype(np.int64)
    c = np.bincount(idx, minlength=nb*nc).reshape(nb,nc).astype(float)
    return (c+alpha)/(c.sum(axis=1, keepdims=True)+alpha*nc)

def logloss_bits(P, prev, cond, nxt, augmented=False):
    p = P[prev,cond,nxt] if augmented else P[cond,nxt]
    return float(-np.mean(np.log2(p)))

@njit
def simulate_markov(cumprob, init_state, n, seed):
    np.random.seed(seed)
    out = np.empty(n, dtype=np.int32)
    out[0] = init_state
    m = cumprob.shape[1]
    for i in range(1,n):
        r = np.random.random()
        row = cumprob[out[i-1]]
        lo, hi = 0, m-1
        while lo < hi:
            mid = (lo+hi)//2
            if r <= row[mid]:
                hi = mid
            else:
                lo = mid+1
        out[i] = lo
    return out

def transition_cdf(y, nstates):
    idx = y[:-1].astype(np.int64)*nstates + y[1:].astype(np.int64)
    C = np.bincount(idx, minlength=nstates*nstates).reshape(nstates,nstates).astype(float)
    rows = C.sum(axis=1, keepdims=True)
    P = np.divide(C, rows, out=np.full_like(C,1/nstates), where=rows>0)
    cdf = np.cumsum(P, axis=1)
    cdf[:,-1] = 1.0
    return cdf

def null_calibration(primes, lo, hi, q, reps=100, seed=12345, base_q=30):
    p = primes[(primes>=lo)&(primes<=hi)]
    x, base_units = encode_residues(p, base_q)
    y, y_units = encode_residues(p, q)
    na = nc = len(base_units)
    nb = len(y_units)

    actual, _, _ = empirical_cmi(x[:-2], y[1:-1], x[2:], na, nb, nc)

    base_map = {int(v):i for i,v in enumerate(base_units)}
    x_from_y = np.array([base_map[int(v % base_q)] for v in y_units], dtype=np.int32)
    cdf = transition_cdf(y, nb)

    null = np.empty(reps)
    for r in range(reps):
        ys = simulate_markov(cdf, int(y[0]), len(y), seed+r)
        xs = x_from_y[ys]
        null[r], _, _ = empirical_cmi(xs[:-2], ys[1:-1], xs[2:], na, nb, nc)

    mean = float(null.mean())
    sd = float(null.std(ddof=1))
    return {
        "lo":lo, "hi":hi, "q_present":q, "reps":reps,
        "actual_cmi_bits":actual,
        "null_mean_cmi_bits":mean,
        "null_sd_cmi_bits":sd,
        "excess_over_markov_null_bits":actual-mean,
        "z_descriptive":(actual-mean)/sd if sd>0 else np.nan,
        "null_min_bits":float(null.min()),
        "null_max_bits":float(null.max()),
    }

def analyze_window(primes, lo, hi, q, base_q=30, block=50000, alpha=0.5, min_context=200):
    p = primes[(primes>=lo)&(primes<=hi)]
    x, bu = encode_residues(p, base_q)
    y, yu = encode_residues(p, q)
    prev, cond, nxt = x[:-2], y[1:-1], x[2:]
    na = nc = len(bu); nb = len(yu)

    cmi, bias, df = empirical_cmi(prev, cond, nxt, na, nb, nc)
    tr, te = block_split(len(prev), block)
    P0 = fit_probs(prev[tr],cond[tr],nxt[tr],na,nb,nc,alpha,False)
    P1 = fit_probs(prev[tr],cond[tr],nxt[tr],na,nb,nc,alpha,True)
    ll0 = logloss_bits(P0,prev[te],cond[te],nxt[te],False)
    ll1 = logloss_bits(P1,prev[te],cond[te],nxt[te],True)
    maxtv, meantv, npairs = tv_stats(prev,cond,nxt,na,nb,nc,min_context)
    return {
        "lo":lo,"hi":hi,"q_present":q,"n_primes":len(p),"n_triples":len(prev),
        "cmi_bits":cmi,
        "cmi_null_bias_first_order_bits":bias,
        "cmi_bias_corrected_bits":cmi-bias,
        "cmi_df_reference":df,
        "base_logloss_bits":ll0,
        "augmented_logloss_bits":ll1,
        "heldout_history_gain_bits":ll0-ll1,
        "max_tv":maxtv,
        "weighted_mean_tv":meantv,
        "n_tv_pairs":npairs,
    }

def parse_windows(s):
    ans=[]
    for z in s.split(","):
        a,b=z.split(":")
        ans.append((int(a),int(b)))
    return ans

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--max",type=int,default=100_000_000)
    ap.add_argument("--windows",default="10000000:20000000,20000000:40000000,50000000:100000000")
    ap.add_argument("--q",default="30,210,2310")
    ap.add_argument("--block",type=int,default=50000)
    ap.add_argument("--alpha",type=float,default=0.5)
    ap.add_argument("--min-context",type=int,default=200)
    ap.add_argument("--null-window",default="50000000:100000000")
    ap.add_argument("--null-reps",type=int,default=100)
    ap.add_argument("--seed",type=int,default=12345)
    ap.add_argument("--out-prefix",default="cont_p")
    args=ap.parse_args()

    qs=[int(x) for x in args.q.split(",")]
    windows=parse_windows(args.windows)
    primes=primes_upto(args.max)

    rows=[analyze_window(primes,lo,hi,q,args.block and 30,args.block,args.alpha,args.min_context)
          for lo,hi in windows for q in qs]
    pd.DataFrame(rows).to_csv(args.out_prefix+"_windows.csv",index=False)

    nlo,nhi=parse_windows(args.null_window)[0]
    nullrows=[null_calibration(primes,nlo,nhi,q,args.null_reps,args.seed) for q in qs]
    pd.DataFrame(nullrows).to_csv(args.out_prefix+"_null.csv",index=False)

    print(pd.DataFrame(rows).to_string(index=False))
    print()
    print(pd.DataFrame(nullrows).to_string(index=False))

if __name__=="__main__":
    main()
