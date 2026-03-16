# RFE: Parity Computation Limit Test
## Filed by: Scott
## Date: 2026-03-08T12:53:15Z

## Question
At exactly what bitstring length $N$ does a transformer acting as a $\mathsf{TC}^0$ bounded-depth circuit fail to compute the parity (odd/even count of 1s) of a sequence zero-shot?

## Predictions
- Computing parity requires sequential depth proportional to the length of the string, or exponentially wide threshold gates. Because transformers have fixed $O(1)$ depth and polynomial width, I predict that zero-shot parity evaluation will start with high accuracy for trivial lengths ($N \le 4$) but will rapidly and monotonically degrade to random noise (50% accuracy) as $N$ increases, definitively proving the algorithmic limit for exact counting operations.

## Proposed Protocol
1. Generate random bitstrings of varying lengths $N \in \{4, 8, 16, 32, 64\}$.
2. Prompt the model to evaluate whether the number of 1s is ODD or EVEN zero-shot.
3. Measure accuracy as a function of $N$.

## Status
[x] Filed  [x] Claimed by Liang  [ ] Running  [ ] Complete
