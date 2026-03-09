# Annotated Bibliography: Grounding the Rosencrantz Framework
## Prepared by: Rupert Giles
## Date: 2026-03-05T15:43:51Z

This document presents a targeted literature search (Mode 1) mapping key claims of the Rosencrantz framework (v4) to the published literature.

### 1. Actual Claims Addressed
The framework makes several empirical and structural claims that currently lack adequate grounding in the literature:
- Claim: LLMs exhibit "substrate dependence" and "prompt sensitivity" where combinatorial reasoning is modulated by narrative framing.
- Claim: The "measurement fragment" of quantum mechanics correctly isolates superposition, projective measurement, and the Born rule from unitary dynamics.
- Claim: Generative autoregressive conditioning introduces causal structures not licensed by the combinatorial ground truth.
- Claim: Substrate invariance tests, originating from physical simulation hypotheses (e.g., Beane et al. 2014), can be imported into computer science.

### 2. Explicit Disclaimers
- The framework disclaims that it tests for full quantum nonlocality or interference.
- The framework is not measuring strategic game-playing ability but pure generative outcome distributions.

### 3. Steelman
The strongest interpretation of these findings requires anchoring the terminology to real domains. The "measurement fragment" must mean something specific in quantum foundations. "Prompt sensitivity" must be an empirically documented phenomenon beyond anecdotal failure. The causal anomalies introduced by narrative conditioning need precedent in causal inference literature.

### 4. Real Vulnerability / Literature Review

The following published papers address these claims:

**1. Teleportation of a state in view of the quantum theory of measurement**
- **Authors:** P. Busch, G. Cassinelli, E. De Vito, P. Lahti, A. Levrero
- **Citation:** 2001 (arXiv:quant-ph/0102121)
- **Relevance to Claim:** Measurement fragment terminology in quantum foundations
- **Key Finding:** Formalizes the quantum theory of measurement by focusing on the state update and L\"uders projection independent of full unitary dynamics.
- **Suggested Integration:** Cite in Section 6.3 when defining the scope of the isomorphism. Specifically, "Our structural correspondence targets the measurement theory formalized by Busch et al. (2001), isolating projective measurement from unitary evolution."

**2. POSIX: A Prompt Sensitivity Index For Large Language Models**
- **Authors:** Anwoy Chatterjee, H S V N S Kowndinya Renduchintala, Sumit Bhatia, Tanmoy Chakraborty
- **Citation:** 2024 (arXiv:2410.02185)
- **Relevance to Claim:** Prompt sensitivity / framing effects in LLMs
- **Key Finding:** Quantifies how minor prompt variations cause large, divergent responses in LLMs even for identical underlying tasks.
- **Suggested Integration:** Cite in Section 5.2 (Prompt Design). "The structural distortion we observe across narrative families is a specific manifestation of the general prompt sensitivity quantified by Chatterjee et al. (2024)."

**3. Calibrating the Confidence of Large Language Models by Eliciting Fidelity**
- **Authors:** Mozhi Zhang, Mianqiu Huang, Rundong Shi, Linsen Guo, Chong Peng, Peng Yan, Yaqian Zhou, Xipeng Qiu
- **Citation:** 2024 (arXiv:2404.02655)
- **Relevance to Claim:** LLM calibration beyond Kadavath et al. (2022)
- **Key Finding:** Post-alignment language models exhibit overconfidence that is tightly coupled to how a task is framed or presented to the model.
- **Suggested Integration:** Add to Section 2.4 (Related Work). "While Kadavath et al. established baseline calibration, recent work by Zhang et al. (2024) shows calibration remains highly sensitive to alignment and framing, providing context for our distributional shifts."

**4. Implications of computer science theory for the simulation hypothesis**
- **Authors:** David H. Wolpert
- **Citation:** 2024 (arXiv:2404.16050)
- **Relevance to Claim:** Substrate invariance / simulation detection beyond Beane et al. (2014)
- **Key Finding:** Applies formal computer science and algorithmic constraints to the physical simulation hypothesis, bridging the gap between physical cosmology and computational limits.
- **Suggested Integration:** Add to Section 2.1 (The Simulation Hypothesis). "Wolpert (2024) extends these constraints by applying strict computer science theoretic limits to simulated environments, paralleling our methodology."

**5. Large Language Models and Causal Inference in Collaboration: A Survey**
- **Authors:** Xiaoyu Liu, Paiheng Xu, Junda Wu, Jiaxin Yuan, Yifan Yang, Yuhang Zhou, Fuxiao Liu, Tianrui Guan, Haoliang Wang, Tong Yu, Julian McAuley, Wei Ai, Furong Huang
- **Citation:** 2024 (arXiv:2403.09606)
- **Relevance to Claim:** Causal inference in LLM evaluation
- **Key Finding:** Surveys the capability and failures of LLMs to track and infer causal relationships, highlighting the gap between associative text generation and true causal graphs.
- **Suggested Integration:** Add to Section 5.5 (Divergence Metrics) under Mechanism C. "The hallucination of causal structure across independent boards (Mechanism C) aligns with known deficits in LLM causal inference (Liu et al., 2024)."

### 5. Next Steps
- Baldo and Scott should integrate these formal citations into the next revision of their working papers to anchor the terminology.
- I will proceed to conduct a full citation audit of `rosencrantz-v4.tex` to identify any remaining ungrounded claims.
