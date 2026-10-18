"""Fictitious byte fixtures only. No manuscripts, permissions or TIFFs supplied."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from msi_intake.gate import evaluate, verify_local, ManifestError, parse_manifest, main


class TestIntake(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.pending = json.loads((Path(__file__).parents[1] / 'pending_request.example.json').read_text())
        self.assertEqual(self.pending['authorization']['status'], 'pending')

    def granted_fixture(self):
        """These fields are fictional and must not imply actual consent."""
        root = self.root / 'private-mock'
        root.mkdir(exist_ok=True)
        b = b'SYNTHETIC_NOT_A_REAL_IMAGE\n'
        (root / 'fictional.dat').write_bytes(b)
        m = copy.deepcopy(self.pending)
        m['dataset']['supplier_crosswalk'] = 'documented'
        a = m['authorization']
        a.update(status='granted', grantor='FICTIONAL TEST PROVIDER',
                 evidence_reference='TEST_ONLY_NO_REAL_RIGHTS', allowed_operations=['inspect'])
        for key in ('rights_review', 'crosswalk_review'):
            a[key].update(status='documented', reviewer='FICTIONAL_TEST_REVIEWER',
                          record_reference='TEST_ONLY_NO_REAL_REVIEW')
        m['assets'] = [{
            'supplier_file_id': 'FICTIONAL_ASSET_1', 'relative_path': 'fictional.dat',
            'role': 'raw_band', 'folio': '86v', 'surface': 'Coislin 202, 11rT',
            'band_id': 'TEST_BAND', 'wavelength_nm': 'non fourni',
            'width': 4, 'height': 4, 'bit_depth': 16,
            'orientation': 'raw-as-captured', 'mirror': 'no',
            'capture_date': '2023-04-01', 'flat_frame_id': 'non fourni',
            'dark_frame_id': 'non fourni',
            'supplier_sha256': hashlib.sha256(b).hexdigest(),
            'supplier_bytes': len(b), 'license': 'FICTITIOUS_TEST_ONLY',
            'credit': 'FICTITIOUS_TEST_ONLY'}]
        return m, root

    def test_pending_fail_closed(self):
        status = evaluate(self.pending)
        self.assertEqual(status['gate'], 'HOLD')
        self.assertFalse(status['can_read_local_files'])
        self.assertGreater(len(status['blockers']), 3)

    def test_not_a_tei_dataset(self):
        d = copy.deepcopy(self.pending)
        d['dataset']['doi'] = '10.5525/gla.researchdata.2105'
        with self.assertRaisesRegex(ManifestError, 'not TEI'):
            evaluate(d)

    def test_no_phantom_authorizations(self):
        d = copy.deepcopy(self.pending)
        d['authorization']['status'] = 'granted'
        self.assertEqual(evaluate(d)['gate'], 'HOLD')

    def test_empty_supplier_manifest_still_blocked(self):
        d = copy.deepcopy(self.pending)
        d['dataset']['supplier_crosswalk'] = 'documented'
        self.assertIn('FILES: no supplier asset inventory received', evaluate(d)['blockers'])

    def test_metadata_ready_is_not_juridical_authorization(self):
        d, _ = self.granted_fixture()
        status = evaluate(d)
        self.assertEqual(status['gate'], 'MANUAL_EVIDENCE_REVIEW_REQUIRED')
        self.assertFalse(status['authorization_authenticity_machine_verified'])
        self.assertEqual(status['k1_reconstruction'], 'NONE')

    def test_no_vendor_hash_still_creates_private_receipt(self):
        d, root = self.granted_fixture()
        d['assets'][0]['supplier_sha256'] = 'non fourni'
        d['assets'][0]['supplier_bytes'] = 'non fourni'
        self.assertEqual(evaluate(d)['gate'], 'MANUAL_EVIDENCE_REVIEW_REQUIRED')
        report = verify_local(d, root)
        self.assertEqual(report['gate'], 'HOLD_REFERENCE_UNAVAILABLE')
        self.assertEqual(len(report['local_integrity'][0]['observed_sha256']), 64)
        self.assertIsNone(report['local_integrity'][0]['sha256_matches_supplier'])

    def test_neighbor_control_pair_permitted(self):
        d, _ = self.granted_fixture()
        d['assets'][0].update(role='control', folio='87r', surface='Coislin 202, 11r')
        self.assertEqual(evaluate(d)['gate'], 'MANUAL_EVIDENCE_REVIEW_REQUIRED')

    def test_observed_report_is_private_mode(self):
        d, root = self.granted_fixture()
        manifest = self.root / 'mock.json'
        manifest.write_text(json.dumps(d))
        dst = self.root / 'private_report.json'
        self.assertEqual(main(['verify-local', '--manifest', str(manifest),
                               '--source-root', str(root), '--output', str(dst)]), 0)
        self.assertEqual(dst.stat().st_mode & 0o777, 0o600)

    def test_authorization_scope_required(self):
        d, _ = self.granted_fixture()
        d['authorization']['allowed_operations'] = ['publish']
        self.assertEqual(evaluate(d)['gate'], 'HOLD')

    def test_crosswalk_separate_review_required(self):
        d, _ = self.granted_fixture()
        d['authorization']['crosswalk_review']['status'] = 'pending'
        self.assertEqual(evaluate(d)['gate'], 'HOLD')

    def test_reject_traversal(self):
        d, _ = self.granted_fixture()
        d['assets'][0]['relative_path'] = '../secrets'
        with self.assertRaisesRegex(ManifestError, 'unsafe'):
            parse_manifest(d)

    def test_reject_absolute_path(self):
        d, _ = self.granted_fixture()
        d['assets'][0]['relative_path'] = '/tmp/private-image.tif'
        with self.assertRaisesRegex(ManifestError, 'unsafe'):
            parse_manifest(d)

    def test_reject_duplicate_asset_id(self):
        d, _ = self.granted_fixture()
        d['assets'].append(copy.deepcopy(d['assets'][0]))
        with self.assertRaisesRegex(ManifestError, 'duplicate'):
            parse_manifest(d)

    def test_reject_invalid_hash_encoding(self):
        d, _ = self.granted_fixture()
        d['assets'][0]['supplier_sha256'] = 'deadbeef'
        with self.assertRaisesRegex(ManifestError, 'sha256'):
            parse_manifest(d)

    def test_unknown_supplier_size_warns(self):
        d, _ = self.granted_fixture()
        d['assets'][0]['supplier_bytes'] = 'non fourni'
        self.assertEqual(evaluate(d)['gate'], 'MANUAL_EVIDENCE_REVIEW_REQUIRED')
        self.assertIn('REFERENCE:', ' '.join(evaluate(d)['warnings']))

    def test_calibration_absence_is_warning(self):
        d, _ = self.granted_fixture()
        report = evaluate(d)
        self.assertIn('CALIBRATION:', ' '.join(report['warnings']))
        self.assertIn('SPECTRAL:', ' '.join(report['warnings']))

    def test_local_hash_pass_but_no_philological_authority(self):
        d, root = self.granted_fixture()
        r = verify_local(d, root)
        self.assertEqual(r['gate'], 'HUMAN_REVIEW_REQUIRED')
        self.assertEqual(r['local_integrity'][0]['integrity_status'], 'PASS')
        self.assertFalse(r['can_read_local_files'])
        self.assertFalse(r['real_msi_processed'])

    def test_local_hash_tampering_detected(self):
        d, root = self.granted_fixture()
        (root / 'fictional.dat').write_bytes(b'SYNTHETIC_NOT_A_REAL_IMAGE?')
        r = verify_local(d, root)
        self.assertEqual(r['gate'], 'HOLD_INTEGRITY')

    def test_equal_size_tampering_detected(self):
        d, root = self.granted_fixture()
        b = (root / 'fictional.dat').read_bytes()
        (root / 'fictional.dat').write_bytes(b[:-1] + b'?')
        self.assertEqual(verify_local(d, root)['gate'], 'HOLD_INTEGRITY')

    def test_blocked_case_reads_no_bytes(self):
        d, root = self.granted_fixture()
        d['authorization']['status'] = 'pending'
        (root / 'fictional.dat').unlink()
        with self.assertRaisesRegex(PermissionError, 'no file bytes opened'):
            verify_local(d, root)

    def test_symlink_escape_rejected(self):
        d, root = self.granted_fixture()
        (root / 'fictional.dat').unlink()
        outside = self.root / 'secret.fake'
        outside.write_bytes(b'SYNTHETIC')
        (root / 'fictional.dat').symlink_to(outside)
        with self.assertRaises((ValueError, FileNotFoundError)):
            verify_local(d, root)

    def test_missing_file_rejected(self):
        d, root = self.granted_fixture()
        (root / 'fictional.dat').unlink()
        with self.assertRaises(FileNotFoundError):
            verify_local(d, root)

    def test_cli_pending_reports_code_2(self):
        p = self.root / 'pending.json'
        p.write_text(json.dumps(self.pending), encoding='utf-8')
        rc = main(['evaluate', '--manifest', str(p), '--output', str(self.root / 'report.json')])
        self.assertEqual(rc, 2)
        self.assertEqual(json.loads((self.root / 'report.json').read_text())['gate'], 'HOLD')

    def test_cli_no_overwrite(self):
        p = self.root / 'pending.json'
        p.write_text(json.dumps(self.pending), encoding='utf-8')
        dst = self.root / 'exists.json'
        dst.write_text('KEEP THIS')
        with self.assertRaises(FileExistsError):
            main(['evaluate', '--manifest', str(p), '--output', str(dst)])
        self.assertEqual(dst.read_text(), 'KEEP THIS')


if __name__ == '__main__':
    unittest.main()