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
        rows = self.alter(1, "source_layer", "unverified")
        with self.assertRaises(ValueError):
            validate_rows(rows, HEADERS)

    def test_source_attribution_required(self):
        with self.assertRaises(ValueError):
            validate_rows(self.alter(0, "source_id", ""), HEADERS)

    def test_tradition_not_witness_alignment(self):
        with self.assertRaises(ValueError):
            validate_rows(self.alter(0, "reported_alignment", "Titus 1:1-9"), HEADERS)

    def test_column_change_requires_review(self):
        with self.assertRaises(ValueError):
            validate_rows(self.rows, HEADERS[:-1])

    def test_digital_source_receipt_required(self):
        with self.assertRaises(ValueError):
            validate_rows(self.alter(1, "source_id", "IRHT_CPG3642"), HEADERS)

    def test_digital_title_is_not_complete_span(self):
        with self.assertRaises(ValueError):
            validate_rows(self.alter(1, "reported_alignment", "Titus 1:10-16"), HEADERS)

    def test_k1_cannot_be_taken_from_87r(self):
        rows = deepcopy(self.rows)
        rows[0].update(source_layer="GA015_digital_edition",
                       source_id="GLASGOW_GA015_87r_20261013")
        with self.assertRaises(ValueError):
            validate_rows(rows, HEADERS)

    def test_acquired_xml_has_five_rubrics_and_supplied_letters(self):
        import xml.etree.ElementTree as ET
        ns = {"t": "http://www.tei-c.org/ns/1.0"}
        root = ET.parse(ROOT / "sources" / "GA015_87r.xml").getroot()
        self.assertEqual([e.get("n") for e in root.findall(".//t:num[@type='chapNum']", ns)],
                         ["2", "3", "4", "5", "6"])
        supplied = root.findall(".//t:supplied", ns)
        self.assertEqual([(e.text, e.get("source")) for e in supplied],
                         [("ς", "Omont"), ("ς", "Omont")])


if __name__ == "__main__":
    unittest.main()
