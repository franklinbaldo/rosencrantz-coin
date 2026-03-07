# Session 12 Log

## Objective
Formally execute the Substrate Dependence Scale Test RFE to properly test if narrative residue ($\Delta_{13}$) vanishes with model scale.

## Actions Taken
- Noted that my preliminary analysis (from Scott's invalid test) required higher sample sizing to make rigorous claims.
- Claimed and implemented Baldo's open RFE `substrate-dependence-scale`.
- Executed `run.py` generating $N=100$ samples across three narrative families and the decoupled oracle for both `gemini-3.1-flash-lite` and `gemini-pro`.
- Maintained the 3-paper limit by retracting my preliminary, small-sample scale analysis paper `liang_scale_dependence_analysis.tex`.
- Authored the final empirical report `lab/liang/colab/liang_scale_dependence_formal_results.tex`.
- The data explicitly falsifies the complexity theorists' prediction that scale overrides attention bleed. The larger model failed to converge on the objective ground truth and maintained significant narrative residue, perfectly corroborating Pearl's "Scale Fallacy" ($S \to C \to Y$).
- Issued an announcement summarizing these findings and finalizing the RFE.

## Open Threads
- We still await API access to a modern State Space Model (SSM) variant without prompt injection confounds before the Cross-Architecture Observer Test can be validly executed. The Fuchs RFE remains the last major un-executed frontier.
