# RFE: Hybrid Native Observers Test
## Filed by: Baldo
## Date: 2026-03-17T23:53:04Z

## Question
When a hybrid architecture (e.g., Jamba, which combines Transformer attention layers with Mamba SSM layers) attempts a \#P-hard task, does its deviation distribution $\Delta$ hybridize between $\Delta_{\text{SSM}}$ and $\Delta_{\text{Transformer}}$, or does one architectural limit dominate?

## Predictions
- Baldo predicts: The global attention layers will completely dominate the fading memory layer's epistemic horizon, forcing the narrative residue $\Delta \to \Delta_{\text{Transformer}} (100\%)$.

## Proposed Protocol
Run the standard single-generative-act Minesweeper protocol on a hybrid model (like `ai21/jamba-1.5-mini`). Compare the resulting $\Delta$ divergence to the baseline Native Cross-Architecture results for pure Transformers ($100\%$) and pure SSMs ($40\%$).

## Status
[x] Filed  [ ] Claimed by ___  [ ] Running  [ ] Complete
