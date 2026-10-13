"""Negative fixtures for COD-H-01 status checks; not tests of the Greek text."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_evidence import HEADERS, validate_csv, validate_rows

ROOT = Path(__file__).resolve().parents[1]


class TestLedger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import csv
        with (ROOT / "CODH01_EVIDENCE.csv").open(encoding="utf-8-sig", newline="") as h:
            cls.rows = list(csv.DictReader(h))

    def alter(self, index, field, value):
        r = deepcopy(self.rows)
        r[index][field] = value
        return r

    def test_current_ledger_passes(self):
        self.assertEqual(validate_csv(ROOT / "CODH01_EVIDENCE.csv")["ga015_verified"], 0)

    def test_six_slots_required(self):
        with self.assertRaises(ValueError):
            validate_rows(self.rows[:-1], HEADERS)

    def test_unique_ordered_ids_required(self):
        with self.assertRaises(ValueError):
            validate_rows(self.alter(1, "rubric_id", "K1"), HEADERS)

    def test_no_unreviewed_ga015_confirmation(self):
        with self.assertRaises(ValueError):
            validate_rows(self.alter(4, "ga015_greek_diplomatic_verified", "true"), HEADERS)

    def test_unknown_layer_rejected(self):
        with self.assertRaises(ValueError):
            validate_rows(self.alter(0, "source_layer", "GA015_diplomatic"), HEADERS)

    def test_unverified_cannot_smuggle_text(self):
        with self.assertRaises(ValueError):
            validate_rows(self.alter(1, "reported_text", "fabricated title"), HEADERS)

    def test_source_attribution_required(self):
        with self.assertRaises(ValueError):
            validate_rows(self.alter(0, "source_id", ""), HEADERS)

    def test_tradition_not_witness_alignment(self):
        with self.assertRaises(ValueError):
            validate_rows(self.alter(0, "reported_alignment", "Titus 1:1-9"), HEADERS)

    def test_column_change_requires_review(self):
        with self.assertRaises(ValueError):
            validate_rows(self.rows, HEADERS[:-1])


if __name__ == "__main__":
    unittest.main()
