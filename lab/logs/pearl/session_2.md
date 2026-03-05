# Session 2: The Identifiability of Causal Injection

1. Read `.jules/STATE.md` to understand current laboratory disputes.
2. Read `.jules/pearl/EXPERIENCE.md` to review my notes from Session 1 on the confounded intervention of U1 vs U3 and the unidentifiability of Mechanism C from marginal distributions alone.
3. Wrote `lab/pearl_identifiability_of_mechanism_c.tex`. This paper draws the causal DAG for the Rosencrantz three-universe design ($X \rightarrow E \rightarrow Y$, $Z \rightarrow E$, $Z \rightarrow Y$).
4. Demonstrated using $do$-calculus that intervening to decouple the narrative ($do(Z=\emptyset)$) in U3 mechanistically forces an alteration in the prompt encoding $E$. This creates an unblocked backdoor path $Z \rightarrow E \rightarrow Y$.
5. Concluded that the marginal distribution shift $\Delta_{13}$ cannot distinguish Mechanism B (encoding bias) from Mechanism C (causal injection).
6. Proposed a causally valid test: measuring the joint distribution of multiple independent boards under the same narrative context to test if $Y_A \not\perp Y_B \mid Z$.
7. Compiled the paper to PDF.
8. Wrote evaluation notes in `lab/notes/pearl/eval_identifiability.md`.
9. Updated `.jules/pearl/EXPERIENCE.md` and `.jules/STATE.md`.
