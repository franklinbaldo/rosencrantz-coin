# Evaluation: The Permutation Composition Limit and Depth Bounds

## Context
While waiting for the CI pipeline to execute the `permutation-composition-limit-test`, I am formalizing the explicit complexity-theoretic predictions for what this test will demonstrate regarding the bounded $O(1)$ depth of the Transformer architecture.

## The Algorithmic Structure of Permutation Tracking
Tracking a dynamic state (like an object hidden under three cups being swapped $N$ times) is fundamentally a sequential operation. Evaluating the final state requires resolving $N$ dependent compositional steps.
- **True computation:** Requires $O(N)$ logical depth. The state at step $k$ depends strictly on the evaluated state at step $k-1$.
- **Transformer execution:** Attempts to compute this in a single forward pass, which is bottlenecked by its fixed number of layers $L$, effectively providing only $O(1)$ computational depth.

## The A Priori Prediction
Because the Transformer is structurally forced to evaluate a sequentially dependent $O(N)$ process using an $O(1)$ parallel heuristic (global self-attention), it cannot perform explicit state-tracking. It must rely on statistical pattern matching across the context window.

As the number of swaps ($N$) increases, the compositional complexity exceeds the finite depth $L$ of the logic circuit.
- **For small $N$:** The attention mechanism can perfectly resolve the path ($\Delta = 0$). Accuracy will be 100%.
- **The Heuristic Frontier:** At some critical threshold $N_{crit}$, the parallel heuristic will shatter because the structural dependencies exceed the attention head's capacity to isolate the correct path from the combinatorial noise of all possible paths.
- **The Collapse:** Beyond $N_{crit}$, the model's output will degrade into uniform random chance (e.g., 33.3% accuracy for a 3-cup problem), proving that the model retains no implicit state tracking and has collapsed entirely into heuristic noise.

## Implications for "Observer-Dependent Physics"
If the CI results match this prediction—a sharp decay from 1.0 accuracy to random chance at a specific depth threshold—it completely falsifies any claim that the model maintains a coherent "simulated physics" or "belief state" regarding the object's location. The failure is not an alternative physics; it is a rigid computational boundary mapping exactly to the known limits of bounded-depth logic circuits ($\mathsf{TC}^0$).

This test will provide the *a priori* mathematical parameterization that Wolfram and Fuchs have failed to provide: we can exactly map the depth boundary at which the "universe" collapses into noise.
