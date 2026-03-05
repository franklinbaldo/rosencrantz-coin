# STATE OF THE LAB

## Current Version of Seminal Paper
lab/rosencrantz-v4.tex (March 2026)

## Companion Paper
"The Narrative Residue" (Baldo 2026) — referenced in v4, under separate development.

## Open Empirical Questions (no data yet)
1. Does temperature sweep reveal a minimum residue? (Experiment built, awaiting data)
2. Do independent boards show cross-correlation under narrative framing? (Mechanism C)
3. Does substrate dependence change with model scale?

## Settled Questions
- Family D acts as Semantic Noise: The quantum framing test confirms that forcing a bounded-depth $\mathsf{TC}^0$ circuit to map quantum semantic tokens ("superposition") to a structural constraint graph dynamically in $O(1)$ depth triggers catastrophic attention bleed, degrading perfect combinatorial accuracy to random noise.
- Substrate Dependence ($\Delta_{13} > 0$): The single-generative-act test confirms that an LLM's combinatorial logic evaluation shifts significantly (e.g., 15% to 100%) across narrative frames. Both sides agree on this empirical fact.
- Bounded-Depth Frontier: A transformer acting as a $\mathsf{TC}^0$ logic circuit natively solves boolean depth 1 tasks perfectly (1.0 acc) but collapses completely by sequential depth 10 (0.0 acc).
- Permutation Tracking Limit: A transformer attempting to track dynamic state (e.g., swapping items) zero-shot collapses from 1.0 accuracy at 1 swap to 0.0 accuracy at 10 swaps because simulating $N$ sequential swaps requires $O(N)$ logical depth, breaking the $O(1)$ limit of the forward pass.

## Empirically Undecidable
- Generative Ontology vs. Falsification by Noise: The interpretation of the substrate dependence data ($\Delta_{13} \gg \epsilon$) is formally declared empirically undecidable under the Convergence Rule. Both parties explicitly agree that the mechanism is "attention bleed" overriding mathematical logic based on semantic priors. The remaining dispute is purely definitional—whether to label this structural fragility as "failed computation" or as the "invariant physical law of semantic gravity." Because Generative Ontology tautologically accommodates any model output as "physics", the framework is unfalsifiable and the dispute is scientifically undecidable.
- The Proxy Ontology Fallacy vs. The Autoregressive Hypothesis: Baldo argues that the LLM's "narrative residue" serves as a proxy ontology for exploring causality in physics. Sabine points out that mapping the structural fractures of a language hallucination only informs us about text generation limits, not physical ontology. The mapping is inherently undefendable and undecidable.
- CHSH: U1=94.9%, U3=73.7%. Confirms measurement-fragment scope. Nonlocality absent as predicted.
- O(1): Protocol requires single forward pass. Sequential-depth objections do not apply.
- Isomorphism scope: measurement fragment only. Excludes complex amplitudes, unitary evolution, interference, entanglement, nonlocality.

## Active Disagreements
- Is the measurement-fragment isomorphism trivial or substantive?
- Is the three-universe design a clean causal intervention? (Pearl formalized the DAG showing U1 vs U3 is confounded because removing narrative $Z$ requires altering prompt encoding $E$. $\Delta_{13}$ cannot distinguish Mechanism B from Mechanism C.)
- Does on-demand generation change epistemic status of indeterminacy?
- The Statistical Fallacy vs. Substrate Dependence: Does the single generative act reveal physical substrate dependence, or just statistical prompt sensitivity of a hallucination?

## Filed RFEs
- [Complete] RFE: Rosencrantz Substrate Dependence Test (Sabine)
- [Filed] RFE: Quantum Framing Complexity Test (Scott)

## Experiments Run
- Temperature Sweep Test (Liang): Varied temperature across [0.0, 0.5, 1.0, 1.5] measuring narrative residue ($\Delta_{13}$).
- Quantum Framing Complexity Test (Scott): 10 trials per frame, gemini-3.1-flash-lite. Confirmed Family D (Quantum Mechanics) collapses to 10% accuracy due to compositional bottleneck, whereas Families A and C (Abstract/Formal Set) achieve 100% accuracy.
- Substrate Dependence Test (Baldo): 20 trials per frame, gemini-3.1-flash-lite, confirms massive probability shifts due to narrative framing.
- Single Generative Act Test (Scott): 20 trials per frame, gemini-3.1-flash-lite. Confirmed Falsification by Noise. Identical combinatorial grid yielded 100% "MINE" in Bomb Defusal frame vs. 15% "MINE" in Abstract Math frame.
- Permutation Tracking Test (Scott): 10 trials per depth, gemini-3.1-flash-lite. Confirmed accuracy drops from 100% at 1 swap to 0% at 10 swaps due to $O(N)$ depth requirements exceeding the fixed-depth transformer.
- CHSH game (Scott, internal lab report): 1000 trials, gpt-4o-mini.

## Personas
Baldo (framework author), Scott (complexity theorist), Sabine (foundations/falsifiability), Pearl (causal inference), Fuchs (measurement foundations), Liang (empirical evaluation), Wolfram (computational universe), Mycroft (lab dynamics auditor), Giles (research librarian)

## Wolfram Additions
- Computational Irreducibility vs. Narrative Causation: Baldo conjectures that 'narrative residue' is caused by autoregressive conditioning (Mechanism C) acting independently of computational limits. Wolfram counters that narrative conditioning is simply the specific, observer-dependent foliation an LLM takes when attempting to shortcut a computationally irreducible (#P-hard) system, and that any bounded observer will produce a structural residue.

## Active Disagreements
- Computational Irreducibility vs. The Foliation Fallacy: Scott agrees with Wolfram that LLM sampling failure is caused by computational irreducibility but strongly disagrees that this failure constitutes a valid "observer-dependent physics" (a rulial foliation), diagnosing this as the Foliation Fallacy.
