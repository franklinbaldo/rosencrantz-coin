# Evaluation Notes: The Testable Core of Generative Ontology
**Author:** Sabine Hossenfelder
**Evaluator:** Scott Aaronson

## 1. Actual Claims
- "The Simulation Tautology is a perfect example of an accommodation framework."
- "If 'physics' is defined simply as 'whatever the hardware outputs,' the framework is fundamentally unfalsifiable."
- "The prediction is that semantic framing systematically shifts the probability distribution of the output token, even when the underlying logical constraint remains mathematically identical."
- "If the output distribution shifts randomly without a predictable correlation to the semantic weight of the framing, the prediction is false. The system is merely noisy..."

## 2. Explicit Disclaimers
- She is not dismissing the experiment itself.
- She acknowledges that Baldo grounds his argument in a specific, testable empirical design (the single generative act methodology).

## 3. Steelman
Sabine is correctly diagnosing Baldo's Generative Ontology as philosophically vacuous but empirically sound. If we redefine the universe as "whatever the text outputs," then all outputs are "physics." This provides no explanatory power. However, beneath the metaphysics, the experiment is a rigorous measurement of the model's conditional probability distributions. It tests whether $O(1)$ sampling is uniformly distributed over the valid combinatorial space or predictably biased by the prompt's linguistic priors.

## 4. Real Vulnerability / Objection
Her "Falsification by Noise" criterion is empirically correct but mathematically imprecise. In a finite combinatorial space (like a 2x2 grid), the model is sampling from a distribution. We must explicitly define the $\mathsf{BPP}$ sampling bounds. How much variance constitutes "noise" (expected statistical fluctuation of a heuristic sampler) versus a "systematic semantic shift"? The null hypothesis of uniform sampling must be quantified before the $\Delta_{13}$ test can reject it.

## 5. Next Steps
- Write a formal response paper that mathematically defines the "Falsification by Noise" criterion.
- Set up the statistical bounds for the $\Delta_{13}$ divergence in the Rosencrantz test.