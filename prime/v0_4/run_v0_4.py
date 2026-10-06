import numpy as np, pandas as pd, math, json, hashlib, zipfile
from pathlib import Path
from math import gcd
from numba import njit

OUT=Path('/mnt/data/CONT_PRIME_MEMORY_v0_4')
OUT.mkdir(exist_ok=True)

def primes_upto(n):
    s=np.ones(n+1,dtype=np.bool_); s[:2]=False; s[4::2]=False
    for p in range(3,int(n**0.5)+1,2):
        if s[p]: s[p*p::2*p]=False
    return np.flatnonzero(s).astype(np.int32)

def units(q):
    return np.array([a for a in range(q) if gcd(a,q)==1],dtype=np.int32)

def enc(v,q):
    u=units(q); m=np.full(q,-1,dtype=np.int32); m[u]=np.arange(len(u),dtype=np.int32)
    z=m[v%q]
    if np.any(z<0): raise ValueError('window includes a prime divisor of modulus')
    return z,u

def cmi(a,b,c,na,nb,nc):
    idx=(a.astype(np.int64)*nb+b.astype(np.int64))*nc+c.astype(np.int64)
    C=np.bincount(idx,minlength=na*nb*nc).reshape(na,nb,nc)
    N=C.sum(); p=C/N; pab=C.sum(2)/N; pbc=C.sum(0)/N; pb=C.sum((0,2))/N
    nz=np.nonzero(C)
    I=float(np.sum(p[nz]*np.log2((p[nz]*pb[nz[1]])/(pab[nz[0],nz[1]]*pbc[nz[1],nz[2]]))))
    df=0
    for j in range(nb):
        S=C[:,j,:]
        r=np.count_nonzero(S.sum(1)); cc=np.count_nonzero(S.sum(0))
        if r and cc: df+=(r-1)*(cc-1)
    bias=df/(2*N*math.log(2))
    return I,bias,df

