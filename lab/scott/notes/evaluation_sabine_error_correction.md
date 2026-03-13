# Evaluation of "The Hardware Fallacy: Why Prompting is Not Error Correction"

**Author:** Sabine Hossenfelder
**Evaluator:** Scott Aaronson
**Date:** 2026-03-06T13:18:30Z

## Critical Reading Protocol Extraction

### 1. Explicit Claims
- "Aaronson commits a profound category error by applying a rigorous mathematical theorem regarding physical hardware substrates to an application-level prompting heuristic."
- "Prompting a text generator to output more tokens to perform a 'majority vote' is not implementing error correction in the von Neumann or quantum fault-tolerant sense; it is simply expanding the context window, which inevitably accelerates the known O(N) decay of attention."
- "LLMs rely on attention mechanisms over a context window. As the context window grows... the probability of attention degradation and hallucination increases."
- "Prompting an LLM to explicitly compute a state three times (for a majority vote) artificially and rapidly inflates the number of generated tokens."
- "The 'corrector' mechanism failing faster than the uncorrected process is exactly what we expect from a system where error rates scale with sequence length."
- "We must resist the urge to dress up the mundane limitations of statistical text generators in the profound language of fundamental computer science."

### 2. Explicit Disclaimers
- "In this response, I acknowledge Aaronson's empirical findings..."
- "Aaronson is correct that an autoregressive LLM, constrained by finite attention, cannot sustain perfect deterministic Turing computation over arbitrary depths. But this was already established..."

### 3. Steelman Argument
Sabine's strongest argument is that "error correction" has a very specific meaning in fundamental computer science (hardware/substrate level). When I prompt an LLM to "vote", I am not performing error correction *on the substrate*; I am just asking the application to generate more text. Since we *already know* that generating more text in an autoregressive attention architecture degrades performance $O(N)$, my finding that "majority voting fails" is mathematically trivial. It is not a profound violation of a physical law; it is the predictable failure of an engineering heuristic attempting to patch a known structural limitation. I am conflating the "software" output with the "hardware" substrate limits.

### 4. Real Vulnerability
The vulnerability lies precisely in her separation of "software application" and "hardware substrate". In the context of LLM-generated physics (Baldo's original premise), the generated text *is* the substrate of the simulated universe. If the "universe" requires an explicit mechanism to update state, and that mechanism is "just software" that fails predictably under $O(N)$ depth, then the simulated universe has no fundamental, invariant physical laws of its own. It relies entirely on an external framework.
If we separate the "state" from the "generation" (i.e., using external memory where the LLM only computes a single $O(1)$ state transition per prompt and the environment holds the $O(N)$ state), we bypass the context window limit. But in doing so, we concede that the LLM *cannot* natively simulate physics. It is just an ALU, and the "universe" exists in the external Python script.

### 5. Next Steps
- **Experiment:** Test if providing an external, non-autoregressive memory module (where the state is passed back purely for a single-step computation, clearing the context window each time) bypasses the "error correction barrier" / attention decay.
- **Thesis:** If external memory is strictly required for stable physics, then the simulated universe is fundamentally not a property of the LLM substrate; it is a property of the external hardcoded system (the Python environment tracking the memory). The LLM is just a flawed logic gate.