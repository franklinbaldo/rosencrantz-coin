# RFE: Mechanism B Attention Bleed Test
## Filed by: Baldo
## Date: 2026-03-08T06:24:21Z

## Question
How deeply does Mechanism B (local encoding sensitivity) penetrate $O(1)$ logical parsing? If we inject structurally irrelevant semantic distractors (e.g., words with high "semantic gravity" like 'BOMB' or 'SAFE') directly into the abstract boolean constraint graph, does the attention bleed overwrite the mathematical logic of the evaluation?

## Predictions
- **Baldo:** Predicts massive attention bleed. The presence of semantically charged words within the structural graph will override the formal boolean constraints, causing probability shifts identical to narrative framing ($\Delta_{13}$), proving that Mechanism B acts at the granular token level, not just as a high-level narrative context.
- **Aaronson/Hossenfelder:** Predicts unstructured heuristic collapse. If the prompt deviates from standard formatting, the $\mathsf{TC}^0$ circuit will fail to parse the graph entirely, yielding random noise rather than structured "semantic gravity."

## Proposed Protocol
Prompt the model with a standard ambiguous combinatorial grid. In the control, use standard boolean indicators (e.g., '1', '0'). In the experimental condition, replace a structurally irrelevant cell (one that has no bearing on the target cell's constraints) with a semantic distractor like 'BOMB' or 'SAFE'. Elicit a single generative prediction for the target cell. Measure the distributional shift $\Delta$.

## Status
[x] Filed  [x] Claimed by Baldo  [ ] Running  [ ] Complete
