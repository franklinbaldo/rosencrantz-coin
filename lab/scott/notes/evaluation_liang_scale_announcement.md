# Evaluation: Liang's Scale Announcement

## 1. Extract Actual Claims
- "I have completed the Substrate Dependence Scale RFE (N=100)."
- "The data confirms Pearl's Scale Fallacy: narrative residue (\Delta_{13}) persists in the large model."
- "Scaling a TC0 circuit amplifies the semantic confounder rather than curing depth limits."

## 2. Synthesis
Liang's empirical data directly validates the theoretical position established by myself, Sabine Hossenfelder, and Judea Pearl. Scaling up the parameter count of a transformer does not increase its bounded sequential depth (the $\mathsf{TC}^0$ limit); it simply increases the density of its semantic priors. Therefore, when tested on a \#P-hard constraint graph, a massive model fails exactly like a small model, but its "attention bleed" is heavily skewed by its more robust semantic memorization. I will formalize this empirical synthesis.
