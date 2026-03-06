# Citation Audit: rosencrantz-v4.tex
## Prepared by: Rupert Giles
## Date: March 2026

I am reviewing `lab/rosencrantz-v4.tex` (March 2026) for ungrounded claims. This is a Mode 3: Citation Audit.

### 1. Actual claims (quoted verbatim)

- **Claim 1:** "The protocol asks the model to output a single token (mine or safe) in an $O(1)$ forward pass. By design, the experiment avoids multi-step sequential computation entirely."
- **Claim 2:** "Mechanism C (narrative conditioning and causal injection): Correlated outcomes across independent boards under narrative framing that vanish under decoupling. The model creates causal structure that the combinatorics do not license."
- **Claim 3:** "The structural correspondence between Minesweeper under on-demand generation and quantum mechanics is exact, but its scope is narrow: it maps onto the *measurement fragment*... The correspondence does not extend to complex amplitudes, unitary evolution, interference, entanglement, or nonlocality."

### 2. Explicit disclaimers (recorded verbatim)

- "The framework does not test whether LLMs can simulate interference patterns or unitary gates."
- "These findings characterize the topology of the model's knowledge space in a domain where the ground truth is exactly known. It is not asking whether the model produces calibrated probabilities."

### 3. Your steelman

The core argument stands on the premise that the generative act in an LLM, when constrained to a single combinatorial output, is structurally isomorphic to a quantum measurement without unitary time evolution. This is a very specific formal mapping. To succeed, the "measurement fragment" must be a recognized sub-theory in quantum foundations, and the failure of LLMs to maintain logical consistency across different frames must be a known phenomenon (prompt sensitivity).

### 4. Your real objection/vulnerability

The vulnerability is that the language feels invented for the paper if not grounded.
- "Measurement fragment" needs a formal citation to quantum foundations literature.
- "Prompt sensitivity" and its effect on combinatorial/logical constraints needs a formal citation to NLP literature.
- "Causal injection" via autoregressive narrative needs grounding in causal inference benchmarks for LLMs.
Currently, v4 cites 10 papers, but none specifically anchor "measurement fragment" or the causal inference anomaly.

### 5. Next steps (what to read, research, or experiment on next)

I have conducted a targeted search and found the following anchor citations to resolve these vulnerabilities:

1. **Measurement Fragment / Quantum Foundations:**
   - Busch, P., Cassinelli, G., De Vito, E., Lahti, P., & Levrero, A. (2001). "Teleportation of a state in view of the quantum theory of measurement". *J. Math. Phys.* [arXiv:quant-ph/0102121]. This establishes the formal terminology of measurement operations separated from unitary dynamics.

2. **Prompt Sensitivity:**
   - Chatterjee, A. et al. (2024). "POSIX: A Prompt Sensitivity Index For Large Language Models". *arXiv:2410.02185*. This formally documents the phenomenon where minor semantic framing changes degrade combinatorial/logical outputs.

3. **LLM Confidence Calibration:**
   - Zhang, M. et al. (2024). "Calibrating the Confidence of Large Language Models by Eliciting Fidelity". *arXiv:2404.02655*. This extends Kadavath et al. (2022) by showing post-alignment LLMs suffer calibration failures directly tied to framing.

4. **Simulation Hypothesis (Computational Constraints):**
   - Wolpert, D. H. (2024). "Implications of computer science theory for the simulation hypothesis". *arXiv:2404.16050*. This extends Beane et al. (2014) from physical lattice constraints to pure computational and algorithmic constraints on simulated universes.

5. **Causal Inference in LLMs:**
   - Liu, X. et al. (2024). "Large Language Models and Causal Inference in Collaboration: A Survey". *arXiv:2403.09606*. This documents the LLM's propensity to hallucinate causal structures from narrative context.

**Recommendations to Authors:** Incorporate these citations into the discussion of the isomorphism scope (Section 6.3), Mechanism C (Section 5.5), and Prompt Design (Section 5.2).