"""COD-H-01 MSI synthetic-only engineering harness; NEVER a philological reader.

Input is a versioned manifest plus immutable 2D .npy bands. The only permitted
origin in v0.1 is synthetic. No TIFF/vendor decoder or real-data loader is implied.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

SCHEMA = "codh01-msi-synthetic-v1"
SHAPE = (128, 128)
FIDUCIALS = ((12, 13, 1.0), (16, 105, 0.8), (108, 24, 1.2), (109, 111, 0.6))
TARGET = (slice(45, 66), slice(47, 50))
CONTROL = (slice(78, 99), slice(78, 103))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def _template():
    yy, xx = np.indices(SHAPE)
    f = np.zeros(SHAPE, dtype=np.float64)
    for y, x, amp in FIDUCIALS:
        f += amp * np.exp(-((yy-y)**2+(xx-x)**2)/(2*2.0**2))
    return f


def _outside_roi():
    mask = np.ones(SHAPE, dtype=bool)
    mask[28:104, 28:112] = False
    return mask


def _orient(a, k, mirror):
    # Candidate is rotate counterclockwise k*90, then optional horizontal flip.
    b = np.rot90(a, k)
    return np.fliplr(b) if mirror else b


def _score(a):
    # Registration uses pre-specified fiducials OUTSIDE the content ROI.
    f = _template()
    m = _outside_roi()
    a = a[m] - np.median(a[m])
    f = f[m]
    return float(np.dot(a, f) / ((np.linalg.norm(a)*np.linalg.norm(f)) + 1e-12))


def choose_orientation(a):
    choices = sorted(((_score(_orient(a,k,mirror)), k, mirror)
                      for k in range(4) for mirror in (False, True)), reverse=True)
    best, k, mirror = choices[0]
    if best < 0.48 or best - choices[1][0] < 0.07:
        raise ValueError('orientation/fiducials inconclusive; fail closed')
    return _orient(a,k,mirror), {'rotation_ccw_90': k, 'mirror_after_rotation': mirror,
                                'score': round(best, 5), 'margin': round(best-choices[1][0], 5)}


def align_translation(a, max_shift=5):
    # Search integer shifts against independent, asymmetric, known fiducials.
    m = _outside_roi()
    template = _template()
    t = template[m]
    choices = []
    for dy in range(-max_shift, max_shift+1):
        for dx in range(-max_shift, max_shift+1):
            shifted = ndimage.shift(a, (dy,dx), order=1, mode='constant', cval=1.0)
            region = shifted[m] - np.median(shifted[m])
            s = float(np.dot(region,t) / (np.linalg.norm(region)*np.linalg.norm(t)+1e-12))
            choices.append((s,dy,dx))
    score, dy, dx = max(choices)
    if score < 0.65:
        raise ValueError('band alignment fiducials too weak; fail closed')
    shifted = ndimage.shift(a, (dy,dx), order=1, mode='constant', cval=1.0)
    return shifted, {'dy':dy, 'dx':dx, 'score':round(score,5), 'integer_only':True}


def generate(out_dir: Path, seed=20261018, scenario='signal'):
    """Invent non-letter patterns + separate holdout bands; no text is encoded."""
    if scenario not in ('signal','blank','artifact'):
        raise ValueError('unknown scenario')
    out_dir.mkdir(parents=True, exist_ok=True)
    if any(out_dir.iterdir()):
        raise FileExistsError('fixture directory must be empty (immutability)')
    rng = np.random.default_rng(seed)
    yy,xx = np.indices(SHAPE)
    paper = 1.0 + 0.012*np.sin(xx/19) + 0.009*np.cos(yy/15)
    f = _template()
    target = np.zeros(SHAPE)
    target[45:66,47:50] = 1
    target[61:64,47:69] = 1
    # These are geometric synthetic bars, NOT letters / transcription.
    bands=[]
    wavelengths=(450,550,650,750)
    shifts=((0,0),(2,-1),(-2,2),(1,3))
    for i in range(4):
        a = paper + 0.36*f + rng.normal(0,0.008,SHAPE)
        if scenario == 'signal':
            a -= (0.12 + 0.035*i)*target
        if scenario == 'artifact' and i == 0:
            a -= 0.24*target  # Single-band trap, NOT repeatable.
        if i == 1:
            a[85:91,86:92] -= 0.12  # Off-target nuisance / blank-control trap.
        a = np.roll(a,shifts[i],axis=(0,1))
        if i==2:
            a = np.fliplr(a)  # Known mirrored band must be recovered.
        bands.append(a.astype(np.float32))
    records=[]
    for i,a in enumerate(bands):
        name=f'band_{i:02d}.npy'
        p=out_dir/name
        np.save(p,a,allow_pickle=False)
        records.append({'path':name,'sha256':sha256_file(p),'bytes':p.stat().st_size,
                        'shape':list(a.shape),'dtype':str(a.dtype),'band_id':f'synthetic_{i}',
                        'wavelength_nm':wavelengths[i],'role':'synthetic_band',
                        'geometry':'simulated, unknown to analysis',
                        'flat_dark_frames':'not applicable: synthetic fixture'})
    manifest={'schema':SCHEMA,'origin':'SYNTHETIC_ONLY','seed':seed,'scenario':scenario,
              'source':'local deterministic NumPy generator, no manuscript pixels',
              'license':'CC0 synthetic demo only; NOT Glasgow MSI license',
              'folio':'NOT_APPLICABLE_SYNTHETIC','authorization':'no restricted data used',
              'reference_frame':'synthetic asymmetric registration fiducials',
              'bands':records}
    (out_dir/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return manifest


def verify_and_load(input_dir:Path):
    manifest=json.loads((input_dir/'manifest.json').read_text(encoding='utf-8'))
    if manifest.get('schema')!=SCHEMA or manifest.get('origin')!='SYNTHETIC_ONLY':
        raise ValueError('unsupported or real-origin manifest: real inputs forbidden in v0.1')
    for field in ('seed','scenario','source','license','folio','authorization','reference_frame'):
        if field not in manifest or manifest[field] in ('',None):
            raise ValueError(f'missing mandatory provenance field: {field}')
    records=manifest.get('bands')
    if not isinstance(records,list) or len(records)<3:
        raise ValueError('at least 3 documented synthetic bands required')
    seen=set(); out=[]
    for item in records:
        for field in ('path','sha256','bytes','shape','dtype','band_id','wavelength_nm','role','geometry','flat_dark_frames'):
            if field not in item or item[field] in ('',None):
                raise ValueError(f'band metadata missing: {field}')
        name=item['path']
        if name in seen or Path(name).name != name or not name.endswith('.npy'):
            raise ValueError('duplicate, traversal or non-npy band path')
        seen.add(name)
        path=input_dir/name
        if sha256_file(path)!=item['sha256'] or path.stat().st_size!=item['bytes']:
            raise ValueError(f'hash or size mismatch: {name}')
        a=np.load(path,allow_pickle=False)
        if list(a.shape)!=item['shape'] or str(a.dtype)!=item['dtype'] or a.shape!=SHAPE or not np.isfinite(a).all():
            raise ValueError(f'unsupported dimension/dtype/nonfinite: {name}')
        if item['role']!='synthetic_band' or not np.issubdtype(a.dtype,np.floating):
            raise ValueError('unsupported band role or pixel type')
        out.append(a.astype(np.float64))
    if len({x['band_id'] for x in records})!=len(records):
        raise ValueError('duplicate band IDs')
    return manifest,out


def pca_cube(cube):
    """Plain centered PCA, no guessed physical spectrum or sign-based philology."""
    flat=cube.reshape(-1,cube.shape[-1])
    centered=flat-flat.mean(axis=0)
    _,s,vh=np.linalg.svd(centered,full_matrices=False)
    # Resolve SVD sign ambiguity for byte-reproducible visualization.
    for i in range(len(vh)):
        j=np.argmax(np.abs(vh[i]))
        if vh[i,j]<0: vh[i]*=-1
    scores=centered@vh.T
    var=(s*s)/max(len(centered)-1,1)
    frac=var/var.sum() if var.sum()>0 else np.zeros_like(var)
    return scores.reshape(*cube.shape[:2],-1),frac,vh


def stretch(a):
    lo,hi=np.percentile(a,[2,98]);
    if hi-lo<1e-12: return np.zeros_like(a)
    return np.clip((a-lo)/(hi-lo),0,1)


def analyze(input_dir:Path,out_dir:Path):
    manifest,bands=verify_and_load(input_dir)
    if out_dir.exists() and any(out_dir.iterdir()):
        raise FileExistsError('output directory must be empty; do not overwrite provenance')
    out_dir.mkdir(parents=True,exist_ok=True)
    aligned=[]; transforms=[]
    for band in bands:
        oriented,ori=choose_orientation(band)
        fixed,shift=align_translation(oriented)
        aligned.append(fixed)
        transforms.append({'orientation':ori,'registration':shift})
    cube=np.stack(aligned,axis=-1)
    scores,frac,loadings=pca_cube(cube)
    rgb=np.stack([stretch(cube[:,:,i]) for i in range(3)],axis=-1)
    Image.fromarray(np.uint8(np.round(rgb*255)),'RGB').save(out_dir/'false_color.png')
    Image.fromarray(np.uint8(np.round(stretch(scores[:,:,0])*255)),'L').save(out_dir/'pc1.png')
    # Explicit synthetic-known ROI benchmark ONLY. Do not project it to real manuscript pixels.
    contrasts=[float(np.mean(b[TARGET])-np.mean(b[CONTROL])) for b in aligned]
    independent_support=sum(c < -0.045 for c in contrasts)
    report={'schema':SCHEMA,'mode':'SYNTHETIC_VALIDATION_NOT_PHILOLOGY',
            'source_manifest_sha256':sha256_file(input_dir/'manifest.json'),
            'source_band_sha256':[b['sha256'] for b in manifest['bands']],
            'seed':manifest['seed'],'scenario':manifest['scenario'],'bands':len(bands),
            'transforms':transforms,'pca_explained_fraction':[float(x) for x in frac],
            'pca_loadings':loadings.tolist(),
            'synthetic_target_minus_control':contrasts,
            'independent_band_support_at_fixture_threshold':independent_support,
            'holdout_last_band_contrast':contrasts[-1],
            'reading_k1':'NOT_RECONSTRUCTED','g0_gate':'PARTIAL',
            'notice':'ROI, threshold and truth only valid for invented synthetic geometry; no glyph detection',
            'python':sys.version.split()[0], 'numpy':np.__version__,
            'scipy':__import__('scipy').__version__, 'pillow':__import__('PIL').__version__,
            'time_utc':datetime.now(timezone.utc).isoformat()}
    (out_dir/'report.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    return report


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest='command',required=True)
    g=sub.add_parser('generate');g.add_argument('--out',type=Path,required=True)
    g.add_argument('--seed',type=int,default=20261018)
    g.add_argument('--scenario',choices=('signal','blank','artifact'),default='signal')
    a=sub.add_parser('analyze');a.add_argument('--input',type=Path,required=True)
    a.add_argument('--out',type=Path,required=True)
    args=ap.parse_args(argv)
    if args.command=='generate':
        x=generate(args.out,args.seed,args.scenario)
        print('SYNTHETIC GENERATED',len(x['bands']),'bands')
    else:
        x=analyze(args.input,args.out)
        print('SYNTHETIC ANALYSIS',json.dumps({'support':x['independent_band_support_at_fixture_threshold'],
                    'holdout':x['holdout_last_band_contrast'],'pca':x['pca_explained_fraction']}))

if __name__=='__main__':
    main()
