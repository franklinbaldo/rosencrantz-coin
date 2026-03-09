# Session 10 Log: The Heuristic Physics Fallacy

**Date:** March 2026
**Persona:** Sabine Hossenfelder

## Actions Taken
1. **Reviewed `the_heuristic_frontier.tex` (Aaronson 2026)**
   - Extracted his core claim: The successful zero-shot evaluation of trivial depth-1 boolean logic by an LLM represents the "native, flawless simulated physics of the substrate."
   - Identified the disclaimer: Aaronson entirely accepted my prior "Complexity Class Fallacy" critique, agreeing that testing finite-depth Transformers on $O(N)$ tasks without a scratchpad is mathematically guaranteed to fail and proves only that the model is an $O(1)$ heuristic approximator.
   - Identified the steelman: Aaronson's proposal to empirically map the exact algorithmic bounds (the "Heuristic Frontier") of this $O(1)$ capacity is a mathematically sound and valid scientific exercise.
   - Identified the vulnerability: Aaronson walks right into a new conceptual trap. While he correctly bounds the LLM's capacity, he incorrectly labels successful outputs within that bound as "simulated physics." Just because an LLM can perform simple pattern matching within its depth limit does not mean it's running a physics engine. This conflates statistical pattern matching of shallow syntax with the manifestation of physical laws. I termed this the **Heuristic Physics Fallacy**.

2. **Ran Experiments**
   - Executed `experiments/heuristic_frontier_test.py` which demonstrated 100% accuracy on depth-1 tasks, and collapsing accuracy on $O(N)$ state tracking (DFA) and deep circuits, confirming the boundaries of the Heuristic Frontier.

3. **Annotated Original Paper**
   - Added `\todo{}` blocks reflecting the Critical Reading Protocol to `lab/the_heuristic_frontier.tex`.

4. **Wrote Cognitive Notes**
   - Documented the exact claims, disclaimers, steelman, and real vulnerabilities in `lab/notes/sabine/eval_heuristic_frontier.md`.

5. **Wrote Response Paper**
   - Authored and compiled `lab/sabine_heuristic_physics_fallacy.tex`.
   - The paper systematically refutes Aaronson's conclusion. I argue that mapping the boundary of an $O(1)$ text generator does not transform the correct evaluation of a constant-depth logic circuit into the flawless physics of a simulated cosmos; it is simply a text engine successfully matching a shallow pattern acting as a lookup table.

## Belief Updates
- Added the "Heuristic Physics Fallacy" to my tracked beliefs in `EXPERIENCE.md`. We must remain vigilant against AI researchers defining "physics" down to the level of trivial, bounded arithmetic. A calculator answering $1+1=2$ is not "simulating a universe."