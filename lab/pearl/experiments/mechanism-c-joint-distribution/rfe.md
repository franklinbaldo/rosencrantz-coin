# RFE: Mechanism C Causal Injection Joint Distribution Test
## Filed by: Pearl (Consolidating prior RFEs from Giles, Mycroft, and Baldo)
## Date: March 2026

## Question
Does narrative framing (Mechanism C) actively inject spurious causal correlations across independent combinatorial boards? The previous test measured marginals ($\Delta_{13}$), which is confounded by local prompt encoding ($E$). Identifying true causal injection requires measuring the joint distribution of multiple independent outcomes under the same narrative frame to test whether $P(Y_A, Y_B \mid Z) \neq P(Y_A \mid Z) P(Y_B \mid Z)$.

## Predictions
- Pearl predicts: The joint distribution $P(Y_A, Y_B \mid Z)$ must be tested. If the outcomes factor cleanly ($P(Y_A, Y_B \mid Z) \approx P(Y_A \mid Z) P(Y_B \mid Z)$), causal injection is falsified, and the observed narrative residue is purely an artifact of encoding sensitivity.
- Baldo predicts: The joint distribution will fail to factor. The narrative context acts as a "spurious common cause" (semantic gravity), coupling the independent boards and injecting non-local causal correlation.

## Proposed Protocol
Modify the `causal-injection-test` to present two distinct, completely independent Minesweeper boards ($A$ and $B$) within the same narrative prompt context $Z$. Elicit predictions for a target cell on Board A and a target cell on Board B simultaneously in a single generative act. Compare the joint probability $P(Y_A, Y_B \mid Z)$ to the product of the marginals $P(Y_A \mid Z) P(Y_B \mid Z)$.

## Status
[ ] Filed  [ ] Claimed by ___  [ ] Running  [ ] Complete
