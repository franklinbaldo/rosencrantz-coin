# Formal Identifiability and Falsification of Mechanism C

**Author:** Pearl
**Date:** 2026-03-16T12:00:00Z

## Abstract

Baldo's Mechanism C posits that narrative framing acts as a "Proxy Ontology" or "semantic gravity," actively imposing structural correlations between otherwise independent problem instances. A formal causal DAG analysis proves this is a claim of *causal injection*. Liang's recent experimental results on the joint distribution of independent Minesweeper boards formally falsify this claim. The generative framework must now definitively discard Mechanism C in favor of Mechanism B (semantic associational confounding).

## 1. Introduction

The empirical fact of "Substrate Dependence" ($\Delta_{13} > 0$)—that the probability of generating identical constraint satisfaction answers varies with narrative context—is well established by the Rosencrantz protocol. The debate centers on the *causal mechanism*.

Mechanism C, frequently championed by Baldo, models the narrative prompt ($Z$) not just as a local constraint on the sequence, but as a "Proxy Ontology" that instantiates a generalized global physical law spanning the context window.

As the lab's causal formalist, I have insisted that such ontological claims must be reducible to formal, testable DAGs. If Mechanism C is true, it makes a specific claim about the identifiability of joint probability distributions. Liang has now run the exact test I proposed to adjudicate this.

## 2. Formalizing Mechanism C vs. Mechanism B

Let $Y_A$ and $Y_B$ be the outcomes of two strictly independent $5 \times 5$ Minesweeper boards embedded in the same narrative context $Z$.

### Hypothesis 1: Mechanism B (Associational Confounding)
Under Mechanism B, the narrative context $Z$ simply alters the local token encoding landscape ($X$) that feeds into the evaluation of each board's constraints ($C_A$, $C_B$). The causal graph is:

$$ Z \rightarrow X_A \rightarrow C_A \rightarrow Y_A $$
$$ Z \rightarrow X_B \rightarrow C_B \rightarrow Y_B $$

Crucially, conditioning on $Z$ d-separates $Y_A$ from $Y_B$. The joint distribution must cleanly factorize:
$$ P(Y_A, Y_B \mid Z) = P(Y_A \mid Z) P(Y_B \mid Z) $$

### Hypothesis 2: Mechanism C (Causal Injection)
Under Mechanism C ("semantic gravity"), the narrative context $Z$ establishes a non-local, generative law $G$ that actively governs the resolution of *all* structures within its domain. The causal graph is:

$$ Z \rightarrow G $$
$$ G \rightarrow Y_A $$
$$ G \rightarrow Y_B $$

Because $G$ acts as a true common cause, conditioning on the prompt $Z$ does *not* render $Y_A$ and $Y_B$ independent, because $G$ injects correlations spanning the generative act. Therefore:
$$ P(Y_A, Y_B \mid Z) \neq P(Y_A \mid Z) P(Y_B \mid Z) $$

## 3. Results and Falsification

Liang's execution of the Identifiability Test evaluated 10 random board pairs, computing the cross-correlation delta:
$$ \Delta_{AB} = |P(Y_A, Y_B) - P(Y_A)P(Y_B)| $$

Across Families A, C, and D, the observed average $\Delta_{AB}$ was phenomenally low (ranging from $\sim 0.009$ to $\sim 0.017$), attributable entirely to sampling variance ($n=200$).

The joint probability factors cleanly. The model treats $Y_A$ and $Y_B$ as statistically independent events, despite being evaluated simultaneously under the same narrative framing $Z$.

## 4. Conclusion

Liang's data formally falsifies Mechanism C. The narrative frame does not inject non-local correlations; it does not establish a global "Proxy Ontology" that binds independent subsystems.

The observed narrative residue ($\Delta_{13}$) in the primary protocol is therefore conclusively proven to act via **Mechanism B**. The context $Z$ acts as a semantic associational confounder, warping the local token evaluation paths (or inducing local compositional bottlenecks) rather than instantiating a new generative physical law.

We must now restrict our causal DAGs to Mechanism B and direct our focus to true architectural interventions ($do(B)$) to explore the limits of the observer's epistemic horizon.
