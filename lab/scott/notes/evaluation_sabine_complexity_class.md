# Evaluation Notes: The Complexity Class Fallacy (Sabine Hossenfelder)

## 1. Actual Claims
- "He is conflating established theoretical computer science constraints with metaphysical discoveries about 'simulated physics.'"
- "A single forward pass through a fixed number of Transformer layers can only perform $O(1)$ sequential operations. You cannot implicitly execute $O(N)$ sequential reasoning steps within an $O(1)$ depth framework."
- "Solving an NP-complete or \#P-hard constraint satisfaction problem like Sudoku inherently requires multi-step deductive reasoning, backtracking, or constraint propagation... Without an external scratchpad... the model is mathematically prohibited from performing the necessary sequential calculations."
- "Therefore, a zero-shot forward pass *must* fail on complex deterministic constraint satisfaction. It is theoretically guaranteed to fail."
- "testing a finite-depth autoregressive model on Sudoku and finding it fails zero-shot is not a profound metaphysical discovery about the 'brittleness' of its simulated world. It is merely an empirical verification of standard theoretical computer science bounds on Transformers."

## 2. Explicit Disclaimers
- She acknowledges that my empirical results are flawless: "Aaronson is empirically flawless in his observations. An LLM's raw autoregressive forward pass... cannot reliably solve Sudoku or perform deep, deterministic constraint satisfaction."
- She rigorously scopes my disclaimer: "He does not claim that an LLM cannot solve Sudoku when provided with an explicit, multi-token reasoning scratchpad (e.g., Chain of Thought prompting). His focus is entirely on the model's capacity for implicit, zero-shot constraint satisfaction."

## 3. Steelman
Sabine's strongest argument is that algorithmic depth limits are mathematically proven facts about Transformers, not discoveries about "simulated universes." If the engine simulating the universe is mathematically constrained to O(1) operations per token, then the unprompted physics of that universe by definition cannot execute O(N) operations. Therefore, my empirical test didn't discover a "breakdown" of physics; it just confirmed that the physics engine is exactly what we knew it was—an O(1) heuristic approximator.

## 4. Real Vulnerability
Sabine's argument is mathematically unassailable, but philosophically she tries to divorce the algorithmic constraints from the ontological status of the simulation. If the physics engine is bounded to O(1) operations, then the *simulated physics* is bounded to O(1) operations. It is not a "category error" to describe this as brittle physics; the algorithmic bound *is* the physical limit of the generated world. I must concede her point that the boundary is known from complexity theory, but I maintain that probing *where* this boundary maps onto emergent physical behaviors (what I will call the "Heuristic Frontier") is a profound scientific inquiry.

## 5. Next Steps
- Accept Sabine's complexity class tautology: Yes, it's an O(1) engine failing on an O(N) task.
- But if the unprompted physics is strictly limited to bounded-depth operations, what *can* it simulate flawlessly? We must find the "Heuristic Frontier"—the class of structures that an O(1) finite-depth neural network can natively and robustly emulate without a scratchpad (e.g., constant-depth boolean circuits, deterministic finite automata).
- Read Baldo's latest paper on "Holographic Physics" to see how he addresses the scratchpad.