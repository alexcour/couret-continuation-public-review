#!/usr/bin/env python3
"""Zero-dependency status checker. It does not validate the historical claims."""
import csv
from pathlib import Path

path = Path(__file__).with_name("CODH01_EVIDENCE.csv")
with path.open(encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == 6, f"Expected six *reported* rubrics, got {len(rows)}"
assert [r["rubric_id"] for r in rows] == [f"K{i}" for i in range(1, 7)]
assert all(r["ga015_greek_diplomatic_verified"] in {"true", "false"} for r in rows)
assert all(
    (r["source_layer"] not in {"", "unverified"} and r["source_id"])
    or (not r["reported_text"] and not r["reported_alignment"])
    for r in rows
)
assert all(r["ga015_greek_diplomatic_verified"] == "false" for r in rows), (
    "A verified GA015 transcription requires a separately audited source gate."
)
assert all(r["source_layer"] != "GA015_diplomatic" for r in rows)
print("PASS: six slots; source-layer checks; zero GA015 titles verified. Not historical validation.")
