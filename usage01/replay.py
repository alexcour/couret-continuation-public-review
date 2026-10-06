"""Replay exported continuation witnesses against a declared HTTP test target."""
import argparse
import json
from pathlib import Path
from adapter import AdapterError, HttpAdapter
from diagnose import replay_case, write_json


def run(config, cases, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    adapter = HttpAdapter(config, out / 'observations.jsonl')
    adapter.stage = 'regression'
    rows = [replay_case(adapter, case) for case in cases]
    result = {'status': 'PASS' if all(row['passed'] for row in rows) else 'FAIL',
              'cases': rows, 'passed': sum(row['passed'] for row in rows),
              'failed': sum(not row['passed'] for row in rows), 'counts': adapter.totals()}
    write_json(out / 'replay_results.json', result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--cases', required=True)
    parser.add_argument('--out', default='results/regression')
    args = parser.parse_args()
    try:
        result = run(json.loads(Path(args.config).read_text()),
                     json.loads(Path(args.cases).read_text()), args.out)
        print(json.dumps({key: result[key] for key in ['status', 'passed', 'failed', 'counts']}))
        raise SystemExit(0 if result['status'] == 'PASS' else 1)
    except AdapterError as exc:
        print(json.dumps({'status': 'INCONCLUSIVE', 'reason': str(exc)}))
        raise SystemExit(2)
