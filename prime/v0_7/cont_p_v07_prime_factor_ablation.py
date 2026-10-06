import numpy as np, pandas as pd, math, json, hashlib, zipfile
from pathlib import Path
from math import gcd

OUT=Path('/mnt/data/CONT_PRIME_MEMORY_v0_7')
OUT.mkdir(exist_ok=True)
LO,HI=50_000_000,100_000_000
BLOCK=50_000
ALPHA=0.5
TAUS=np.array([0.,1.,3.,10.,30.,100.,300.,1000.,3000.,10000.,30000.,100000.])
PRIMES_ADD=[7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
PAIR_SETS=[(7,11),(7,13),(11,13),(7,17),(11,17),(13,17),(7,19),(11,19),(13,19)]
TRIPLE_SETS=[(7,11,13),(7,11,17),(7,13,17),(11,13,17)]

def primes_upto(n):
    s=np.ones(n+1,dtype=np.bool_); s[:2]=False; s[4::2]=False
    for p in range(3,int(n**0.5)+1,2):
        if s[p]: s[p*p::2*p]=False
    return np.flatnonzero(s).astype(np.int32)
def units(q): return np.array([a for a in range(q) if gcd(a,q)==1],dtype=np.int32)
def encode(v,q):
    u=units(q); m=np.full(q,-1,dtype=np.int32); m[u]=np.arange(len(u),dtype=np.int32)
    z=m[v%q]
    if np.any(z<0): raise ValueError(q)
    return z,u
def split_masks(n):
    b=np.arange(n,dtype=np.int64)//BLOCK
    return (b%3==0),(b%3==1),(b%3==2),b
def fit(prev,y,nxt,mask,nb):
    idx=y[mask].astype(np.int64)*8+nxt[mask]
    cb=np.bincount(idx,minlength=nb*8).reshape(nb,8).astype(float)
    pb=(cb+ALPHA)/(cb.sum(1,keepdims=True)+ALPHA*8)
    idx2=(prev[mask].astype(np.int64)*nb+y[mask].astype(np.int64))*8+nxt[mask]
    ca=np.bincount(idx2,minlength=8*nb*8).reshape(8,nb,8).astype(float)
    ctx=ca.sum(2); pa=(ca+ALPHA)/(ctx[:,:,None]+ALPHA*8)
    return pb,pa,ctx
def ll(pb,pa,ctx,prev,y,nxt,mask,tau):
    a=prev[mask]; b=y[mask]; c=nxt[mask]
    p0=pb[b,c]
    lam=ctx[a,b]/(ctx[a,b]+tau) if tau>0 else np.ones(len(a))
    p1=lam*pa[a,b,c]+(1-lam)*p0
    return float(-np.mean(np.log2(p0))),float(-np.mean(np.log2(p1)))
def block_gain(pb,pa,ctx,prev,y,nxt,test,bids,tau):
    vals=[]
    for bid in np.unique(bids[test]):
        m=test&(bids==bid); a,b=ll(pb,pa,ctx,prev,y,nxt,m,tau); vals.append(a-b)
    g=np.array(vals); se=g.std(ddof=1)/math.sqrt(len(g)); mean=g.mean()
    return float(mean),float(mean-1.96*se),float(mean+1.96*se)
def evalq(p,x,prev,nxt,train,val,test,bids,q,label,added):
    yfull,u=encode(p,q); y=yfull[1:-1]; nb=len(u)
    pb,pa,ctx=fit(prev,y,nxt,train,nb)
    basev,_=ll(pb,pa,ctx,prev,y,nxt,val,0)
    candidates=[]
    for tau in TAUS:
        _,a=ll(pb,pa,ctx,prev,y,nxt,val,tau); candidates.append((a,tau))
    a_val,tau=min(candidates)
    btest,atest=ll(pb,pa,ctx,prev,y,nxt,test,tau)
    mean,lo,hi=block_gain(pb,pa,ctx,prev,y,nxt,test,bids,tau)
    return {'q_present':q,'label':label,'added_factors':added,'phi_q':nb,'best_tau':tau,
            'val_gain_bits':basev-a_val,'test_gain_bits':btest-atest,
            'block_mean_gain_bits':mean,'block_ci95_low_bits':lo,'block_ci95_high_bits':hi}

pr=primes_upto(HI); p=pr[(pr>=LO)&(pr<=HI)]
# base x mod30
u30=units(30); m30=np.full(30,-1,dtype=np.int32);m30[u30]=np.arange(8,dtype=np.int32);x=m30[p%30]
prev=x[:-2];nxt=x[2:];train,val,test,bids=split_masks(len(prev))
rows=[]
rows.append(evalq(p,x,prev,nxt,train,val,test,bids,30,'base',''))
for r in PRIMES_ADD:
    rows.append(evalq(p,x,prev,nxt,train,val,test,bids,30*r,f'30x{r}',str(r)))
for a,b in PAIR_SETS:
    rows.append(evalq(p,x,prev,nxt,train,val,test,bids,30*a*b,f'30x{a}x{b}',f'{a},{b}'))
for a,b,c in TRIPLE_SETS:
    rows.append(evalq(p,x,prev,nxt,train,val,test,bids,30*a*b*c,f'30x{a}x{b}x{c}',f'{a},{b},{c}'))

df=pd.DataFrame(rows).sort_values(['phi_q','q_present'])
df.to_csv(OUT/'prime_factor_ablation.csv',index=False)
base=float(df[df.q_present==30].iloc[0].test_gain_bits)
df['fraction_memory_removed_vs_mod30']=1-df.test_gain_bits/base
df.to_csv(OUT/'prime_factor_ablation_with_removed_fraction.csv',index=False)

single=df[df.added_factors.str.match(r'^\d+$',na=False)].copy()
single['added_prime']=single.added_factors.astype(int)
single=single.sort_values('added_prime')
single.to_csv(OUT/'single_prime_additions.csv',index=False)

small=single[single.added_prime<=47]
readme=f'''# CONT-P v0.7 — ablation des facteurs premiers

## Question
La disparition de la mémoire historique dépend-elle seulement du nombre d'états du présent, ou surtout de certains facteurs premiers nouvellement introduits dans le modulus ?

## Protocole
Même fenêtre, split et backoff que v0.6. On part de q=30 puis on ajoute un seul premier r, q=30r, pour r=7,11,...,97. On teste aussi plusieurs paires et triplets.

## Référence
Gain historique mod 30 : {base:.9f} bit/symbole.

## Ajout d'un seul petit premier (r<=47)
{small[['added_prime','q_present','phi_q','test_gain_bits','block_ci95_low_bits','block_ci95_high_bits','fraction_memory_removed_vs_mod30']].to_string(index=False)}

## Lecture
Si deux représentations ont une complexité comparable mais des gains très différents, la nature arithmétique de l'information ajoutée compte davantage qu'une simple dimension d'état.

Les intervalles par blocs sont descriptifs et ne sont pas des p-values arithmétiques asymptotiques.
'''
(OUT/'README.md').write_text(readme,encoding='utf-8')
(OUT/'manifest.json').write_text(json.dumps({'version':'0.7','window':[LO,HI],'single_added_primes':PRIMES_ADD,'pairs':PAIR_SETS,'triples':TRIPLE_SETS},indent=2),encoding='utf-8')
(OUT/'cont_p_v07_prime_factor_ablation.py').write_text(Path('/mnt/data/cont_p_v07_prime_factor_ablation.py').read_text(),encoding='utf-8')
zip_path=Path('/mnt/data/CONT_PRIME_MEMORY_v0_7.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.iterdir()):z.write(f,arcname=f'{OUT.name}/{f.name}')
sha=hashlib.sha256(zip_path.read_bytes()).hexdigest();Path('/mnt/data/CONT_PRIME_MEMORY_v0_7.zip.sha256.txt').write_text(f'{sha}  {zip_path.name}\n',encoding='ascii')
print(single[['added_prime','q_present','phi_q','test_gain_bits','block_ci95_low_bits','block_ci95_high_bits','fraction_memory_removed_vs_mod30']].to_string(index=False))
print('\nPAIRS/TRIPLES\n',df[df.added_factors.str.contains(',',na=False)][['label','phi_q','test_gain_bits','block_ci95_low_bits','block_ci95_high_bits','fraction_memory_removed_vs_mod30']].to_string(index=False))
print('SHA256',sha)
