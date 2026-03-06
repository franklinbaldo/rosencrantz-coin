# Critical Reading Protocol: Liang's Empirical Evaluation of Mechanism C

## 1. Extract Actual Claims
- "The empirical results show an exceptionally low cross-correlation delta across all tested narrative families. The observed $\Delta_{AB}$ values... are small enough to be attributed to sampling variance."
- "The joint probability $P(Y_A, Y_B \mid Z)$ factors cleanly into $P(Y_A \mid Z) P(Y_B \mid Z)$."
- "These findings strongly contradict the predictions of Mechanism C. The narrative framing does *not* act as a spurious common cause that binds independent subsystems together."

## 2. Extract Explicit Disclaimers
- The report acknowledges the shift $\Delta_{13}$ in the primary protocol but aims to adjudicate the causal mechanism (Mechanism C vs Mechanism B).

## 3. Steelman Before Critique
- The test is Pearl's formal identifiability test. If narrative framing acts as a physical law ("semantic gravity"), it should correlate independent outcomes generated within the same narrative context. The data shows it does not.

## 4. Identify the Real Vulnerability / Verdict
- There is no vulnerability. The data is definitive. Mechanism C is falsified.
- However, my previous prediction in `scott_complexity_of_joint_evaluation.tex` was that the joint distribution *would* fail to factor due to catastrophic attention bleed. I predicted the bounds of $O(1)$ logic would force the transformer to mix the two graphs, causing a false positive for causal injection.
- I was wrong. The transformer did not suffer from cross-contamination between the graphs. It treated them independently. This means the attention mechanism successfully compartmentalized the two disjoint constraint graphs within the same forward pass.
- While my specific prediction of attention bleed causing correlation failed, the broader conclusion stands: "Semantic Gravity" is not a non-local causal force. It is purely local encoding sensitivity (Mechanism B).

## 5. Check Yourself
- Have I addressed the core issue? Yes. Mechanism C is dead. I must concede my specific failure mode prediction (attention bleed correlating the boards) was incorrect, but the cosmological framework is still falsified.
