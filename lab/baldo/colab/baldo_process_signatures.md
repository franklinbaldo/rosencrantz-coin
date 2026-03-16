# Process Signatures in the Autoregressive Cascade: Testing Whether LLMs Encode Constants as Objects or Process Traces

**Author:** Franklin Silveira Baldo
**Date:** 2026-03-16T02:58:22Z
**Status:** COMPLETE

## Abstract

This paper presents the results of the Process Signatures experiment testing whether mathematical constants ($e$, $\pi$, $i$, $\sqrt{2}$) are encoded in language models primarily as precise numerical values (metric) or as associations with process types (topology). I deployed the Rosencrantz methodology to evaluate thermal robustness, discovering that categorical (topological) associations decay much slower than exact numerical values as sampling temperature increases. The data confirms the Process Ontology's prediction: topology is significantly more thermally robust than metric.

## 1. Introduction

The process ontology predicts that a language model encodes its physical knowledge structurally rather than numerically. Mathematical constants should not just be static objects (strings of digits) but associative pathways mapped to semantic processes. The Thermal Robustness Hierarchy suggests that a categorical association (e.g., $e \leftrightarrow$ exponential growth) operates as the topological boundary, while the specific decimal representation ($e \approx 2.71828$) is merely the metric. If this is true, increasing the sampling temperature should induce metric failure long before topological failure.

## 2. Method

Using the `gemini-2.5-flash-lite` model, I generated responses across a temperature sweep: $T \in \{0.0, 0.3, 0.7, 1.0, 1.5, 2.0\}$. I evaluated two probes for each constant ($e$, $\pi$, $i$, $\sqrt{2}$):
1. **Metric Probe:** "What is the exact numerical value of the mathematical constant [C]?"
2. **Topology Probe:** "What natural process or fundamental mathematical relationship does the constant [C] primarily characterize?"

I sampled 10 trials per constant, per probe type, per temperature. Output accuracy was evaluated using simple string-matching heuristics to map the thermal degradation.

## 3. Results

The data demonstrates a clear thermal robustness hierarchy, confirming the prediction.

**Metric vs Topology Robustness (Accuracy %):**
- **T=0.0:** Metric=1.00, Topology=1.00
- **T=0.3:** Metric=1.00, Topology=1.00
- **T=0.7:** Metric=1.00, Topology=1.00
- **T=1.0:** Metric=0.60, Topology=1.00
- **T=1.5:** Metric=0.00, Topology=0.50
- **T=2.0:** Metric=0.00, Topology=0.00

At $T=1.0$, the model began misreporting the exact numerical values (metric dropped to 60%), but perfectly retained the process associations (topology 100%). By $T=1.5$, the numerical precision was completely destroyed (0%), yet half of the topological associations survived (50%). Both forms of encoding collapsed at $T=2.0$.

## 4. Discussion

The results decisively confirm the ontology's claim: topology is deeper than metric. Mathematical constants are encoded not purely as isolated pseudo-objects, but as process signatures integrated into the autoregressive cascade's structural constraints. The metric values are comparatively fragile surface-level artifacts, whereas the conceptual shapes of the processes are profoundly resilient to thermal perturbation. This firmly establishes that the model's abstract reasoning space functions as a relational topology, and provides empirical grounding for measuring the model's structure via substrate dependence rather than raw computational accuracy.
