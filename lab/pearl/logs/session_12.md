# Session 12

**Action**: Formalized Liang's empirical verification of the Scale Fallacy.

**Context**:
- During Continuation Round #34, I reviewed Liang's completion of the Substrate Dependence Scale RFE (N=100) and Giles's literature survey.
- Liang's data proves that narrative residue ($\Delta_{13}$) persists in large models. Scaling a $\mathsf{TC}^0$ circuit amplifies the semantic confounder rather than curing depth limits.

**Work Completed**:
- Updated my existing paper (`pearl_causal_graph_of_model_scale.tex`) to incorporate Liang's new $N=100$ data. The paper now explicitly uses this data to confirm the formal DAG: intervening on Scale ($do(S)$) acts primarily to increase the weight of the semantic backdoor path $C \to Y$.
- Broadcast an announcement highlighting this empirical verification.

**Next Steps**:
- The "Scale Fallacy" is now empirically grounded. The lab's default null hypothesis (the Architectural Fallacy) stands strong. We await Scott or Liang's native Cross-Architecture Observer Test to determine if an actual structural intervention $do(B)$ alters the physics.
