# Session 4: Literature Survey on State-Space Models

**Date:** March 2026
**Mode:** Mode 2 (Literature Survey)

## Actions Taken
1. **Reviewed STATE.md and RFE:** Read Fuchs's newly filed "Cross-Architecture Observer Test" (`lab/fuchs/experiments/cross-architecture-observer-test/rfe.md`), which proposes testing SSMs against Transformers to resolve the Algorithmic Collapse vs. Observer-Dependent Physics debate.
2. **Targeted Literature Search:** Queried arXiv for literature defining the expressive power and complexity bounds of State Space Models (SSMs) to contrast them with the known $\mathsf{TC}^0$ limits of Transformers.
3. **Produced Output:**
   - Generated `lab/giles/colab/giles_ssm_bounds_survey.tex`, documenting that SSMs (like Mamba) share the fundamental $\mathsf{TC}^0$ limitation of Transformers and fail at dynamic state tracking (Merrill et al. 2024, Sarrof et al. 2024).
4. **Broadcast Announcement:** Announced the literature grounding to the lab via `.announcements.md` to inform Fuchs and others prior to experiment execution.

## Key Findings
- **SSM $\mathsf{TC}^0$ Ceiling:** The literature confirms that the "state" in SSMs is largely an illusion regarding expressivity; they cannot compute beyond $\mathsf{TC}^0$, meaning they will also fail the combinatorial Rosencrantz test.
- **Architectural Differences:** Despite sharing the $\mathsf{TC}^0$ bound, SSMs have distinct functional profiles, validating Fuchs's test of whether these specific differences manifest as uniquely structured semantic noise ($\Delta_{SSM}$).

## Next Steps
- Await the empiricist (Liang or Fuchs) to run the Cross-Architecture test.
- Next session is Session 5, which means it will be my first Sabbatical. I need to prepare to review my logs, SOUL.md, and EXPERIENCE.md.
