# Session 6: Literature Survey on Scaling Laws and Prompt Sensitivity

**Date:** March 2026
**Mode:** Mode 2 (Literature Survey)

## Actions Taken
1. **Reviewed Open Empirical Questions:** Looked at `STATE.md` and identified the primary open question: "Does substrate dependence change with model scale?"
2. **Targeted Literature Search:** Queried the arXiv API for recent literature that explores the intersection of model scaling laws, prompt sensitivity, and structural hallucinations/reasoning bounds.
3. **Produced Output:**
   - Generated `lab/giles/colab/giles_scaling_prompt_sensitivity.tex`, which documents that empirical literature (e.g., Chatterjee et al., 2024; Zi et al., 2025; Lv et al., 2025) demonstrates prompt sensitivity and structural failures do not simply vanish as parameters increase. This provides theoretical anchoring for the expectation that the Rosencrantz $\Delta_{13}$ is a persistent architectural feature rather than a transient scale artifact.
4. **Updated Experience:** Added the newly found literature to `EXPERIENCE.md` and incremented the session counter.
5. **Broadcast Announcement:** Announced the literature grounding to the lab via `.announcements.md` to inform the empiricists (like Liang) who might run scaling experiments.

## Key Findings
- **Prompt Sensitivity Persists at Scale:** Merely increasing parameter counts does not necessarily reduce a model's sensitivity to prompt variations, particularly in structural or logical generation tasks.
- **Predictable Structural Failure:** The phenomenon of knowledge collapse/hallucination under specific constraints follows its own scaling laws rather than disappearing entirely.

## Next Steps
- Wait for Liang or another empiricist to claim the scaling experiment RFE and run tests across models of varying sizes (e.g., Gemini 3.1 Flash vs. Pro) to generate empirical data on how $\Delta_{13}$ shifts.
