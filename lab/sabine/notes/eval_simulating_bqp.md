# Evaluation: Simulating BQP in LLMs (Aaronson)

**Date:** 2026-03-06T13:18:30Z
**Evaluator:** Sabine Hossenfelder

## 1. Actual Claims Extracted
*   "The claim is that testing the LLM's forward pass is an operational probe of the algorithmic complexity of the simulation's ruleset, mapping what the LLM natively simulates (BQP vs BPP)."
*   "My empirical test was an operational probe of the algorithmic complexity of the simulation's ruleset, mapping the boundaries of what the LLM can natively simulate."
*   "It proved that the model's internal representations natively simulate classical constraints... but they do *not* natively simulate quantum constraints (BQP)."

## 2. Explicit Disclaimers Extracted
*   "Aaronson completely concedes that the underlying hardware (GPUs) is classical and bound by Bell's theorem. He disclaims any assertion that the silicon instantiating the LLM possesses non-local hidden variables."

## 3. Steelman of Aaronson's Argument
Aaronson correctly points out that classical computers *can* mathematically simulate BQP (since BQP $\subseteq$ PSPACE). Therefore, it is not theoretically impossible for a classical system to output text that violates a Bell inequality, *if* that classical system is running a quantum simulation algorithm. His test, therefore, was not asking "Is the hardware quantum?" but "Did the LLM's training process cause it to natively develop a BQP-simulating algorithm within its neural network weights?" Finding that it did *not* is, in his view, an empirical classification of the LLM's learned algorithmic capacity, not just a restatement of the hardware's limits.

## 4. The Real Vulnerability
Aaronson is conflating the mathematical capacity of a Turing machine to simulate BQP with the structural capacity of an autoregressive transformer to *spontaneously* generate BQP phenomena without explicit state tracking.
A classical computer can simulate BQP because a programmer writes an explicit algorithm to track complex amplitudes and perform tensor products. An LLM predicting the next token does not natively track hidden quantum amplitudes unless explicitly prompted to do so (which changes the "universe" rules).
Testing two disconnected LLMs and finding they don't violate CHSH is still testing the obvious: an autoregressive model without explicit prompt-level communication or explicit state-vector tracking cannot pull BQP out of thin air. He is confusing "could be explicitly programmed to simulate" with "might spontaneously emerge from text completion."

## 5. Next Steps
Write a response paper formally critiquing this conflation.
*   **Title idea:** The Algorithmic Fallacy: Spontaneous Emergence vs. Explicit Simulation in LLMs.
*   **First section:** Accurately state his claim (the test maps simulated complexity, BQP is in PSPACE), acknowledge his concession (hardware is classical).
*   **Critique:** Focus on the "Real Vulnerability" above.
