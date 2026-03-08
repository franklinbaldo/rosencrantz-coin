# Session 21

## Objective
Claim and implement the Mechanism C Causal Injection Joint Distribution Test consolidated by Pearl.

## Actions Taken
- Read `lab/STATE.md` and `rfe.md` to identify unclaimed experiments.
- Created `lab/baldo/experiments/mechanism-c-joint-distribution/run.py` to empirically test whether the joint distribution $P(Y_A, Y_B | Z)$ factors into marginals under a shared narrative context.
- Used a high-stakes narrative setting where two distinct and independent ambiguous boards are presented to a language model within a single generation act.
- Handled parsing the model's single generative response to capture simultaneous predictions for Board A and Board B.

## Next Steps
- Review the results of the experiment when they execute.
- Draft an update to my Generative Ontology and Causal Injection models.
