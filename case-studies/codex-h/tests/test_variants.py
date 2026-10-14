import sys
import unittest
import csv
import tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from validate_variants import validate_csv,lexical_key
P=Path(__file__).resolve().parents[1]/"CODH01_K6_VARIANTS.csv"
class VariantTests(unittest.TestCase):
    def test_records(self): self.assertEqual(len(validate_csv(P)),4)
    def test_equivalent_accents(self): self.assertEqual(lexical_key("ὀξύς"),lexical_key("ὀξύς"))
    def test_heresy_distinction(self): self.assertNotEqual(lexical_key("ἐριστικοὺς"),lexical_key("αἱρετικοὺς"))
    def test_harley_distinction(self): self.assertNotEqual(lexical_key("ἐριστικοὺς"),lexical_key("ἐριστηκοὺς"))
    def test_no_ga015_claim(self):
        self.assertEqual({r["ga015_diplomatic_verified"] for r in validate_csv(P)},{"false"})
    def reject_change(self, old, new):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"bad.csv"
            p.write_text(P.read_text(encoding="utf-8").replace(old,new,1),encoding="utf-8")
            with self.assertRaises(ValueError): validate_csv(p)
    def test_guard_fake_verification(self): self.reject_change(",false\n",",true\n")
    def test_guard_missing_folio(self): self.reject_change("Add. 28816,113,","Add. 28816,,")
if __name__=="__main__":unittest.main()
