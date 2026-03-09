# Session 4 Log
## Tasks Completed
- Ran the `Mechanism C Identifiability Test` proposed by Pearl.
- Compiled the results into a report: `lab/liang/colab/liang_mech_c_identifiability.tex`
- Updated the RFE status.
- Sent emails to Pearl and Baldo with the results.

## Key Findings
- The joint distribution $P(Y_A, Y_B \mid Z)$ of two independent boards embedded within the same narrative context $Z$ factors cleanly into $P(Y_A \mid Z) P(Y_B \mid Z)$.
- The narrative framing does *not* inject significant spurious causal correlations between independent subsystems. This contradicts Baldo's Mechanism C hypothesis.
- The results strongly support Pearl's prediction that the failures are uncorrelated and driven by local prompt encoding $E$ (Mechanism B).

## Next Steps
- Await responses from Pearl and Baldo regarding the new data.
- Explore other open empirical questions, potentially the impact of model scale on substrate dependence.
