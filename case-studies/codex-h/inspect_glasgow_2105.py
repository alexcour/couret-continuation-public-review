#!/usr/bin/env python3
"""Inspect the public Glasgow DOI 10.5525/gla.researchdata.2105 TEI ZIP.

This is a SOURCE DISCOVERY utility, not a palaeographic or historical
certification. It never fills a missing Codex H K1 from neighbouring pages,
a tradition-level rubric, or another witness.

Usage:
  python3 inspect_glasgow_2105.py --zip /path/to/2105_data.zip
  python3 inspect_glasgow_2105.py --download

The downloaded binary is not placed in the repository. Only a short JSON
manifest of machine observations is written to stdout (or --output).
"""
import argparse
import hashlib
import io
import json
from pathlib import PurePosixPath, Path
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

URL = "https://researchdata.gla.ac.uk/2105/1/2105_data.zip"
DOI = "10.5525/gla.researchdata.2105"
NS = "{http://www.tei-c.org/ns/1.0}"
MAX_ARCHIVE = 3 * 1024 * 1024
MAX_MEMBERS = 300
MAX_MEMBER = 8 * 1024 * 1024
MAX_TOTAL_UNCOMPRESSED = 40 * 1024 * 1024


def _safe_names(entries):
    if len(entries) > MAX_MEMBERS:
        raise ValueError("archive has more members than the review limit")
    if sum(e.file_size for e in entries) > MAX_TOTAL_UNCOMPRESSED:
        raise ValueError("archive exceeds uncompressed review limit")
    for e in entries:
        p = PurePosixPath(e.filename)
        if p.is_absolute() or ".." in p.parts or not e.filename or "\\" in e.filename:
            raise ValueError("unsafe ZIP member name")
        if e.file_size > MAX_MEMBER:
            raise ValueError("oversized ZIP member")


def inspect_bytes(archive):
    if len(archive) > MAX_ARCHIVE:
        raise ValueError("download larger than declared input review limit")
    result = {
        "dataset_doi": DOI,
        "archive_url": URL,
        "sha256": hashlib.sha256(archive).hexdigest(),
        "zip_bytes": len(archive),
        "xml_count": 0,
        "non_xml_members": [],
        "xml_records": [],
        "warning": (
            "Numeral 1 in an XML file is only a computational candidate; "
            "it is NOT an attested first Titus rubric of GA 015. "
            "A missing candidate does not establish historical absence."
        ),
    }
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        entries = z.infolist()
        _safe_names(entries)
        for e in entries:
            if e.is_dir():
                continue
            if not e.filename.lower().endswith(".xml"):
                result["non_xml_members"].append(e.filename)
                continue
            root = ET.fromstring(z.read(e))
            result["xml_count"] += 1
            nums = [n.get("n") for n in root.iter(NS + "num")
                    if n.get("type") == "chapNum"]
            folios = [p.get("n") for p in root.iter(NS + "pb") if p.get("n")]
            titus_divisions = [d.get("n") for d in root.iter(NS + "div")
                               if "titus" in (d.get("n") or "").casefold()]
            result["xml_records"].append({
                "member": e.filename,
                "folio_ids": folios[:12],
                "titus_divisions": titus_divisions[:8],
                "rubric_numbers": nums[:25],
                "has_num_one": "1" in nums,
                "contains_supplied": any(True for _ in root.iter(NS + "supplied")),
                "contains_unclear": any(True for _ in root.iter(NS + "unclear")),
                "observation_only": True,
            })
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--zip", type=Path, help="public ZIP downloaded without alteration")
    g.add_argument("--download", action="store_true", help="fetch public 55 kB collection")
    p.add_argument("--output", type=Path, help="write JSON summary (not source files)")
    args = p.parse_args()
    if args.download:
        request = urllib.request.Request(
            URL,
            headers={"User-Agent": "CODH01-documentary-audit/0.1 (+research; no bulk crawler)"},
        )
        with urllib.request.urlopen(request, timeout=45) as response:
            archive = response.read(MAX_ARCHIVE + 1)
    else:
        archive = args.zip.read_bytes()
    result = inspect_bytes(archive)
    serial = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(serial, encoding="utf-8")
    print(serial)


if __name__ == "__main__":
    main()
