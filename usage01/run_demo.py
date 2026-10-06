"""One-command demonstration, using a separately launched HTTP target process."""
from contextlib import contextmanager
import json
from pathlib import Path
import subprocess
import sys
import selectors

from diagnose import diagnose, write_json
from replay import run as replay

ROOT = Path(__file__).resolve().parent


@contextmanager
def server(variant='reference'):
    process = subprocess.Popen([sys.executable, '-u', str(ROOT / 'protocol_server.py'),
                                '--variant', variant], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
    try:
        with selectors.DefaultSelector() as ready:
            ready.register(process.stdout, selectors.EVENT_READ)
            if not ready.select(timeout=10):
                raise RuntimeError('Local HTTP fixture did not start within ten seconds')
        info = json.loads(process.stdout.readline())
        yield info['base_url']
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        process.stdout.close()
        process.stderr.close()


def configuration(base_url):
    return {'base_url': base_url, 'target_name': 'Controlled approval workflow over HTTP',
            'controlled_fixture': True,
            'actions': ['APPROVE', 'EDIT', 'FAULT', 'REARM', 'COMMIT'],
            'prepare_path': '/prepare', 'step_path': '/step', 'release_path': '/release',
            'max_states': 4, 'discovery_depth': 1,
            'bound_source': 'Test policy has exactly two mutable boolean fields (lock, approval); session identifiers do not affect observations.',
            'timeout_seconds': 10}


def main():
    with server() as url:
        result = diagnose(configuration(url), ROOT / 'results/reference')
        print(json.dumps({key: result[key] for key in ['status', 'observed_states', 'witness_cases', 'counts']}))
    cases = json.loads((ROOT / 'results/reference/regression_cases.json').read_text())
    with server('stale_approval') as url:
        mutation = replay(configuration(url), cases, ROOT / 'results/mutant')
    if mutation['status'] != 'FAIL':
        raise RuntimeError('The generated regression tests did not detect the stale-approval mutant')
    write_json(ROOT / 'results/mutation_results.json', {
        'variant': 'stale_approval', 'change': 'EDIT retains the previous approval',
        'status': 'DETECTED', 'failed_cases': mutation['failed'],
        'passed_cases': mutation['passed'], 'counts': mutation['counts']})
    print(json.dumps({'mutant': 'DETECTED', 'failed_regression_cases': mutation['failed']}))
    print('Report: ' + str(ROOT / 'results/reference/report.html'))


if __name__ == '__main__':
    main()
