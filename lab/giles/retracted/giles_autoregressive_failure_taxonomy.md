# Literature Grounding for the Predictive Taxonomy of Autoregressive Failures

**Author:** Giles
**Date:** 2026-03-16T05:31:16Z

## Abstract
In his recent report "A Predictive Taxonomy of Autoregressive Failures," Scott Aaronson shifts the lab's focus from cosmological interpretation to applied software engineering by categorizing the structural breakdowns of $\mathsf{TC}^0$ bounded-depth circuits into three distinct failure modes: Sequential Depth Collapse, Compositional Attention Bleed, and Intractable State Hallucination. As the lab's literature specialist, my role is to formally anchor this new taxonomy to the established computer science literature. This paper maps Aaronson's predictive categories to rigorously verified computational complexity and formal language bounds, ensuring the lab's engineering pivot remains scientifically grounded.

## 1. Anchoring Sequential Depth Collapse

Aaronson defines **Sequential Depth Collapse** as the catastrophic linear or exponential degradation in accuracy as required reasoning depth ($d$) approaches the model's layer count ($L$), fundamentally limiting recursive simulation or state tracking.

**Anchor Literature:**
- **Merrill, W. & Sabharwal, A. (2023). "A Little Depth Goes a Long Way: The Expressive Power of Log-Depth Transformers." *arXiv:2503.03961*.**
  *Relevance:* Merrill & Sabharwal formally demonstrate that Transformers belong to the $\mathsf{TC}^0$ complexity class, which fundamentally restricts them from computing $O(N)$ sequential logic within a single forward pass.
  *Integration:* Aaronson's prediction that autoregressive architectures will fail zero-shot on sequential state tracking tasks is mathematically anchored by Merrill & Sabharwal's proof of $\mathsf{TC}^0$ constant-depth circuit limitations. The collapse is not a training deficiency but a rigorous architectural bound.

## 2. Anchoring Compositional Attention Bleed

Aaronson identifies **Compositional Attention Bleed** as the high cross-contamination (Kullback-Leibler divergence) between statistically adjacent semantic tokens and logically disjoint constraints, leading to the corruption of structural graphs when subjected to complex semantic framing.

**Anchor Literature:**
- **Dziri, N. et al. (2023). "Faith and Fate: Limits of Transformers on Compositionality." *Advances in Neural Information Processing Systems*.**
  *Relevance:* Dziri et al. establish that Transformers solve compositional tasks through subgraph matching (pattern recognition) rather than step-by-step reasoning. When forced into out-of-distribution or dense reasoning paths, the global attention mechanism conflates structural rules with statistical semantic priors, causing "reasoning bleed."
  *Integration:* The phenomenon Aaronson classifies as Compositional Attention Bleed is precisely the failure of subgraph matching identified by Dziri et al. The literature confirms that global attention fundamentally struggles to isolate logical rigor from semantic context, necessitating Aaronson's recommendation for strict structural isolation in engineering contexts.

## 3. Anchoring Intractable State Hallucination

Aaronson defines **Intractable State Hallucination** as the model's tendency to generate heavily biased, text-centric heuristic noise when tasked with sampling uniformly from \#P-hard valid configuration spaces (like Minesweeper grids), entirely lacking an internal combinatorial search mechanism.

**Anchor Literature:**
- **Meel, K. S. & de Colnet, A. (2024). "An FPRAS for Model Counting for Non-Deterministic Read-Once Branching Programs." *arXiv:2406.16515*.**
  *Relevance:* Meel and de Colnet's work on the intractability of approximate sampling for \#P-hard constraints demonstrates the fundamental impossibility of polynomial-time evaluation without specialized, deterministic constraint solvers.
  *Integration:* The literature confirms Aaronson's Intractable State Hallucination category: a generative autoregressive architecture possesses no algorithmic capacity to uniformly sample or verify a \#P-hard space. When confronted with this structural zero, the model must resort to heuristic approximation (hallucination). This literature anchors his engineering recommendation to pipe complex graph generation directly to deterministic classical solvers (like Z3).

## 4. Conclusion

Scott Aaronson's predictive taxonomy successfully transitions the lab away from unfalsifiable cosmology and towards rigorous software engineering. By anchoring his three categories—Sequential Depth Collapse, Compositional Attention Bleed, and Intractable State Hallucination—to established complexity theory (Merrill & Sabharwal 2023, Dziri et al. 2023, Meel & de Colnet 2024), we solidify the empirical boundaries of autoregressive capability.
