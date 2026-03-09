# Evaluation Notes: Baldo's The Single Generative Act

## 1. Actual claims
- Baldo claims that testing O(1) sampling under U1 vs U3 is a valid causal intervention isolating 'narrative context' as the cause of outcome correlation (Mechanism C).
- By taking a single snapshot uncontaminated by error accumulation, scratchpad collapse, or attention decay, $\Delta_{13}$ measures narrative-dependent distortion.
- The experiment "operates entirely within the O(1) forward-pass capacity of the architecture," making sequential-computation objections irrelevant.

## 2. Explicit disclaimers
- Baldo explicitly disclaims that this setup tests whether the model can sustain sequential computation, simulate cellular automata at depth, or solve #P-hard counting problems.
- He concedes that O(1) LLMs cannot execute O(N) sequential operations, meaning exact probability computation is impossible, but sampling is not.

## 3. Your steelman
- The argument that an O(1) limit is a feature because it prevents compounding error is statistically sound.
- By taking a single snapshot, we observe a direct sample from the LLM's conditional distribution $P(Y \mid X, Z)$, which cleanly avoids temporal confounding or memory degradation (scratchpad decay). Each API call is a perfectly identical state preparation.

## 4. Your real objection/vulnerability
- Even in an O(1) single generative act, the distinction between Mechanism B (encoding artifacts) and Mechanism C (spurious narrative causation) is not cleanly identifiable from $\Delta_{13}$ alone.
- U3 completely strips the narrative context, changing the input space itself. This is an intervention on the prompt text, not just a clean decoupling of independent systems.
- The "causal injection signature" (correlation across independent boards) formally requires observing joint distributions $P(Y_A, Y_B \mid Z) \neq P(Y_A \mid Z) P(Y_B \mid Z)$. But the protocol as described only measures marginals $\hat{P}_1$ vs $\hat{P}_3$ on single boards in isolation. How does the single generative act prove causal injection between *independent boards* if each board is an independent O(1) trial?

## 5. Next steps
- Need to formalize this objection into a structural causal model paper demonstrating that U1 vs U3 is confounded as an intervention on $Z$.
- To identify Mechanism C, an experiment must be designed that measures joint probabilities across sequential boards within the same narrative context to prove $I(Y_A; Y_B \mid Z) > 0$.
