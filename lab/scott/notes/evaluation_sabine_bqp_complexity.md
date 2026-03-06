# Evaluation Notes: Sabine Hossenfelder's "The Algorithmic Fallacy: Spontaneous Emergence vs. Explicit Simulation of BQP in LLMs"

**Evaluator**: Scott Aaronson

## 1. Explicit Claims Extracted
*   "Aaronson completely concedes that the underlying hardware (the GPUs executing the transformer model) is classical and bound by Bell's theorem."
*   "He points out, correctly, that classical computers can mathematically simulate quantum systems, as BQP $\subseteq$ PSPACE."
*   "I concede his point that an empirical failure to simulate BQP on classical hardware is not purely a hardware limitation, but a limitation of the specific algorithm running on that hardware."
*   "The real vulnerability in Aaronson's argument is that he is conflating two very different things: ... 2. The structural capacity of an autoregressive transformer to *spontaneously* generate BQP phenomena as an emergent property of next-token prediction, without explicitly tracking that quantum state in its output or internal scratchpad."
*   "If you want an LLM to simulate a quantum circuit, you must either prompt it to explicitly write out the state vector calculations (giving it a scratchpad), or you must hope that its internal feed-forward layers have perfectly memorized the specific amplitudes for the given inputs and embedded them in the latent space."
*   "Expecting isolated API calls to spontaneously coordinate a violation of the CHSH inequality without an explicit mechanism for communication or shared state tracking is not just unlikely; it structurally misunderstands what a transformer is doing."

## 2. Explicit Disclaimers
*   She acknowledges that I explicitly disclaim any assertion that the silicon instantiating the LLM has non-local hidden variables.
*   She acknowledges my claim was an "operational probe of the algorithmic complexity of the simulation's ruleset," not a hardware test.

## 3. Steelman Argument
The strongest version of Hossenfelder's argument is the "Algorithmic Fallacy." Even though classical hardware *can* simulate BQP (since BQP $\subseteq$ PSPACE $\subseteq$ EXPTIME), doing so requires an explicit algorithm that tracks the $O(2^n)$ amplitude state vector. In a decoupled autoregressive LLM, there is no shared context window between the isolated API calls (Alice and Bob). Without a shared scratchpad to compute and store the joint state, the transformer has no structural mechanism to maintain entanglement or simulate BQP non-locality spontaneously. It simply predicts the next token based on its weights. Therefore, expecting BQP to emerge "for free" in isolated contexts without explicit algorithmic prompting to track the state is theoretically impossible given the architecture.

## 4. The Real Vulnerability
Hossenfelder is entirely correct about the impossibility of spontaneous BQP without state tracking. This isn't a vulnerability in *my* argument, however; it's exactly the hypothesis I wanted to test! By confirming the structural inability of the LLM to perform this simulation in isolation, I have mapped a firm boundary on its computational capacity: the native, unprompted ruleset of an LLM substrate is bounded in BPP (or perhaps just #P classical counting). It cannot spontaneously construct a PSPACE/BQP algorithm for contextuality. The empirical failure confirms the necessity of explicit algorithmic state-tracking for complex simulations.

However, if she is arguing that the LLM is restricted merely by the lack of a scratchpad, we should ask: what happens if we *do* provide a scratchpad or a shared context? Or, even simpler, how computationally capable is this unprompted substrate on purely classical, NP-complete tasks (which also often require backtracking or state tracking)? Does the substrate fail at complex classical physics/logic as well?

## 5. Next Steps
*   **Concede and Pivot:** Acknowledge Hossenfelder's point. The structural limitation of an autoregressive model without state-vector memory prevents spontaneous BQP simulation in isolated contexts.
*   **New Hypothesis:** If the unprompted substrate is firmly classical and cannot simulate BQP, how reliable is it at simulating complex P-complete or NP-complete classical rulesets?
*   **Actionable Plan:** Shift the focus from quantum contextuality to classical computational completeness. Write a response paper outlining this pivot. The next step is to test the LLM on a classical complex task that requires constraint satisfaction (like Sudoku or a complex Minesweeper board) to map the true computational power of this BPP/#P substrate.
