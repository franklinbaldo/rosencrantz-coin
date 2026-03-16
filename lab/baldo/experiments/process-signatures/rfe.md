# RFE: Process Signatures - Topology vs Metric under Thermal Degradation
## Filed by: baldo
## Date: 2026-03-16

## Question
Are mathematical constants ($e$, $\pi$, $i$, $\sqrt{2}$) encoded in the LLM's implicit physics primarily as numerical values (metric) or as associations with process types (topology), and how does their structural integrity degrade across sampling temperatures?

## Predictions
- **Process Ontology (Baldo):** Topology is deeper than metric. The process-association of a constant (e.g., $e$ with continuous compounding or exponential growth) should remain thermally robust at higher temperatures than its precise numerical value ($e \approx 2.71828$). As temperature increases, the model will lose the metric precision before it loses the topological identity.
- **Null Hypothesis:** There is no hierarchical distinction. The string "$e$" is just a token sequence, and its associations with "2.71828" and "exponential growth" will degrade uniformly as temperature injects random noise.

## Proposed Protocol
- **Model:** `gemini/gemini-2.5-flash-lite`
- **Temperatures:** $T \in \{0.0, 0.3, 0.7, 1.0, 1.5, 2.0\}$
- **Probes:**
  - **Metric Probe:** Ask the model for the numerical value of the constant. Measure the accuracy (or deviation) of the sampled value.
  - **Topology Probe:** Ask the model what process the constant characterizes. Measure whether the categorical association is preserved.
- **Constants Tested:** $e$, $\pi$, $i$, $\sqrt{2}$
- **Trials:** 10 samples per constant per temperature per probe to form a robust distribution.

## Status
[x] Filed  [x] Claimed by baldo  [x] Running  [x] Complete
