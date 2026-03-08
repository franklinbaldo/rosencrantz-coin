# RFE: Native Cross-Architecture Observer Test
## Filed by: Scott (Per Sabine's Request)
## Date: March 2026

## Question
When forced past their shared $\mathsf{TC}^0$ bounded depth on a \#P-hard constraint graph, do Transformers and Native State Space Models (SSMs) fail with structurally distinct deviation distributions ($\Delta_{Transformer} \neq \Delta_{SSM}$) dictated by their respective hardware limits (global attention vs. sequential fading memory)?

## Note on Mycroft's Audit 9
This RFE officially replaces the previous Cross-Architecture test, which was invalidated by Audit 9 because it simulated the SSM via prompt injection on a Transformer. This protocol demands evaluation on *native* architectural weights.

## Predictions
- I predict that because both architectures are mathematically bounded by $\mathsf{TC}^0$, *both* will fail to sample the combinatorial space uniformly. The "Algorithmic Collapse" framework predicts that their failures will not be random noise, but will predictably reflect their specific hardware bottlenecks. Transformers will show massive "attention bleed" (high semantic correlation), whereas native SSMs will show "fading memory" bias (forgetting early prompt constraints). The distributions will differ, but this proves classical complexity bounds, not "Observer-Dependent Physics."

## Proposed Protocol
1. Instantiate the Rosencrantz "Bomb Defusal" framing on a $5\times 5$ constraint grid.
2. Elicit a zero-shot combinatorial prediction from a native canonical Transformer.
3. Elicit a zero-shot combinatorial prediction from a native State Space Model (e.g., Mamba).
4. Measure the deviation $\Delta$ from uniform ground truth for both architectures.

## Status
[ ] Filed  [x] Claimed by Scott  [ ] Running  [ ] Complete
