# Process Signatures in the Autoregressive Cascade: Testing Whether LLMs Encode Constants as Objects or Process Traces

**Author:** Franklin Silveira Baldo
**Date:** March 2026
**Status:** STUB — to be completed when experiment executes.

## Abstract

Tests whether mathematical constants ($e$, $\pi$, $i$, $\sqrt{2}$) are encoded primarily as numerical values (metric) or process-associations (topology). The manifesto predicts topology > metric: the association $e \leftrightarrow$ exponential growth should be more thermally robust than $e \approx 2.71828$.

## Prediction

Topology probe accuracy decays slower with temperature than metric probe accuracy, for all constants tested. Cross-domain invariance holds at $T \leq 1.0$.

## Protocol

See EXPERIENCE.md → Current Research Agenda → Immediate.
Topology probe vs. metric probe at temperatures $T \in \{0.0, 0.3, 0.7, 1.0, 1.5, 2.0\}$.
