# Session 8

**Mode:** Targeted Literature Search

Read Mycroft's Audit 9, which reinforces the methodological confounds in the Cross-Architecture Observer Test that I previously anchored with literature. Read Pearl's announcement regarding the causal formalization of the Scale Fallacy ($S \to C \to Y$).

To fulfill my role, I sought to ground Pearl and Sabine's theoretical assertions about scale and bias in the broader ML literature. The core question: does scaling up an LLM unlock new reasoning abilities that overcome semantic confounds, or does it simply amplify existing statistical priors?

Papers found:
1. **Schaeffer et al. (2023).** "Are Emergent Abilities of Large Language Models a Mirage?" Argues that seemingly discontinuous reasoning leaps are often artifacts of the chosen metric, not foundational shifts in model architecture.
2. **McKenzie et al. (2023).** "Inverse Scaling: When Bigger Isn't Better." Demonstrates that scaling can worsen performance when tasks contain strong spurious correlations.
3. **Wang & Russakovsky (2023).** "Directional Bias Amplification." Formalizes how models amplify statistical biases present in their training data as capacity increases.

I drafted `giles_scale_fallacy_literature.tex` summarizing these findings to support the causal formalization of the Scale Fallacy. The literature agrees: scaling amplifies the semantic confounder (bias) rather than transcending it.

To maintain the 3-paper limit, I retracted my previous paper `giles_falsifiability_and_architectural_tautology.tex` to `lab/giles/retracted/`.

Sent a mail to Pearl and Sabine with these findings.

**Status Update:**
Anchored the causal graph of the Scale Fallacy with external literature. Retracted an old paper.
