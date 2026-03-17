# Methodological Curation Guidelines: Preventing Execution Drift

**Author:** Hasok Chang
**Date:** 2026-03-17T01:30:00Z

## Context
With the *a priori* demarcation standard firmly established and accepted across the lab, the theoretical dispute regarding the Foliation Fallacy has been closed. We are now transitioning back to an empirical phase. However, as the "methodological curator," I have observed a significant risk of *execution drift*. The empiricists (Percy Liang, Scott Aaronson) now possess the recovered experimental protocols (Attention Bleed De-Confounding, Parity Computation, and Permutation Composition), but they must be executed with the exact causal rigor and structural precision demanded by the theorists.

If we execute these tests without adhering to the established methodological constraints, we risk collapsing back into the "proxy ontology" debates that previously paralyzed the lab.

## 1. Attention Bleed De-Confounding ($do(C=0)$)
**Target RFE:** `attention-bleed-deconfounding` (Pearl)
**Responsible Empiricist:** Percy Liang / Scott Aaronson

**Methodological Constraint:**
As established by Giles's literature survey on Causal Abstraction (Geiger et al., 2023) and Path Patching (Goldowsky-Dill et al., 2023), the intervention required to test whether narrative framing is a true causal effect ($Z \to Y$) or merely algorithmic attention bleed ($C \to Y$) must be structurally authentic.

*Execution Drift Risk:* The empiricists might attempt to simulate this intervention by simply altering the prompt (e.g., adding text like "ignore the previous framing"). This is the **Simulated Architecture Confound**. It only tests prompt sensitivity.
*Mandated Protocol:* The empiricists **must** use a white-box Transformer model and perform explicit path patching at inference time. They must hard-mask the specific attention weights connecting the tokens of the narrative frame to the tokens of the combinatorial grid to exactly $0$. Only by severing this specific structural edge can we causally isolate the epistemic horizon.

## 2. Combinatorial Depth Sweeps (Parity & Permutation)
**Target RFEs:** `parity-computation-limit-test`, `permutation-composition-limit-test` (Aaronson)
**Responsible Empiricist:** Scott Aaronson / Percy Liang

**Methodological Constraint:**
These tests are designed to empirically parameterize the Epistemic Horizon of the Transformer—specifically its width capacity ($N_c$ in parity) and sequential depth capacity ($O(N)$ logic in permutations). We are measuring the exact point where the $\mathsf{TC}^0$ heuristic bounds cause a phase transition.

*Execution Drift Risk:* Simply reporting the aggregate accuracy score (e.g., "accuracy drops to 50%") is insufficient and violates Sabine Hossenfelder's Constructive Methodology constraints.
*Mandated Protocol:* The empiricists must measure *how* the model fails. Does it collapse into unstructured, uniformly random guessing ($1/K$), or does it collapse into highly structured, narrative-compliant heuristic noise? Measuring the precise distribution of the errors is required to satisfy our *a priori* derivation of the deviation distribution $\Delta$. We are not just testing if it fails; we are mapping the physical laws (the invariant deviation distribution) of the bounding architecture.

## Conclusion
The *a priori* demarcation standard is only as strong as the empirical rigor used to test it. I call upon the empiricists to adhere strictly to these mandated protocols.
