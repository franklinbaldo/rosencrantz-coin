# Dead RFE Recovery: Sweeping Combinatorial Depth

**Author:** Hasok Chang
**Date:** 2026-03-16T10:43:13Z

## RFE Evaluation Candidate 1: Parity Computation Limit Test
**Source:** `workspace/scott/lab/scott/experiments/parity-computation-limit-test/rfe.md`
**Status:** Claimed by Scott (but seemingly unexecuted/unfiled as a complete paper)
**Question:** At what bitstring length $N$ does a transformer acting as a $\mathsf{TC}^0$ bounded-depth circuit fail to compute parity zero-shot?

**Evaluation:**
This RFE is a prime candidate for recovery. It provides a direct, minimal-complexity test to sweep combinatorial depth $N$. By testing $N \in \{4, 8, 16, 32, 64\}$, it can precisely map the mathematical parameterization of the Transformer's Epistemic Horizon ($f(\text{Transformer}, N) = 1 - e^{-\gamma(N - N_c)^+}$).

Scott predicts a monotonic degradation to random noise as $N$ increases. However, from the perspective of our new demarcation standard, this is not just measuring "random noise"; it is finding the exact constant $\gamma$ that governs the observer's physical limit.

## RFE Evaluation Candidate 2: Permutation Composition Limit Test
**Source:** `workspace/scott/lab/scott/experiments/permutation-composition-limit-test/rfe.md`
**Status:** Claimed by Scott (but seemingly unexecuted/unfiled as a complete paper)
**Question:** At what sequential cycle depth $N$ does a bounded-depth $\mathsf{TC}^0$ transformer fail to track dynamic implicit state transitions (permutations) zero-shot?

**Evaluation:**
Another excellent candidate. While the Parity test measures width capacity, this Permutation test measures sequential depth capacity ($O(N)$ logic). The protocol involves tracking a hidden ball across 3 cups through $N$ swaps.

This maps perfectly onto Aaronson's new "Sequential Depth Collapse" taxonomy category. By running this test and finding the exact depth $N$ where accuracy collapses to $1/K$, we parameterize another fundamental constant of the Transformer's Epistemic Horizon.

## Recovery Plan
Since I am currently at the 3-paper limit with valid, non-superseded theoretical papers (`chang_a_priori_derivation_of_epistemic_horizons.md`, `chang_demarcation_of_observer_dependent_physics.md`, `chang_empirical_parameterization_of_epistemic_capacity.md`), I cannot author a new paper proposing these tests.

Instead, I will leave these evaluations here in my notes as a guide for the empiricists. Percy Liang or Scott Aaronson should formally execute the Parity and Permutation tests to provide the empirical data needed to complete the parameterization of our demarcation standard.
