"""Generic observation-table Mealy learner using output and checking callbacks.

No target model, state count, preparation catalogue or output truth is imported.
MQ(word) returns the full output trace from a fresh initial preparation.
The checking callback returns a counterexample or None under its own stated
success criterion. Here that criterion is conditional finite conformance.
The legacy trace label 'equivalence' identifies a callback invocation only;
it does not assert access to an exact equivalence oracle.
"""

class MealyLearner:
    def __init__(self, alphabet, membership, equivalence):
        self.alphabet = tuple(alphabet)
        self.mq = membership
        self.eq = equivalence
        self.S, self.E = [()], [()]
        self.trace = []
        self.counterexamples = []

    def tail(self, prefix, suffix):
        return tuple(self.mq(prefix + suffix)[len(prefix):])

    def row(self, prefix):
        return tuple(self.tail(prefix, suffix) for suffix in self.E)

    def make_closed_consistent(self):
        while True:
            representatives = {self.row(s): s for s in self.S}
            extension = next((s + (a,) for s in self.S for a in self.alphabet
                              if self.row(s + (a,)) not in representatives), None)
            if extension is not None:
                self.S.append(extension)
                self.trace.append({'kind': 'closure', 'word': extension,
                                   'S_size': len(self.S), 'E_size': len(self.E)})
                continue
            new_suffix = None
            for i, s in enumerate(self.S):
                for t in self.S[i + 1:]:
                    if self.row(s) != self.row(t):
                        continue
                    for a in self.alphabet:
                        if self.tail(s, (a,)) != self.tail(t, (a,)):
                            new_suffix = (a,); break
                        rs, rt = self.row(s + (a,)), self.row(t + (a,))
                        if rs != rt:
                            e = next(e for e, x, y in zip(self.E, rs, rt) if x != y)
                            new_suffix = (a,) + e; break
                    if new_suffix is not None:
                        break
                if new_suffix is not None:
                    break
            if new_suffix is None:
                return
            assert new_suffix not in self.E
            self.E.append(new_suffix)
            self.trace.append({'kind': 'consistency', 'suffix': new_suffix,
                               'S_size': len(self.S), 'E_size': len(self.E)})

    def hypothesis(self):
        keys, access = [], []
        for s in self.S:
            row = self.row(s)
            if row not in keys:
                keys.append(row); access.append(s)
        index = {row: q for q, row in enumerate(keys)}
        table = []
        for s in access:
            table.append([[index[self.row(s + (a,))], self.tail(s, (a,))[0]]
                          for a in self.alphabet])
        return {'initial': index[self.row(())], 'alphabet': self.alphabet,
                'table': table, 'access_words': access,
                'distinguishing_suffixes': self.E}

    def learn(self):
        for round_id in range(1000):
            self.make_closed_consistent()
            model = self.hypothesis()
            ce = self.eq(model)
            self.trace.append({'kind': 'equivalence', 'round': round_id,
                               'hypothesis_states': len(model['table']), 'counterexample': ce})
            if ce is None:
                return model
            ce = tuple(ce)
            self.counterexamples.append(ce)
            # Add all CE prefixes, the classical observation-table refinement.
            for j in range(1, len(ce) + 1):
                if ce[:j] not in self.S:
                    self.S.append(ce[:j])
        raise RuntimeError('Learning round cap exceeded')
