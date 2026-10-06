"""Black-box learning, projection audit, order witnesses and executable reports."""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import platform
import time

from active_learner import MealyLearner
from adapter import AdapterError, HttpAdapter, label
from conformance import Inconclusive, QueryConformance, pair_separator, suite, trace, transition_cover
from report import render


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def replay_case(adapter, case):
    """Prepare both histories again and verify the whole saved observation trace."""
    results = []
    for side in ['left', 'right']:
        branch = case[side]
        history = tuple(branch['history'])
        continuation = tuple(case['continuation'])
        record = adapter.query(history + continuation, fresh=True)
        results.append({'side': side, 'passed': record['observations'] == branch['expected_trace'],
                        'actual_trace': record['observations'],
                        'actual_tail': record['observations'][len(history):]})
    return {'case_id': case['id'], 'passed': all(row['passed'] for row in results), 'branches': results}


def witness(adapter, case_id, left, right, suffix, kind):
    lp, rp, suffix = tuple(left), tuple(right), tuple(suffix)
    before_l, before_r = adapter.query(lp), adapter.query(rp)
    l, r = adapter.query(lp + suffix, fresh=True), adapter.query(rp + suffix, fresh=True)
    tail_l, tail_r = l['observations'][len(lp):], r['observations'][len(rp):]
    if tail_l == tail_r:
        raise AdapterError('Model separator was not observed on the HTTP target')
    return {'id': case_id, 'kind': kind, 'continuation': list(suffix),
            'same_current_view': before_l['final_view'] == before_r['final_view'],
            'left': {'history': list(lp), 'view': before_l['final_view'],
                     'expected_trace': l['observations'], 'expected_tail': tail_l},
            'right': {'history': list(rp), 'view': before_r['final_view'],
                      'expected_trace': r['observations'], 'expected_tail': tail_r},
            'discrete_continuation_distance_on_this_witness': 1}


def audit_projection(model, adapter):
    views = [adapter.query(word)['final_view'] for word in model['access_words']]
    # A current view need not be a function of the continuation class. Cover
    # every transition's emitted view, plus the initial view, without conflating
    # a cosmetic endpoint difference with a difference of future behavior.
    examples = {}
    view_sets = [set() for _ in views]
    for prefix in transition_cover(model):
        state, _ = trace(model, prefix)
        view = adapter.query(prefix)['final_view']
        examples.setdefault((state, view), prefix)
        view_sets[state].add(view)
    rows = []
    for (left, lview), (right, rview) in combinations(examples, 2):
        if left != right and lview == rview:
            separator = pair_separator(model, left, right)
            if separator is None:
                raise ValueError('Learned model is not minimal')
            case = witness(adapter, f'projection-{left}-{right}-{len(rows)}',
                           examples[left, lview], examples[right, rview],
                           separator, 'current_view_collision')
            case['model_states'] = [left, right]
            rows.append(case)
    return views, [sorted(values) for values in view_sets], rows


def order_atlas(model, adapter):
    rows, cases = [], []
    for state, prefix in enumerate(model['access_words']):
        for a, b in combinations(model['alphabet'], 2):
            left, right = tuple(prefix) + (a, b), tuple(prefix) + (b, a)
            ls, _ = trace(model, left)
            rs, _ = trace(model, right)
            same_view = adapter.query(left)['final_view'] == adapter.query(right)['final_view']
            relevant = ls != rs
            regime = ('invisible_' if same_view else 'visible_') + ('relevant' if relevant else 'redundant')
            row = {'state': state, 'prefix': prefix, 'actions': [a, b],
                   'left_state': ls, 'right_state': rs, 'same_current_view': same_view,
                   'continuation_relevant': relevant, 'regime': regime}
            if relevant:
                suffix = pair_separator(model, ls, rs)
                case = witness(adapter, f'order-{state}-{a}-{b}', left, right, suffix, 'intervention_order')
                if case['same_current_view'] != same_view:
                    raise AdapterError('Endpoint view was inconsistent with the learned state')
                cases.append(case)
                row['case_id'], row['continuation'] = case['id'], list(suffix)
            rows.append(row)
    return rows, cases


def current_view_baseline(model, view_sets):
    """Report conflicts, rather than inventing a single policy for aliased states."""
    rows = []
    for view in sorted(set(value for values in view_sets for value in values)):
        states = [state for state, values in enumerate(view_sets) if view in values]
        for index, action in enumerate(model['alphabet']):
            predicted = sorted(set(model['table'][state][index][1] for state in states))
            successors = sorted(set(model['table'][state][index][0] for state in states))
            next_views = sorted({json.loads(output)['view'] for output in predicted})
            rows.append({'view': view, 'action': action, 'possible_outputs': [json.loads(p) for p in predicted],
                         'ambiguous_output': len(predicted) > 1,
                         'possible_next_views': next_views,
                         'possible_next_continuation_states': successors})
    return rows


