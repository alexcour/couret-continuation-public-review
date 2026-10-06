# Related work and remaining evaluation

The general quotient and recursive-state principles overlap with Myhill--Nerode
equivalence, predictive state representations, causal states, epsilon-transducers,
information states and bisimulation metrics. The observation-table learner and
W-style conformance tests use classical automata-learning and testing methods.
These foundations are not claimed as discoveries of this project.

The software question is practical: how well does the full workflow expose hidden
differences between histories, export replayable witnesses and maintain the useful
state on a distinct controlled service? A four-state HTTP fixture now implements
that workflow. Performance and innovative use on a real target remain unestablished.

Compare with the same target, alphabet, state bound and preparation assumptions:
- LearnLib: https://github.com/LearnLib/learnlib
- AALpy: https://github.com/DES-Lab/AALpy
- ALEX: https://learnlib.de/pages/alex

Measure adapter setup time, preparations, action calls, witness readability,
coverage and regression detection. Keep fixture execution, real-target validation,
scientific novelty and practical usefulness as separate conclusions.

Prime context:
- Lemke Oliver and Soundararajan, PNAS 113 (2016), E4446--E4454, DOI 10.1073/pnas.1605366113.
- Lemke Oliver and Soundararajan, Math. Proc. Cambridge Philos. Soc. 168 (2020), 149--169, DOI 10.1017/S0305004118000592.
- Daniel John Murray, Prime-Residue Projection Tomography of Consecutive-Prime Biases, SSRN preprint dated 2026-06-15, DOI 10.2139/ssrn.6947578.

The overlap is acknowledged explicitly. A finite prime calculation and a negative
search result do not establish priority or an asymptotic prime theorem.
