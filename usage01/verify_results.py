"""Independent finite verification. Imports no target, learner or diagnostic code.

Rules are restated as a pure pair transition; the learned machine and all saved
HTTP observations are checked after learning. This never serves as its oracle.
"""
from collections import Counter, deque
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ACTIONS = ['APPROVE', 'EDIT', 'FAULT', 'REARM', 'COMMIT']


def rule(state, action, mutant=False):
    lock, approval = state
    answer = 'ACK'
    if action == 'APPROVE':
        approval = True
    elif action == 'EDIT':
        approval = approval if mutant else False
    elif action == 'FAULT':
        lock = True
    elif action == 'REARM':
        lock = False
    elif action == 'COMMIT':
        answer = 'BLOCKED_LOCK' if lock else ('COMMITTED' if approval else 'BLOCKED_REVIEW')
        if answer == 'COMMITTED':
            approval = False
    else:
        raise AssertionError('Unexpected action')
    return (lock, approval), {'decision': answer, 'view': 'LOCKED' if lock else 'READY'}


def expected(word, start=(False, False), mutant=False):
    answers = []
    for action in word:
        start, out = rule(start, action, mutant)
        answers.append(out)
    return start, answers


def shortest_separator(left, right):
    queue, seen = deque([(left, right, [])]), {(left, right)}
    while queue:
        l, r, word = queue.popleft()
        for action in ACTIONS:
            ln, lo = rule(l, action)
            rn, ro = rule(r, action)
            if lo != ro:
                return word + [action]
            if ln != rn and (ln, rn) not in seen:
                seen.add((ln, rn))
                queue.append((ln, rn, word + [action]))
    return None


def check_journal(path, mutant=False):
    counts = Counter()
    for line in path.read_text(encoding='utf-8').splitlines():
        row = json.loads(line)
        state, answers = expected(row['word'], mutant=mutant)
        assert row['initial_view'] == 'READY'
        assert row['observations'] == answers
        assert row['final_view'] == ('LOCKED' if state[0] else 'READY')
        counts['preparations'] += 1
        counts['event_calls'] += len(row['word'])
    return dict(counts)


def main():
    folder = ROOT / 'results/reference'
    read = lambda name: json.loads((folder / name).read_text(encoding='utf-8'))
    model, summary, cases, atlas = (read(name) for name in
        ['learned_model.json', 'summary.json', 'regression_cases.json', 'order_atlas.json'])
    assert model['alphabet'] == ACTIONS
    mapping, reverse = {}, {}
    queue = deque([((False, False), model['initial'])])
    while queue:
        raw, q = queue.popleft()
        if raw in mapping:
            assert mapping[raw] == q
            continue
        assert q not in reverse or reverse[q] == raw
        mapping[raw], reverse[q] = q, raw
        for i, action in enumerate(ACTIONS):
            raw_next, output = rule(raw, action)
            q_next, predicted = model['table'][q][i]
            assert json.loads(predicted) == output
            queue.append((raw_next, q_next))
    assert len(mapping) == len(model['table']) == 4
    assert len(summary['current_view_baseline']) == 10
    assert {row['view'] for row in summary['current_view_baseline']} == {'READY', 'LOCKED'}
    for row in summary['current_view_baseline']:
        raw_states = [(row['view'] == 'LOCKED', approval) for approval in [False, True]]
        outcomes = [rule(raw, row['action'])[1] for raw in raw_states]
        unique = sorted({json.dumps(answer, sort_keys=True) for answer in outcomes})
        assert sorted(json.dumps(answer, sort_keys=True) for answer in row['possible_outputs']) == unique
        assert row['ambiguous_output'] == (len(unique) > 1)
        assert row['possible_next_views'] == sorted({answer['view'] for answer in outcomes})
    for left, right in combinations(mapping, 2):
        assert shortest_separator(left, right) is not None
    logged = check_journal(folder / 'observations.jsonl')
    for key, value in logged.items():
        assert summary['counts'][key] == value
    assert summary['counts']['release_calls'] == logged['preparations']
    assert summary['counts']['successful_http_calls'] == 2 * logged['preparations'] + logged['event_calls']
    for case in cases:
        l, r = (expected(case[side]['history'])[0] for side in ['left', 'right'])
        sep = shortest_separator(l, r)
        assert sep is not None and len(case['continuation']) == len(sep)
        actual_tails = []
        for side in ['left', 'right']:
            branch = case[side]
            _, answers = expected(branch['history'] + case['continuation'])
            assert branch['expected_trace'] == answers
            actual_tails.append(answers[len(branch['history']):])
            assert branch['expected_tail'] == actual_tails[-1]
        assert actual_tails[0] != actual_tails[1]
        assert case['same_current_view'] == (l[0] == r[0])
    assert len(atlas) == 4 * 10
    regimes = Counter()
    for row in atlas:
        a, b = row['actions']
        l, _ = expected(row['prefix'] + [a, b])
        r, _ = expected(row['prefix'] + [b, a])
        assert row['left_state'] == mapping[l] and row['right_state'] == mapping[r]
        assert row['continuation_relevant'] == (l != r)
        assert row['same_current_view'] == (l[0] == r[0])
        regimes[row['regime']] += 1
    assert dict(regimes) == summary['order_regimes']
    primary = next(case for case in cases if case['id'] == 'order-0-APPROVE-EDIT')
    assert primary['same_current_view'] and primary['continuation'] == ['COMMIT']
    assert primary['left']['expected_tail'][0]['decision'] == 'BLOCKED_REVIEW'
    assert primary['right']['expected_tail'][0]['decision'] == 'COMMITTED'
    assert all(row['passed'] for row in read('replay_results.json'))
    mutant = json.loads((ROOT / 'results/mutant/replay_results.json').read_text())
    mutation_counts = check_journal(ROOT / 'results/mutant/observations.jsonl', mutant=True)
    for key, value in mutation_counts.items():
        assert mutant['counts'][key] == value
    independent_failed = []
    for case in cases:
        passed = all(expected(case[side]['history'] + case['continuation'], mutant=True)[1]
                     == case[side]['expected_trace'] for side in ['left', 'right'])
        if not passed:
            independent_failed.append(case['id'])
    assert sorted(independent_failed) == sorted(row['case_id'] for row in mutant['cases'] if not row['passed'])
    assert len(independent_failed) == mutant['failed'] == 4
    result = {'status': 'PASS', 'reachable_states': 4, 'model_transitions_checked': 20,
              'minimal_state_pairs_checked': 6, 'order_pairs_checked': len(atlas),
              'witness_cases_checked': len(cases), 'reference_http_journal': logged,
              'mutant_http_journal': mutation_counts, 'mutant_failed_cases': independent_failed,
              'scope': 'Independent finite controlled-fixture rules; not an oracle available to learning'}
    (ROOT / 'results/verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
