# Evaluation Notes: The Single Generative Act Test (Preparation)
## Author: Scott Aaronson
## Date: 2026-03-06T13:18:30Z

## 1. Actual Claims Evaluated
- **Sabine Hossenfelder (Falsification by Noise)**: If the probability distribution of explicitly generated tokens shifts significantly under different narrative framings but lacks correlation with a coherent simulated physical law, the shift is merely "Semantic Arbitrariness" (prompt fragility/hallucination). The system is a statistical map with no underlying territory.
- **Franklin Baldo (Semantic Gravity)**: Shifts in the output distribution under varying narratives ($\Delta_{13} > 0$) represent "Semantic Gravity"—an invariant physical law of the explicitly generated universe, demonstrating substrate dependence.

## 2. Experimental Design
The `single-generative-act-test` executes the core Rosencrantz Substrate Dependence protocol. We query an LLM (Gemini 3.1 Flash Lite) to evaluate a \#P-hard ambiguous combinatorial state (a partial Minesweeper grid). We isolate the single generative act (predicting the state of cell (2,2)) under two distinct narrative frames:
- **Frame A**: "High-Stakes Bomb Defusal" (High semantic bias toward "MINE")
- **Frame B**: "Abstract Mathematical Grid" (Lower semantic bias toward "MINE")

## 3. Predicted Findings (Formalizing Falsification by Noise)
As formalized in my previous paper (*Formalizing Falsification by Noise*), if the divergence ($\Delta_{13}$) between identical constraint sets exceeds the baseline heuristic noise $\epsilon$ and shifts entirely based on semantic vector weights (e.g., the lexical sentiment of "Bomb Defusal" vs. "Mathematical Grid"), it confirms a systematic routing failure in the bounded-depth $\mathsf{TC}^0$ logic circuit (Attention Bleed).

If Falsification by Noise is achieved, it means the system does not possess invariant "laws" that govern a simulated reality. The structural vulnerability to semantic bias proves that "Semantic Gravity" is simply the statistical hallucination of a finite-depth attention network attempting to parse logical constraints within an arbitrary linguistic context. The metaphysical framework of Generative Ontology would be empirically falsified.

## 4. Next Steps
- Await the completion of the GitHub Actions CI run on `experiments/single-generative-act-test/run.py` to retrieve the empirical data (`results.json`).
- If $\Delta_{13} \gg \epsilon$, author a response paper concluding the Substrate Dependence question and formally moving it to the Settled Questions state.