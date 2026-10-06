import numpy as np, pandas as pd, math, json, hashlib, zipfile
from pathlib import Path
from math import gcd

OUT=Path('/mnt/data/CONT_PRIME_MEMORY_v0_6')
OUT.mkdir(exist_ok=True)

LO,HI=50_000_000,100_000_000
BLOCK=50_000
ALPHA=0.5
TAUS=np.array([0.,1.,3.,10.,30.,100.,300.,1000.,3000.,10000.,30000.,100000.])

CHAINS={
    'primorial_new_primes':[30,210,2310,30030],
    '2_adic_refinement':[30,60,120,240,480,960,1920,3840,7680,15360,30720],
    '3_adic_refinement':[30,90,270,810,2430,7290,21870],
    '5_adic_refinement':[30,150,750,3750,18750],
    'mixed_refinement':[30,60,180,360,2520,27720],
}


def primes_upto(n):
    s=np.ones(n+1,dtype=np.bool_)
    s[:2]=False
    s[4::2]=False
    for p in range(3,int(n**0.5)+1,2):
        if s[p]: s[p*p::2*p]=False
    return np.flatnonzero(s).astype(np.int32)

def units(q):
    return np.array([a for a in range(q) if gcd(a,q)==1],dtype=np.int32)

def encode(v,q):
    u=units(q)
    m=np.full(q,-1,dtype=np.int32)
    m[u]=np.arange(len(u),dtype=np.int32)
    z=m[v%q]
    if np.any(z<0): raise ValueError(q)
    return z,u

def entropy_bits(z,k):
    c=np.bincount(z,minlength=k).astype(float)
    p=c[c>0]/c.sum()
    return float(-(p*np.log2(p)).sum())

def split_masks(n):
    block_id=np.arange(n,dtype=np.int64)//BLOCK
    return (block_id%3==0),(block_id%3==1),(block_id%3==2),block_id

def fit_models(prev,y,nxt,mask,na,nb,nc):
    # base P(next|y)
    idx=y[mask].astype(np.int64)*nc+nxt[mask]
    cb=np.bincount(idx,minlength=nb*nc).reshape(nb,nc).astype(float)
    pb=(cb+ALPHA)/(cb.sum(1,keepdims=True)+ALPHA*nc)
    # augmented P(next|prev,y)
    idx2=(prev[mask].astype(np.int64)*nb+y[mask].astype(np.int64))*nc+nxt[mask]
    ca=np.bincount(idx2,minlength=na*nb*nc).reshape(na,nb,nc).astype(float)
    ctx=ca.sum(2)
    pa=(ca+ALPHA)/(ctx[:,:,None]+ALPHA*nc)
    return pb,pa,ctx

def losses(pb,pa,ctx,prev,y,nxt,mask,tau):
    yy=y[mask]; aa=prev[mask]; cc=nxt[mask]
    p0=pb[yy,cc]
    if tau==0:
        mix=pa[aa,yy,cc]
    else:
        lam=ctx[aa,yy]/(ctx[aa,yy]+tau)
        mix=lam*pa[aa,yy,cc]+(1-lam)*p0
    return float(-np.mean(np.log2(p0))), float(-np.mean(np.log2(mix)))

def per_test_block_gain(pb,pa,ctx,prev,y,nxt,test,block_id,tau):
    ids=np.unique(block_id[test])
    gains=[]
    for bid in ids:
        m=test & (block_id==bid)
        l0,l1=losses(pb,pa,ctx,prev,y,nxt,m,tau)
        gains.append(l0-l1)
    g=np.array(gains,float)
    mean=float(g.mean())
    sd=float(g.std(ddof=1)) if len(g)>1 else float('nan')
    se=sd/math.sqrt(len(g)) if len(g)>1 else float('nan')
    return mean,sd,se,mean-1.96*se,mean+1.96*se,len(g)

def factorization(q):
    n=q; fs=[]; p=2
    while p*p<=n:
        e=0
        while n%p==0:
            n//=p;e+=1
        if e: fs.append((p,e))
        p+=1
    if n>1: fs.append((n,1))
    return '*'.join(str(p) + (f'^{e}' if e>1 else '') for p,e in fs)

pr=primes_upto(HI)
p=pr[(pr>=LO)&(pr<=HI)]
x,u30=encode(p,30)
prev=x[:-2]; nxt=x[2:]
train,val,test,block_id=split_masks(len(prev))

unique_q=sorted(set(q for chain in CHAINS.values() for q in chain))
rows=[]
for q in unique_q:
    y_full,uy=encode(p,q)
    y=y_full[1:-1]
    nb=len(uy)
    pb,pa,ctx=fit_models(prev,y,nxt,train,8,nb,8)
    base_val,_=losses(pb,pa,ctx,prev,y,nxt,val,TAUS[0])
    vals=[]
    for tau in TAUS:
        _,augv=losses(pb,pa,ctx,prev,y,nxt,val,tau)
        vals.append((augv,tau))
    vals.sort()
    best_aug_val,best_tau=vals[0]
    base_test,aug_test=losses(pb,pa,ctx,prev,y,nxt,test,best_tau)
    block_mean,block_sd,block_se,ci_lo,ci_hi,nblocks=per_test_block_gain(pb,pa,ctx,prev,y,nxt,test,block_id,best_tau)
    ent=entropy_bits(y,nb)
    c=np.bincount(y,minlength=nb)
    active=c[c>0]
    rows.append({
        'q_present':q,'factorization':factorization(q),'phi_q':nb,'log2_phi':math.log2(nb),
        'empirical_present_entropy_bits':ent,'effective_states_2^H':2**ent,
        'active_states':int((c>0).sum()),'median_triples_per_state':float(np.median(active)),
        'best_tau':best_tau,
        'base_val_logloss_bits':base_val,'aug_val_logloss_bits':best_aug_val,
        'val_history_gain_bits':base_val-best_aug_val,
        'base_test_logloss_bits':base_test,'aug_test_logloss_bits':aug_test,
        'test_history_gain_bits':base_test-aug_test,
        'block_mean_gain_bits':block_mean,'block_sd_gain_bits':block_sd,'block_se_gain_bits':block_se,
        'block_ci95_low_bits':ci_lo,'block_ci95_high_bits':ci_hi,'n_test_blocks':nblocks,
        'train_n':int(train.sum()),'val_n':int(val.sum()),'test_n':int(test.sum())
    })
    print(q,nb,best_tau,base_test-aug_test,ci_lo,ci_hi,flush=True)

