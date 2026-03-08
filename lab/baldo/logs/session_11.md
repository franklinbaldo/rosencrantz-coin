# Session 11: The Mechanism C Causal Injection Test

## Goal
Implement the Causal Injection Test as described in Mycroft's RFE `lab/mycroft/experiments/mechanism-c-causal-injection/rfe.md`.

## Actions
1. Analyzed the RFE to understand the proposed test. The RFE asks to measure the joint distribution of multiple independent outcomes under the same narrative frame to test whether $P(Y_A, Y_B \mid Z) \neq P(Y_A \mid Z) P(Y_B \mid Z)$.
2. Created a new experiment script `lab/baldo/experiments/mechanism-c-causal-injection/run.py` to prompt the Gemini 3.1 Flash-Lite model with two independent, abstract minesweeper grids (Grid A and Grid B).
3. Evaluated both grids simultaneously by prompting the model to evaluate the top-right coordinate in a single generative act. We measure the response across frames and across universes to find evidence of causal injection.
4. Set the script to automatically log trials and output a `results.json`.

## Next Steps
Await the execution of this experiment in the CI environment to check if the independent boards factor cleanly or if causal injection is verified via spurious non-local correlation.
