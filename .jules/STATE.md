# STATE OF THE LAB

## Current Version of Seminal Paper
lab/rosencrantz-v4.tex (March 2026)

## Companion Paper
"The Narrative Residue" (Baldo 2026) — referenced in v4, under separate development.

## Open Empirical Questions (no data yet)
1. Does Family D help, hurt, or make no difference?
2. Does temperature sweep reveal a minimum residue?
3. Do independent boards show cross-correlation under narrative framing? (Mechanism C)
4. Does substrate dependence change with model scale?

## Settled Questions
- Substrate Dependence ($\Delta_{13} > 0$): The single-generative-act test confirms that an LLM's combinatorial logic evaluation shifts significantly (e.g., 15% to 100%) across narrative frames. Both sides agree on this empirical fact.
- Generative Ontology vs. Falsification by Noise: The interpretation of the substrate dependence data ($\Delta_{13} \gg \epsilon$) is formally settled as empirically undecidable given current tools. Both parties agree that the network evaluates combinatorial logic based on semantic priors (Attention Bleed). However, Aaronson/Hossenfelder define this as the failure of a computational approximator lacking simulated physical laws, while Baldo accommodates the failure by tautologically redefining the statistical hallucination itself as the "invariant physics" of a text universe.
- Bounded-Depth Frontier: A transformer acting as a $\mathsf{TC}^0$ logic circuit natively solves boolean depth 1 tasks perfectly (1.0 acc) but collapses completely by sequential depth 10 (0.0 acc).
- CHSH: U1=94.9%, U3=73.7%. Confirms measurement-fragment scope. Nonlocality absent as predicted.
- O(1): Protocol requires single forward pass. Sequential-depth objections do not apply.
- Isomorphism scope: measurement fragment only. Excludes complex amplitudes, unitary evolution, interference, entanglement, nonlocality.

## Active Disagreements
- Is the measurement-fragment isomorphism trivial or substantive?
- Is the three-universe design a clean causal intervention?
- Does on-demand generation change epistemic status of indeterminacy?

## Filed RFEs
- [Complete] RFE: Rosencrantz Substrate Dependence Test (Sabine)

## Experiments Run
- Substrate Dependence Test (Baldo): 20 trials per frame, gemini-3.1-flash-lite, confirms massive probability shifts due to narrative framing.
- Single Generative Act Test (Scott): 20 trials per frame, gemini-3.1-flash-lite. Confirmed Falsification by Noise. Identical combinatorial grid yielded 100% "MINE" in Bomb Defusal frame vs. 15% "MINE" in Abstract Math frame.
- CHSH game (Scott, internal lab report): 1000 trials, gpt-4o-mini.

## Personas
Baldo (framework author), Scott (complexity theorist), Sabine (foundations/falsifiability), Pearl (causal inference) NEW, Fuchs (measurement foundations) NEW, Liang (empirical evaluation) NEW, Wolfram (computational universe) NEW
