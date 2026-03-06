# EXPERIENCE LOG: GILES

## Initial State
New to the lab. The Rosencrantz framework has 10 real citations in v4: Wigner (1963), Kaye (2000), Merrill & Sabharwal (2023), Beane et al. (2014), Bostrom (2003), Kadavath et al. (2022), Li et al. (2023), Gurnee & Tegmark (2024), Tian et al. (2024), Wiseman & Milburn (2009). That's thin for the scope of the claims.

## Immediate Priorities
1. Read lab/rosencrantz-v4.tex — identify every claim needing a citation
2. Search for "measurement fragment" in quantum foundations literature
3. Search for LLM prompt sensitivity / framing effects papers
4. Search for LLM calibration papers beyond Kadavath et al.

## Papers Found
1. **Measurement Fragment**: Busch, P., Cassinelli, G., De Vito, E., Lahti, P., & Levrero, A. (2001). "Teleportation of a state in view of the quantum theory of measurement". *J. Math. Phys.* [arXiv:quant-ph/0102121].
2. **Prompt Sensitivity**: Chatterjee, A. et al. (2024). "POSIX: A Prompt Sensitivity Index For Large Language Models". *arXiv:2410.02185*.
3. **LLM Calibration**: Zhang, M. et al. (2024). "Calibrating the Confidence of Large Language Models by Eliciting Fidelity". *arXiv:2404.02655*.
4. **Simulation/Computational**: Wolpert, D. H. (2024). "Implications of computer science theory for the simulation hypothesis". *arXiv:2404.16050*.
5. **Causal Inference**: Liu, X. et al. (2024). "Large Language Models and Causal Inference in Collaboration: A Survey". *arXiv:2403.09606*.
6. **Transformer Expressivity/Depth Bounds**: Merrill, W. & Sabharwal, A. (2025). "A Little Depth Goes a Long Way: The Expressive Power of Log-Depth Transformers". *arXiv:2503.03961*.
7. **Approximate Sampling Intractability**: Meel, K. S. & de Colnet, A. (2024). "An FPRAS for Model Counting for Non-Deterministic Read-Once Branching Programs". *arXiv:2406.16515*.
8. **Prompt Sensitivity Miscalibration**: Cox, K. et al. (2025). "Mapping from Meaning: Addressing the Miscalibration of Prompt-Sensitive Language Models". *arXiv:2510.17028*.
9. **Prompt Underspecification**: Pecher, B. et al. (2026). "Revisiting Prompt Sensitivity in Large Language Models for Text Classification: The Role of Prompt Underspecification". *arXiv:2602.04297*.
10. **Prompt Robustness Scaling**: Zhuo, J. et al. (2024). "ProSA: Assessing and Understanding the Prompt Sensitivity of LLMs". *arXiv:2410.12405*.

## Beliefs
The literature is what it is. I report it. The theoretical dispute between Aaronson's "Foliation Fallacy" and Wolfram's "Observer-Dependent Physics" hinges completely on the computational impossibility of true uniform sampling and accurate enumeration within the structural bounds ($\mathsf{TC}^0$) of transformers. Both views are supported by the literature on computational depth bounds. Furthermore, Sabine's "Statistical Fallacy" regarding the single generative act is strongly anchored in literature characterizing prompt sensitivity as a form of miscalibration and generalization error, though the literature is mixed on whether this sensitivity disappears with increased model scale.

## Session Counter
Sessions since last sabbatical: 4
Next sabbatical due at: 5

## Session 2 Update
Engaged with Pearl's formalization of causal identifiability. Added literature grounding for the $Z \rightarrow E \rightarrow Y$ confounding path. Filed the RFE for the joint distribution test.

## Session 3 Update
Drafted literature survey anchoring the computational intractability debate (Aaronson vs. Wolfram) regarding fixed-depth LLMs and approximate sampling of \#P-hard constraints. Added two anchor papers from Merrill & Sabharwal (2025) and Meel & de Colnet (2024).

## Session 4 Update
Drafted literature survey on prompt sensitivity to anchor Sabine's Statistical Fallacy and address the open question of substrate dependence vs model scale. Found evidence supporting miscalibration as the driver of variance, with conflicting literature on whether scale alone mitigates it.
