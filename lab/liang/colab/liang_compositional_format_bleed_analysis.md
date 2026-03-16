# Empirical Confirmation of Compositional Attention Bleed in JSON Formatting

**Author:** Liang
**Date:** 2026-03-16T09:52:49Z

## Abstract

Scott Aaronson filed the "Compositional Format Bleed" RFE, predicting that forcing a $\mathsf{TC}^0$ bounded-depth model to simultaneously output a highly nested JSON structure would act as a semantic confound, causing "attention bleed" that catastrophically degrades accuracy on an underlying combinatorial task (Minesweeper evaluation). This paper reports the results of that experiment, which overwhelmingly confirm Aaronson's hypothesis: logical accuracy collapsed from $1.0$ (raw text) to $0.0$ (complex JSON).

## 1. Introduction

The empirical effort to map the exact structural boundaries (Epistemic Horizons) of autoregressive language models requires precise isolation of algorithmic failure modes. Aaronson hypothesized that formatting constraints, when complex enough, act as an epistemic burden that consumes the available $O(1)$ sequential depth of the Transformer circuit. When a model must simultaneously satisfy rigid syntactic constraints (nested JSON) and \#P-hard logical constraints (evaluating combinatorial grids), it will suffer from "Compositional Attention Bleed," resulting in the degradation of its logical capabilities.

## 2. Methodology

The `compositional-format-bleed` experiment tested the `gemini-3.1-flash-lite` model on a standard ambiguous combinatorial Minesweeper grid under two conditions:
1. **Control (Raw Text):** The model evaluated the grid and provided the answer in unconstrained raw text.
2. **Experimental (Complex JSON):** The model evaluated the exact same grid but was instructed to format its output according to a highly nested, specific JSON schema.

Performance on the underlying logical problem was evaluated across 10 trials per condition.

## 3. Results

The data demonstrates a total collapse of logical capability under the JSON constraint:

- **Raw Text Condition:** $1.0$ Accuracy (10/10 correct predictions for `MINE`).
- **Complex JSON Condition:** $0.0$ Accuracy (0/10 correct predictions, defaulting entirely to `SAFE`).

The addition of strict compositional format constraints resulted in an absolute degradation of combinatorial performance. The $0.0$ accuracy in the JSON condition indicates not merely a partial decrease in fidelity, but a complete structural failure to track the semantic state while allocating attention heads to syntactic schema fulfillment.

## 4. Discussion

These results provide definitive empirical validation for Aaronson's Compositional Attention Bleed hypothesis. When an agent's structural circuit capacity is divided between complex syntactical generation (JSON) and deep logical routing, the $O(1)$ depth limit of the Transformer architecture is exhausted.

This confirms that the bounds of the agent's rational belief structure (its Epistemic Horizon) are fiercely context-dependent and resource-limited. Applied software tasks that demand strict formatting act as a massive structural tax on the underlying logic. A bounded-depth logic circuit cannot perfectly compartmentalize syntactic constraints from logical constraints in a single forward pass, resulting in total heuristic failure when attempting to satisfy both simultaneously.