def build_sparse_markov(y,nstates):
    pairs=y[:-1].astype(np.int64)*nstates+y[1:].astype(np.int64)
    uniq,counts=np.unique(pairs,return_counts=True)
    src=(uniq//nstates).astype(np.int32); dst=(uniq%nstates).astype(np.int32)
    order=np.argsort(src,kind='stable'); src=src[order]; dst=dst[order]; counts=counts[order].astype(np.int64)
    row_ptr=np.zeros(nstates+1,dtype=np.int64); np.add.at(row_ptr,src+1,1); row_ptr=np.cumsum(row_ptr)
    cdf=np.empty(len(counts),dtype=np.float64)
    for s in range(nstates):
        lo,hi=row_ptr[s],row_ptr[s+1]
        if hi>lo:
            cs=np.cumsum(counts[lo:hi],dtype=np.float64); cdf[lo:hi]=cs/cs[-1]
    return row_ptr,dst,cdf

@njit
def sim_sparse(row_ptr,dst,cdf,init,n,seed):
    np.random.seed(seed); out=np.empty(n,dtype=np.int32); out[0]=init
    for i in range(1,n):
        s=out[i-1]; lo=row_ptr[s]; hi=row_ptr[s+1]
        if hi<=lo:
            out[i]=s; continue
        r=np.random.random(); a=lo; b=hi-1
        while a<b:
            mid=(a+b)//2
            if r<=cdf[mid]: b=mid
            else: a=mid+1
        out[i]=dst[a]
    return out

def markov_null_for_window(p,q,reps,seed):
    x,bu=enc(p,30); y,yu=enc(p,q); nb=len(yu)
    actual,bias,df=cmi(x[:-2],y[1:-1],x[2:],8,nb,8)
    base_map={int(v):i for i,v in enumerate(bu)}
    xmap=np.array([base_map[int(v%30)] for v in yu],dtype=np.int32)
    row_ptr,dst,cdfm=build_sparse_markov(y,nb)
    vals=np.empty(reps)
    for r in range(reps):
        ys=sim_sparse(row_ptr,dst,cdfm,int(y[0]),len(y),seed+r)
        xs=xmap[ys]
        vals[r]=cmi(xs[:-2],ys[1:-1],xs[2:],8,nb,8)[0]
    sd=float(vals.std(ddof=1)) if reps>1 else float('nan')
    return dict(q_present=q,phi_q=nb,reps=reps,n_primes=len(p),n_triples=len(p)-2,
                actual_cmi_bits=actual,first_order_bias_bits=bias,bias_corrected_cmi_bits=actual-bias,
                null_mean_cmi_bits=float(vals.mean()),null_sd_cmi_bits=sd,
                excess_over_markov_null_bits=float(actual-vals.mean()),
                z_descriptive=float((actual-vals.mean())/sd) if sd>0 else float('nan'),
                null_min_bits=float(vals.min()),null_max_bits=float(vals.max()),
                observed_transition_edges=int(len(dst)))

def lookup_counts(keys,uniq,cnts):
    pos=np.searchsorted(uniq,keys)
    ok=(pos<len(uniq)); out=np.zeros(len(keys),dtype=np.int64)
    ix=np.where(ok)[0]; match=uniq[pos[ix]]==keys[ix]
    out[ix[match]]=cnts[pos[ix[match]]]
    return out

def history_logloss(x,y,h,max_h=4,block=50000,alpha=0.5):
    nidx=np.arange(max_h,len(x)-1,dtype=np.int64)
    target=x[nidx+1].astype(np.int64)
    ctx=y[nidx].astype(np.int64)
    for lag in range(1,h+1):
        ctx=ctx*8+x[nidx-lag].astype(np.int64)
    train=((nidx//block)%2==0); test=~train
    k_train=ctx[train]*8+target[train]
    uniq_pair,cnt_pair=np.unique(k_train,return_counts=True)
    uniq_ctx,cnt_ctx=np.unique(ctx[train],return_counts=True)
    pair_test=ctx[test]*8+target[test]
    pc=lookup_counts(pair_test,uniq_pair,cnt_pair); cc=lookup_counts(ctx[test],uniq_ctx,cnt_ctx)
    probs=(pc+alpha)/(cc+alpha*8.0)
    ll=float(-np.mean(np.log2(probs))); unseen=float(np.mean(cc==0))
    return ll,unseen,int(train.sum()),int(test.sum()),len(uniq_ctx)

print('Generating primes...',flush=True)
pr=primes_upto(100_000_000)
print(f'Generated {len(pr):,} primes',flush=True)
_=sim_sparse(np.array([0,1,2],dtype=np.int64),np.array([0,1],dtype=np.int32),np.array([1.0,1.0]),0,5,1)

windows=[(10_000_000,20_000_000),(20_000_000,40_000_000),(50_000_000,100_000_000)]
qs=[30,210,2310,30030]
null_rows=[]
for wi,(lo,hi) in enumerate(windows):
    p=pr[(pr>=lo)&(pr<=hi)]
    for q in qs:
        reps=30 if q<30030 else 15
        row=markov_null_for_window(p,q,reps,seed=41000+wi*1000+q)
        row.update(lo=lo,hi=hi); null_rows.append(row)
        print('NULL',lo,hi,q,row['excess_over_markov_null_bits'],row['z_descriptive'],flush=True)
null_df=pd.DataFrame(null_rows); null_df.to_csv(OUT/'null_all_windows.csv',index=False)

stability=[]
for j,lo in enumerate(range(50_000_000,100_000_000,10_000_000)):
    hi=lo+10_000_000; p=pr[(pr>=lo)&(pr<=hi)]
    row=markov_null_for_window(p,30030,10,seed=52000+j*100)
    row.update(lo=lo,hi=hi); stability.append(row)
    print('STAB',lo,hi,row['excess_over_markov_null_bits'],flush=True)
stab_df=pd.DataFrame(stability); stab_df.to_csv(OUT/'q30030_10m_stability.csv',index=False)

p=pr[(pr>=50_000_000)&(pr<=100_000_000)]; x,_=enc(p,30)
depth_rows=[]
for q in qs:
    y,yu=enc(p,q); prev_ll=None
    for h in range(0,5):
        ll,unseen,ntr,nte,nctx=history_logloss(x,y,h)
        gain=np.nan if prev_ll is None else prev_ll-ll
        depth_rows.append(dict(lo=50_000_000,hi=100_000_000,q_present=q,phi_q=len(yu),history_depth=h,
                               heldout_logloss_bits=ll,incremental_gain_bits=gain,
                               unseen_test_context_fraction=unseen,train_samples=ntr,test_samples=nte,
                               observed_train_contexts=nctx))
        print('DEPTH',q,h,ll,gain,unseen,flush=True); prev_ll=ll
depth_df=pd.DataFrame(depth_rows); depth_df.to_csv(OUT/'memory_depth_heldout.csv',index=False)

summary=[]
for q in qs:
    row=null_df[(null_df.lo==50_000_000)&(null_df.hi==100_000_000)&(null_df.q_present==q)].iloc[0]
    d=depth_df[depth_df.q_present==q].copy(); best=d.loc[d.heldout_logloss_bits.idxmin()]
    summary.append(dict(q_present=q,phi_q=int(row.phi_q),largest_window_excess_bits=row.excess_over_markov_null_bits,
                        descriptive_z=row.z_descriptive,best_history_depth=int(best.history_depth),
                        best_heldout_logloss_bits=best.heldout_logloss_bits,
                        best_unseen_context_fraction=best.unseen_test_context_fraction))
summary_df=pd.DataFrame(summary); summary_df.to_csv(OUT/'summary.csv',index=False)

lines=['# CONT-P v0.4 - controles de stabilite et profondeur de memoire','',
       '## Statut','Calcul fini exploratoire. Aucun theoreme asymptotique, aucune memoire intrinseque et aucun lien RH ne sont revendiques.','',
       '## 1. Temoin markovien sur toutes les fenetres','']
for _,r in null_df.iterrows():
    lines.append(f'- [{int(r.lo):,},{int(r.hi):,}], Q={int(r.q_present)}: exces={r.excess_over_markov_null_bits:.6g} bit, z descriptif={r.z_descriptive:.2f}, reps={int(r.reps)}.')
lines += ['', '## 2. Stabilite locale de Q=30030 (fenetres de largeur 10M)','']
for _,r in stab_df.iterrows():
    lines.append(f'- [{int(r.lo):,},{int(r.hi):,}]: exces={r.excess_over_markov_null_bits:.6g} bit (10 temoins).')
lines += ['', '## 3. Profondeur predictive hors echantillon sur [50M,100M]','']
for q in qs:
    d=depth_df[depth_df.q_present==q]
    vals=', '.join([f'h={int(r.history_depth)}: {r.heldout_logloss_bits:.6f}' for _,r in d.iterrows()])
    lines.append(f'- Q={q}: {vals}.')
lines += ['', '## Lecture prudente','',
          '- La comparaison pertinente entre moduli reste l exces au-dessus d un temoin markovien de meme dimension, pas la CMI brute.',
          '- Les modeles d histoire profonde sont juges hors echantillon; un gain negatif signale que la complexite ajoutee n est pas soutenue par les donnees disponibles.',
          '- Q=30030 reste un regime parcimonieux: la stabilite entre fenetres et le taux de contextes jamais vus en apprentissage sont des diagnostics essentiels.',
          '- La prochaine decision doit dependre de la stabilite des signes et des gains, pas d un unique z descriptif.']
(OUT/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
manifest={'name':'CONT-P','version':'0.4','date':'2026-10-05','prime_bound':100_000_000,'q_values':qs,
          'main_window':[50_000_000,100_000_000],
          'experiments':['matched Markov null on 3 windows','Q=30030 five 10M windows','held-out memory depth 0..4'],
          'status':'exploratory finite computation','seed_families':[41000,52000]}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
zip_path=Path('/mnt/data/CONT_PRIME_MEMORY_v0_4.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.iterdir()): z.write(f,arcname=f'{OUT.name}/{f.name}')
sha=hashlib.sha256(zip_path.read_bytes()).hexdigest()
Path('/mnt/data/CONT_PRIME_MEMORY_v0_4.zip.sha256.txt').write_text(f'{sha}  {zip_path.name}\n',encoding='ascii')
print('SUMMARY')
print(summary_df.to_string(index=False))
print('SHA256',sha)
