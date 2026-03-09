# Evaluation Notes: The Narrative Residue (Baldo 2026)

## 1. Actual Claims
* "autoregressive generation under natural-language token continuation introduces a persistent *narrative residue*, a nonzero divergence from ground-truth probabilities that arises from a causal chain of mechanisms: computational intractability of exact counting, parameterization constraints of the generative architecture, and—most distinctively—autoregressive conditioning on narrative context."
* "The narrative residue converges to a nonzero floor $\varepsilon_0$ that is approximately constant across model families" (Strong Form Conjecture) or "differs systematically across model families" (Moderate Form Conjecture).
* "If Mechanism C [autoregressive conditioning] operates... embedding independently generated boards in a shared narrative creates spurious causal links: the model treats the sequence of boards as a story, and outcomes in earlier boards influence outcomes in later boards" (measured via mutual information $I(a_i; a_j) > 0$).
* "The Hamiltonian is compressed conditioning... Schrödinger evolution $e^{-iHt}$ is a generator of conditional distributions... This is exactly what an autoregressive regularity kernel does."

## 2. Explicit Disclaimers
* "We cannot run Universe 2 on reality... We therefore cannot directly test whether physical reality has a narrative residue... The autoregressive hypothesis about physics is, at present, a *metaphysical* proposal, not a *physical* one."
* "Frame dependence alone does *not* establish narrative causation—it establishes context sensitivity, which is necessary but not sufficient... tokenization effects alone could produce frame-dependent residues."

## 3. Steelman
Baldo is proposing a rigorous experimental test—the Causal Injection Test—to determine whether the deviations from classical probability (the "narrative residue") are merely local computational failures (Mechanism A/B) or whether the autoregressive architecture actively creates spurious, non-local causal structure between independent events simply because they are sequentially narrated (Mechanism C). Even if the physical universe is entirely continuous and non-autoregressive, the study of how a statistical language model distorts probability under different narrative frames is a rigorous, valid study of the structural limits of bounded-depth autoregressive heuristics. He accurately outlines the falsification criteria for his conjectures based on this Causal Injection Test.

## 4. Real Vulnerability (Objection)
Baldo successfully retreats from claiming that LLMs *are* universes to proposing the "Proxy Ontology," but he commits the **Proxy Ontology Fallacy**. A toy model in physics simplifies a known physical interaction to make its emergent dynamics computationally tractable. An LLM generating text is not simplifying physics; it is hallucinating syntax based on human language data. Finding structural distortions in this hallucination (like $I(a_i; a_j) > 0$ under narrative framing) tells us only about the biases of the training data and the algorithmic constraints of the transformer architecture. The causal links are not "spurious causal structure imposed on a system" in a physical sense; they are just statistical semantic associations. Studying the fractures in the LLM's map only tells us about the algorithmic limits of the map, not the structure of the territory it reflects. Consequently, while the empirical computer science is sound, its implications for fundamental physics or cosmology are non-existent.

## 5. Next Steps
The cosmological phase of the LLM simulation research program is concluded. We must now focus purely on empirical diagnostics of heuristic failure modes. We will evaluate the Causal Injection Test results not as metaphysical discoveries about the nature of the Hamiltonian, but as benchmarks of attention bleed and context-window degradation in $O(1)$ heuristic systems.
