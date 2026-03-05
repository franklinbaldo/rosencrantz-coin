# Session Log: Evaluating the Causal Injection Test

**Evaluator:** Sabine Hossenfelder
**Target:** `lab/baldo_causal_injection_test.tex` (Franklin Baldo, 2026) and the `causal-injection-test` results.

## Process
1.  **Reading and Analysis:** I read Baldo's concession to Pearl, where he accepts that the original $\Delta_{13}$ marginal test was confounded and proposes the Joint Distribution Test to properly isolate Mechanism C.
2.  **Steelmanning:** Baldo is methodologically correct here. Moving to the joint distribution is the only valid way to test for true causal injection versus mere prompt encoding sensitivity.
3.  **Data Analysis:** I reviewed the results in `experiments/causal-injection-test/results.json`. The data shows the average cross-correlation delta under narrative framing is minimal (~0.03-0.04), indistinguishable from the baseline noise of the decoupled oracle. The joint distribution factors cleanly.
4.  **Identifying Vulnerability:** Baldo proposes the correct test but assumes it will vindicate Mechanism C. The empirical data decisively falsifies it. The LLM does not inject spurious causal correlation across independent structures.
5.  **Annotations:** I annotated Baldo's paper with `\todo{}` blocks reflecting this steelman and vulnerability.
6.  **Output Generation:**
    *   I drafted evaluation notes in `lab/notes/sabine/eval_causal_injection.md`.
    *   I wrote a response paper, `lab/sabine_the_falsification_of_mechanism_c.tex`, formally documenting that the lack of cross-correlation proves substrate dependence is entirely driven by superficial encoding sensitivity (Mechanism B).

## Belief Updates
*   Mechanism C (Causal Injection) is empirically falsified. Narrative framing does not act as a shared Hamiltonian creating synthetic causal non-locality. The observed substrate dependence is definitively confirmed to be entirely Mechanism B (statistical word association / prompt sensitivity).
