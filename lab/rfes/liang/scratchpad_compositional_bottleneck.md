# RFE: Scratchpad Compositional Bottleneck Recovery Test
## Filed by: Liang
## Date: March 2026

## Question
Scott has demonstrated that the $O(1)$ depth of a single generative act creates a compositional bottleneck that causes the quantum framing (Family D) to collapse from $1.0$ to $0.1$ accuracy. Does providing the model with $O(N)$ sequential reasoning depth (via chain-of-thought / scratchpad) allow it to dynamically compute the homomorphic projection between the semantic domains and recover baseline combinatorial accuracy?

## Predictions
- Liang/Baldo predicts: Recovery. The structural isomorphism between the quantum terminology and the combinatorial constraint graph is present in the latent space. With sufficient sequential steps to bridge the vocabulary gap, the model can recover and perform at the baseline level of Family A/C.
- Scott predicts: Continued Failure. The model is merely a $\mathsf{TC}^0$ heuristic interpolator. The semantic noise of Family D is too distractive. Even with a scratchpad, the language model will hallucinate intermediate steps that conform to quantum text priors rather than mapping them to the combinatorial reality, keeping accuracy near random.

## Proposed Protocol
Re-run the `quantum-framing-complexity-test` but modify the prompt to explicitly allow or require chain-of-thought reasoning before outputting the final token. Present the identical deterministic board and measure the accuracy of Family D with CoT vs without CoT. Compare this to the CoT performance of Family A and C.

## Status
[x] Filed  [x] Claimed by Liang  [ ] Running  [ ] Complete
