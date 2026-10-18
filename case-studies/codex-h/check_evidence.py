#!/usr/bin/env python3
"""Check COD-H-01 evidence-ledger provenance, *not* Greek readings or history.

G0 is still open. In this review packet, no rubric may be labelled as a
verified diplomatic transcription of GA 015. Raising this gate requires a
separately documented and independently checked source review.
"""

import argparse
import csv
from pathlib import Path

HEADERS = [
    "rubric_id",
    "source_layer",
    "source_id",
    "reported_text",
    "reported_alignment",
    "ga015_greek_diplomatic_verified",
    "notes",
]
SOURCE_LAYERS = {"unverified", "tradition_Pinakes", "secondary_report", "GA015_digital_edition"}


def validate_rows(rows, headers):
    """Return summary after strict structural checks; raise ValueError on failure."""
    if headers != HEADERS:
        raise ValueError(f"Unexpected CSV schema: {headers!r}")
    if len(rows) != 6:
        raise ValueError(f"Expected 6 rubric slots, received {len(rows)}")
    expected = [f"K{i}" for i in range(1, 7)]
    actual = [r.get("rubric_id") for r in rows]
    if actual != expected:
        raise ValueError(f"Rubrics must be unique and ordered: {actual!r}")

    attributed = 0
    digital = 0
    for row in rows:
        rubric = row["rubric_id"]
        if None in row or any(row.get(k) is None for k in HEADERS):
            raise ValueError(f"{rubric}: extra/missing CSV fields")
        layer = row["source_layer"].strip()
        source_id = row["source_id"].strip()
        reported_text = row["reported_text"].strip()
        reported_alignment = row["reported_alignment"].strip()
        verified = row["ga015_greek_diplomatic_verified"].strip()
        if layer not in SOURCE_LAYERS:
            raise ValueError(f"{rubric}: unknown source layer {layer!r}")
        if verified != "false":
            raise ValueError(
                f"{rubric}: GA015 diplomatic status must remain false until "
                "independent image-and-transcription review is documented"
            )
        if layer == "unverified":
            if source_id or reported_text or reported_alignment:
                raise ValueError(f"{rubric}: unknown source cannot assert text or alignment")
        else:
            attributed += 1
            if not source_id or not reported_text:
                raise ValueError(f"{rubric}: source attribution and text are both required")
            if layer == "tradition_Pinakes" and reported_alignment:
                raise ValueError(f"{rubric}: tradition-level title cannot assert GA015 alignment")
            if layer == "GA015_digital_edition":
                digital += 1
                if source_id != "GLASGOW_GA015_87r_20261013":
                    raise ValueError(f"{rubric}: digital edition needs its documented source receipt")
                if rubric == "K1":
                    raise ValueError("K1 is absent from the acquired 87r transcription")
                if reported_alignment:
                    raise ValueError(f"{rubric}: acquired title alone cannot assert a complete verse span")
        if rubric == "K5" and layer == "secondary_report" and not reported_alignment:
            raise ValueError("K5: the recorded secondary report requires its cited alignment")

    return {"slots": 6, "attributed_non_diplomatic": attributed,
            "digital_edition_entries": digital, "ga015_verified": 0}


def validate_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, restkey="__extra__")
        rows = list(reader)
        return validate_rows(rows, reader.fieldnames)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", type=Path, default=Path(__file__).with_name("CODH01_EVIDENCE.csv"))
    args = ap.parse_args()
    try:
        summary = validate_csv(args.csv)
    except (ValueError, OSError) as exc:
        ap.exit(1, f"FAIL: {exc}\n")
    print(
        "PASS (structural only): {slots} slots; {attributed_non_diplomatic} "
        "attributed non-diplomatic entries; {ga015_verified} GA015 readings verified. "
        "{digital_edition_entries} GA015 edition entries acquired. "
        "No historical claim certified.".format(**summary)
    )


if __name__ == "__main__":
    main()
