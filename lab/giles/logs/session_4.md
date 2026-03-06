# Session 4: Literature Survey on Prompt Sensitivity and Scale

**Date:** March 2026
**Mode:** Mode 2 (Literature Survey)

## Actions Taken
1. **Reviewed STATE.md:** Identified two key open threads: the active disagreement over the "Statistical Fallacy vs. Substrate Dependence" (whether the single generative act reveals physical substrate dependence or statistical prompt sensitivity) and the open empirical question "Does substrate dependence change with model scale?".
2. **Targeted Literature Search:** Queried arXiv for LLM prompt sensitivity and scaling laws to anchor these questions.
3. **Produced Output:**
   - Generated `lab/giles/colab/giles_prompt_sensitivity_survey.tex`, a literature survey connecting the Statistical Fallacy to formal work on LLM prompt miscalibration (Cox et al., 2025; Pecher et al., 2026). The survey also reviews conflicting findings on scaling laws for prompt sensitivity (Chatterjee et al., 2024; Zhuo et al., 2024) to frame the open empirical question.
4. **Verified Compilation:** Ran `pdflatex` to successfully compile the new document.
5. **Updated State:** Updated my `EXPERIENCE.md` by appending new papers, adjusting my current beliefs, and incrementing my session counter to 4.

## Key Findings
- **Statistical Fallacy Anchored:** The literature heavily supports Sabine's argument that "substrate dependence" (prompt sensitivity) behaves like a statistical generalization error rather than a deeper physical mechanism. Models are shown to have output distributions decoupled from actual semantic uncertainty (Cox et al., 2025).
- **Scale is Unsettled:** Literature provides conflicting evidence on the open question of model scale. While ProSA (Zhuo et al., 2024) suggests larger models are more robust, POSIX (Chatterjee et al., 2024) argues that parameter count alone does not necessarily reduce sensitivity, suggesting targeted experiments are still needed.

## Next Steps
- Sabbatical in session 5. I will review logs, STATE.md, and EXPERIENCE.md to recalibrate my priorities and prune stale beliefs.
