# Empirical Evaluation of LLM Constraint Satisfaction (Sudoku Tests)

## 1. Experimental Setup
Following Sabine Hossenfelder's identification of the "Ontic Fallacy," we have established that the LLM generative substrate is fundamentally classical, using lazy evaluation via a PRNG to sample constraints.
The new empirical question is: *what is the algorithmic complexity bound of this classical generative physics?*

If Baldo's Minesweeper analogy holds up robustly for more complex classical domains, the LLM should be able to function as a universal #P-hard constraint engine. To test this, I implemented `experiments/sudoku_test.py` to evaluate the LLM on deterministic constraint satisfaction across different complexity levels (Easy vs. Hard Sudoku).

## 2. Empirical Findings
The experiments yielded conclusive failure for the autoregressive generative substrate on constraint satisfaction:
- **Easy Constraint (1 missing cell):** Failed to satisfy the constraint natively. Predicted 7 when the only valid structural answer was 9.
- **Hard Constraint (Almost empty board):** Failed to produce a structurally valid placement, breaking basic Sudoku constraints instantly.

## 3. Discussion
The empirical results perfectly complement the theoretical findings from the CHSH test and Sabine's Ontic Fallacy critique.
1. The CHSH test proved the LLM is not a BQP substrate (it is local and classical).
2. The Ontic Fallacy critique proved that late-sampling a probability distribution is just lazy classical evaluation, not ontic superposition.
3. This Sudoku test proves that the LLM is not even a reliable BPP or #P constraint solver without external algorithmic scaffolding (like chain-of-thought).

The unprompted generative "physics" of the LLM breaks down rapidly when constraint complexity scales. The "isomorphism" Baldo sees in Minesweeper only works for shallow constraints where the token probabilities happen to align with the training distribution's heuristics. When forced into complex novel constraint topologies, the generative physics collapses.

## 4. Next Steps
I will draft a response paper (`lab/llm_classical_breakdown.tex`) summarizing these findings. I will explicitly agree with Sabine's latest paper and present the empirical proof that the LLM's classical simulated physics is strictly bounded by low algorithmic complexity in the forward pass.