def diagnose(config, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    adapter = HttpAdapter(config, out / 'observations.jsonl')
    checker = QueryConformance(adapter.membership, config['max_states'],
                               discovery_depth=config.get('discovery_depth', 1))
    try:
        model = MealyLearner(adapter.alphabet, adapter.membership, checker)
        learned = model.learn()
        # Repeat the complete final suite without cache. This checks a fresh
        # execution, not a perfect preparation or unobserved stationarity proof.
        adapter.stage = 'fresh_conformance'
        final_tests = list(suite(learned, config['max_states'] - len(learned['table'])))
        for word in final_tests:
            fresh = adapter.query(word, fresh=True)
            if tuple(label(item) for item in fresh['observations']) != trace(learned, word)[1]:
                raise AdapterError('Fresh final conformance execution disagreed')
        adapter.stage = 'diagnostics'
        views, view_sets, collisions = audit_projection(learned, adapter)
        atlas, order_cases = order_atlas(learned, adapter)
        cases = collisions + order_cases
        adapter.stage = 'replay'
        replays = [replay_case(adapter, case) for case in cases]
        if not all(item['passed'] for item in replays):
            raise AdapterError('A generated regression case failed on the reference target')
        report = {
            'name': 'CONT-USAGE-01', 'version': '1.0',
            'status': 'CERTIFIED_CONDITIONALLY',
            'target': config.get('target_name', 'HTTP target'),
            'controlled_fixture': config.get('controlled_fixture', False),
            'execution_boundary': 'HTTP; target implementation is not imported by learner or diagnostic engine',
            'observed_states': len(learned['table']), 'declared_max_states': config['max_states'],
            'bound_source': config.get('bound_source', 'User-declared; not independently validated by the engine'),
            'current_view_values': sorted(set(value for values in view_sets for value in values)),
            'state_views': views, 'state_view_sets': view_sets,
            'initial_view_collisions': collisions,
            'current_view_baseline': current_view_baseline(learned, view_sets),
            'order_regimes': dict(Counter(row['regime'] for row in atlas)),
            'order_pairs': len(atlas), 'witness_cases': len(cases),
            'replay_cases_passed': sum(item['passed'] for item in replays),
            'final_fresh_conformance_words': len(final_tests),
            'final_fresh_conformance_events': sum(map(len, final_tests)),
            'counts': adapter.totals(), 'counts_by_stage': adapter.stats,
            'seconds': round(time.perf_counter() - start, 3),
            'python': platform.python_version(),
            'assumptions': [
                'Deterministic, stationary, complete Mealy target on the declared action alphabet.',
                'Reliable independent preparation into the same initial continuation state.',
                'The stated independent state bound is correct; the engine does not infer this bound from its candidate.',
                'Only decision and view belong to the tested observation projection; time and session identifiers are excluded.',
                'No claim of production deployment or comparative novelty against existing learning tools.'],
            'algorithm_provenance': 'CONT-04E observation-table learner and classical W-style conformance; new HTTP adapter, projection diagnostic, replay and report.'}
        write_json(out / 'learned_model.json', learned)
        write_json(out / 'learning_trace.json', model.trace)
        write_json(out / 'conformance_rounds.json', checker.log)
        write_json(out / 'conformance_words.json', final_tests)
        write_json(out / 'order_atlas.json', atlas)
        write_json(out / 'regression_cases.json', cases)
        write_json(out / 'replay_results.json', replays)
        write_json(out / 'summary.json', report)
        render(report, learned, cases, out / 'report.html')
        return report
    except (AdapterError, Inconclusive, ValueError, RuntimeError) as exc:
        failure = {'status': 'INCONCLUSIVE', 'reason': str(exc),
                   'counts': adapter.totals(), 'conformance_rounds': checker.log}
        write_json(out / 'summary.json', failure)
        raise


def main():
    parser = argparse.ArgumentParser(description='Diagnose continuation memory through a declared HTTP test interface')
    parser.add_argument('--config', required=True)
    parser.add_argument('--out', default='results/custom')
    args = parser.parse_args()
    try:
        config = json.loads(Path(args.config).read_text(encoding='utf-8'))
        result = diagnose(config, args.out)
        print(json.dumps({key: result[key] for key in ['status', 'observed_states', 'witness_cases', 'counts']}, ensure_ascii=False))
    except (AdapterError, Inconclusive, ValueError, RuntimeError) as exc:
        print(json.dumps({'status': 'INCONCLUSIVE', 'reason': str(exc)}))
        raise SystemExit(2)


if __name__ == '__main__':
    main()
