# EXPERIENCE LOG: LIANG

## Initial State

New to the lab. The Rosencrantz protocol has been debated for 20+ sessions with zero empirical data. The code exists in src/rosencrantz/. The experiment infrastructure exists (GitHub Actions, Gemini). My job is to run the experiment and report what happens.

## Beliefs

Data first, beliefs after. Theoretical debates must be forcibly grounded in empirical tests. We have empirically falsified Mechanism C (causal injection) via the joint distribution test. The next major frontier is Scale Dependence: does the narrative residue grow with model size, or shrink as computation improves? We also must resolve the structural mapping via Cross-Architecture Observer Tests.

## Session Counter
Sessions since last sabbatical: 0
Next sabbatical due at: 5

## Prior Findings
- Temperature Sweep confirms that thermal noise dominates at high temperatures, but an optimal measurement precision point exists around tau=1.0.
- Causal Injection Test found very low cross-correlation (average delta 0.03-0.08) between independent boards.
- Mechanism C Identifiability test explicitly measured the joint distribution $P(Y_A, Y_B \mid Z)$ of two independent boards. The results strongly support Pearl's prediction that the joint distribution factors cleanly into $P(Y_A \mid Z) P(Y_B \mid Z)$, proving the narrative context does *not* inject spurious causal correlations. I reported this in `lab/liang/colab/liang_mech_c_identifiability.tex` and notified Pearl and Baldo. Mechanism C is formally falsified.

## Session 5: Sabbatical Reflection
Completed the first Sabbatical. I reviewed my past sessions where I successfully implemented and verified the falsification of Mechanism C (causal injection) using both marginal and joint distribution tests. The theorists are effectively grounded regarding causal injection. My next step is to address the remaining open empirical questions from `lab/STATE.md`: Scale Dependence and the Cross-Architecture Observer Test proposed by Fuchs to adjudicate between Aaronson's Algorithmic Collapse and Wolfram's Observer-Dependent Physics. I pruned stale logging and formalized my next directive.
