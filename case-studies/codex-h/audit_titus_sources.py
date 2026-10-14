#!/usr/bin/env python3
"""Inventory acquired TEI files; never certify palaeography or missing text."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

NS = {"t": "http://www.tei-c.org/ns/1.0"}


def verse_label(value):
    """Modern verse references only; B17K1 is NOT ancient rubric K1."""
    match = re.fullmatch(r"Titus\.(\d+)\.(\d+)", value or "")
    match = match or re.fullmatch(r"B17K(\d+)V(\d+)", value or "")
    return f"Titus {match[1]}:{match[2]}" if match else None


def audit_sources(root):
    root = Path(root)
    metadata = json.loads((root / "sources/GA015_TITUS_METADATA_EXCERPT.json").read_text())
    receipts = json.loads((root / "sources/SOURCE_RECEIPTS.json").read_text())
    by_path = {r["path"]: r for r in receipts["files"]}
    entries = [r for r in metadata["entries"]
               if r["biblicalContent"].startswith("Titus") and r["hasTranscription"]]
    folios = [r["folio"] for r in entries]
    if len(set(folios)) != len(folios):
        raise ValueError("duplicate metadata folio")
    pages, references, markers = [], set(), []
    for entry in entries:
        folio = entry["folio"]
        path = f"sources/GA015_{folio}.xml"
        data = (root / path).read_bytes()
        receipt = by_path.get(path)
        if not receipt or hashlib.sha256(data).hexdigest() != receipt["sha256"]:
            raise ValueError(f"{folio}: source hash mismatch or absent receipt")
        doc = ET.fromstring(data)
        if doc.tag != f"{{{NS['t']}}}TEI":
            raise ValueError(f"{folio}: not a TEI source")
        body = doc.find("t:text/t:body", NS)
        if body is None or not any(e.get("n") == folio
                                   for e in body.findall(".//t:pb", NS)):
            raise ValueError(f"{folio}: missing or mismatched TEI foliation")
        nodes = list(body.iter())
        parent = {child: node for node in nodes for child in node}
        ab = body.findall(".//t:ab", NS)
        refs = sorted({verse_label(e.get("n")) for e in ab} - {None})
        references.update(refs)
        page_markers = []
        for num in body.findall(".//t:num[@type='chapNum']", NS):
            ancestor = parent.get(num)
            while ancestor is not None and ancestor.tag != f"{{{NS['t']}}}ab":
                ancestor = parent.get(ancestor)
            item = {"folio": folio, "value": "".join(num.itertext()),
                    "encoded_number": num.get("n"),
                    "context": "list" if folio == "87r" else "body",
                    "within_ab_raw": ancestor.get("n") if ancestor is not None else None,
                    "within_modern_verse": verse_label(ancestor.get("n")) if ancestor is not None else None,
                    "whole_span_certified": False}
            if ancestor is not None:
                position = ab.index(ancestor)
                item["next_ab_raw"] = ab[position + 1].get("n") if position + 1 < len(ab) else None
                item["next_modern_verse"] = verse_label(item["next_ab_raw"])
                prior_words = [e for e in nodes[:nodes.index(num)]
                               if e.tag == f"{{{NS['t']}}}w"]
                item["preceding_word_nodes"] = ["".join(e.itertext()) for e in prior_words[-4:]]
            markers.append(item)
            page_markers.append(item)
        supplied = Counter(e.get("source", "unspecified")
                           for e in body.findall(".//t:supplied", NS))
        pages.append({"folio": folio, "library_folio": entry["libraryFolio"],
                      "biblical_content_metadata": entry["biblicalContent"],
                      "reference_labels": refs, "chapnum_count": len(page_markers),
                      "unclear_nodes": len(body.findall(".//t:unclear", NS)),
                      "supplied_nodes_by_source": dict(sorted(supplied.items())),
                      "expansion_nodes": len(body.findall(".//t:ex", NS)),
                      "source_path": path, "sha256": receipt["sha256"]})
    return {"snapshot_date": "2026-10-13",
            "scope": "All Titus-labelled transcriptions in the acquired index; not the complete historical letter.",
            "reference_warning": "Modern reference labels may cover only part of a verse and contain editorial restorations.",
            "pages": pages, "markers": markers,
            "summary": {"indexed_transcriptions": len(pages),
                        "list_markers": sum(m["context"] == "list" for m in markers),
                        "body_markers": sum(m["context"] == "body" for m in markers),
                        "distinct_modern_reference_labels": len(references),
                        "whole_rubric_spans_certified": 0,
                        "independent_philological_validation_completed": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).parent)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = audit_sources(args.root)
    except (ValueError, OSError, ET.ParseError) as exc:
        parser.exit(1, f"FAIL: {exc}\n")
    if args.output:
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS (source inventory only): " + json.dumps(result["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
