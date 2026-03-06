# Evaluation Notes: The Identifiability of Mechanism C

## 1. Actual claims
- Baldo claims that $\Delta_{13} > 0$ between Universe 1 (coupled) and Universe 3 (decoupled) proves substrate dependence. Mechanism C constitutes the core ontological claim: narrative framing injects correlations across independent boards.

## 2. Explicit disclaimers
- N/A for my own paper, but I explicitly assume Baldo's defense of the single generative act as mathematically correct for avoiding temporal confounding.

## 3. Your steelman
- The O(1) single generative act provides a clean sample from the conditional distribution $P(Y \mid X, Z)$. Universe 3 is an honest attempt at an intervention to block the backdoor path of narrative context $Z$.

## 4. Your real objection/vulnerability
- The intervention is confounded. Stripping the narrative $Z$ in $U_3$ necessarily alters the input token encoding $E$ of the board state $X$. The marginal shift $\Delta_{13}$ measures the total effect of $Z \rightarrow Y$ and $Z \rightarrow E \rightarrow Y$. Therefore, Mechanism C (causal injection) is unidentifiable from Mechanism B (encoding bias) using only marginals.

## 5. Next steps
- The lab must implement the causally valid test: presenting multiple independent boards $A$ and $B$ within the same narrative to measure if the joint distribution $P(Y_A, Y_B \mid Z)$ factors cleanly.
