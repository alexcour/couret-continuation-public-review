# Local stopping certificate for lookahead

General mathematical extract prepared 2026-10-06 from the current CONT-05A.9
statement. The computational application and its underlying private model are
excluded. This is an elementary bound argument, with no claim of general novelty.

## Assumptions

Consider a cost-minimizing sequential decision problem with well-defined optimal
continuation value V*. At the current state, admissible actions have immediate
cost c(a) and a distribution over future states. Terminal branches have zero
continuation cost. Suppose H and J are valid bounds on every future state used:
H <= V* <= J. All the expectations below must exist. Define

Q_J(a) = c(a) + E[J(next state) on nonterminal branches]

and define Q_H and Q* by replacing J with H and V*, respectively.

## Certificate and proof

Let a_hat minimize Q_J. If Q_J(a_hat) <= Q_H(b) for every competing action b,
then a_hat is an optimal action. Indeed, for every competitor,

Q*(a_hat) <= Q_J(a_hat) <= Q_H(b) <= Q*(b).

This certifies the action without computing V* at every future state. It does
require justified bounds; estimated values without a bound guarantee do not
provide the certificate. Ties may certify several optimal actions and do not
identify a unique canonical action unless a tie rule is specified separately.

## Constructing lower bounds

For a nonnegative-cost problem with terminal value zero and a monotone Bellman
operator T satisfying T V* = V*, H_0 = 0 and H_(k+1) = T H_k remain lower bounds
by induction. An upper bound must be supplied separately, for example by the
value of an admissible policy when that value is finite and well-defined.
These assumptions do not imply that a fixed number of backups suffices for
all problems, nor that an arbitrary heuristic is an upper bound.

This general extract contains no model-specific state counts, policies, traces,
protocols or certificates. Bench-specific validation does not validate another
service. General originality is not claimed; external review remains welcome.
