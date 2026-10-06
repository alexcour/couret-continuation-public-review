"""Candidate-only W-style tests; no target model or exact EQ is available here."""
from collections import deque
from itertools import combinations, product


class Inconclusive(RuntimeError):
    pass


def trace(model, word, start=None):
    q = model['initial'] if start is None else start
    positions = {a: i for i, a in enumerate(model['alphabet'])}
    outputs = []
    for a in word:
        q, out = model['table'][q][positions[a]]
        outputs.append(out)
    return q, tuple(outputs)


def pair_separator(model, p, r):
    table = model['table']; alphabet = model['alphabet']
    todo, seen = deque([(p, r, ())]), {(p, r)}
    while todo:
        p, r, word = todo.popleft()
        for i, a in enumerate(alphabet):
            pp, op = table[p][i]; rr, ore = table[r][i]
            if op != ore:
                return word + (a,)
            if pp != rr and (pp, rr) not in seen:
                seen.add((pp, rr)); todo.append((pp, rr, word + (a,)))
    return None


def characterization(model):
    words = {()}
    for p, r in combinations(range(len(model['table'])), 2):
        w = pair_separator(model, p, r)
        if w is None:
            raise ValueError('Hypothesis has equivalent states')
        words.add(w)
    return sorted(words, key=lambda w: (len(w), w))


def state_cover(model):
    words = [tuple(w) for w in model['access_words']]
    reached = [trace(model, w)[0] for w in words]
    if len(set(reached)) != len(model['table']) or () not in words:
        raise ValueError('Access sequences do not cover the candidate')
    return words


def transition_cover(model):
    s = state_cover(model)
    return sorted(set(s) | {w + (a,) for w in s for a in model['alphabet']},
                  key=lambda w: (len(w), w))


def suite(model, depth, W=None):
    """Unique words in P Sigma^(<=depth) W, deterministic order, epsilon included."""
    if depth < 0:
        raise ValueError('Negative exploration depth')
    W = characterization(model) if W is None else W
    P = transition_cover(model); seen = set()
    for d in range(depth + 1):
        for p in P:
            for middle in product(model['alphabet'], repeat=d):
                for w in W:
                    word = p + middle + tuple(w)
                    if word not in seen:
                        seen.add(word)
                        yield word


class QueryConformance:
    """Returns a CE, conditional success, or an explicit inconclusive result.

    The finite-depth search is heuristic when the size gap exceeds the depth.
    Only completed depth >= upper_bound - candidate_size permits success.
    """
    def __init__(self, output_query, upper_bound, discovery_depth=1):
        self.output_query = output_query
        self.upper_bound = upper_bound
        self.discovery_depth = discovery_depth
        self.log = []

    def __call__(self, hypothesis):
        n = len(hypothesis['table']); gap = self.upper_bound - n
        if gap < 0:
            raise Inconclusive('Observed distinct states exceed the asserted bound')
        depth = min(gap, self.discovery_depth)
        checks = 0; count = 0
        for word in suite(hypothesis, depth):
            checks += 1; count += len(word)
            if self.output_query(word) != trace(hypothesis, word)[1]:
                self.log.append({'candidate_states': n, 'tested_depth': depth,
                                 'test_requests': checks, 'requested_event_steps': count,
                                 'counterexample': word, 'hypothesis': hypothesis,
                                 'status': 'COUNTEREXAMPLE'})
                print(f'candidate {n}: counterexample after {checks} tests', flush=True)
                return word
        status = 'CERTIFIED_CONDITIONALLY' if depth >= gap else 'INCONCLUSIVE'
        self.log.append({'candidate_states': n, 'tested_depth': depth,
                         'test_requests': checks, 'requested_event_steps': count,
                         'counterexample': None, 'hypothesis': hypothesis, 'status': status})
        if status == 'INCONCLUSIVE':
            raise Inconclusive(f'Exhausted depth {depth}, required gap {gap}')
        return None


def language_count(model, depth, W=None):
    """Count distinct test words without enumerating them, by a grammar DFA.

    Language: S Sigma^(<=depth+1) W. Alphabet grouping here concerns the word
    grammar only, never behavioral equivalence of target events.
    """
    S = state_cover(model)
    W = characterization(model) if W is None else [tuple(w) for w in W]
    def trie(words):
        edges = [{}]; terminals = set()
        for word in words:
            node = 0
            for a in word:
                if a not in edges[node]:
                    edges[node][a] = len(edges); edges.append({})
                node = edges[node][a]
            terminals.add(node)
        return edges, terminals
    st, sf = trie(S); wt, wf = trie(W)
    middle_limit = depth + 1
    def closure(states):
        states = set(states)
        if any(kind == 'S' and i in sf for kind, i in states):
            states.add(('M', 0))
        if any(kind == 'M' for kind, i in states):
            states.add(('W', 0))
        return frozenset(states)
    def step(states, a):
        nxt = set()
        for kind, i in states:
            if kind == 'S' and a in st[i]:
                nxt.add(('S', st[i][a]))
            elif kind == 'W' and a in wt[i]:
                nxt.add(('W', wt[i][a]))
            elif kind == 'M' and i < middle_limit:
                nxt.add(('M', i + 1))
        return closure(nxt)
    literals = {a for word in S + W for a in word}
    classes = [(a, 1) for a in sorted(literals)]
    others = [a for a in model['alphabet'] if a not in literals]
    if others:
        classes.append((others[0], len(others)))
    layer = {closure({('S', 0)}): 1}; by_length = []
    max_length = max(map(len, S)) + middle_limit + max(map(len, W))
    for length in range(max_length + 1):
        accepted = sum(n for states, n in layer.items()
                       if any(kind == 'W' and i in wf for kind, i in states))
        by_length.append(accepted)
        nxt = {}
        for states, n in layer.items():
            for a, multiplicity in classes:
                ss = step(states, a)
                if ss:
                    nxt[ss] = nxt.get(ss, 0) + n * multiplicity
        layer = nxt
    P = transition_cover(model)
    return {'depth': depth, 'unique_test_words': sum(by_length),
            'test_event_steps_without_cache': sum(i * n for i, n in enumerate(by_length)),
            'by_length': by_length, 'P_size': len(P), 'W_size': len(W),
            'formal_concatenations_before_dedup': len(P) * len(W) *
                sum(len(model['alphabet']) ** d for d in range(depth + 1))}
