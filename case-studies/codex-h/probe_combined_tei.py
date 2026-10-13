#!/usr/bin/env python3
"""Exhaustive, provenance-aware structural scan of Glasgow GA015 combined TEI.

This is machine observation, NEVER certification of a diplomatic Greek reading.
The main text's ancient chapter marker must have type=chapNum, not modern
verse labels. A numeral one elsewhere in the codex does not establish Titus K1.
"""
import argparse
import bisect
import hashlib
import io
import json
import re
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from inspect_glasgow_2105 import URL, DOI, MAX_ARCHIVE, _safe_names

FOCUS_PAGES = {"85r", "85v", "86r", "86v", "87r", "87v", "88r", "88v"}
TERMS = ("διδασκ", "ἐπιτηδ", "διακον", "ἀπειθ", "κατατ", "κεφαλαι")

def local(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""

def norm(text):
    return "".join(c for c in unicodedata.normalize("NFD", text).casefold()
                   if unicodedata.category(c) != "Mn")

def short(text, length=160):
    return re.sub(r"\s+", " ", text or "").strip()[:length]

def _ctx_ancestors(element, parent):
    seen = []
    e = element
    for _ in range(25):
        e = parent.get(e)
        if e is None:
            break
        if local(e.tag) == "div":
            seen.append({"type":e.get("type"),"n":e.get("n"),"subtype":e.get("subtype")})
    return seen[:6]

def inspect_xml(name, raw):
    root = ET.fromstring(raw)
    # Restrict to TEI text: a manuscript number in a header/catalogue is NOT a body rubric.
    body = next((x for x in root.iter() if local(x.tag) == "body"), None)
    if body is None:
        return {"member":name, "root":local(root.tag), "body_present":False}
    nodes = list(body.iter())
    parent = {child:elem for elem in nodes for child in elem}
    pages = [(i, e.get("n")) for i,e in enumerate(nodes)
             if local(e.tag) == "pb" and e.get("n")]
    page_indices = [i for i,_ in pages]
    def page_at(i):
        j = bisect.bisect_right(page_indices, i) - 1
        return pages[j][1] if j >= 0 else None
    word_by_page = {}
    rubric_by_page = {}
    one_markers = []
    match_tokens = []
    titus_divisions = []
    for i,e in enumerate(nodes):
        tag=local(e.tag)
        page = page_at(i)
        if tag == "w" and page:
            word_by_page.setdefault(page,[]).append(short("".join(e.itertext()),80))
            t = norm("".join(e.itertext()))
            if any(norm(term) in t for term in TERMS):
                match_tokens.append({"page":page,"token":short("".join(e.itertext()),80),
                                     "book_context":_ctx_ancestors(e,parent)})
        elif tag == "num" and e.get("type") == "chapNum":
            n=e.get("n")
            record={"page":page,"n":n,
                    "inscription":short("".join(e.itertext()),50),
                    "book_context":_ctx_ancestors(e,parent)}
            rubric_by_page.setdefault(page,[]).append(record)
            if n == "1":
                one_markers.append(record)
        elif tag == "div" and ("titus" in (e.get("n") or "").casefold()
                               or "titus" in (e.get("type") or "").casefold()):
            titus_divisions.append({"page":page,
                                    "type":e.get("type"),
                                    "n":e.get("n")})
    selected_pages={}
    for pg in FOCUS_PAGES:
        if pg in word_by_page or pg in rubric_by_page or any(x[1]==pg for x in pages):
            selected_pages[pg]={"words":len(word_by_page.get(pg,[])),
                                "first_words":word_by_page.get(pg,[])[:18],
                                "last_words":word_by_page.get(pg,[])[-10:],
                                "chapter_markers":rubric_by_page.get(pg,[])}
    return {
      "member":name, "xml_bytes":len(raw), "root":local(root.tag),
      "body_present":True,
      "page_count":len(pages),
      "first_pages":[p[1] for p in pages[:12]],
      "last_pages":[p[1] for p in pages[-12:]],
      "exact_86v_present":any(p=="86v" for _,p in pages),
      "exact_87r_present":any(p=="87r" for _,p in pages),
      "titus_divisions_count":len(titus_divisions),
      "titus_divisions":titus_divisions[:30],
      "total_chapNum":sum(len(v) for v in rubric_by_page.values()),
      "chapNum_one_count":len(one_markers),
      "chapNum_one_examples":one_markers[:25],
      "titus_focus_pages":{k:selected_pages[k] for k in sorted(selected_pages)},
      "lexical_matches_total":len(match_tokens),
      "lexical_matches_focus":[x for x in match_tokens if x["page"] in FOCUS_PAGES][:30],
      "lexical_matches_other_examples":[x for x in match_tokens if x["page"] not in FOCUS_PAGES][:15],
      "warning":"Do not identify Titus K1 from numbering or lexical parallels without folio and material provenance."
    }

def inspect_archive(raw):
    if len(raw) > MAX_ARCHIVE:
        raise ValueError("ZIP exceeds maximum size")
    data={"dataset_doi":DOI, "source_url":URL,
          "zip_sha256":hashlib.sha256(raw).hexdigest(),"members":[]}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        entries=z.infolist()
        _safe_names(entries)
        for entry in entries:
            if entry.is_dir():
                continue
            if entry.filename.lower().endswith(".xml"):
                data["members"].append(inspect_xml(entry.filename,z.read(entry)))
    return data

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--zip",type=Path)
    group.add_argument("--download",action="store_true")
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    if args.download:
        request=urllib.request.Request(URL,headers={"User-Agent":"CODH01/0.2-source-provenance"})
        with urllib.request.urlopen(request,timeout=45) as response:
            raw=response.read(MAX_ARCHIVE+1)
    else:
        raw=args.zip.read_bytes()
    data=inspect_archive(raw)
    result=json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.write_text(result,encoding="utf-8")
    print(result)

if __name__=="__main__":
    main()
