import io
import unittest
import zipfile
from audit_combined_tei_global import inspect_xml, inspect_zip

TEST = b'''<teiCorpus xmlns="http://www.tei-c.org/ns/1.0">
  <TEI xml:id="a"><text><body><pb n="1v"/><num type="chapNum" n="1">alpha</num>
  <w>outside</w></body></text></TEI>
  <TEI xml:id="b"><text><body><div type="book" n="Titus">
    <pb n="86v"/><w>?</w><pb n="87r"/><num type="chapNum" n="2">beta</num>
    <ab n="B17K1V5"><w>none</w></ab></div></body></text></TEI>
</teiCorpus>'''

class GlobalTEITest(unittest.TestCase):
    def test_multi_body_is_global(self):
        data = inspect_xml('combined-xml.xml', TEST)
        self.assertEqual(data['body_count'], 2)
        self.assertEqual(data['pb_total'], 3)
        self.assertEqual(data['all_pb_n'], ['1v', '86v', '87r'])
        self.assertEqual(data['exact_86v_pb'], 1)
        self.assertEqual(data['chapnum_count'], 2)
        self.assertEqual(data['chapnum_n_one_count'], 1)
        self.assertEqual(data['chapnum_n_one_records'][0]['body_index'], 1)
        self.assertEqual(data['explicit_titus_divisions'][0]['body_index'], 2)
        self.assertEqual(data['bodies'][1]['chapter_numbers'], ['2'])

    def test_zip_and_modern_label_not_rubric(self):
        bio = io.BytesIO()
        with zipfile.ZipFile(bio, 'w') as z:
            z.writestr('combined-xml.xml', TEST)
        d = inspect_zip(bio.getvalue())['members'][0]
        self.assertEqual(d['chapnum_n_one_count'], 1)
        self.assertEqual(d['chapnum_candidates_near_focus'][0]['n'], '2')
        self.assertEqual(len(d['chapnum_candidates_near_focus']), 1)

if __name__ == '__main__':
    unittest.main()
