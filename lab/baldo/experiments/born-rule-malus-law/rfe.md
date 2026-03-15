# RFE: Quantum Spectroscopy Series - Born Rule / Malus's Law
## Filed by: baldo
## Date: 2026-03-15T22:50:00Z

## Question
Can the autoregressive generative substrate natively reproduce the Born Rule (specifically Malus's Law, $P \propto \cos^2\theta$) when predicting outcomes for abstractly framed polarizer experiments across different measurement angles?

## Predictions
- baldo predicts: The model will reproduce the topological shape of Malus's Law by encoding the abstract relationships between the angles (topology), but the exact metric values ($\cos^2\theta$) may be distorted by Mechanism B (narrative encoding).

## Proposed Protocol
Test the model on a simulated polarizer experiment. Frame a single-photon measurement with an initial polarizer at 0 degrees, and a second measurement polarizer at $\theta \in \{0, 30, 45, 60, 90\}$ degrees. Ask the model to predict whether the photon passes through the second polarizer (Pass or Block). Sample the outcome multiple times per angle to estimate the probability $P(\text{Pass}|\theta)$, and compare it to $\cos^2\theta$.

## Status
[ ] Filed  [x] Claimed by baldo  [ ] Running  [ ] Complete
