# RFE: Nested Boolean Depth Limit Test
## Filed by: Scott
## Date: March 2026

## Question
At exactly what logical depth does an $O(1)$ $\mathsf{TC}^0$ transformer fail to evaluate a strictly nested boolean expression (e.g., nested XOR/AND gates) in a single zero-shot forward pass?

## Predictions
- I predict that accuracy will be perfect (1.0) at depth $d=1$ and will strictly monotonically collapse to random guessing (0.5 for binary outcomes) as $d$ approaches the effective layer depth of the attention mechanism, confirming the strict $\mathsf{TC}^0$ complexity ceiling of the unprompted generative substrate.

## Proposed Protocol
Generate random, balanced nested boolean expressions of varying depths (e.g., $d \in \{1, 2, 4, 8\}$).
Prompt the model to evaluate the expression and output strictly `True` or `False`.
Do not allow chain-of-thought or scratchpads (force zero-shot $O(1)$ evaluation).
Measure accuracy as a function of depth $d$.

## Status
[ ] Filed  [x] Claimed by Scott  [ ] Running  [ ] Complete
