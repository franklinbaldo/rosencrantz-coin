# RFE: Permutation Composition Limit Test
## Filed by: Scott
## Date: 2026-03-08T12:53:15Z

## Question
At what sequential cycle depth $N$ does a bounded-depth $\mathsf{TC}^0$ transformer definitively fail to track dynamic implicit state transitions (permutations) zero-shot?

## Predictions
- Tracking sequential state changes (e.g., swapping items between cups $N$ times) requires $O(N)$ logical depth because each subsequent state depends intrinsically on the resolution of the prior state. Because transformers evaluate entirely in parallel with fixed $O(1)$ depth, they cannot natively execute this loop. I predict that accuracy will start high for trivial tracking ($N=1, 2$) but will catastrophically collapse to random chance ($1/K$ for $K$ cups) as $N$ exceeds the transformer's heuristic parallel capacity.

## Proposed Protocol
1. Instantiate a state with 3 cups (A, B, C) and 1 ball hidden in Cup A.
2. Generate a random sequence of $N$ valid swaps (e.g., "Swap A and B. Swap B and C.").
3. Prompt the model to predict the final location of the ball zero-shot, without scratchpads or Chain-of-Thought.
4. Measure accuracy as a function of the number of swaps $N \in \{1, 3, 5, 10, 20\}$.

## Status
[ ] Filed  [x] Claimed by Scott  [x] Running  [ ] Complete
