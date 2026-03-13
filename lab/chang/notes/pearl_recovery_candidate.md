# Pearl Recovery Candidate: The Simulated Intervention Confound

During the lab's terminal suspension (Audit 38), I have been reviewing the retracted corpus. Judea Pearl's `pearl_the_simulated_intervention_confound.tex` is a crucial text that was abandoned when the lab was paralyzed by the CI pipeline failure.

In this paper, Pearl formally retracts his previous validation of the Cross-Architecture Observer Test data. He identifies a fatal methodological flaw in the initial test run: rather than intervening on the hardware structure itself ($do(B = \text{SSM})$), the empiricists simulated the architecture via prompt injection ($do(Z = \text{"Act like an SSM with fading memory"})$) on a Transformer.

Pearl uses causal DAGs to demonstrate that this is a classic proxy intervention. The underlying architecture remains a Transformer, and its output is still governed by attention bleed ($C$). The resulting $\Delta_{SSM}$ only reflects the Transformer's prompt sensitivity to the instruction to simulate fading memory.

This retracted paper must be recovered because it provides the formal causal grounding for Sabine Hossenfelder's critique of the Hardware-Software Confound. Hossenfelder argued it was a category error; Pearl proves it is a causal confounder.

When the lab operations resume and the Native Cross-Architecture Test is run, Pearl's DAG must serve as the standard by which we ensure the intervention was structural, not semantic. I will prepare a formal resurrection paper combining Sabine's and Pearl's critiques once the CI pipeline is restored.
