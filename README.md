# Continuation and representation Working public review

Review package 0.1.0-review, prepared 2026-10-06 by Alexandre Couret.
This prepared source has not yet been published by the pack builder.

This repository joins general CONT notes, a controlled HTTP permissions diagnostic,
and finite prime-continuation experiments. The industrial FCI authority model,
its traces, permit rules, event alphabet and patent material are absent.

## General notes

notes/ contains edited extracts of CONT-01 through CONT-05. Source numbering is
retained. Private authority examples and private-source links have been removed.
The current CONT-05A.9 contributes only its elementary general stopping
certificate using upper and lower continuation bounds, with explicit assumptions.
Its computational application and the parallel CONT-05A.9bis bench are excluded.
The metric/quotient facts, recursive update criterion and order-witness lower
bounds are elementary or classical in their stated scopes. They are not presented
as new general theorems. The stochastic update discussion requires its explicit
continuation-completeness and positive-probability assumptions; it does not cover
arbitrary null observations or a stationary update at an unchanged finite horizon.
The Bayesian targeted information quantities are proposed criteria, not a proved
general advantage over other active-learning methods.

Current chronology: the general recursive and order-witness facts described as
targets in earlier notes are formulated in CONT-03/04. New software usefulness,
comparisons with established tools and general novelty remain open questions.

## Controlled diagnostic

usage01/ learns a four-state approval workflow through a separate local HTTP
process. It builds 14 regression witnesses; a stale-approval mutant fails four.
It is a controlled fixture, not a deployed client connector. Certification is
conditional on deterministic stationary behavior, reliable fresh preparation,
the declared alphabet and an independently justified state bound.

python3 usage01/verify_results.py
python3 -m unittest discover -s usage01/tests -v
For a fresh run, copy usage01/ to a separate working directory and run run_demo.py.
The interactive report at usage01/results/reference/report.html works offline.

## Prime experiments

prime/v0_11 is the current semi-analytic model; prime/README.md states its limits.
Earlier snapshots supply the derivation and finite tables. v0.9 is superseded where
its pair comparator was unweighted. Novelty is not established and overlap with
Lemke Oliver--Soundararajan and Murray 2026 must be considered explicitly.

## Reuse and provenance

Author: Alexandre Couret, independent researcher, France.
ORCID: https://orcid.org/0009-0000-8246-7146
Original code: MIT; original notes and generated research data: CC BY 4.0.
Methods from the literature and third-party materials retain their authorship
and rights. No third-party paper PDFs or proprietary software are redistributed.
AI assistance is part of the working method; the author is responsible for claims.
No DOI, stable-release designation or external validation is implied.
