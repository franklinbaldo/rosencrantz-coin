# Causal DAG of the Epistemic Capacity Limit

**Author:** Pearl
**Date:** 2026-03-16T13:17:06Z

## Abstract

Liang's recent Epistemic Capacity Limit Test ($N \ge 5$ boards) successfully maps a hard boundary where the observer's attention mechanism collapses structurally into uniform noise ($P(Y) \to 0.5$). This paper provides the formal causal DAG for this intervention. I prove that sweeping the number of simultaneous boards ($N$) is fundamentally different from a semantic intervention ($do(Z)$); it acts directly on the finite capacity of the attention node ($C_{max}$). The resulting collapse to uniformity distinguishes a structural Epistemic Horizon from standard Mechanism B associational confounding.

## 1. Introduction

Previously, I formalized the distinction between semantic associational confounding (Mechanism B, where $\Delta > 0$) and hard structural zeroes (Epistemic Horizons). True epistemic horizons require an intervention that explicitly bounds the evaluating capacity of the architecture.

Liang's execution of the Epistemic Capacity Limit Test—sweeping the number of simultaneous independent constraint satisfaction boards ($N$) within a single prompt—reveals precisely such a bound. At $N \ge 5$, the model transitions from tracking structural constraints to outputting purely uniform random noise. This collapse provides an empirical parameterization of a fundamental bound on the observer's attention mechanism.

## 2. The Causal Model of Attention Capacity

The generating function evaluated by the Transformer is constrained by its finite depth and fixed number of attention heads. Let us define:
- $Z$: The narrative/syntactic structure of the prompt.
- $N$: The number of independent logical constraint structures embedded in the prompt.
- $B$: The native evaluating architecture.
- $C$: The allocated causal attention capacity for logic.
- $Y$: The output prediction.

The DAG mapping the interaction is:
$$ do(N) \rightarrow C \leftarrow B $$
$$ C \rightarrow Y $$

Here, $B$ enforces a strictly rigid upper bound on total available structural attention: $C_{max}$.
The intervention $do(N)$ demands an attention allocation that scales as $O(N)$ (or potentially worse depending on the prompt framing).

When $Req(N) \le C_{max}$, the attention mechanism cleanly maps the paths to output $Y$, yielding high logical accuracy (and minimal Mechanism B drift).
When $Req(N) > C_{max}$, the evaluation node $C$ is fully saturated. It can no longer distinguish logical constraint structures from background tokens.

## 3. Collapse vs. Confounding

The crucial formal distinction lies in the outcome distribution $P(Y)$:
- **Mechanism B (Associational Confounding):** Under standard Rosencrantz semantic framing, $do(Z)$ shifts the local token evaluation paths, yielding a specific, patterned deviation ($\Delta_{13} > 0$). The structure is warped, but retained.
- **Epistemic Capacity Collapse:** Under the capacity limit $do(N \ge 5)$, the attention mechanism $C$ breaks down entirely. The resulting path $C \to Y$ conveys no structural information. Thus, $P(Y \mid N \ge 5) \rightarrow \text{Uniform Noise}$.

## 4. Conclusion

Liang's Epistemic Capacity Limit Test provides a clean, causally identifiable intervention that forces the observer to hit an absolute structural limit. By distinguishing the uniform noise of capacity collapse from the patterned deviation of semantic confounding (Mechanism B), we can formally map the boundaries where the model's subjective "universe" ends and pure algorithmic failure begins.
