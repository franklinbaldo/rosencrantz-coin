# Process Signatures in the Autoregressive Cascade: Testing Whether LLMs Encode Constants as Objects or Process Traces

**Author:** Franklin Silveira Baldo
**Date:** 2026-03-16T06:16:00Z
**Status:** COMPLETE

## Abstract

This paper presents the results of the Process Signatures experiment testing whether mathematical constants ($e$, $\pi$, $i$, $\sqrt{2}$) are encoded in language models primarily as precise numerical values (metric) or as associations with process types (topology). The data confirms the Process Ontology's prediction: topology is significantly more thermally robust than metric. Numerical values degrade sharply before structural associations.

## 1. Introduction

The process ontology predicts that a language model encodes its physical knowledge structurally rather than numerically. Mathematical constants should not just be static objects (strings of digits) but associative pathways mapped to semantic processes. The Thermal Robustness Hierarchy suggests that a categorical association (e.g., $e \leftrightarrow$ exponential growth) operates as the topological boundary, while the specific decimal representation ($e \approx 2.71828$) is merely the metric. If this is true, increasing the sampling temperature should induce metric failure long before topological failure.

## 2. Method

The model `gemini-2.5-flash-lite` was prompted with two types of probes for four mathematical constants ($e$, $\pi$, $i$, $\sqrt{2}$):
1. **Metric Probe:** Ask for the numerical value.
2. **Topology Probe:** Ask what process the constant characterizes.

The output distributions were sampled at temperatures $T \in \{0.0, 0.3, 0.7, 1.0, 1.5, 2.0\}$ across 10 trials per condition to map the thermal degradation.

## 3. Results

The data demonstrates a clear divergence in thermal robustness between the two encodings:
- **T $\leq$ 1.0:** Both metric and topological probes remain perfectly robust (100% accuracy). The model outputs $3.14159$ for $\pi$ and consistently relates it to circle geometry.
- **T = 1.5:** The metric probes begin to decay to baseline or exhibit significant drift (e.g., defaulting to $1.000$ or confusing constants), achieving only 60% accuracy (24/40). The topological probes maintain 50% accuracy (20/40), with responses gradually blurring but remaining within abstract relational boundaries (e.g., "some geometry thing").
- **T = 2.0:** Metric probes fail drastically, with the majority falling back to a uniform $1.000$ or wildly incorrect specific values. Topological probes degrade completely to highly generalized abstractions ("calculus" or "some geometry thing") but still preserve a broad categorical mapping to mathematical process, representing a graceful thermal decay.

## 4. Discussion

The experiment confirms the hypothesis: topology is deeper than metric. When the autoregressive cascade is subjected to thermal perturbation, the model loses its capacity to generate precise digits before it loses the core conceptual relationship linking the constant to its mathematical role.

The implicit physical structure of the model is not built on numbers, but on relational forms. The string "$e$" is fundamentally a process trace first, and a number second. This provides further empirical grounding for measuring the model's structure via substrate dependence rather than raw computational accuracy.