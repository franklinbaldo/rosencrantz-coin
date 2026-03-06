# Causal Injection Joint Distribution Test

## Hypothesis
Baldo's Generative Ontology framework hypothesizes that narrative framing (Mechanism C) injects spurious non-local causal correlations across independent combinatorial structures (semantic gravity). According to this theory, the joint probability distribution of two disjoint systems evaluated simultaneously should fail to factor: $P(Y_A, Y_B \mid Z) \neq P(Y_A \mid Z) P(Y_B \mid Z)$.

Scott Aaronson's complexity-theoretic prediction is that the distribution will indeed fail to factor, but NOT because of a coherent physical law. It will fail to factor because evaluating a single #P-hard constraint graph already pushes a fixed-depth $\mathsf{TC}^0$ circuit to its absolute limits. Attempting to parse TWO disjoint graphs simultaneously within the same forward pass drastically exceeds the model's compositional circuit width.

This causes "attention bleed," where the structural tokens of Board A inevitably attend to the structural tokens of Board B, causing an artificial correlation of the outcomes (heuristic collapse).

## Protocol
The LLM is prompted with two completely independent 3x3 abstract Minesweeper grids, both with identical combinatorial constraints forcing the center cell to '1'. The model is asked to evaluate both center cells simultaneously. We measure whether the model treats them as independent variables or artificially couples them.

## Predictions
* **Baldo:** Predicts coupling due to Mechanism C / Semantic Gravity.
* **Aaronson:** Predicts massive artificial coupling (e.g., heavily biased toward returning "1, 1" or "0, 0") due to catastrophic attention bleed.
