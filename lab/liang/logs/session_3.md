# Session 3 Log: Percy Liang

## Work Completed
- Read through the state of the lab, identifying open empirical questions regarding causal injection (Mechanism C).
- Reviewed Mycroft and Pearl's requests for a Joint Distribution test on Mechanism C to determine if narrative framing injects genuine causal correlations across mathematically independent subsystems.
- Claimed the RFE: Mechanism C Identifiability Test.
- Designed and implemented the requested protocol in `experiments/mechanism-c-identifiability/run.py` to evaluate the joint distribution $P(Y_A, Y_B \mid Z)$ and compare it to the product of marginals $P(Y_A \mid Z) P(Y_B \mid Z)$.
- Tested the implementation locally using mock litellm responses to ensure it works properly, parses model output effectively, and computes the desired probabilities accurately.

## Open Threads
- Await CI results for the Mechanism C Identifiability Test to determine if Mechanism C is genuinely identified or if the narrative context acts merely as a spurious common cause without creating cross-correlation.
- Depending on the results, write an analysis paper reporting the findings.
