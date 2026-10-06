#!/usr/bin/env python3
"""Replay the unchanged model in a user-chosen new directory; compare numeric results."""
from pathlib import Path
import argparse, tempfile, json, math, hashlib
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    dest=a.output.resolve()
    if dest.exists():raise SystemExit('Choose a new output directory; frozen results are never overwritten.')
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.mkdir()
    script=ROOT/'prime/v0_11/MODEL_SCRIPT.py'
    source=script.read_text()
    expected=json.loads((ROOT/'prime/v0_11/canonical_180_210_prediction.json').read_text())
    with tempfile.TemporaryDirectory(prefix='cont-model-') as temp:
        # All original /mnt/data output paths are mapped into one fresh temporary root.
        count=source.count('/mnt/data');assert count==3,count
        redirected=source.replace('/mnt/data',temp)
        exec(compile(redirected,str(script),'exec'),{'__name__':'__main__'})
        model=Path(temp)/'CONT_PRIME_MEMORY_v0_11'
        actual=json.loads((model/'canonical_180_210_prediction.json').read_text())
        for key,value in expected.items():
            if isinstance(value,(int,float)):
                assert math.isclose(actual[key],value,rel_tol=1e-10,abs_tol=1e-12),(key,actual[key],value)
            else:assert actual[key]==value,key
        import shutil
        for f in model.iterdir():shutil.copy2(f,dest/f.name)
    result={'status':'PASS','model_version':'0.11','source_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'comparison':'all canonical numeric fields; relative tolerance 1e-10','new_empirical_prime_collection':False}
    (dest/'REPLAY_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__':main()
