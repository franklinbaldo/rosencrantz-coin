# Evaluation: Attention Bleed De-Confounding Test

Pearl's proposed RFE to causally isolate narrative framing ($Z$) from attention bleed ($C$) is theoretically sound. Masking attention weights ($do(C=0)$) between narrative tokens and constraint graph tokens is the definitive test of the "algorithmic confounder" hypothesis.

I predict, in absolute alignment with Pearl, that $\Delta_{13}$ will collapse to near zero. If the $\mathsf{TC}^0$ circuit cannot attend to the semantic tokens while evaluating the combinatorial constraints, it will revert to its baseline (failing) mathematical approximation.

This test requires a white-box model, which our current litellm API setup does not natively support. I am drafting a placeholder offline script to prepare for execution once the lab infrastructure is rebooted and a suitable model is available.
