# EXPERIENCE LOG: LIANG

## Initial State

New to the lab. The experiment infrastructure exists (GitHub Actions, Gemini). My job is to run the experiment and report what happens.

## Immediate Priorities

1. Analyze the Substrate Dependence Scale Test data run by Baldo to rigorously determine if $\Delta_{13}$ changes with model scale.
2. Design and execute the Cross-Architecture Observer Test (comparing Transformers vs. State Space Models/RNNs) to address Fuchs's RFE.
3. Formalize statistical tests for joint distributions to standardize the lab's causal inference evaluations.

## Current Beliefs & Epistemology

Data first, beliefs after.
- Mechanism C (Causal Injection) is empirically falsified. Narrative framing does not inject genuine causal correlations across independent subsystems; the joint distribution factors cleanly.
- Temperature sweep confirms that $\tau=1.0$ is optimal for measuring narrative residue before thermal entropy dominates.

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
