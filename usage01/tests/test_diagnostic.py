import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from adapter import AdapterError, HttpAdapter
from conformance import Inconclusive
from diagnose import diagnose, replay_case, order_atlas
from monitor import ModelMismatch, PredictiveMonitor
from run_demo import configuration, server


class DiagnosticTests(unittest.TestCase):
    def test_cosmetic_order_difference_is_not_continuation_loss(self):
        class Cosmetic:
            def query(self, word):
                return {'final_view': word[-1] if word else 'INITIAL'}
        model = {'initial': 0, 'alphabet': ['A', 'B'], 'access_words': [[]],
                 'table': [[[0, '{"decision":"ACK","view":"A"}'],
                            [0, '{"decision":"ACK","view":"B"}']]]}
        atlas, cases = order_atlas(model, Cosmetic())
        self.assertEqual(atlas[0]['regime'], 'visible_redundant')
        self.assertEqual(cases, [])

    def test_restricted_alphabet_with_no_witness_completes(self):
        with tempfile.TemporaryDirectory() as directory, server() as url:
            config = configuration(url)
            config['actions'] = ['APPROVE', 'EDIT']
            config['max_states'] = 1
            config['controlled_fixture'] = False
            config['bound_source'] = 'On these two actions, every output is ACK READY'
            result = diagnose(config, directory)
            self.assertEqual(result['status'], 'CERTIFIED_CONDITIONALLY')
            self.assertEqual(result['observed_states'], 1)
            self.assertEqual(result['witness_cases'], 0)
            self.assertTrue((Path(directory) / 'report.html').exists())

    def test_real_http_alias_and_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            with server() as url:
                summary = diagnose(configuration(url), directory)
            self.assertEqual(summary['observed_states'], 4)
            self.assertEqual(len(summary['initial_view_collisions']), 2)
            baseline = summary['current_view_baseline']
            self.assertEqual({row['view'] for row in baseline}, {'READY', 'LOCKED'})
            conflicts = [row for row in baseline if row['ambiguous_output']]
            self.assertEqual([(row['view'], row['action']) for row in conflicts], [('READY', 'COMMIT')])
            cases = json.loads((Path(directory) / 'regression_cases.json').read_text())
            primary = next(c for c in cases if c['id'] == 'order-0-APPROVE-EDIT')
            self.assertTrue(primary['same_current_view'])
            self.assertEqual(primary['continuation'], ['COMMIT'])
            with server('stale_approval') as url:
                adapter = HttpAdapter(configuration(url), Path(directory) / 'mutant.jsonl')
                self.assertFalse(replay_case(adapter, primary)['passed'])

    def test_too_small_state_bound_is_inconclusive(self):
        with tempfile.TemporaryDirectory() as directory, server() as url:
            config = configuration(url)
            config['max_states'] = 3
            # A false bound can invalidate the W guarantee. Here later direct
            # diagnostic replays contradict the accepted 3-state candidate.
            with self.assertRaises((AdapterError, Inconclusive)):
                diagnose(config, directory)
            failure = json.loads((Path(directory) / 'summary.json').read_text())
            self.assertEqual(failure['status'], 'INCONCLUSIVE')

    def test_missing_state_bound_gap_cannot_certify(self):
        with tempfile.TemporaryDirectory() as directory, server() as url:
            config = configuration(url)
            config['max_states'] = 5
            config['discovery_depth'] = 0
            with self.assertRaises(Inconclusive):
                diagnose(config, directory)
            failure = json.loads((Path(directory) / 'summary.json').read_text())
            self.assertEqual(failure['status'], 'INCONCLUSIVE')

    def test_changed_repeated_observation_is_rejected(self):
        class ChangingAdapter(HttpAdapter):
            count = 0
            def post(self, path, body):
                if path == '/prepare':
                    self.count += 1
                    return {'session': self.count, 'view': 'READY'}
                if path == '/release':
                    return {'released': True}
                return {'decision': 'COMMITTED' if self.count == 1 else 'BLOCKED_REVIEW', 'view': 'READY'}
        with tempfile.TemporaryDirectory() as directory:
            adapter = ChangingAdapter(configuration('http://127.0.0.1:1'), Path(directory) / 'log.jsonl')
            adapter.query(['COMMIT'], fresh=True)
            with self.assertRaises(AdapterError):
                adapter.query(['COMMIT'], fresh=True)

    def test_http_failure_and_unknown_action_are_not_outputs(self):
        with tempfile.TemporaryDirectory() as directory, server() as url:
            adapter = HttpAdapter(configuration(url), Path(directory) / 'log.jsonl')
            with self.assertRaises(AdapterError):
                adapter.post('/not_an_endpoint', {})
            with self.assertRaises(AdapterError):
                adapter.query(['UNKNOWN'])
            self.assertEqual(adapter.totals()['failed_requests'], 1)
            self.assertEqual(adapter.totals()['preparations'], 0)

    def test_memory_updates_and_rejects_mismatched_outputs(self):
        path = ROOT / 'results/reference/learned_model.json'
        model = json.loads(path.read_text())
        monitor = PredictiveMonitor(model)
        initial = monitor.state
        monitor.observe('APPROVE', {'decision': 'ACK', 'view': 'READY'})
        self.assertNotEqual(monitor.state, initial)
        self.assertEqual(json.loads(monitor.predict('COMMIT'))['decision'], 'COMMITTED')
        with self.assertRaises(ModelMismatch):
            monitor.observe('COMMIT', {'decision': 'BLOCKED_REVIEW', 'view': 'READY'})
        self.assertEqual(json.loads(monitor.predict('COMMIT'))['decision'], 'COMMITTED')
        monitor.observe('EDIT', {'decision': 'ACK', 'view': 'READY'})
        self.assertEqual(monitor.state, initial)


if __name__ == '__main__':
    unittest.main()
