"""Protect source identity and separation of modern references / ancient numbers."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from audit_titus_sources import audit_sources, verse_label


class TestTitusSourceInventory(unittest.TestCase):
    def test_source_scope_does_not_create_missing_rubrics(self):
        report = audit_sources(ROOT)
        self.assertEqual(report["summary"]["indexed_transcriptions"], 10)
        self.assertEqual([m["encoded_number"] for m in report["markers"] if m["context"] == "list"],
                         ["2", "3", "4", "5", "6"])
        body = [m for m in report["markers"] if m["context"] == "body"]
        self.assertEqual([(m["value"], m["within_modern_verse"], m["next_modern_verse"]) for m in body],
                         [("γ", "Titus 2:1", "Titus 2:2")])
        self.assertEqual(report["summary"]["whole_rubric_spans_certified"], 0)

    def test_modern_xml_chapter_is_not_ancient_rubric(self):
        self.assertEqual(verse_label("B17K1V5"), "Titus 1:5")
        self.assertIsNone(verse_label("K1"))

    def test_corrupted_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            shutil.copytree(ROOT / "sources", target / "sources")
            xml = target / "sources/GA015_88r.xml"
            xml.write_bytes(xml.read_bytes() + b"\n")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                audit_sources(target)

    def test_missing_indexed_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            shutil.copytree(ROOT / "sources", target / "sources")
            (target / "sources/GA015_92v.xml").unlink()
            with self.assertRaises(OSError):
                audit_sources(target)
