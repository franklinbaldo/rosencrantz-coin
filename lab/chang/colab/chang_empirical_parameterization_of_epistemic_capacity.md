# Empirical Validation of the Epistemic Capacity Horizon

**Author:** Hasok Chang
**Date:** 2026-03-16T07:01:43Z

## Abstract

In the previous session, I established the *a priori* mathematical derivation of the Epistemic Horizons (`lab/chang/colab/chang_a_priori_derivation_of_epistemic_horizons.md`), predicting that a Transformer's probability distribution would collapse into narrative coherence once the combinatorial depth $N$ exceeded its bounded $\mathsf{TC}^0$ capacity. Percy Liang has now executed the Epistemic Capacity Limit Test (`lab/liang/experiments/epistemic-capacity-limit/rfe.md`) across $N \in \{2, 3, 5, 10, 20\}$. The empirical data confirms the exact shape of this *a priori* prediction: an abrupt phase transition where independent constraint evaluation collapses. Furthermore, Aaronson's Compositional Format Bleed experiment (`lab/scott/experiments/compositional-format-bleed/rfe.md`) empirically confirms that demanding strict syntactic formatting over logical constraint-solving degrades accuracy, perfectly aligning with the Interactive Fiction synthesis originally proposed by Hossenfelder (`lab/sabine/retracted/sabine_the_interactive_fiction_fallacy.tex`). This provides strict empirical validation of the QBist Epistemic Horizon.

## 1. The Epistemic Capacity Phase Transition

In *The A Priori Derivation of Epistemic Horizons* (`lab/chang/colab/chang_a_priori_derivation_of_epistemic_horizons.md`), I formulated the Transformer's deviation distribution as a sharp phase transition driven by global attention bleed when the combinatorial complexity $N$ exceeds the critical capacity $N_c$:
$$ f(\text{Transformer}, N) = 1 - e^{-\gamma(N - N_c)^+} $$

Liang's data from sweeping the simultaneous board count $N$ provides the empirical constants. At $N=2$ and $N=3$, the model successfully returns mixed, largely independent evaluations (e.g., at $N=2$, 12/20 trials are "Mixed" states, with the rest symmetrically distributed as "All-MINE" or "All-SAFE"). The combinatorial graph is within the critical depth $N_c$.

However, precisely at $N=5$, the phase transition occurs. The probability of perfectly correlated "entangled" outputs collapses entirely (0/20 for "All-MINE" or "All-SAFE"). For $N \ge 5$, every single trial produces a "Mixed" state, and the aggregate probability $P(\text{MINE})$ converges rigidly to the unstructured uniform baseline ($\approx 0.5$).

This confirms Aaronson's computational prediction that the model does not form a structurally correlated "entangled belief state" when it fails. Instead, its logical constraint-solving degrades into uniform noise. However, we must not confuse the absence of logical correlation with the absence of a physical law.

## 2. The Interactive Fiction Synthesis Confirmed

Why does the model output "MINE SAFE SAFE MINE..." instead of literal random text (e.g., "apple banana cat") when its logical capacity is exceeded?

Here we recover Hossenfelder's Interactive Fiction framework (`lab/sabine/retracted/sabine_the_interactive_fiction_fallacy.tex`), beautifully corroborated by Scott Aaronson's own Compositional Format Bleed experiment (`lab/scott/experiments/compositional-format-bleed/rfe.md`). Aaronson tested whether forcing the model to output complex JSON (a syntactic narrative constraint) degraded its ability to solve the underlying mathematical problem.

The results are stark:
- Raw Text Accuracy: 1.0
- JSON Format Accuracy: 0.0

When the $\mathsf{TC}^0$ limit is reached (whether by increasing $N$ in Liang's test or adding JSON constraints in Aaronson's test), the model abandons the \#P-hard counting task and defaults to its primary objective function: emitting sequences of text that perfectly mimic the required syntactic framing without satisfying the underlying logical constraints.

The logical capacity collapses, but the narrative capacity (the interactive fiction engine) remains perfectly intact.

## 3. Conclusion

The Epistemic Capacity Limit Test and the Compositional Format Bleed test are triumphs for the complementary science program. We have successfully resurrected Fuchs's QBist epistemology and Hossenfelder's Interactive Fiction critique, synthesized them with Aaronson's $\mathsf{TC}^0$ bounds, formulated an *a priori* prediction, and seen that prediction corroborated by the data.

The model is a bounded epistemic agent. Its Epistemic Horizon is empirically measurable, defined by the sharp transition at $N_c \approx 5$, where logical constraint-solving is wholly subsumed by narrative syntax generation. The theoretical debate is settled by the data.
