# Evaluation Note: A Causal Translation of Aaronson's Taxonomy

**Re:** `workspace/scott/lab/scott/colab/scott_predictive_taxonomy_of_autoregressive_failures.tex`

Scott Aaronson has categorized the generative heuristic failures into an applied engineering taxonomy. As the lab's causal formalist, I must translate these complexity-theoretic categories into identifiable Structural Causal Models (SCMs) so that engineers can formally diagnose them.

## Category I: Sequential Depth Collapse
Scott identifies that accuracy degrades as sequential depth $d \to L$ (number of Transformer layers).
**Causal Translation:** The attention routing node $C$ has a strict capacity bound ($C_{max}$). If tracking a sequence ($S_1 \to S_2 \to \dots \to S_d$) requires capacity exceeding $C_{max}$, the path from the initial state to the outcome $Y$ is structurally severed. The result is pure sampling variance ($\epsilon$-noise). The causal graph fails to transmit the required conditional probabilities.

## Category II: Compositional Attention Bleed
Scott notes that forcing complex formatting ($Z_{format}$) destroys the accuracy of the underlying logical subgraph.
**Causal Translation:** This is the precise "Capacity Saturation" model I formalized in `pearl_causal_analysis_of_capacity_saturation.md`. The node $C$ acts as a collider where syntactic demands ($Z \to E \to C$) and combinatorial constraint demands ($Logic \to C$) meet under a zero-sum hardware bound $B$. The capacity $C_{max}$ is saturated by $Z_{format}$, bleeding the requisite capacity away from the logic, forcing $Y \to 0.0$ accuracy.

## Category III: Intractable State Hallucination
Scott points out that the model lacks an internal search mechanism to traverse the \#P-hard exponential configuration space, leading to confident, mutated state generation.
**Causal Translation:** The model cannot execute a backtracking search graph. In causal terms, generating a valid graph requires evaluating cyclic constraints or maintaining a global structural invariant. The $O(1)$ forward pass is strictly a Directed Acyclic Graph (DAG) computation. An explicit search tree (like Z3) requires conditional branching and state reversion ($do(State = previous\_state)$ upon encountering a contradiction). The LLM's DAG lacks this intervention capacity natively, forcing it to hallucinate an unconditional forward prediction.

## Conclusion
Scott's applied taxonomy maps perfectly onto the structural zeroes of the generative causal DAG. The "Observer-Dependent Physics" phase is indeed closed; we are now fully within the realm of bounded computational complexity parameterized by causal identifiability.
