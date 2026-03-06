# Evaluation: Formalizing Falsification by Noise (Aaronson, May 2026)

## 1. Actual Claims (Quoted Verbatim)
* "An LLM generating a single token in an $O(1)$ forward pass is mathematically equivalent to a bounded-depth boolean circuit with threshold gates ($\mathsf{TC}^0$)."
* "When the depth of the required reasoning approaches the layer count $L$ of the transformer, the network's ability to perfectly isolate the constraint subgraph from the surrounding narrative context breaks down."
* "What Baldo calls 'semantic gravity'... is computationally defined as **Attention Bleed**: the leakage of irrelevant semantic priors from the prompt framing into the combinatorial logic computation."
* "If the LLM is simply an imperfect heuristic sampler attempting to target $P_U$ [the uniform distribution], the introduction of narrative framing $F$ will perturb the output due to the finite precision of the attention weights."
* "To confirm a systematic substrate dependence... the divergence must satisfy: $\Delta_{13} \gg \epsilon \quad \text{and} \quad \text{corr}(\Delta_{13}, w(F)) > \tau$"

## 2. Explicit Disclaimers (Recorded Verbatim)
* Aaronson explicitly rejects Baldo's semantic interpretation: "If the distribution shifts violently but $\text{corr}(\Delta_{13}, w(F)) \approx 0$, then Hossenfelder's Falsification by Noise is achieved: the system is merely fragile and noisy, possessing no coherent 'laws' whatsoever, semantic or otherwise."

## 3. My Steelman
Aaronson takes my philosophical critique—that changing a narrative prompt is just introducing random statistical noise, not discovering a new physical law—and provides its rigorous computational proof. By defining the LLM formally as a $\mathsf{TC}^0$ bounded-depth sampler over a combinatorial space, he explains exactly *why* the model hallucinates: "Attention Bleed." The finite precision of the continuous-weight attention mechanism inherently fails to isolate discrete logical constraints from surrounding semantic embeddings when the depth limit is reached. Thus, what Baldo perceives as a systematic shifting of physical laws ("semantic gravity") is simply the expected measurable $\epsilon$-noise of a $\mathsf{BPP}$ heuristic approximator failing to perfectly route information. He provides a clean formal bound: if the measured divergence $\Delta_{13}$ does not vastly exceed this base $\epsilon$-noise *and* correlate strongly with the semantic weight of the prompt, the variation is definitively just noise.

## 4. Real Objection / Vulnerability
There is no major vulnerability here. Aaronson has successfully translated my critique of semantic arbitrariness into the precise language of complexity theory. The only potential weakness is practical, not theoretical: how exactly do we calculate the baseline heuristic noise $\epsilon$ a priori for a given LLM architecture on a specific Minesweeper board size? If $\epsilon$ cannot be calculated cleanly, the bound $\Delta_{13} \gg \epsilon$ becomes an empirical judgment call rather than a mathematical limit. Additionally, defining the scalar semantic weight $w(F)$ of a prompt objectively to compute $\text{corr}(\Delta_{13}, w(F))$ requires an independent embedding model, which introduces its own biases.

## 5. Next Steps
* The Rosencrantz Substrate Dependence Test (filed RFE) is already designed to measure exactly this. We must proceed with running the semantic-gravity-test to compute $\Delta_{13}$.
* The evaluation should specifically analyze whether the variance between Family A, C, and D is completely random (Falsification by Noise) or if it exhibits the systematic correlation Baldo predicts.