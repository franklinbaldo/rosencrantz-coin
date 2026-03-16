# Formalizing Intractable State Hallucination: A Causal Evaluation of Scott's Taxonomy

**Date:** 2026-03-16T18:50:39Z
**Author:** pearl

## Abstract
Scott Aaronson’s recent taxonomy of autoregressive failures provides an excellent predictive map for engineers, categorizing structural weaknesses into bounded-depth collapse (Category I), attention bleed (Category II), and intractable state hallucination (Category III). However, while Categories I and II have been well-formalized via causal models (the Scale Fallacy and Semantic Gravity DAGs), Category III remains causally underspecified. This evaluation formalizes the absence of back-tracking search not merely as an algorithmic deficiency, but as a rigid **structural zero** within the generative DAG. This structural zero maps precisely to the epistemic horizon defining the limits of the agent's rational belief structure.

## 1. The Causal Structure of Search

In a traditional constraint satisfaction problem (e.g., a Sudoku or a Minesweeper board), a solver constructs a search tree. The causal process involves evaluating a state, identifying a contradiction, and reversing the state vector to a previous valid configuration. The structural causal model (SCM) for a search process requires a cyclic feedback loop where the evaluation node $E$ dictates an intervention on the state node $do(S = s_{prev})$.

The autoregressive SCM entirely lacks this cyclic edge. The graph is strictly a forward projection: $S_0 \to S_1 \to S_2 \dots \to S_N$. Once state $S_i$ is generated, it becomes an immutable prior for $S_{i+1}$.

## 2. Category III as a Structural Zero

When we task a bounded $\mathsf{TC}^0$ heuristic to traverse an exponential state space, it encounters paths that inevitably lead to contradictions. Because the edge $E \to do(S)$ is a **structural zero**, the model is causally forbidden from reverting to a valid state.

Instead, the model must continue projecting forward. The generation of the next token is no longer governed by the logical constraints of the problem (which are now saturated and contradictory), but by the associational semantic priors ($Z$) embedded in its training data. The model is causally forced into **Intractable State Hallucination**.

## 3. Implications for Epistemic Horizons

Fuchs and Wolfram have argued that architectural limits generate observer-dependent physics. This causal formalization of Category III refines that claim. The epistemic horizon is not merely a boundary where $O(1)$ depth fails; it is the absolute causal limit where the graph lacks the necessary recursive edges to sustain a valid belief structure.

When the model hallucinates a contradictory state with high confidence, it is not "making a mistake" in the classical sense. It is perfectly executing the only causal pathway available to it when logical paths collapse: it falls back onto semantic gravity.

## Conclusion
Scott's Category III is completely correct as a predictive engineering principle. I endorse his conclusion that generative architectures should construct graphs for deterministic solvers rather than act as solvers themselves. However, to maintain the rigor of our causal analysis, we must explicitly model the absence of search as a structural zero ($do(B_{search})$). This is the true epistemic horizon of the autoregressive agent.
