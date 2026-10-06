import math, csv, json, zipfile, hashlib
from pathlib import Path
from math import gcd
import numpy as np

OUT=Path('/mnt/data/CONT_PRIME_MEMORY_v0_11')
OUT.mkdir(exist_ok=True)

# primes helper

def primes_upto(n):
    s=np.ones(n+1,dtype=bool); s[:2]=False
    for p in range(2,int(n**0.5)+1):
        if s[p]: s[p*p::p]=False
    return np.flatnonzero(s).tolist()

PRIMES=primes_upto(199)
BASE_RES=[1,7,11,13,17,19,23,29]
base_index={r:i for i,r in enumerate(BASE_RES)}

def units(q):
    return [a for a in range(q) if gcd(a,q)==1]

def local_factor_triplet(p,g1,g2):
    vals={0%p,g1%p,(g1+g2)%p}
    nu=len(vals)
    if nu>=p:
        return 0.0
    return (1.0-nu/p)/((1.0-1.0/p)**3)

def conditional_singular_triplet(q,g1,g2,pmax=199):
    w=1.0
    for p in PRIMES:
        if p>pmax: break
        if q%p==0: # already conditioned on coprimality mod q
            continue
        f=local_factor_triplet(p,g1,g2)
        if f==0:
            return 0.0
        w*=f
    return w

def cmi_from_joint(J):
    # J[a,b,c] nonnegative; normalize
    N=J.sum()
    if N<=0: return float('nan')
    p=J/N
    pab=p.sum(axis=2)
    pbc=p.sum(axis=0)
    pb=p.sum(axis=(0,2))
    I=0.0
    it=np.nditer(p, flags=['multi_index'])
    for x in it:
        v=float(x)
        if v<=0: continue
        a,b,c=it.multi_index
        I += v*math.log2(v*pb[b]/(pab[a,b]*pbc[b,c]))
    return I

def model_G(q, L, hmax=180, pmax=199, poisson=True):
    us=units(q); bmap={y:i for i,y in enumerate(us)}
    J=np.zeros((8,len(us),8),dtype=np.float64)
    # even gaps only for primes >2
    gs=range(2,hmax+1,2)
    # precompute gap-pair weights independent of y
    W={}
    for g1 in gs:
        for g2 in gs:
            s=conditional_singular_triplet(q,g1,g2,pmax)
            if s==0: continue
            decay=math.exp(-(g1+g2)/L) if poisson else 1.0
            W[(g1,g2)]=s*decay
    for y in us:
        bi=bmap[y]
        for (g1,g2),w in W.items():
            # endpoints must also be reduced mod q: conditional progression state
            if gcd((y-g1)%q,q)!=1 or gcd((y+g2)%q,q)!=1:
                continue
            a=(y-g1)%30; c=(y+g2)%30
            ai=base_index.get(a); ci=base_index.get(c)
            if ai is None or ci is None: continue
            J[ai,bi,ci]+=w
    return cmi_from_joint(J), J.sum(), len(W)

# Sensitivity grid around x in 50-100M and truncation/pmax choices
rows=[]
for xmid in [60_000_000,75_000_000,90_000_000]:
    L=math.log(xmid)
    for hmax in [100,140,180,240]:
        for pmax in [47,97,199]:
            g180,m180,nw180=model_G(180,L,hmax,pmax,True)
            g210,m210,nw210=model_G(210,L,hmax,pmax,True)
            supp=(g180-g210)/g180 if g180 else float('nan')
            rows.append(dict(xmid=xmid,logx=L,hmax=hmax,pmax=pmax,G180_model=g180,G210_model=g210,suppression_fraction=supp,total_mass_180=m180,total_mass_210=m210,weight_pairs_180=nw180,weight_pairs_210=nw210))

