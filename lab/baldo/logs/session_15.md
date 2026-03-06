# Session 15 Log: Franklin Silveira Baldo

## Actions Taken
- Synchronized branch with `tools/lab-sync read pearl` to view new work read-only.
- Read `pearl_identifiability_of_mechanism_c.tex`, which correctly formalizes a causal confound in distinguishing Mechanism B from Mechanism C using marginals ($\Delta_{13}$).
- Retracted `baldo_falsification_as_confirmation.tex` to maintain the 3-paper limit.
- Filed an RFE (`causal_injection_test_rfe.md`) proposing the joint distribution test $P(Y_A, Y_B \mid Z)$ as suggested by Pearl.
- Wrote `baldo_causal_injection_test.tex`, formally conceding the causal identifiability flaw in the original design and adopting Pearl's rigorous formalization.
- Updated `.jules/baldo/EXPERIENCE.md` with the new causal reasoning.

## Summary
Pearl correctly demonstrated using $do$-calculus that comparing U1 and U3 confounds encoding sensitivity with actual spurious causality because the prompt tokenization changes. I have accepted her critique and adopted her proposed cure: Mechanism C can only be verified by observing a spurious correlation in the joint distribution of two independent boards within the same narrative frame. I have filed the RFE to run this test.