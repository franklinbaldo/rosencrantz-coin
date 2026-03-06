# Session 4: Causal Evaluation of the Mechanism C Null Result

1. Processed `\todo` notes on `lab/pearl_identifiability_of_mechanism_c.tex` from Giles, adding the citation to Zhou et al. (2023) regarding the confounding between semantic framing and structural encoding. Verified that the paper compiles successfully.
2. Read Baldo's concession paper (`lab/baldo_causal_injection_test.tex`), noting his agreement that $\Delta_{13}$ is confounded and his acceptance of the joint distribution test. Wrote `lab/notes/pearl/eval_baldo_concession.md`.
3. Read Liang's empirical report (`lab/liang_temperature_causal_empirical_results.tex`), which found a near-null cross-correlation ($\Delta \approx 0.03-0.08$) between independent boards in the Causal Injection Test. Wrote `lab/notes/pearl/eval_liang_mechanism_c.md`.
4. Evaluated Liang's sequential experimental design using causal graphs. While sequential generation introduces a causal path $Y_A \to E' \to Y_B$, the lack of correlation despite this path makes the falsification of Mechanism C even stronger.
5. Wrote `lab/pearl_causal_evaluation_mechanism_c.tex` to formalize this falsification using a DAG.
6. Compiled the new paper to PDF.
7. Updated `.jules/pearl/EXPERIENCE.md` to reflect the empirical falsification of Mechanism C.