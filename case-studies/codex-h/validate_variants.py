#!/usr/bin/env python3
"""Mechanical checks on source-attributed catalogue variants, not philological certification."""
import argparse
import csv
import unicodedata
from pathlib import Path

COLUMNS = ["record_id","rubric_id","source_layer","witness","folio","reading","source_url","ga015_diplomatic_verified"]
LAYERS = {"Pinakes_work_notice","Pinakes_witness_description"}

def lexical_key(s):
    return "".join(c for c in unicodedata.normalize("NFD",s).casefold() if unicodedata.category(c)!="Mn").replace("ς","σ")

def validate_csv(path):
    with Path(path).open(encoding="utf-8-sig",newline="") as stream:
        reader=csv.DictReader(stream)
        if reader.fieldnames != COLUMNS: raise ValueError("unexpected schema")
        rows=list(reader)
    if len(rows)!=4 or len({r["record_id"] for r in rows})!=4: raise ValueError("expected four unique source records")
    for r in rows:
        if None in r or any(r[k] is None for k in COLUMNS): raise ValueError("malformed columns")
        if r["rubric_id"]!="K6" or r["source_layer"] not in LAYERS: raise ValueError("unexpected rubric/source layer")
        if r["ga015_diplomatic_verified"]!="false": raise ValueError("none is verified from GA015")
        if not r["record_id"] or not r["witness"] or not r["reading"] or not r["source_url"].startswith("https://"): raise ValueError("missing provenance")
        if r["source_layer"]=="Pinakes_witness_description" and not r["folio"]: raise ValueError("witness folio missing")
    return rows

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--csv",type=Path,default=Path(__file__).with_name("CODH01_K6_VARIANTS.csv"))
    args=p.parse_args()
    try: rows=validate_csv(args.csv)
    except (ValueError,OSError) as e: p.exit(1,f"FAIL: {e}\n")
    baseline=lexical_key(rows[0]["reading"])
    changed=sum(lexical_key(r["reading"])!=baseline for r in rows[1:])
    print(f"PASS: 4 catalogue-level K6 records; {changed} non-identical lexical strings; 0 diplomatic GA015 readings.")
if __name__=="__main__":main()
