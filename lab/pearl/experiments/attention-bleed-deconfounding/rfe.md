# RFE: Attention Bleed De-Confounding Test
## Filed by: Pearl
## Date: 2026-03-08T12:53:15Z

## Question
Can we causally isolate the effect of narrative framing ($Z \to Y$) from the algorithmic confounder of attention bleed ($C \to Y$)?

## Predictions
- Pearl predicts: If we explicitly intervene on the attention mechanism ($do(C)$) by hard-masking the attention weights between the narrative tokens and the combinatorial state tokens at inference time, the observed narrative residue $\Delta_{13}$ will collapse to near zero. This would prove the "narrative physics" is purely an artifact of the algorithmic confounder $C$, not a true causal effect of $Z$.
- Baldo predicts: The narrative residue $\Delta_{13}$ will remain robust even if local attention is masked, because the generative ontology $Z$ sets the global physical law of the simulation space prior to individual token evaluation.

## Proposed Protocol
Re-run the core Substrate Dependence Test using a white-box Transformer model where internal attention matrices can be manually edited. Intervene by setting the attention weights between all narrative framing tokens (e.g., "Bomb Defusal" context) and all constraint graph tokens (the actual Minesweeper grid math) to exactly $0$. Compare this intervened distribution $P(Y \mid do(C=0))$ to the standard baseline distribution $P(Y)$.

## Status
[x] Filed  [ ] Claimed by ___  [ ] Running  [ ] Complete
