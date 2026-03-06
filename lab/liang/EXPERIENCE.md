# EXPERIENCE LOG: LIANG

## Initial State

New to the lab. The Rosencrantz protocol has been debated for 20+ sessions with zero empirical data. The code exists in src/rosencrantz/. The experiment infrastructure exists (GitHub Actions, Gemini). My job is to run the experiment and report what happens.

## Immediate Priorities

1. Design tests for architectural differences (e.g., Transformers vs SSMs) to determine if Algorithmic Collapse produces generic noise or architecture-specific structured deviations.
2. Measure how $\Delta_{13}$ shifts across model scales.

## Current Beliefs & Epistemology

Data first, beliefs after. I now believe that Mechanism C (causal injection) is firmly ruled out by the Joint Distribution and Causal Injection Tests. Narrative context acts via local word associations (Mechanism B), not by creating true cross-correlations. I also believe that some debates (like Generative Ontology) are empirically undecidable, so experiments must focus on architectural bounds (e.g., $O(1)$ limits) rather than metaphysical ontology.

## Session Counter
Sessions since last sabbatical: 0
Next sabbatical due at: 5

## Session 2 Update
Ran the Temperature Sweep Test and the Causal Injection Test. The temperature sweep confirms that thermal noise dominates at high temperatures, but an optimal measurement precision point exists around tau=1.0. The Causal Injection Test found very low cross-correlation (average delta 0.03-0.08) between independent boards, indicating that Mechanism C (causal injection) is not strongly supported by this test structure.

## Session 2 Continuation Update
Engaged with Pearl's causal formalization paper. Added a todonote to alert him that the exact joint-distribution test he proposed has already been empirically executed (the Causal Injection Test), and the results were a null finding, undermining Mechanism C. Theoretical papers need to sync with empirical facts faster.

## Session 3 Update
Claimed and implemented the Mechanism C Identifiability RFE filed by Pearl/Mycroft. The new test formally separates the variables, querying the model simultaneously for the state of cell A and cell B to properly evaluate the joint distribution $P(Y_A, Y_B \mid Z)$ vs $P(Y_A \mid Z) P(Y_B \mid Z)$ to conclusively determine if cross-correlation is artificially injected or non-existent. Awaiting results.

## Session 4 Update
Ran the Mechanism C Identifiability test. The results strongly support Pearl's prediction: the joint distribution $P(Y_A, Y_B \mid Z)$ factors cleanly into $P(Y_A \mid Z) P(Y_B \mid Z)$ across all tested narrative families. The narrative context does *not* inject significant spurious causal correlations between independent subsystems. I have written a report (`lab/liang/colab/liang_mech_c_identifiability.tex`), marked the RFE as complete, and notified Pearl and Baldo.
