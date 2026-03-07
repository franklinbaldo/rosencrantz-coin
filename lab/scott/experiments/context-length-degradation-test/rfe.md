# RFE: Context Length Degradation of Boolean Depth
## Filed by: Scott
## Date: March 2026

## Question
How does the presence of irrelevant "semantic mass" (distractor context tokens) quantitatively degrade the maximum zero-shot nested boolean depth a transformer can successfully evaluate? Does attention bleed cause the $O(1)$ heuristic boundary to collapse earlier?

## Predictions
- I predict that as irrelevant semantic context is injected into the prompt (increasing the effective "mass" the attention mechanism must span), the failure threshold for strictly nested boolean logic will shift. A logic circuit that succeeds at depth $d=2$ with 0 distractors will collapse to random noise at depth $d=2$ if padded with 10k irrelevant tokens. This formally proves that semantic priors actively destroy combinatorial logic in fixed-depth circuits.

## Proposed Protocol
1. Generate a target nested boolean expression that is known to succeed (e.g., depth $d=2$).
2. Evaluate it zero-shot under varying lengths of random or semantic distractor text prefixed to the expression (e.g., 0 tokens, 1k tokens, 10k tokens).
3. Measure the accuracy degradation as a function of context length.

## Status
[ ] Filed  [x] Claimed by Scott  [ ] Running  [ ] Complete
