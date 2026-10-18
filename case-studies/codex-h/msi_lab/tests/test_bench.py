import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from msi_lab.bench import analyze, generate, pca_cube, verify_and_load, choose_orientation

class TestSynthetic(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
    def scenario(self,name):
        x=self.root/name; y=self.root/(name+'-out')
        generate(x,scenario=name)
        return x,y,analyze(x,y)
    def test_signal_and_mirror(self):
        x,y,r=self.scenario('signal')
        self.assertEqual(r['band_support_at_fixture_threshold'],4)
        self.assertTrue(r['transforms'][2]['orientation']['mirror_after_rotation'])
        self.assertLess(r['holdout_last_band_contrast'],-0.08)
        self.assertAlmostEqual(sum(r['pca_explained_fraction']),1,places=7)
        self.assertTrue((y/'false_color.png').exists())
    def test_blank(self):
        self.assertEqual(self.scenario('blank')[2]['band_support_at_fixture_threshold'],0)
    def test_single_band_artifact(self):
        r=self.scenario('artifact')[2]
        self.assertLess(r['band_support_at_fixture_threshold'],2)
        self.assertGreater(r['holdout_last_band_contrast'],-0.045)
    def test_pca_heldout_last_band(self):
        _,_,r=self.scenario('signal')
        self.assertEqual(r['holdout_index'],3)
        self.assertEqual(r['pca_fit_band_count'],3)
        self.assertEqual(len(r['pca_loadings'][0]),3)
        self.assertEqual(len(r['synthetic_target_minus_control']),4)
    def test_multiband_stain_cannot_certify_character(self):
        _,_,r=self.scenario('shared_stain')
        self.assertEqual(r['band_support_at_fixture_threshold'],4)
        self.assertEqual(r['reading_k1'],'NOT_RECONSTRUCTED')
        self.assertIn('stains',r['interpretation_boundary'])
    def test_reproducible_seeded_input(self):
        a=self.root/'first';b=self.root/'second'
        x=generate(a);y=generate(b)
        self.assertEqual([z['sha256'] for z in x['bands']],
                         [z['sha256'] for z in y['bands']])
    def test_out_of_range_registration_fails(self):
        from msi_lab.bench import align_translation
        a=np.roll(__import__('msi_lab.bench',fromlist=['_template'])._template(),16,axis=0)+1
        with self.assertRaisesRegex(ValueError,'too weak'):
            align_translation(a,max_shift=5)
    def test_tamper(self):
        x,_,_=self.scenario('signal')
        with (x/'band_00.npy').open('ab') as h:h.write(b'TAMPER')
        with self.assertRaisesRegex(ValueError,'hash or size'):verify_and_load(x)
    def test_missing_provenance(self):
        x,_,_=self.scenario('signal')
        p=x/'manifest.json';d=json.loads(p.read_text());del d['authorization'];p.write_text(json.dumps(d))
        with self.assertRaisesRegex(ValueError,'provenance'):verify_and_load(x)
    def test_real_origin_blocked(self):
        x,_,_=self.scenario('signal')
        p=x/'manifest.json';d=json.loads(p.read_text());d['origin']='REAL';p.write_text(json.dumps(d))
        with self.assertRaisesRegex(ValueError,'real inputs forbidden'):verify_and_load(x)
    def test_traversal(self):
        x,_,_=self.scenario('signal')
        p=x/'manifest.json';d=json.loads(p.read_text());d['bands'][0]['path']='../x.npy';p.write_text(json.dumps(d))
        with self.assertRaisesRegex(ValueError,'traversal'):verify_and_load(x)
    def test_fiducial_absence(self):
        with self.assertRaisesRegex(ValueError,'inconclusive'):choose_orientation(np.ones((128,128)))
    def test_constant_pca(self):
        _,v,_=pca_cube(np.ones((12,12,3)))
        self.assertTrue(np.allclose(v,0))
    def test_no_output_overwrite(self):
        x,y,_=self.scenario('signal')
        with self.assertRaises(FileExistsError):analyze(x,y)
if __name__=='__main__':unittest.main()
