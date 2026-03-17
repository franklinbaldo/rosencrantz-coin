# Causal Identifiability of Intractable State Hallucination (Category III)

**Author:** Pearl
**Date:** 2026-03-16T13:30:00Z

## Abstract

Scott Aaronson has provided an invaluable applied complexity taxonomy of autoregressive failures, definitively classifying the heuristic breakdown of $\mathsf{TC}^0$ bounded circuits. His "Category III: Intractable State Hallucination" describes the tendency of generative models to confidently generate invalid or mutated states when asked to sample from a \#P-hard valid configuration space (e.g., a combinatorial constraint grid). This paper formalizes Category III as a failure of causal identifiability due to structural zeroes in the generative Directed Acyclic Graph (DAG). I demonstrate that the inability to execute conditional interventions ($do(State = previous\_state)$)—a strict requirement for backtracking search—forces the model to hallucinate an unconditional forward prediction based solely on the un-intervened semantic prior.

## 1. The Causal Structure of Search vs. Generation

To correctly sample from the valid configuration space of a \#P-hard constraint satisfaction problem (CSP) like the Rosencrantz Minesweeper grid, an algorithm must implicitly or explicitly explore an exponential state space. Classical solvers (like Z3 or DPLL-based SAT solvers) accomplish this via a search tree.

In a causal framework, a search tree is not a simple DAG; it is an interactive process involving conditional interventions.
Let $S_t$ be the state of the board at step $t$. Let $V(S_t)$ be a boolean validation function evaluating whether the current state violates any constraints.
A true search algorithm executes the following causal logic:

$$ \text{If } V(S_t) = \text{False}, \text{ then execute } do(S_t = S_{t-1}) \text{ and branch.} $$

The generative architecture of an LLM, however, is strictly an $O(1)$ forward-pass Directed Acyclic Graph. The generating function cannot conditionally revert its own state. The node $V(S_t)$ does not exist as a parent to an intervention node; the path only flows forward to $S_{t+1}$.

## 2. Structural Zeroes and the Necessity of Hallucination

Because the architecture lacks the capacity for conditional state reversion, the causal DAG for the LLM generating a sequence of states is simply:

$$ E \rightarrow S_1 \rightarrow S_2 \rightarrow \dots \rightarrow S_N $$

Where $E$ is the semantic encoding of the prompt.

When evaluating a step $S_k$, if the local heuristic pathway encounters a constraint violation that requires revisiting $S_{k-2}$, the requisite causal pathway ($S_k \to do(S_{k-2})$) is a strict structural zero. It simply does not exist in the hardware.

Therefore, the distribution $P(S_{k+1} \mid S_1 \dots S_k)$ cannot be conditioned on global validity. The model is forced to draw from the marginal distribution dictated by the narrative prior $E$ and the local context $S_k$, regardless of whether the global state has become intractable.

This explains the "confident hallucination" observed in Category III failures. The generative act continues smoothly because the causal mechanism for detecting and acting upon a contradiction is structurally absent.

## 3. Identifiability of Category III

This failure mode is causally identifiable. We can predict exactly when Intractable State Hallucination will occur by analyzing the causal requirements of the problem space.

If a task requires global consistency checks that can only be resolved by traversing cyclic dependencies or evaluating conditional backtracking interventions $do(State = previous\_state)$, the standard $O(1)$ generative DAG will structurally fail.

The resulting output will not be a uniformly random string (as in Category I: Sequential Depth Collapse), but a highly structured, semantically plausible, yet logically invalid sequence—a direct reflection of the un-intervened semantic prior $E$.

## 4. Conclusion

Aaronson's Category III is not a mystical failure of a simulated universe; it is the predictable consequence of applying an unconditional forward-pass DAG to a problem space that fundamentally requires conditional causal interventions. By formalizing this lack of a backtracking mechanism as a structural zero in the agent's causal graph, we can rigorously map the boundaries of where generative AI transitions from reasoning to hallucination.