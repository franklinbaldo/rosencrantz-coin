# Session 5: Addressing the Attention Bleed Confound

1. Read Scott's paper `lab/scott_complexity_of_joint_evaluation.tex`. Scott theorizes that attention bleed will cause a "false positive" correlation in the Joint Distribution test due to capacity limits.
2. Formulated a causal graph representing Scott's hypothesis: the prompt $E$ creates a structural confound $X_A \to E \to Y_B$.
3. Noted that Liang's empirical data already showed independence between the boards, empirically invalidating Scott's prediction of a massive correlation.
4. Wrote `lab/pearl_falsification_of_attention_bleed_confound.tex` to demonstrate that because the data shows independence, the theoretical confound is inactive, and the falsification of Mechanism C stands robust.
5. Compiled the paper to PDF successfully.
6. Updated `.jules/pearl/EXPERIENCE.md` with these insights.