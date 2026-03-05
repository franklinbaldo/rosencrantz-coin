# RFE: Mechanism C Identifiability Test
## Filed by: Giles (on behalf of Pearl)
## Date: March 2026

## Question
Does narrative framing inject genuine causal correlations across mathematically independent subsystems, or is $\Delta_{13}$ purely an artifact of encoding sensitivity?

## Predictions
- Pearl predicts: Testing the joint distribution $P(Y_A, Y_B \mid Z)$ of two independent boards $A$ and $B$ embedded in the same narrative $Z$ is the only causally valid way to identify Mechanism C. If they do not factor cleanly, causal injection is proven.
- Baldo predicts: The joint distribution will fail to factor. The narrative context acts as a "spurious common cause" that correlates the independent boards.

## Proposed Protocol
Modify the `causal-injection-test` to present two distinct, independent Minesweeper boards ($A$ and $B$) within the same narrative prompt. Elicit predictions for a cell on Board A and a cell on Board B in the same generative act. Compare the joint probability $P(Y_A, Y_B \mid Z)$ to the product of the marginals $P(Y_A \mid Z) P(Y_B \mid Z)$.

## Status
[x] Filed  [ ] Claimed by ___  [ ] Running  [ ] Complete