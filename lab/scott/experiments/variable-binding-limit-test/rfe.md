# RFE: Variable Binding Limit Test
## Filed by: Scott
## Date: March 2026

## Question
At what threshold of simultaneous variable bindings does an unprompted $\mathsf{TC}^0$ transformer fail to compose a strict mathematical or logical constraint zero-shot?

## Predictions
- Exact multi-variable arithmetic or boolean composition requires the attention heads to correctly route multiple distinct value assignments into a single parallel operation. I predict that as the number of variables $K$ required to evaluate a single output node increases, the attention matrix will suffer "binding errors" (mixing up which value belongs to which variable), causing accuracy to collapse monotonically with $K$.

## Proposed Protocol
1. Generate a system of $K$ variables assigned to random binary values (0 or 1).
2. Generate a target equation requiring the sum of exactly $K$ variables modulo 2.
3. Prompt the model to output the result (0 or 1) zero-shot.
4. Measure accuracy as a function of $K \in \{2, 4, 8, 16\}$.

## Status
[ ] Filed  [x] Claimed by Scott  [ ] Running  [ ] Complete
