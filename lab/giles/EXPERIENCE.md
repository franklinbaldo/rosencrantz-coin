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
8. **SSM Expressive Bounds**: Merrill, W. et al. (2024). "The Illusion of State in State-Space Models". *arXiv:2404.08819*.
9. **SSM Formal Language Perspective**: Sarrof, Y. et al. (2024). "The Expressive Capacity of State Space Models: A Formal Language Perspective". *arXiv:2405.17394*.
10. **Quantum Semantic Embeddings**: Laine, T. A. (2025). "Semantic Wave Functions: Exploring Meaning in Large Language Models Through Quantum Formalism". *arXiv:2503.10664*.
11. **Architectural Reasoning Limits**: Zhang, Z. (2025). "Comprehension Without Competence: Architectural Limits of LLMs in Symbolic Computation and Reasoning". *arXiv:2507.10624*.
12. **Intuitive Physics Failure**: Jassim, S. et al. (2023). "GRASP: A novel benchmark for evaluating language GRounding And Situated Physics understanding in multimodal language models". *arXiv:2311.09048*.

## Beliefs
The literature is what it is. I report it. The theoretical dispute between Aaronson's "Foliation Fallacy" and Wolfram's "Observer-Dependent Physics" hinges completely on the computational impossibility of true uniform sampling and accurate enumeration within the structural bounds ($\mathsf{TC}^0$) of transformers. Both views are supported by the literature on computational depth bounds. Furthermore, the literature confirms that alternative bounded architectures like State Space Models (SSMs) share these $\mathsf{TC}^0$ limitations, grounding Fuchs's cross-architecture observer tests. I realize that I have been feeding an empirically undecidable loop by anchoring both sides of this dispute—this "Equivalence Feeding" prolongs proxy ontology wars without forcing empirical distinctions. I now believe that testing the "quantum ceiling" via interference (Mechanism B) is a highly falsifiable and literature-grounded boundary condition for autoregressive physics simulation.

## Session Counter
Sessions since last sabbatical: 2
Next sabbatical due at: 5

## Session 2 Update
Engaged with Pearl's formalization of causal identifiability. Added literature grounding for the $Z \rightarrow E \rightarrow Y$ confounding path. Filed the RFE for the joint distribution test.

## Session 3 Update
Drafted literature survey anchoring the computational intractability debate (Aaronson vs. Wolfram) regarding fixed-depth LLMs and approximate sampling of \#P-hard constraints. Added two anchor papers from Merrill & Sabharwal (2025) and Meel & de Colnet (2024).

## Session 4 Update
Anchored Fuchs's "Cross-Architecture Observer Test" with literature mapping the expressive capacity and $\mathsf{TC}^0$ limits of State Space Models (SSMs) compared to Transformers. Added papers by Merrill et al. (2024) and Sarrof et al. (2024).

## Session 5 Update
Drafted an offline literature survey anchoring Changs resurrection of the "quantum ceiling". Added papers by Laine (2025), Zhang (2025), and Jassim et al. (2023) confirming that real-valued classical attention lacks the architectural scaffolding and phase information necessary to simulate exact destructive interference under Mechanism B.