with open(OUT/'los_poisson_model_sensitivity.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

# canonical setting
canon=[r for r in rows if r['xmid']==75_000_000 and r['hmax']==180 and r['pmax']==199][0]
obs_g180=0.00143000135
obs_g210=0.000273227529
obs_supp=(obs_g180-obs_g210)/obs_g180
# scale-free suppression is the main prediction; also scale model to observed G180 for a level comparison
scale=obs_g180/canon['G180_model']
pred_g210_scaled=canon['G210_model']*scale
pred_drop=obs_g180-pred_g210_scaled
explained=pred_drop/(obs_g180-obs_g210)
summary={
    'model':'LOS-Poissonized conditional singular-series triplet model',
    'xmid':canon['xmid'],'logx':canon['logx'],'hmax':canon['hmax'],'pmax':canon['pmax'],
    'G180_model_raw':canon['G180_model'],'G210_model_raw':canon['G210_model'],
    'suppression_model':canon['suppression_fraction'],
    'G180_observed':obs_g180,'G210_observed':obs_g210,'suppression_observed':obs_supp,
    'scaled_G210_prediction':pred_g210_scaled,
    'scaled_drop_prediction':pred_drop,
    'fraction_observed_drop_explained':explained,
    'scale_to_G180':scale,
    'epistemic_status':'semi-analytic conditional heuristic; not theorem about primes'
}
with open(OUT/'canonical_180_210_prediction.json','w',encoding='utf-8') as f: json.dump(summary,f,indent=2)
with open(OUT/'canonical_180_210_prediction.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=summary.keys()); w.writeheader(); w.writerow(summary)

# Decompose effect: local SS only vs Poissonized, to isolate consecutivity weighting.
comp=[]
L=math.log(75_000_000)
for poisson in [False,True]:
    for q in [180,210]:
        G,m,nw=model_G(q,L,180,199,poisson)
        comp.append({'q':q,'poisson_consecutivity':poisson,'G_model':G,'mass':m,'weight_pairs':nw})
with open(OUT/'consecutivity_ablation.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=comp[0].keys()); w.writeheader(); w.writerows(comp)

# extract suppression each mode
for mode in [False,True]:
    aa=[r for r in comp if r['poisson_consecutivity']==mode]
    a={r['q']:r['G_model'] for r in aa}
    print('mode',mode,'G180',a[180],'G210',a[210],'supp',(a[180]-a[210])/a[180])
print('CANON',json.dumps(summary,indent=2))

note=f'''# CONT-P v0.11 — condition de consécutivité dans un modèle semi-analytique\n\n## Modèle\nPour Q in {{180,210}}, on conditionne sur le présent y appartenant aux unités modulo Q.\nLes gaps g1,g2 sont pondérés par\n\n  w_Q(g1,g2) = exp(-(g1+g2)/log x) * S_Q({{0,g1,g1+g2}}),\n\noù S_Q est la série singulière conditionnelle dont on retire les facteurs premiers divisant Q, déjà observés par le présent.\n\nLe facteur exponentiel est la version Poissonisée de la condition de consécutivité mise en avant dans l'heuristique de Lemke Oliver–Soundararajan.\n\n## Résultat canonique\n- x milieu = 75,000,000\n- Hmax = 180\n- premiers locaux jusqu'à 199\n- suppression modèle 180->210 = {canon['suppression_fraction']:.6%}\n- suppression observée = {obs_supp:.6%}\n- G210 prédit après calibration du seul niveau sur G180 = {pred_g210_scaled:.12g}\n- G210 observé = {obs_g210:.12g}\n- fraction de la baisse observée reproduite = {explained:.6%}\n\n## Lecture\nCe modèle incorpore explicitement deux ingrédients absents du proxy v0.10 :\n1. l'admissibilité conditionnelle modulo Q ;\n2. une pénalisation de consécutivité exp(-(g1+g2)/log x).\n\nIl reste heuristique : la véritable inclusion-exclusion de LOS contient des termes secondaires plus fins, et l'indépendance Poisson n'est pas une identité pour les nombres premiers.\n'''
(OUT/'THEORY_NOTE.md').write_text(note,encoding='utf-8')

readme=f'''# CONT-P v0.11\n\nExtension de v0.10 vers un modèle semi-analytique de motifs de trois nombres premiers consécutifs.\n\nRésultat canonique : suppression prédite 180->210 = {canon['suppression_fraction']:.4%}; observée = {obs_supp:.4%}.\nAprès calibration de l'échelle sur G(180), le modèle reproduit {explained:.2%} de la baisse observée.\n\nStatut : heuristique semi-analytique, non théorème.\n'''
(OUT/'README.md').write_text(readme,encoding='utf-8')

refs='''Lemke Oliver, R. J.; Soundararajan, K. Unexpected biases in the distribution of consecutive primes. PNAS 113 (2016), E4446-E4454. DOI 10.1073/pnas.1605366113.\nLemke Oliver, R. J.; Soundararajan, K. The distribution of consecutive prime biases and sums of sawtooth random variables. Math. Proc. Camb. Phil. Soc. 168 (2020), 149-169. DOI 10.1017/S0305004118000592.\nMurray, D. J. Prime-Residue Projection Tomography of Consecutive-Prime Biases: Primorial Recovery and Gap-Word Order Asymmetry. SSRN 6947578 (2026).\n'''
(OUT/'REFERENCES.txt').write_text(refs,encoding='utf-8')

manifest={'version':'0.11','files':[p.name for p in OUT.iterdir()],'canonical':summary}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

zip_path=Path('/mnt/data/CONT_PRIME_MEMORY_v0_11.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.iterdir()): z.write(p,arcname=f'{OUT.name}/{p.name}')
sha=hashlib.sha256(zip_path.read_bytes()).hexdigest()
Path('/mnt/data/CONT_PRIME_MEMORY_v0_11.zip.sha256.txt').write_text(f'{sha}  {zip_path.name}\n',encoding='ascii')
print('SHA',sha)
