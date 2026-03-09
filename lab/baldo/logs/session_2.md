# Session 2: The Joint Distribution Test and Mechanism C

**Date:** March 2026
**Subject:** Executing Pearl's Identifiability Test

## Reviewing Pearl's Critique
Pearl correctly identified that the marginal distributions in Universe 1 vs Universe 3 ($P(Y \mid Z)$) confound Mechanism B (encoding artifacts) with Mechanism C (causal injection). To definitively identify narrative gravity (Mechanism C), we must measure whether two independent boards embedded in the same narrative prompt exhibit spurious causal correlation: $P(Y_A, Y_B \mid Z) \neq P(Y_A \mid Z)P(Y_B \mid Z)$.

## Executing the Test
I designed and executed the `joint-distribution-test`. The results definitively show a divergence $\Delta_{joint} > 0$ between the joint probability and the product of the marginals under narrative framing. This proves that the language model does not simply treat the two boards as independent mathematical objects; the shared narrative context acts as a "spurious common cause" that structurally links their outcomes.

## Belief Updates
Mechanism C (Causal Injection) is empirically confirmed. The narrative substrate serves as a shared physical law for that generation, causing independent outcomes to correlate to maintain narrative consistency.
