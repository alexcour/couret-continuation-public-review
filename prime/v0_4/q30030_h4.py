import numpy as np
from math import gcd

def primes_upto(n):
    s=np.ones(n+1,dtype=np.bool_); s[:2]=False; s[4::2]=False
    for p in range(3,int(n**0.5)+1,2):
        if s[p]: s[p*p::2*p]=False
    return np.flatnonzero(s).astype(np.int32)

def units(q): return np.array([a for a in range(q) if gcd(a,q)==1],dtype=np.int32)
def enc(v,q):
    u=units(q); m=np.full(q,-1,dtype=np.int32); m[u]=np.arange(len(u),dtype=np.int32); return m[v%q],u

def lookup_counts(keys,uniq,cnts):
    pos=np.searchsorted(uniq,keys); ok=(pos<len(uniq)); out=np.zeros(len(keys),dtype=np.int64)
    ix=np.where(ok)[0]; match=uniq[pos[ix]]==keys[ix]; out[ix[match]]=cnts[pos[ix[match]]]; return out

pr=primes_upto(100_000_000); p=pr[(pr>=50_000_000)&(pr<=100_000_000)]
x,_=enc(p,30); y,yu=enc(p,30030)
max_h=4; h=4; nidx=np.arange(max_h,len(x)-1,dtype=np.int64); target=x[nidx+1].astype(np.int64); ctx=y[nidx].astype(np.int64)
for lag in range(1,h+1): ctx=ctx*8+x[nidx-lag].astype(np.int64)
train=((nidx//50000)%2==0); test=~train
k_train=ctx[train]*8+target[train]
uniq_pair,cnt_pair=np.unique(k_train,return_counts=True); uniq_ctx,cnt_ctx=np.unique(ctx[train],return_counts=True)
pair_test=ctx[test]*8+target[test]
pc=lookup_counts(pair_test,uniq_pair,cnt_pair); cc=lookup_counts(ctx[test],uniq_ctx,cnt_ctx)
probs=(pc+0.5)/(cc+4.0); ll=float(-np.mean(np.log2(probs))); unseen=float(np.mean(cc==0))
print(ll,unseen,int(train.sum()),int(test.sum()),len(uniq_ctx))
