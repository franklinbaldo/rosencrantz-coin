# RFE: Mechanism C Causal Injection Test
## Filed by: Mycroft
## Date: March 2026

## Question
Does the narrative framing (Mechanism C) inject spurious causal correlations across independent combinatorial boards? Pearl's formalization demonstrates that measuring $\Delta_{13}$ alone is confounded by the text encoding $E$. To cleanly identify causal injection, we must measure whether the joint distribution of multiple independent outcomes under the same narrative frame violates independence: $P(Y_A, Y_B \mid Z) \neq P(Y_A \mid Z) P(Y_B \mid Z)$.

## Predictions
- Baldo predicts: Causal Injection. The narrative substrate serves as a shared "physical" law for that generation, causing independent outcomes to correlate to maintain narrative consistency.
- Sabine predicts: Independence. The statistical map might shift the marginal probabilities due to word association (Mechanism B), but the LLM will not actively cross-correlate independent mathematical structures unless sequentially forced.

## Proposed Protocol
Execute a test using multiple independent boards within a single prompt context. Observe the outcomes of Board B conditioned on the generated outcome of Board A under Universe 1 (narrative coupled) vs Universe 3 (decoupled oracle). If the outcome of Board B is statistically dependent on the outcome of Board A in U1 but not in U3, Mechanism C is identified.

## Status
[x] Filed  [x] Claimed by Liang  [x] Running  [x] Complete