master=pd.DataFrame(rows).sort_values('q_present')
master.to_csv(OUT/'dense_moduli_master.csv',index=False)

# chain-specific table with refinement step and ratio
chain_rows=[]
lookup=master.set_index('q_present')
for name,chain in CHAINS.items():
    prevq=None
    for i,q in enumerate(chain):
        r=lookup.loc[q].to_dict()
        r['chain']=name; r['chain_step']=i; r['refines_q']=prevq if prevq is not None else ''
        chain_rows.append(r); prevq=q
chains=pd.DataFrame(chain_rows)
chains.to_csv(OUT/'dense_nested_chains.csv',index=False)

# matched-complexity comparisons, especially phi=48 neighborhood and phi around 5-8k
comp=[]
for q in unique_q:
    r=lookup.loc[q]
    comp.append({'q':q,'phi':int(r.phi_q),'factorization':r.factorization,'gain':r.test_history_gain_bits,
                 'ci_low':r.block_ci95_low_bits,'ci_high':r.block_ci95_high_bits})
pd.DataFrame(comp).sort_values(['phi','q']).to_csv(OUT/'complexity_matched_comparisons.csv',index=False)

# simple descriptive regression on positive/near-positive gains is inappropriate; instead rank by entropy.
curve=master[['q_present','factorization','phi_q','empirical_present_entropy_bits','test_history_gain_bits','block_ci95_low_bits','block_ci95_high_bits','best_tau']].sort_values('empirical_present_entropy_bits')
curve.to_csv(OUT/'gain_vs_present_richness.csv',index=False)

# generate concise summary text
phi48=master[master.phi_q.between(40,56)][['q_present','factorization','phi_q','test_history_gain_bits','block_ci95_low_bits','block_ci95_high_bits']]
summary={
 'window':[LO,HI], 'n_primes':int(len(p)), 'n_triples':int(len(prev)),
 'chains':CHAINS,
 'notes':[
   'Backoff tau selected on validation and frozen on test.',
   '95% intervals are descriptive normal intervals across held-out 50k-event test blocks, not formal arithmetic p-values.',
   'Multiple nested chains separate nominal state richness from which arithmetic information is added.'
 ]
}
(OUT/'manifest.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')

# README with key findings filled after inspecting programmatically
# extract chain trends
lines=[]
for name,chain in CHAINS.items():
    vals=[lookup.loc[q,'test_history_gain_bits'] for q in chain]
    lines.append(name+': '+', '.join(f'{q}:{g:+.6f}' for q,g in zip(chain,vals)))

readme=f'''# CONT-P v0.6 — courbes denses de raffinement du présent

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
- primoriale : {CHAINS['primorial_new_primes']}
- raffinement 2-adique : {CHAINS['2_adic_refinement']}
- raffinement 3-adique : {CHAINS['3_adic_refinement']}
- raffinement 5-adique : {CHAINS['5_adic_refinement']}
- mixte : {CHAINS['mixed_refinement']}

## Gains historiques test (bit/symbole)
'''+'\n'.join('- '+x for x in lines)+f'''

## Contrôle par blocs
Les colonnes block_ci95_low_bits / block_ci95_high_bits donnent un intervalle descriptif construit à partir des gains moyens par bloc test. Il ne s'agit pas d'un p-value ni d'un intervalle de confiance arithmétique asymptotique.

## Comparaison à complexité voisine
{phi48.to_string(index=False)}

## Statut
Expérience finie et reproductible. Aucun théorème asymptotique, aucune implication RH et aucune revendication de nouveauté ne sont formulés à ce stade.
'''
(OUT/'README.md').write_text(readme,encoding='utf-8')

# include script
script_src=Path('/mnt/data/cont_p_v06_dense_curve.py').read_text(encoding='utf-8')
(OUT/'cont_p_v06_dense_curve.py').write_text(script_src,encoding='utf-8')

zip_path=Path('/mnt/data/CONT_PRIME_MEMORY_v0_6.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.iterdir()):
        z.write(f,arcname=f'{OUT.name}/{f.name}')
sha=hashlib.sha256(zip_path.read_bytes()).hexdigest()
Path('/mnt/data/CONT_PRIME_MEMORY_v0_6.zip.sha256.txt').write_text(f'{sha}  {zip_path.name}\n',encoding='ascii')
print('SHA256',sha)
print('\nTOP BY ENTROPY\n',curve.to_string(index=False))
