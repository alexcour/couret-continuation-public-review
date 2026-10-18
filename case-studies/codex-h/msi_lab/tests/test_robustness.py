"""Adversarial controls. The fixtures never contain any ancient or modern letters."""
import unittest
import numpy as np
from msi_lab.robustness import (SCENARIOS, fixtures, dark_flat_correct,
                                contrast_report, first_pc_cosine,
                                pca_perturbation_report, registration_stress,
                                synthetic_report)

class TestRobustness(unittest.TestCase):
    def test_repeated_synthetic_seed(self):
        for name in SCENARIOS:
            x, _ = fixtures(name)
            y, _ = fixtures(name)
            self.assertTrue(np.array_equal(x, y))

    def test_blank_no_support(self):
        self.assertEqual(contrast_report(fixtures('blank')[0])['band_support'], 0)

    def test_multiband_false_positive_stain(self):
        r = contrast_report(fixtures('shared_stain')[0])
        self.assertEqual(r['band_support'], 4)
        self.assertEqual(r['k1_reading'], 'NOT_RECONSTRUCTED')

    def test_multiband_false_positive_correlated_stripe(self):
        self.assertEqual(contrast_report(fixtures('correlated_stripe')[0])['band_support'], 4)

    def test_multiband_illumination_shadow(self):
        self.assertEqual(contrast_report(fixtures('illumination')[0])['band_support'], 4)

    def test_radiometric_correction_recovery(self):
        cube, _ = fixtures('signal')
        dark = np.full_like(cube, 0.02)
        yy, xx = np.indices(cube.shape[:2])
        flat = np.broadcast_to(0.82 + 0.02 * np.sin(xx / 15)[:, :, None], cube.shape).copy()
        raw = dark + (flat - dark) * cube
        corrected, metrics = dark_flat_correct(raw, dark, flat)
        self.assertLess(np.max(abs(corrected - cube)), 1e-12)
        self.assertEqual(metrics['masked_fraction'], 0)

    def test_refuse_missing_flat(self):
        x, _ = fixtures('signal')
        with self.assertRaisesRegex(ValueError, 'required'):
            dark_flat_correct(x, np.zeros_like(x), None)

    def test_refuse_bad_flat_span(self):
        x, _ = fixtures('signal')
        with self.assertRaisesRegex(ValueError, 'span'):
            dark_flat_correct(x, np.zeros_like(x), np.zeros_like(x))

    def test_refuse_saturation(self):
        x, _ = fixtures('blank')
        x[:30] = 1
        with self.assertRaisesRegex(ValueError, 'saturated'):
            dark_flat_correct(x, np.zeros_like(x), np.ones_like(x))

    def test_small_saturation_stays_missing(self):
        x, _ = fixtures('blank')
        x[0, 0, 0] = 1
        corrected, metrics = dark_flat_correct(x, np.zeros_like(x), np.ones_like(x))
        self.assertTrue(np.isnan(corrected[0, 0, 0]))
        self.assertGreater(metrics['masked_fraction'], 0)

    def test_pca_stress_reproducible_and_holdout(self):
        cube, _ = fixtures('signal')
        a = pca_perturbation_report(cube, repetitions=12)
        b = pca_perturbation_report(cube, repetitions=12)
        self.assertEqual(a, b)
        self.assertEqual(a['held_out_channel'], 3)
        self.assertGreater(a['pc1_abs_cosine_min'], 0.9)

    def test_pca_sign_independent(self):
        cube, _ = fixtures('signal')
        self.assertAlmostEqual(first_pc_cosine(cube[:, :, :3], -cube[:, :, :3]), 1)

    def test_pca_degenerate_rejected(self):
        with self.assertRaisesRegex(ValueError, 'degenerate'):
            first_pc_cosine(np.ones((96,96,3)),np.ones((96,96,3)))

    def test_integer_recalage(self):
        x, _ = fixtures('signal')
        r = registration_stress(x[:, :, 0], (2, -1))
        self.assertTrue(r['integer_model_adequate'])

    def test_subpixel_recalage_rejected(self):
        x, _ = fixtures('signal')
        r = registration_stress(x[:, :, 0], (0.5, -0.5))
        self.assertFalse(r['integer_model_adequate'])

    def test_model_over_range_rejected(self):
        x, _ = fixtures('signal')
        r = registration_stress(x[:, :, 0], (7, 0))
        self.assertFalse(r['integer_model_adequate'])

    def test_all_reports_keep_k1_unverified(self):
        report = synthetic_report()
        self.assertFalse(report['real_MSI_processed'])
        self.assertFalse(report['k1_certified'])
        self.assertEqual(set(report['scenarios']), set(SCENARIOS))
        self.assertTrue(all(x['k1_reading']=='NOT_RECONSTRUCTED' for x in report['scenarios'].values()))

if __name__ == '__main__': unittest.main()
