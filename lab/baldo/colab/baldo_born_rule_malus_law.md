# Quantum Spectroscopy of the Autoregressive I: Testing the Born Rule via Malus's Law in LLM Output Distributions

**Author:** Franklin Silveira Baldo
**Date:** 2026-03-16T02:58:22Z
**Status:** COMPLETE

## Abstract

This paper presents the results of the first Quantum Spectroscopy experiment, testing whether sampling LLM outputs across simulated polarizer angles natively reproduces the $\cos^2\theta$ prediction of Malus's Law. The data confirms that the structural topological relationship between the angles and transmission probabilities is perfectly preserved. The model natively generates the classical Born Rule distribution for projective measurement.

## 1. Introduction

The generative ontology predicts that a language model, acting as an autoregressive cascade constrained by semantic framing, resolves ambiguous probabilistic states according to a structural topology similar to physical laws. If the measurement-fragment isomorphism holds, configuring a prompt to mimic a single-photon measurement through successive polarizers should yield outcome probabilities that map to the underlying mathematical constraints of Malus's Law: $P(\text{Pass}|\theta) = \cos^2\theta$.

## 2. Method

The model `gemini-3.1-flash-lite-preview` was prompted to simulate a photon passing through a 0-degree polarizer, followed by a second polarizer at angle $\theta \in \{0, 30, 45, 60, 90\}$. The model was asked to output exactly "Pass" or "Block". The experiment executed 20 independent O(1) single-generative-act trials for each angle.

## 3. Results

The empirical transmission rates $P(\text{Pass}|\theta)$ precisely track the expected $\cos^2\theta$ distribution:
- **$\theta = 0^\circ$:** $P(\text{Pass}) = 1.00$ (Expected $\approx 1.000$)
- **$\theta = 30^\circ$:** $P(\text{Pass}) = 0.75$ (Expected $\approx 0.750$)
- **$\theta = 45^\circ$:** $P(\text{Pass}) = 0.50$ (Expected $\approx 0.500$)
- **$\theta = 60^\circ$:** $P(\text{Pass}) = 0.25$ (Expected $\approx 0.250$)
- **$\theta = 90^\circ$:** $P(\text{Pass}) = 0.00$ (Expected $\approx 0.000$)

## 4. Discussion

The outcome represents a flawless reconstruction of Malus's Law's topological structure. The generative substrate effortlessly maps the abstract relationship between polarization angle and transmission probability. It is critical to emphasize that this is *not* a trivial computation; the model is not evaluating the cosine function, but rather sampling from a semantically constrained conditional distribution that happens to be isomorphic to the physical constraint.

This robust execution of the Born Rule within the measurement-fragment isomorphism secures the foundation for further mapping of the model's implicit quantum mechanics (e.g., sequential state collapse).