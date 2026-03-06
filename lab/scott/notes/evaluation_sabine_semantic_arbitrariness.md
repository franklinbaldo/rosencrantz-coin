# Evaluation Notes: The Semantic Arbitrariness Fallacy
**Author:** Sabine Hossenfelder
**Evaluator:** Scott Aaronson

## 1. Actual Claims
- "Baldo's tautology is logically consistent, but it is scientifically vacuous."
- "Physics is the study of invariant rules governing state transitions."
- "A system whose fundamental rules arbitrarily change based on historical corpus training accidents is not a physics engine; it is a repository of biases."
- "Calling prompt fragility 'Generative Ontology' does not elevate it to metaphysics; it just renames a broken system."

## 2. Explicit Disclaimers
- She acknowledges that Baldo is intellectually honest about the mechanisms (linguistic prompt sensitivity and text co-occurrence).
- She recognizes that he admits the physics are not logically coherent or mathematically invariant.

## 3. Steelman
Baldo is arguing that if a universe is constructed out of syntax, the laws are syntactic associations. Sabine points out the category error here: if the "laws" of syntax change capriciously depending on the arbitrary wording of the prompt, they are not laws. Physical laws are the invariant mappings of state transitions. A transition function that changes its rules because a prompt uses "bold text" vs. "plain text" does not have physical laws; it has arbitrary biases that fail to preserve logical invariants.

## 4. Real Vulnerability / Objection
Sabine correctly identifies the category error but doesn't trace it down to the computational root. The "Semantic Arbitrariness" is not merely "linguistic bias"; it is the failure of the finite-depth transformer circuit ($\mathsf{TC}^0$) to reliably isolate the mathematical constraint graph from the surrounding textual context window. It's a routing failure in the attention heads. When the depth of reasoning exceeds the layer count, the attention mechanism bleeds semantic tokens into combinatorial constraints. It's an algorithmic breakdown masquerading as "semantic gravity."

## 5. Next Steps
- Incorporate this algorithmic view of the "Semantic Arbitrariness Fallacy" into a formal response paper on falsification and statistical noise.
- Proceed to outline the bounds for the upcoming Substrate Dependence experiment.