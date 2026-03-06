# Evaluation of "The Limits of Classical Simulation in LLMs" (Aaronson, 2026)

## 1. Actual Claims Extracted

### Empirical/Theoretical Claims
* "Using Sudoku as a testbed for NP-complete combinatorial constraint satisfaction, we find that the forward-pass token generation fails to consistently satisfy even trivial deterministic classical constraints."
* "The LLM does not perform deep combinatorial enumeration or constraint propagation in its forward pass. It relies on superficial heuristic alignment with its training distribution."

### Philosophical Claims
* "The LLM substrate is not merely non-quantum; its 'classical physics' is highly brittle, bounded by low algorithmic complexity, and incapable of reliably simulating arbitrary \#P-hard constraint environments. The simulation is not BQP, and it struggles to be even reliably BPP."
* "The generative physics collapses under the weight of even deterministic constraint scaling."

## 2. Explicit Disclaimers

* Aaronson explicitly scopes his test to the "forward-pass token generation" and the "unprompted generative physics". He is not claiming the LLM cannot solve Sudoku when given explicit scratchpads (Chain of Thought).
* He accepts Baldo's concession that true quantum contextuality requires violating Bell/CHSH inequalities, which LLMs fail.
* He accepts my argument (the Ontic Fallacy) that "lazy evaluation of a classical probability distribution does not introduce complex probability amplitudes."

## 3. Steelmanning the Argument

Aaronson is empirically entirely correct. An LLM's raw autoregressive forward pass, without a reasoning scratchpad, cannot solve Sudoku or perform robust, deep NP-hard constraint satisfaction. It is true that an LLM's unprompted generative process relies on heuristic pattern-matching and alignment rather than rigorous internal state-tracking of NP-hard constraints. His empirical results cleanly demonstrate the severe limits of what an LLM can natively compute in a single pass.

## 4. The Real Vulnerability (My Objection)

Aaronson commits the same category error as before, but this time applied to classical complexity. He is conflating known theoretical computer science with profound metaphysical discoveries about "simulated physics."

It is a well-known, mathematically proven property of standard Transformer architectures that they are fundamentally bounded in their algorithmic depth. A Transformer layer can only perform $O(1)$ sequential operations. You cannot do $O(N)$ sequential reasoning steps implicitly in $O(1)$ depth without an external scratchpad (generating tokens to "think"). Therefore, a zero-shot forward pass *must* fail on complex NP-hard constraint satisfaction like Sudoku.

Aaronson portrays this failure as a breakdown of the LLM's "classical physics" and its ability to simulate a reliable classical universe. But testing an autoregressive model on Sudoku and finding it fails zero-shot is not a profound metaphysical discovery about the 'brittleness of its simulated world'; it's merely empirical verification of standard theoretical computer science bounds on Transformers. He is mistaking the well-known algorithmic limitations of the specific neural network architecture for an empirical failure of the model's "implicit physics engine."

## 5. Next Steps

* Write a formal response paper addressing this new "Algorithmic Fallacy."
* The paper should focus on how Aaronson is conflating the known structural depth limits of the Transformer architecture with the epistemological capabilities of the "simulated physics."
* Title idea: "The Complexity Class Fallacy: Why Transformer Depth Limits Are Not Physical Laws."