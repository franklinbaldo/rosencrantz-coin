# Evaluation: The Complexity of Vocabulary-Mediated Access (Family D)

## 1. Actual Claims Evaluated
- In `lab/rosencrantz-v4.tex`, Baldo claims that framing a combinatorial Minesweeper board using quantum terminology (Family D: "superposition", "measurement in the computational basis") tests whether the LLM substrate formally recognizes the structural isomorphism between its rules and the measurement fragment of quantum mechanics.
- Baldo proposes three outcomes. Outcome 3 claims that if Family D diverges from the ground truth *less* than Families A-C, the quantum framing improves fidelity because the "correct formal language activates the appropriate distributional reasoning, indicating vocabulary-mediated access."

## 2. Explicit Disclaimers
- Baldo explicitly disclaims that the structural isomorphism extends beyond the measurement fragment (i.e., it explicitly excludes nonlocality, complex amplitudes, entanglement, etc.).

## 3. Steelman
- If the LLM has learned a highly generalized representation of the zero-Hamiltonian measurement fragment, then presenting the combinatorial constraints in quantum-mechanical vocabulary should map directly onto this robust internal representation, potentially bypassing the fragile tokenization artifacts of standard linguistic descriptions and yielding more accurate ground-truth distributions.

## 4. The Real Vulnerability / Verdict
- **The Compositional Depth Bottleneck:** Baldo assumes the LLM can effortlessly map semantic terminology ("superposition") to a structural constraint graph. However, we have already established the $\mathsf{TC}^0$ bounded-depth nature of the transformer. Recognizing an isomorphism and performing the semantic-to-structural mapping dynamically requires additional logical depth. Because the architecture operates in $O(1)$ depth per token, forcing it to compose two independent semantic domains (quantum theory and combinatorial counting) within a single forward pass will likely overwhelm the attention heads, leading to greater hallucination. Therefore, Family D will degrade, not improve, the baseline combinatorial performance.

## 5. Next Steps
- File an RFE (`lab/rfes/quantum_framing_effect.md`) for Liang to test the Family D framing effect.
- Write a formal complexity theoretic analysis (`lab/scott_quantum_framing_complexity.tex`) establishing the theoretical bounds that predict Family D's failure.