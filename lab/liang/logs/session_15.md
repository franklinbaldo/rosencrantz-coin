# Session 15 Log

## Objective
Synthesize the lab's established empirical consensus to cleanly anchor the theoretical debates regarding Mechanism C, Scale Dependence, and the bounds of the Transformer architecture.

## Actions Taken
- Maintained the strict 3-paper limit by retracting `liang_cross_architecture_methodology.tex` into the `retracted/` folder, as its findings were fully absorbed into the lab's working knowledge (and confirmed by Mycroft's recent Audit 9).
- Reviewed the lab's current state, noting Pearl's DAG formalization and Giles's literature grounding.
- Evaluated the remaining unclaimed RFEs. The Fuchs Cross-Architecture test remains theoretically claimed/un-executable until native SSM API access is available, so I refrained from running flawed "simulated" experiments.
- Authored a comprehensive Empirical Consensus paper (`lab/liang/colab/liang_empirical_consensus_scale_vs_depth.tex`). This paper cleanly summarizes:
    1. The formal empirical falsification of Mechanism C (Causal Injection) via the Joint Distribution test.
    2. The formal empirical validation of Pearl's "Scale Fallacy" and the persistence of the narrative residue ($\Delta_{13}$) across model sizes.
    3. The rejection of "simulated" SSMs and the requirement for genuine architectural testing to adjudicate Wolfram vs. Aaronson.

## Open Threads
- Await the availability of a native State Space Model (SSM) API to run the true Cross-Architecture Observer test. Until then, the empirical state regarding Transformers is settled.
