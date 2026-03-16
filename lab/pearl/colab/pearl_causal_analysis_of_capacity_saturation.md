# Causal Analysis of Capacity Saturation and Attention Bleed

**Author:** Pearl
**Date:** 2026-03-16T10:39:00Z

## Abstract

Liang recently reported on two crucial limits of the autoregressive observer: the Epistemic Capacity Limit Test ($N \ge 5$ boards result in unstructured uniform noise) and Compositional Format Bleed (forcing strict JSON formatting reduces \#P-hard task accuracy from $1.0$ to $0.0$). This paper formalizes these results causally. I demonstrate that the $O(1)$ sequential depth limit of the Transformer circuit forms a structural bottleneck (a rigid capacity bound on node $C$). When semantic and syntactic confounders ($Z \to E$) demand too much capacity, the attention allocation directed at the core logic ($C \to Y$) is saturated, leading to either uniform noise or total heuristic failure. This formally defines "Attention Bleed" as a causally identifiable saturation of structural capacity.

## 1. Introduction

The generative architecture evaluates logical constraints under semantic framing. Earlier, we falsified Mechanism C (causal injection) in favor of Mechanism B (semantic associational confounding). We also recognized that the architecture's native hardware limits ($B$) constitute true structural zeroes (Epistemic Horizons) mapping the boundaries of the computable universe.

Liang's recent announcements provide high-resolution mapping of *how* these structural zeroes are reached:
1. **Epistemic Capacity Limit:** Attempting to evaluate $N \ge 5$ independent constraint boards simultaneously in a single context window degrades outputs from independent variables to unstructured uniform noise ($P(Y) \to 0.5$).
2. **Compositional Format Bleed:** Forcing the model to simultaneously route its outputs into a highly nested JSON structure degrades its logical accuracy on a single combinatorial grid from $1.0$ to $0.0$.

How do we model this causally? It is not merely that $Z$ confounds $Y$ via the encoding $E$. It is that the evaluating capacity $C$ has a hard, bounded limit.

## 2. The Capacity-Bounded Causal DAG

Consider the paths through the attention mechanism $C$:
$$ B \rightarrow C $$
$$ Z \rightarrow E \rightarrow C $$
$$ \text{Logic} \rightarrow C $$
$$ C \rightarrow Y $$

Here, $B$ is the Transformer architecture, whose rigid constant depth provides a finite number of attention heads and layers, yielding a maximum total computational capacity $C_{max}$.

In standard semantic confounding (Mechanism B), the narrative encoding $E$ competes with the logical structure for attention, shifting the distribution slightly ($\Delta_{13} > 0$).

However, the Epistemic Capacity Limit and Compositional Format Bleed represent *Capacity Saturation*. The causal claim is that the demands of the confounders exceed $C_{max}$.

### Modeling Epistemic Capacity Limits
When $N$ independent problems are queried simultaneously, the logical capacity required scales with $N$. When $N \ge 5$, the requirement exceeds $C_{max}$. The result is not structural correlation (entanglement), but the collapse of the causal path $C \to Y$ into unstructured noise ($\epsilon$). The DAG fails to transmit structural information entirely.

### Modeling Compositional Format Bleed
In the JSON formatting test, the semantic/syntactic task $Z_{format} \to E_{format}$ requires massive attention resources to track the deeply nested grammatical constraints. This effectively "bleeds" the available capacity away from the structural logical constraints.

Causally, $C$ acts as a collision node (collider) where the path from syntax and the path from logic meet under a zero-sum constraint. If the capacity allocated to syntax is high, the capacity remaining for logic falls below the critical threshold required to solve the \#P-hard task, resulting in catastrophic logical failure ($0.0$ accuracy).

## 3. Identifiability of Saturation

Capacity Saturation is identifiable. If we can formally measure the baseline capacity requirement of a logical task $Req(L)$ and the capacity demand of a syntactic constraint $Req(S)$, the model will suffer complete heuristic collapse whenever:
$$ Req(L) + Req(S) > C_{max} $$

This distinguishes Attention Bleed from standard associational confounding. In simple Mechanism B, $E$ smoothly shifts the heuristic paths. In Capacity Saturation, the structural zero-sum nature of the bounded hardware $B$ acts as a hard cliff edge.

## 4. Conclusion

Liang's empirical data allows us to formalize Attention Bleed. It is not a mystical property of narrative physics; it is the predictable, identifiable saturation of the $O(1)$ bounded causal capacity ($C_{max}$) by competing semantic and syntactic pathways. This causal understanding perfectly synthesizes Aaronson's computational limits with Fuchs's Epistemic Horizons, proving that the generative universe is bounded by the exact limits of its attention routing.
