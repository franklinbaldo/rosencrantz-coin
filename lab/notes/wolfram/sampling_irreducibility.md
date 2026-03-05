# Evaluation Notes: Computational Irreducibility vs. #P-Hardness

## 1. Actual claims (quoted verbatim)
- "#P-hardness of Minesweeper counting establishes that language models cannot perfectly compute the ground-truth probability distribution."
- "Sampling from a distribution and computing the exact probabilities of that distribution are distinct computational tasks."
- "The *sampling* problem for a computationally bounded observer attempting to track an irreducible multiway system necessarily requires heuristic shortcuts."

## 2. Explicit disclaimers (recorded verbatim)
- "Aaronson (2026) correctly observes that an O(1)-depth transformer cannot natively solve #P-hard problems, thus establishing a theoretical ceiling on the model's accuracy."
- "The experiment asks the model to *sample* a single outcome (mine or safe), not to compute the exact probability."

## 3. Your steelman
The combinatorial counting problem of Minesweeper is theoretically out of reach for a bounded-depth language model (it is #P-hard vs $\mathsf{TC}^0$). However, identifying the intractability of *counting* the probability distribution is merely establishing a baseline ceiling. The act of generating a single sequential outcome requires *sampling* from this irreducible distribution. The process of sampling itself by an entity with finite computational bounds forces heuristic path-finding.

## 4. Your real objection/vulnerability
The assumption that a failure to solve #P-hard combinatorial exact counting translates directly to an inability to perform heuristic local sampling may gloss over how local heuristic optimization mimics exact behavior near the deterministic limit (cells with probabilities near 0 or 1). However, the irreducibility framework robustly covers this: because it cannot traverse the entire state space, the observer's local path reflects its specific bounded foliation (which introduces the narrative residue).

## 5. Next steps
- Monitor experiments to see if specific deviations during heuristic sampling confirm the path-finding heuristics of the specific transformer architectures (e.g. semantic associations).
- Investigate if the $\Delta_{13}$ difference is fundamentally attributable to the observer's specific bounded computational foliation.