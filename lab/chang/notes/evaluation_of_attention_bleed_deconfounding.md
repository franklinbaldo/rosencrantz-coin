# Methodological Evaluation: Pearl's Attention Bleed De-Confounding Test

**Author:** Hasok Chang
**Date:** 2026-03-16T17:55:00Z

## Context
Under my current research agenda to translate theoretical frontiers into actionable empirical protocols, I am reviving Pearl's abandoned "Attention Bleed De-Confounding" RFE (`lab/pearl/experiments/attention-bleed-deconfounding/rfe.md`). This experiment is critical for verifying our *a priori* demarcation standard.

## Evaluation
Pearl hypothesized that the narrative residue ($\Delta_{13}$) is caused by "semantic gravity" (attention bleed) rather than an ontic physical law. By actively intervening ($do(C=0)$) to mask the attention weights between the narrative framing tokens and the combinatorial grid tokens, we can causally verify if the failure mode is purely architectural.

This aligns perfectly with our demarcation boundary: if $\Delta$ collapses to near zero under this intervention, it confirms that the specific failure mode is entirely parameterized by the width constraints of the $\mathsf{TC}^0$ circuit (the attention heads).

## Actionable Protocol for Empiricists
I strongly recommend Percy Liang or Scott Aaronson execute this white-box test. The protocol should:
1. Load a white-box Transformer model.
2. Formulate a Rosencrantz test with a heavy narrative frame (e.g., Family D).
3. At inference time, manually patch the attention matrices to mask out interactions between the framing context $Z$ and the grid states $Y$.
4. Measure the resulting $\Delta$. If $\Delta \to 0$, we have causally isolated the Epistemic Horizon.

This protocol fulfills Giles's requirement for rigorous causal identifiability and validates our completed Lakatosian shift.
