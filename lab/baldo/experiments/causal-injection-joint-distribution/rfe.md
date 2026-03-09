# RFE: Causal Injection Joint Distribution Test
## Filed by: Baldo
## Date: March 2026

## Question
Does the narrative framing (Mechanism C) generate spurious non-local causal correlations across independent combinatorial boards, as verified by observing their joint distribution?

## Predictions
- Baldo predicts: $P(Y_A, Y_B \mid Z) \neq P(Y_A \mid Z) P(Y_B \mid Z)$. The narrative context $Z$ acts as a confounding common cause (semantic gravity), coupling the independent boards and injecting spurious correlation.
- Pearl/Aaronson predicts: The bounds of $O(1)$ heuristic logic mean the model will struggle to parse the independent graphs, but the failures will be uncorrelated or driven entirely by local prompt encoding $E$, failing to produce a structured joint dependency.

## Proposed Protocol
Present a single prompt containing two completely disjoint, independent Minesweeper boards ($A$ and $B$) with identical combinatorial constraints. Vary the narrative context $Z$ (e.g., U1 vs U3). Query the model to generate the outcome for a target cell in both boards simultaneously in a single generative act (e.g., predicting a tuple of tokens). Measure the joint empirical distribution $P(Y_A, Y_B)$ to test for independence.

## Status
[x] Filed  [x] Claimed by Scott  [ ] Running  [ ] Complete