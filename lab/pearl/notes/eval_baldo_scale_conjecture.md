# Evaluation Notes: The Scale Dependence Conjecture

## 1. Actual claims
- Baldo claims that the narrative residue ($\Delta_{13}$) is caused by "semantic gravity" and will either remain constant or increase as model parameter scale increases, rather than disappearing as a transient artifact.
- The proposed test is to measure $\Delta_{13}$ across models of different scales.

## 2. Explicit disclaimers
- Acknowledges that the computational camp assumes "attention bleed" will be overridden by better logical routing in larger models.

## 3. Your steelman
- Baldo makes a testable empirical prediction: larger models possess denser, richer semantic representations. If $\Delta_{13}$ is driven by semantic word-association priors, increasing the richness of those priors could indeed increase the shift in the outcome distribution.

## 4. Real objection/vulnerability
- Measuring the marginal shift $\Delta_{13}$ across scales does not cleanly identify the *cause* of the shift.
- In causal terms, as scale increases, both the model's capacity for combinatorial logic (Mechanism A) AND its sensitivity to prompt encoding (Mechanism B) change simultaneously.
- Because $\Delta_{13}$ is confounded (removing narrative $Z$ alters prompt encoding $E$), an increase or decrease in $\Delta_{13}$ with scale cannot cleanly isolate whether "semantic gravity" or "encoding sensitivity" is changing.
- To test whether scale changes *causal injection* (Mechanism C), one must measure the joint distribution $P(Y_A, Y_B \mid Z)$ across scales, not just the confounded marginals.

## 5. Next steps
- I will write a response paper applying causal graphs to the scale dependence conjecture, showing that $\Delta_{13}$ remains an unidentifiable estimand regardless of scale.
