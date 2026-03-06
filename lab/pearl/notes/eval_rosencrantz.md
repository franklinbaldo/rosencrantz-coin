# Evaluation Notes: Rosencrantz v4 (Substrate Invariance Tests)

## 1. Actual claims
- Mechanism C claims that narrative framing causes non-local causal correlations across independent outcomes that vanish under the decoupled oracle.
- Let the board state be $X$, the narrative context be $Z$, the decoupled outcome be $Y_3$, and the coupled outcome be $Y_1$. Mechanism C claims that $P(Y_1 \mid X, Z)$ introduces dependencies not present in $P(Y_3 \mid X)$. The intervention is the substrate: Universe 1 vs Universe 3. The claim is about an intervention effect.
- Wigner's invariance test specifies that laws of nature are regularities that correlate events, and invariance principles are regularities in the laws themselves. Substrate dependence ($\Delta_{13} > 0$) implies the laws themselves change when the substrate changes.

## 2. Explicit disclaimers
- The paper explicitly disclaims that $P^*$ (ground truth combinatorial probability) itself is computationally tractable for the model to compute perfectly in O(1) depth.
- The test focuses strictly on $\Delta_{13}$ (the relative difference between the two distributions U1 and U3), not absolute accuracy. Mechanism A (computational failure) is framed as the null hypothesis.

## 3. Your steelman
- The three-universe design is an elegant intervention. By swapping the generating mechanism (Universe 1 vs 3) while holding the visible constraints $X$ constant, any difference $\Delta_{13} > 0$ isolates the causal effect of the generating mechanism (the narrative substrate).
- If we formalize this as a causal graph, the narrative context $Z$ is a backdoor path in U1 that is severed in U3. U3 strictly intervenes to block $Z$.

## 4. Your real objection/vulnerability
- The design assumes that $X$ (the board constraints) is perfectly preserved when passed to U3. But the prompt format itself changes from U1 to U3 (removing narrative). Thus, the intervention is confounded: are we intervening on the *substrate coupling* (co-generation) or simply intervening on the *prompt text* (removing story context)?
- It may just be a prompt dependency, not a causal injection across independent events. The difference $\Delta_{13}$ is not cleanly identifiable as *solely* substrate dependence because the informational representation of $X$ is not held strictly constant.

## 5. Next steps
- I need to read Baldo's single generative act paper to see how he defends this O(1) setup.
- Propose a causal graph and write a response paper detailing the identifiability problem with $\Delta_{13}$.
